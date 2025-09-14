#!/usr/bin/env python3
"""
Summarize a saved run in SOS_Output without changing any behavior.

Usage:
  python tools/summarize_run.py [SOS_Output/YYYY-MM/Run_*/]

If no path is provided, the latest Run_* folder is used.

Outputs:
  - Counts by result (GO, NO-GO, INDETERMINATE)
  - Optional agent disagreement rate if agent fields are present
  - Top knockout categories/patterns (if available)
  - File locations (assessment.csv, data.json)
"""

import json
import sys
from pathlib import Path
from collections import Counter
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'SOS_Output'

def find_latest_run() -> Path:
    if not OUT.exists():
        raise FileNotFoundError("SOS_Output folder not found")
    months = sorted([p for p in OUT.iterdir() if p.is_dir()], key=lambda p: p.stat().st_mtime, reverse=True)
    for month in months:
        runs = sorted([p for p in month.iterdir() if p.is_dir() and p.name.startswith('Run_')], key=lambda p: p.stat().st_mtime, reverse=True)
        if runs:
            return runs[0]
    raise FileNotFoundError("No Run_* folders found under SOS_Output")

def load_data(run_dir: Path) -> Dict:
    dj = run_dir / 'data.json'
    if not dj.exists():
        raise FileNotFoundError(f"data.json not found in {run_dir}")
    return json.loads(dj.read_text(encoding='utf-8'))

def summarize(assessments: List[Dict]):
    results = Counter()
    knock_cats = Counter()
    knock_patterns = Counter()
    disagreements = 0
    with_agent_fields = False

    for a in assessments:
        res = str(a.get('result', '')).upper() or str(a.get('final_decision', '')).upper()
        results[res] += 1
        kc = a.get('knockout_category')
        if kc:
            knock_cats[kc] += 1
        kp = a.get('knock_pattern')
        if kp:
            knock_patterns[kp] += 1
        if 'batch_decision' in a and 'agent_decision' in a:
            with_agent_fields = True
            if a.get('batch_decision') != a.get('agent_decision'):
                disagreements += 1

    return {
        'results': results,
        'knock_cats': knock_cats.most_common(5),
        'knock_patterns': knock_patterns.most_common(5),
        'with_agent_fields': with_agent_fields,
        'disagreements': disagreements,
    }

def main():
    if len(sys.argv) > 1:
        run_dir = Path(sys.argv[1]).resolve()
        if run_dir.is_file():
            run_dir = run_dir.parent
    else:
        run_dir = find_latest_run()

    data = load_data(run_dir)
    assessments = data.get('assessments', [])
    meta = data.get('metadata', {})

    info = summarize(assessments)

    print("=" * 70)
    print("RUN SUMMARY")
    print("=" * 70)
    print(f"Run folder:          {run_dir}")
    print(f"Search ID:           {meta.get('search_id', 'N/A')}")
    print(f"Total assessments:   {len(assessments)}")
    print("-" * 40)
    for k in ('GO', 'NO-GO', 'INDETERMINATE'):
        print(f"{k:16s}: {info['results'].get(k, 0)}")
    other = sum(v for r, v in info['results'].items() if r not in {'GO', 'NO-GO', 'INDETERMINATE'})
    if other:
        print(f"OTHER            : {other}")

    if info['with_agent_fields']:
        need_ver = info['results'].get('GO', 0) + info['results'].get('INDETERMINATE', 0)
        if need_ver:
            rate = (need_ver - info['disagreements']) / need_ver * 100.0
            print("-" * 40)
            print(f"Agent disagreements: {info['disagreements']}")
            print(f"Agreement rate     : {rate:.1f}%")

    if info['knock_cats']:
        print("-" * 40)
        print("Top knockout categories:")
        for cat, cnt in info['knock_cats']:
            print(f"  {cat:8s} : {cnt}")
    if info['knock_patterns']:
        print("Top knockout patterns:")
        for pat, cnt in info['knock_patterns']:
            print(f"  {cnt:4d}  {pat[:80]}")

    # File paths
    print("-" * 40)
    print(f"assessment.csv     : {run_dir / 'assessment.csv'}")
    print(f"data.json          : {run_dir / 'data.json'}")
    print(f"report.md          : {run_dir / 'report.md'}")
    go_csv = run_dir / 'GO_opportunities.csv'
    if go_csv.exists():
        print(f"GO_opportunities   : {go_csv}")
    print("=" * 70)
    return 0

if __name__ == '__main__':
    sys.exit(main())

