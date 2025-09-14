#!/usr/bin/env python3
"""
Archive old SOS_Output runs into dated _ARCHIVE_ folders (non-destructive).

Usage:
  python tools/archive_outputs.py [--days 30]

Behavior:
  - Finds Run_* folders older than N days under SOS_Output/YYYY-MM/
  - Moves them into SOS_Output/_ARCHIVE_YYYY_MM_DD/
  - Skips existing _ARCHIVE_* folders; creates archive folder if needed

Notes:
  - No deletion performed; safe to run repeatedly.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'SOS_Output'


def archive(days: int) -> int:
    if not OUT.exists():
        print("SOS_Output not found; nothing to archive.")
        return 0
    cutoff = datetime.now() - timedelta(days=days)
    moved = 0

    # Collect candidate run folders across monthly subfolders
    for month_dir in OUT.iterdir():
        if not month_dir.is_dir():
            continue
        if month_dir.name.startswith('_ARCHIVE'):
            continue
        for run_dir in month_dir.iterdir():
            if not run_dir.is_dir() or not run_dir.name.startswith('Run_'):
                continue
            mtime = datetime.fromtimestamp(run_dir.stat().st_mtime)
            if mtime >= cutoff:
                continue
            # Prepare archive destination at top level with date stamp
            stamp = datetime.now().strftime('%Y_%m_%d')
            archive_dir = OUT / f"_ARCHIVE_{stamp}"
            archive_dir.mkdir(exist_ok=True)
            dest = archive_dir / f"{month_dir.name}_{run_dir.name}"
            try:
                shutil.move(str(run_dir), str(dest))
                print(f"Archived: {run_dir.relative_to(OUT)} -> {dest.relative_to(OUT)}")
                moved += 1
            except Exception as e:
                print(f"WARN: Failed to archive {run_dir}: {e}")

    print(f"Total archived: {moved}")
    return 0


def main():
    parser = argparse.ArgumentParser(description='Archive old SOS_Output runs')
    parser.add_argument('--days', type=int, default=30, help='Age in days to archive (default: 30)')
    args = parser.parse_args()
    return archive(args.days)


if __name__ == '__main__':
    raise SystemExit(main())

