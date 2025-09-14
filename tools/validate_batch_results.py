#!/usr/bin/env python3
"""
Validate batch results JSONL files (Batch → Agent handoff).

Usage:
  python tools/validate_batch_results.py batch_results_*.jsonl [--metadata Mistral_Batch_Processor/batch_metadata_*.json] [--strict]

Checks (warn-only by default):
  - Each line parses as JSON and contains custom_id + response
  - Extracts assistant content; attempts to parse embedded JSON
  - Warns if model returns NO-GO (batch should avoid NO-GO)
  - Summarizes decisions; flags unexpected distribution
  - If --metadata provided: compares counts with metadata.opportunities
"""

import sys
import json
from pathlib import Path
from typing import List, Tuple, Optional

ALLOWED = {"GO", "NO-GO", "INDETERMINATE", "FURTHER_ANALYSIS", "CONTACT_CO"}

def warn(msg: str):
    print(f"WARN: {msg}")

def extract_content(obj: dict) -> str:
    body = (obj.get('response') or {}).get('body') or {}
    # mistralai SDK format
    if 'choices' in body:
        choices = body.get('choices', [])
        if choices:
            return (choices[0].get('message') or {}).get('content', '')
    # fallback
    return ''

def parse_result_from_text(text: str) -> Tuple[Optional[str], Optional[str]]:
    """Return (result_upper, short_reason) if parsed."""
    if not text:
        return None, None
    t = text
    try:
        # Extract JSON section if present
        if '```json' in t:
            json_str = t.split('```json', 1)[1].split('```', 1)[0].strip()
        elif '{' in t and '}' in t:
            start = t.index('{'); end = t.rindex('}') + 1
            json_str = t[start:end]
        else:
            json_str = ''
        if json_str:
            data = json.loads(json_str)
            # Prefer unified 'result' field
            res = (data.get('result') or data.get('recommendation') or '').upper()
            return (res if res else None, data.get('rationale') or data.get('reasoning'))
    except Exception:
        pass
    # Fallback heuristics
    for key in ('NO-GO', 'GO', 'INDETERMINATE', 'FURTHER', 'CONTACT'):
        if key in t.upper():
            if key == 'FURTHER':
                return 'FURTHER_ANALYSIS', None
            if key == 'CONTACT':
                return 'CONTACT_CO', None
            return key, None
    return None, None

def load_metadata_count(meta_path: Path) -> Optional[int]:
    try:
        with meta_path.open('r', encoding='utf-8') as f:
            meta = json.load(f)
        return int(meta.get('total_opportunities', 0))
    except Exception:
        return None

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    strict = '--strict' in sys.argv
    meta_file = None
    if '--metadata' in sys.argv:
        i = sys.argv.index('--metadata')
        if i + 1 < len(sys.argv):
            meta_file = Path(sys.argv[i+1])

    target = Path(sys.argv[1])
    if target.is_file():
        files = [target]
    else:
        pattern = target.name if '*' in target.name else 'batch_results_*.jsonl'
        root = target.parent if '*' in target.name else target
        files = sorted(root.glob(pattern))
    if not files:
        print('No batch_results_*.jsonl files found')
        return 2

    expected = None
    if meta_file and meta_file.exists():
        expected = load_metadata_count(meta_file)

    exit_code = 0
    for fp in files:
        warnings = 0
        counts = {k: 0 for k in ALLOWED}
        total = 0
        try:
            with fp.open('r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    if not line.strip():
                        continue
                    total += 1
                    try:
                        obj = json.loads(line)
                    except Exception as e:
                        warn(f"[{i}] JSON parse error: {e}")
                        warnings += 1
                        continue
                    content = extract_content(obj)
                    res, _ = parse_result_from_text(content)
                    if res is None:
                        warn(f"[{i}] Could not parse result from content")
                        warnings += 1
                        continue
                    res_u = res.upper()
                    if res_u not in ALLOWED:
                        warn(f"[{i}] Unexpected result value: {res_u}")
                        warnings += 1
                    else:
                        counts[res_u] += 1
                        # Batch ideally should not return NO-GO
                        if res_u == 'NO-GO':
                            warn(f"[{i}] Batch returned NO-GO (should be rare/converted)")
                            warnings += 1
        except Exception as e:
            print(f"ERROR: Failed to read {fp}: {e}")
            exit_code = 1
            continue

        print(f"Validated: {fp.name} | lines: {total} | warnings: {warnings}")
        print("Decision counts:")
        for k in ('GO', 'INDETERMINATE', 'NO-GO', 'FURTHER_ANALYSIS', 'CONTACT_CO'):
            print(f"  {k:17s}: {counts.get(k, 0)}")
        if expected is not None and expected != total:
            warn(f"Result count {total} does not match metadata total_opportunities {expected}")
            if strict:
                exit_code = 1
        if strict and warnings:
            exit_code = 1

    return exit_code

if __name__ == '__main__':
    sys.exit(main())

