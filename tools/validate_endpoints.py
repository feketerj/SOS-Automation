#!/usr/bin/env python3
"""
Validate endpoints.txt format (optional, read-only).

Usage:
  python tools/validate_endpoints.py [endpoints.txt]

Checks:
  - File exists
  - Non-empty search IDs
  - Detects duplicates and prints counts
"""

from __future__ import annotations

import sys
from pathlib import Path
from collections import Counter


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('endpoints.txt')
    if not path.exists():
        print('WARN: endpoints file not found:', path)
        return 2
    ids = []
    for line in path.read_text(encoding='utf-8').splitlines():
        s = line.strip()
        if s and not s.startswith('#'):
            ids.append(s)
    if not ids:
        print('WARN: endpoints contains no search IDs')
        return 0
    counts = Counter(ids)
    dups = [k for k, v in counts.items() if v > 1]
    print('Total search IDs:', len(ids))
    if dups:
        print('WARN: duplicate IDs detected:', ', '.join(dups))
    else:
        print('OK: no duplicates found')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

