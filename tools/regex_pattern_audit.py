#!/usr/bin/env python3
"""
Regex Pattern Audit (read-only, optional).

Usage:
  python tools/regex_pattern_audit.py packs/regex_pack_v419_complete.yaml

Reports:
  - Total patterns and categories
  - Regex compile errors (if any)
  - Top categories by pattern count

Notes:
  - Uses PyYAML if available; otherwise prints a brief notice and exits.
  - Does not modify runtime behavior.
"""

from __future__ import annotations

import sys
from pathlib import Path
from collections import Counter


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    path = Path(sys.argv[1]).resolve()
    if not path.exists():
        print('File not found:', path)
        return 2
    try:
        import yaml  # type: ignore
    except Exception:
        print('PyYAML not installed; install with `pip install pyyaml` to run this audit.')
        return 0

    data = yaml.safe_load(path.read_text(encoding='utf-8'))
    patterns = []
    # Expect a structure like { categories: [ { id, name, patterns: [ ... ] } ] }
    categories = data.get('categories') or data.get('Categories') or []
    cat_counter = Counter()
    compile_errors = []
    total = 0

    import re
    for cat in categories:
        cid = str(cat.get('id') or cat.get('category_id') or cat.get('name') or 'unknown')
        pats = cat.get('patterns') or []
        for p in pats:
            # pattern may be a string or object with 'regex'
            regex = p if isinstance(p, str) else (p.get('regex') if isinstance(p, dict) else None)
            if not regex:
                continue
            total += 1
            cat_counter[cid] += 1
            try:
                re.compile(regex)
            except Exception as e:
                compile_errors.append((cid, regex, str(e)))

    print('=' * 60)
    print('REGEX PATTERN AUDIT')
    print('=' * 60)
    print('File:', path)
    print('Total categories:', len(cat_counter))
    print('Total patterns  :', total)
    if compile_errors:
        print('\nCompile errors (first 10):')
        for cid, rx, err in compile_errors[:10]:
            print(f'  [{cid}] {rx[:80]} -> {err}')
    else:
        print('\nNo compile errors detected.')
    print('\nTop categories by pattern count:')
    for cid, cnt in cat_counter.most_common(10):
        print(f'  {cid:12s}: {cnt}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

