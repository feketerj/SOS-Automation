#!/usr/bin/env python3
"""
Decision Logic Audit (read-only, optional).

Usage:
  python tools/decision_audit.py [SOS_Output/YYYY-MM/Run_*/] [--results batch_results_*.jsonl]

What it does (no runtime changes):
  - Parses a saved run's data.json and reports:
      * Counts by result (GO / NO-GO / INDETERMINATE)
      * Top knockout categories and patterns
      * Agent disagreement rate (if agent fields present)
      * Basic anomalies (missing rationale/URLs)
  - If --results is provided, scans batch results JSONL for unexpected NO-GO
    and reports counts.
  - Writes a markdown summary next to data.json (decision_audit.md).
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple


def find_latest_run(out_root: Path) -> Path:
    if not out_root.exists():
        raise FileNotFoundError(f"SOS output root not found: {out_root}")
    months = sorted([p for p in out_root.iterdir() if p.is_dir()], key=lambda p: p.stat().st_mtime, reverse=True)
    for m in months:
        runs = sorted([p for p in m.iterdir() if p.is_dir() and p.name.startswith('Run_')], key=lambda p: p.stat().st_mtime, reverse=True)
        if runs:
            return runs[0]
    raise FileNotFoundError("No Run_* folders found under SOS_Output")


def load_run(run_dir: Path) -> Dict[str, Any]:
    data = run_dir / 'data.json'
    if not data.exists():
        raise FileNotFoundError(f"data.json not found in {run_dir}")
    return json.loads(data.read_text(encoding='utf-8'))


def summarize_assessments(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    counts = Counter()
    cats = Counter()
    patterns = Counter()
    agency_counts = Counter()
    naics_counts = Counter()
    anomalies = Counter()

    disagreements = 0
    need_ver = 0
    agent_fields = False
    disagree_by_category = Counter()
    disagree_by_agency = Counter()

    for a in items:
        res = (str(a.get('result') or a.get('final_decision') or '').upper())
        if not res:
            anomalies['missing_result'] += 1
        counts[res] += 1

        kc = a.get('knockout_category')
        if kc:
            cats[kc] += 1
        kp = a.get('knock_pattern')
        if kp:
            patterns[kp] += 1

        ag = a.get('agency')
        if isinstance(ag, str) and ag:
            agency_counts[ag] += 1
        na = a.get('naics')
        if isinstance(na, str) and na:
            naics_counts[na] += 1

        # URL presence
        if not (a.get('sam_url') or a.get('highergov_url')):
            anomalies['missing_urls'] += 1

        # Rationale presence (for batch/agent)
        if res in ('GO', 'NO-GO', 'INDETERMINATE'):
            if not (a.get('rationale') or a.get('analysis_notes')):
                anomalies['missing_rationale'] += 1

        # Disagreements (if present)
        if 'batch_decision' in a or 'agent_decision' in a:
            agent_fields = True
            bd = a.get('batch_decision')
            ad = a.get('agent_decision')
            if bd in ('GO', 'INDETERMINATE'):
                need_ver += 1
            if bd and ad and bd != ad:
                disagreements += 1
                if kc:
                    disagree_by_category[kc] += 1
                if isinstance(ag, str) and ag:
                    disagree_by_agency[ag] += 1

    # Build summary
    total = sum(v for k, v in counts.items() if k)
    top_cats = cats.most_common(5)
    top_patterns = patterns.most_common(5)

    summary = {
        'total': total,
        'counts': counts,
        'top_cats': top_cats,
        'top_patterns': top_patterns,
        'agent_fields': agent_fields,
        'disagreements': disagreements,
        'need_ver': need_ver,
        'anomalies': anomalies,
        'top_agencies': agency_counts.most_common(5),
        'top_naics': naics_counts.most_common(5),
        'disagree_by_category': disagree_by_category.most_common(5),
        'disagree_by_agency': disagree_by_agency.most_common(5),
    }
    return summary


def scan_batch_results(results_glob: str) -> Dict[str, int]:
    import glob
    res_counts = Counter()
    for path in glob.glob(results_glob):
        p = Path(path)
        try:
            with p.open('r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except Exception:
                        continue
                    # Extract model content
                    body = (obj.get('response') or {}).get('body') or {}
                    content = ''
                    if 'choices' in body:
                        ch = body.get('choices') or []
                        if ch:
                            content = (ch[0].get('message') or {}).get('content', '')
                    # Try JSON extraction
                    decision = None
                    if '```json' in content:
                        try:
                            json_str = content.split('```json', 1)[1].split('```', 1)[0]
                            data = json.loads(json_str)
                            decision = (data.get('result') or data.get('recommendation') or '').upper()
                        except Exception:
                            pass
                    elif '{' in content and '}' in content:
                        try:
                            start = content.index('{'); end = content.rindex('}') + 1
                            data = json.loads(content[start:end])
                            decision = (data.get('result') or data.get('recommendation') or '').upper()
                        except Exception:
                            pass
                    if decision:
                        res_counts[decision] += 1
        except Exception:
            continue
    return dict(res_counts)


def write_markdown(run_dir: Path, summary: Dict[str, Any], batch_counts: Dict[str, int] | None) -> Path:
    md = run_dir / 'decision_audit.md'
    lines: List[str] = []
    lines.append(f"# Decision Audit\n")
    lines.append(f"**Run folder:** {run_dir}\n\n")

    # Counts
    lines.append("## Counts by Result\n")
    for k in ('GO', 'NO-GO', 'INDETERMINATE'):
        lines.append(f"- {k}: {summary['counts'].get(k, 0)}\n")
    other = sum(v for r, v in summary['counts'].items() if r not in {'GO', 'NO-GO', 'INDETERMINATE', ''})
    if other:
        lines.append(f"- OTHER: {other}\n")
    lines.append("\n")

    # Disagreements
    if summary['agent_fields'] and summary['need_ver']:
        agree_rate = (summary['need_ver'] - summary['disagreements']) / summary['need_ver'] * 100.0
        lines.append("## Agent Verification\n")
        lines.append(f"- Disagreements: {summary['disagreements']}\n")
        lines.append(f"- Agreement rate: {agree_rate:.1f}%\n\n")
        # Hotspots
        if summary.get('disagree_by_category'):
            lines.append("### Disagreement Hotspots by Category\n")
            for cat, cnt in summary['disagree_by_category']:
                lines.append(f"- {cat}: {cnt}\n")
            lines.append("\n")
        if summary.get('disagree_by_agency'):
            lines.append("### Disagreement Hotspots by Agency\n")
            for ag, cnt in summary['disagree_by_agency']:
                lines.append(f"- {ag}: {cnt}\n")
            lines.append("\n")

    # Top cats/patterns
    if summary['top_cats']:
        lines.append("## Top Knockout Categories\n")
        for cat, cnt in summary['top_cats']:
            lines.append(f"- {cat}: {cnt}\n")
        lines.append("\n")
    if summary['top_patterns']:
        lines.append("## Top Knockout Patterns\n")
        for pat, cnt in summary['top_patterns'][:10]:
            lines.append(f"- {cnt} — {pat}\n")
        lines.append("\n")

    # Agencies / NAICS
    if summary['top_agencies']:
        lines.append("## Top Agencies\n")
        for ag, cnt in summary['top_agencies']:
            lines.append(f"- {ag}: {cnt}\n")
        lines.append("\n")
    if summary['top_naics']:
        lines.append("## Top NAICS\n")
        for na, cnt in summary['top_naics']:
            lines.append(f"- {na}: {cnt}\n")
        lines.append("\n")

    # Anomalies
    if summary['anomalies']:
        lines.append("## Anomalies\n")
        for k, v in summary['anomalies'].items():
            if v:
                lines.append(f"- {k}: {v}\n")
        lines.append("\n")

    # Batch results scan
    if batch_counts:
        lines.append("## Batch Results Overview\n")
        for k in ('GO', 'INDETERMINATE', 'NO-GO', 'FURTHER_ANALYSIS', 'CONTACT_CO'):
            if k in batch_counts:
                lines.append(f"- {k}: {batch_counts[k]}\n")
        if batch_counts.get('NO-GO'):
            lines.append("\n> NOTE: Batch produced NO-GO; this should be rare or converted upstream.\n")

    md.write_text(''.join(lines), encoding='utf-8')
    return md


def write_csv(run_dir: Path, summary: Dict[str, Any], csv_path: Path) -> Path:
    import csv
    with csv_path.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        # Result counts
        w.writerow(['section', 'key', 'value'])
        for k in ('GO', 'NO-GO', 'INDETERMINATE'):
            w.writerow(['counts', k, summary['counts'].get(k, 0)])
        # Hotspots by category
        for cat, cnt in summary.get('disagree_by_category', []) or []:
            w.writerow(['disagree_by_category', cat, cnt])
        # Hotspots by agency
        for ag, cnt in summary.get('disagree_by_agency', []) or []:
            w.writerow(['disagree_by_agency', ag, cnt])
    return csv_path


def main():
    p = argparse.ArgumentParser(description='Decision Logic Audit (read-only)')
    p.add_argument('path', nargs='?', help='Run folder (SOS_Output/YYYY-MM/Run_*/). If omitted, uses latest run')
    p.add_argument('--results', help='Optional glob to batch_results JSONL for anomaly scan')
    p.add_argument('--csv', help='Optional path to write a CSV summary (counts and hotspots)')
    args = p.parse_args()

    out_root = Path('SOS_Output').resolve()
    run_dir = Path(args.path).resolve() if args.path else find_latest_run(out_root)
    data = load_run(run_dir)
    items = data.get('assessments', [])
    summary = summarize_assessments(items)
    batch_counts = scan_batch_results(args.results) if args.results else None
    md = write_markdown(run_dir, summary, batch_counts)
    if args.csv:
        csvp = Path(args.csv)
        # If only a filename is given, place it in the run folder
        if not csvp.is_absolute():
            csvp = run_dir / csvp
        write_csv(run_dir, summary, csvp)
        print("Decision audit CSV written:", csvp)
    print("Decision audit written:", md)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
