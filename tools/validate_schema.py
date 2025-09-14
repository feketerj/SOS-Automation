#!/usr/bin/env python3
"""
Validate artifacts against JSON Schemas (optional, warn-only by default).

Usage:
  python tools/validate_schema.py --schema schemas/agent_assessment.schema.json --file SOS_Output/.../data.json
  python tools/validate_schema.py --schema schemas/batch_assessment.schema.json --jsonl Mistral_Batch_Processor/batch_results_*.jsonl
  python tools/validate_schema.py --schema schemas/agent_assessment.schema.json --file SOS_Output/.../data.json --summary

Notes:
  - Uses jsonschema if installed; otherwise prints a note and exits 0.
  - For data.json, validates each item in "assessments" array.
  - For JSONL, extracts per-line JSON object and validates it directly.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict


def load_json(path: Path) -> Any:
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def load_schema(path: Path) -> Dict[str, Any]:
    return load_json(path)


def validate_object(validator, schema: Dict[str, Any], obj: Any, src: str, idx: int, strict: bool) -> int:
    try:
        validator.validate(obj, schema)
    except Exception as e:
        print(f"WARN: {src} item {idx}: {e}")
        return 1 if strict else 0
    return 0


def main():
    p = argparse.ArgumentParser(description='Validate JSON against schema (optional)')
    p.add_argument('--schema', required=True, help='Path to JSON Schema file')
    p.add_argument('--file', help='Path to JSON file (e.g., data.json)')
    p.add_argument('--jsonl', help='Path or glob to JSONL file(s)')
    p.add_argument('--strict', action='store_true', help='Exit non-zero on first error')
    p.add_argument('--summary', action='store_true', help='Print a short summary of validation results')
    args = p.parse_args()

    try:
        import jsonschema  # type: ignore
    except Exception:
        print('jsonschema not installed; skipping strict validation (pass).')
        return 0

    schema_path = Path(args.schema).resolve()
    schema = load_schema(schema_path)
    Validator = jsonschema.Draft202012Validator
    validator = Validator(schema)

    errors = 0
    checked = 0
    first_errors = []
    if args.file:
        path = Path(args.file).resolve()
        data = load_json(path)
        items = data.get('assessments', [])
        for i, obj in enumerate(items, 1):
            checked += 1
            try:
                validator.validate(obj, schema)
            except Exception as e:
                errors += 1
                if len(first_errors) < 10:
                    # Attempt to extract a helpful path
                    loc = getattr(e, 'path', [])
                    loc_s = '/'.join(str(p) for p in loc) if loc else ''
                    first_errors.append(f"{path.name} item {i}: {loc_s} -> {e}")
                if args.strict:
                    print(f"WARN: {path.name} item {i}: {e}")
                    return 1
    elif args.jsonl:
        import glob
        for g in glob.glob(args.jsonl):
            path = Path(g)
            with path.open('r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except Exception as e:
                        if len(first_errors) < 10:
                            first_errors.append(f"{path.name} line {i}: JSON parse error: {e}")
                        if args.strict:
                            print(f"WARN: {path.name} line {i}: JSON parse error: {e}")
                            return 1
                        continue
                    checked += 1
                    try:
                        validator.validate(obj, schema)
                    except Exception as e:
                        errors += 1
                        if len(first_errors) < 10:
                            loc = getattr(e, 'path', [])
                            loc_s = '/'.join(str(p) for p in loc) if loc else ''
                            first_errors.append(f"{path.name} item {i}: {loc_s} -> {e}")
                        if args.strict:
                            print(f"WARN: {path.name} item {i}: {e}")
                            return 1
    else:
        print('Provide either --file or --jsonl')
        return 2

    if args.summary:
        print('Validation summary:')
        print('  Items checked :', checked)
        print('  Errors        :', errors)
        if first_errors:
            print('  First errors:')
            for msg in first_errors:
                print('   -', msg)

    if args.strict and errors:
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
