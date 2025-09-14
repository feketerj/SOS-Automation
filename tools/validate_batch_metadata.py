#!/usr/bin/env python3
"""
Validate saved batch metadata files without affecting runtime.

Usage:
  python tools/validate_batch_metadata.py Mistral_Batch_Processor/batch_metadata_*.json [--strict]

Checks:
  - Required keys present: timestamp, search_ids, total_opportunities, total_regex_knockouts, jsonl_file
  - Counts match: len(opportunities) == total_opportunities; len(regex_knockouts) == total_regex_knockouts
  - jsonl_file exists in the same directory
  - Spot-check shape of entries in opportunities and regex_knockouts
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, Any

def warn(msg: str):
    print(f"WARN: {msg}")

def validate_metadata(path: Path, strict: bool) -> int:
    warnings = 0
    try:
        with open(path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to read {path}: {e}")
        return 1

    # Required keys
    req = [
        'timestamp', 'search_ids', 'total_opportunities', 'total_regex_knockouts',
        'jsonl_file', 'opportunities', 'regex_knockouts'
    ]
    for k in req:
        if k not in meta:
            warn(f"Missing key: {k}")
            warnings += 1

    # Counts
    opps = meta.get('opportunities', []) or []
    knocks = meta.get('regex_knockouts', []) or []
    if meta.get('total_opportunities') != len(opps):
        warn(f"total_opportunities mismatch: {meta.get('total_opportunities')} vs {len(opps)}")
        warnings += 1
    if meta.get('total_regex_knockouts') != len(knocks):
        warn(f"total_regex_knockouts mismatch: {meta.get('total_regex_knockouts')} vs {len(knocks)}")
        warnings += 1

    # jsonl_file existence
    jsonl_name = meta.get('jsonl_file')
    if jsonl_name:
        jsonl_path = path.parent / jsonl_name
        if not jsonl_path.exists():
            warn(f"jsonl_file not found: {jsonl_path}")
            warnings += 1

    # Spot check fields
    if opps:
        sample = opps[0]
        for k in ('search_id', 'opportunity_id', 'title'):
            if not sample.get(k):
                warn(f"opportunities[0] missing field: {k}")
                warnings += 1
    if knocks:
        sample = knocks[0]
        if sample.get('decision') and sample.get('decision') != 'NO-GO':
            warn("regex_knockouts[0] decision is not NO-GO (expected)")
            warnings += 1

    print(f"Validated: {path.name} | Warnings: {warnings}")
    return 1 if strict and warnings else 0

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    strict = '--strict' in sys.argv[2:]
    target = Path(sys.argv[1])
    exit_code = 0
    if target.is_file():
        exit_code = validate_metadata(target, strict)
    else:
        # Glob within a directory
        files = sorted(target.parent.glob(target.name)) if '*' in target.name else list(target.glob('batch_metadata_*.json'))
        if not files:
            print("No batch_metadata_*.json files found")
            return 2
        for f in files:
            rc = validate_metadata(f, strict)
            exit_code = rc if rc else exit_code
    return exit_code

if __name__ == '__main__':
    sys.exit(main())

