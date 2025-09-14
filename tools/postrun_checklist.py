#!/usr/bin/env python3
"""
Post-run checklist (optional, read-only): orchestrates validators and summaries.

Usage:
  python tools/postrun_checklist.py [SOS_Output/YYYY-MM/Run_*/]

Runs (best-effort, warn-only):
  - Output JSON checks (validate_outputs)
  - CSV structure checks (validate_csv)
  - Schema validation (if jsonschema installed)
  - Decision audit + metrics generation

Writes artifacts next to data.json:
  - decision_audit.md
  - metrics.json
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def latest_run(root: Path) -> Path:
    months = sorted([p for p in root.iterdir() if p.is_dir()], key=lambda p: p.stat().st_mtime, reverse=True)
    for m in months:
        runs = sorted([p for p in m.iterdir() if p.is_dir() and p.name.startswith('Run_')], key=lambda p: p.stat().st_mtime, reverse=True)
        if runs:
            return runs[0]
    raise FileNotFoundError('No Run_* folders found')


def run_cmd(args: list[str]) -> None:
    try:
        subprocess.run(args, check=False)
    except Exception as e:
        print('WARN:', ' '.join(args), 'failed:', e)


def main() -> int:
    root = Path('SOS_Output').resolve()
    run_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else latest_run(root)
    data_json = run_dir / 'data.json'
    csv_path = run_dir / 'assessment.csv'

    print('=' * 60)
    print('SOS POST-RUN CHECKLIST (optional)')
    print('=' * 60)
    print('Run folder:', run_dir)

    if data_json.exists():
        run_cmd([sys.executable, str(Path('tools/validate_outputs.py')), str(run_dir)])
        # Schema validation (agent schema) with summary if available
        run_cmd([sys.executable, str(Path('tools/validate_schema.py')), '--schema', str(Path('schemas/agent_assessment.schema.json')), '--file', str(data_json), '--summary'])
        # Decision audit (write markdown + optional CSV summary)
        run_cmd([sys.executable, str(Path('tools/decision_audit.py')), str(run_dir), '--csv', 'decision_audit_summary.csv'])
        run_cmd([sys.executable, str(Path('tools/generate_metrics.py')), str(run_dir)])
    else:
        print('WARN: data.json not found, skipping JSON checks')

    if csv_path.exists():
        run_cmd([sys.executable, str(Path('tools/validate_csv.py')), str(csv_path)])
    else:
        print('WARN: assessment.csv not found, skipping CSV checks')

    print('\nDone.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
