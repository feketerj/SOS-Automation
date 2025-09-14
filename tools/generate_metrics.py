#!/usr/bin/env python3
"""
Generate a machine-readable metrics.json for a saved run (optional, read-only).

Usage:
  python tools/generate_metrics.py [SOS_Output/YYYY-MM/Run_*/]

If no path is provided, uses the latest run.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict


def find_latest_run(out_root: Path) -> Path:
    months = sorted([p for p in out_root.iterdir() if p.is_dir()], key=lambda p: p.stat().st_mtime, reverse=True)
    for m in months:
        runs = sorted([p for p in m.iterdir() if p.is_dir() and p.name.startswith('Run_')], key=lambda p: p.stat().st_mtime, reverse=True)
        if runs:
            return runs[0]
    raise FileNotFoundError("No Run_* folders found")


def summarize(items: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter()
    cats = Counter()
    patterns = Counter()
    agent_fields = False
    disagreements = 0
    need_ver = 0

    for a in items:
        res = (str(a.get('result') or a.get('final_decision') or '').upper())
        if res:
            counts[res] += 1
        kc = a.get('knockout_category')
        if kc:
            cats[kc] += 1
        kp = a.get('knock_pattern')
        if kp:
            patterns[kp] += 1
        if 'batch_decision' in a or 'agent_decision' in a:
            agent_fields = True
            bd = a.get('batch_decision')
            ad = a.get('agent_decision')
            if bd in ('GO', 'INDETERMINATE'):
                need_ver += 1
            if bd and ad and bd != ad:
                disagreements += 1

    metrics = {
        'total': sum(counts.values()),
        'counts': dict(counts),
        'top_knockout_categories': cats.most_common(10),
        'top_knockout_patterns': patterns.most_common(10),
    }
    if agent_fields and need_ver:
        metrics['agent'] = {
            'disagreements': disagreements,
            'agreement_rate': (need_ver - disagreements) / need_ver,
        }
    return metrics


def main() -> int:
    import sys
    out_root = Path('SOS_Output').resolve()
    run_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else find_latest_run(out_root)
    data_path = run_dir / 'data.json'
    if not data_path.exists():
        print('data.json not found:', data_path)
        return 2
    data = json.loads(data_path.read_text(encoding='utf-8'))
    items = data.get('assessments', [])
    metrics = summarize(items)
    out_path = run_dir / 'metrics.json'
    out_path.write_text(json.dumps(metrics, indent=2), encoding='utf-8')
    print('Wrote metrics:', out_path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

