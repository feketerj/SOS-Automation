#!/usr/bin/env python3
"""
Transform artifacts to unified schema (result field) without touching originals.

Usage:
  python tools/transform_to_unified.py --file SOS_Output/.../data.json
  python tools/transform_to_unified.py --jsonl some.jsonl

Behavior:
  - For data.json: reads assessments, normalizes decision fields using DecisionSanitizer,
    and writes data_unified.json next to the original.
  - For JSONL: normalizes any top-level decision fields where possible and writes *_unified.jsonl.

Notes:
  - Purely additive; original files remain unchanged.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict


def normalize_record(rec: Dict[str, Any]) -> Dict[str, Any]:
    try:
        from decision_sanitizer import DecisionSanitizer  # type: ignore
        return DecisionSanitizer.sanitize(dict(rec))
    except Exception:
        # Fallback: simple field mapping
        out = dict(rec)
        if 'result' not in out:
            for k in ('final_decision', 'decision'):
                v = out.get(k)
                if isinstance(v, str) and v:
                    val = v.upper().replace('_', '-')
                    if val in ('GO', 'NO-GO', 'INDETERMINATE') or 'FURTHER' in val or 'CONTACT' in val:
                        out['result'] = 'FURTHER_ANALYSIS' if 'FURTHER' in val else ('CONTACT_CO' if 'CONTACT' in val else val)
                        break
        return out


def transform_json(path: Path) -> Path:
    data = json.loads(path.read_text(encoding='utf-8'))
    items = data.get('assessments', [])
    out_items = [normalize_record(x) for x in items]
    out_data = dict(data)
    out_data['assessments'] = out_items
    out_path = path.with_name('data_unified.json')
    out_path.write_text(json.dumps(out_data, indent=2), encoding='utf-8')
    return out_path


def transform_jsonl(path: Path) -> Path:
    out_path = path.with_name(path.stem + '_unified.jsonl')
    with path.open('r', encoding='utf-8') as fin, out_path.open('w', encoding='utf-8') as fout:
        for line in fin:
            s = line.strip()
            if not s:
                continue
            try:
                obj = json.loads(s)
            except Exception:
                fout.write(line)
                continue
            if isinstance(obj, dict):
                obj = normalize_record(obj)
            fout.write(json.dumps(obj) + '\n')
    return out_path


def main():
    p = argparse.ArgumentParser(description='Transform artifacts to unified schema (additive)')
    p.add_argument('--file', help='Path to data.json')
    p.add_argument('--jsonl', help='Path to a JSONL file')
    args = p.parse_args()

    if args.file:
        out = transform_json(Path(args.file).resolve())
        print('Wrote', out)
        return 0
    if args.jsonl:
        out = transform_jsonl(Path(args.jsonl).resolve())
        print('Wrote', out)
        return 0
    print('Provide --file or --jsonl')
    return 2


if __name__ == '__main__':
    raise SystemExit(main())

