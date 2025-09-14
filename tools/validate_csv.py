#!/usr/bin/env python3
"""
Validate assessment.csv columns and basic row integrity (optional).

Usage:
  python tools/validate_csv.py SOS_Output/YYYY-MM/Run_*/assessment.csv

Checks:
  - Required columns present
  - No empty values in key ID/title columns
  - Optional: print first N rows of URL fields for spot check
"""

import csv
import sys
from pathlib import Path


REQUIRED = [
    'result', 'knock_pattern', 'knockout_category', 'sos_pipeline_title',
    'sam_url', 'highergov_url', 'announcement_number', 'announcement_title',
    'agency', 'due_date'
]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    path = Path(sys.argv[1]).resolve()
    if not path.exists():
        print('File not found:', path)
        return 2
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED if c not in reader.fieldnames]
        if missing:
            print('WARN: Missing required columns:', ', '.join(missing))
        else:
            print('OK: All required columns present')
        # Basic row scans
        empty_ids = 0
        url_samples = []
        for i, row in enumerate(reader, 1):
            if not row.get('announcement_number') or not row.get('announcement_title'):
                empty_ids += 1
            if len(url_samples) < 5:
                url_samples.append((row.get('sam_url', ''), row.get('highergov_url', '')))
        print(f'Total rows: {i if "i" in locals() else 0}')
        print(f'Rows with empty id/title: {empty_ids}')
        if url_samples:
            print('URL samples:')
            for s, h in url_samples:
                print('  sam:', s)
                print('  hg :', h)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

