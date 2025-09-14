#!/usr/bin/env python3
"""
Validate batch input JSONL files (Regex → Batch handoff).

Usage:
  python tools/validate_batch_input.py Mistral_Batch_Processor/batch_input_*.jsonl [--strict]

Checks (warn-only by default):
  - Each line parses as JSON and contains required keys: custom_id, body.messages
  - Message array has a system + user message
  - User content length is within reasonable bounds (<= ~420k chars)
  - Detects if regex decision appears to be NO-GO (should not be forwarded)
"""

import sys
import json
from pathlib import Path
from typing import List

MAX_CONTENT_LEN = 420_000  # soft cap

def warn(msg: str):
    print(f"WARN: {msg}")

def validate_line(idx: int, obj: dict) -> int:
    warnings = 0
    if not isinstance(obj, dict):
        warn(f"[{idx}] Not a JSON object")
        return 1
    if 'custom_id' not in obj:
        warn(f"[{idx}] Missing custom_id")
        warnings += 1
    body = obj.get('body') or obj.get('request') or {}
    messages: List[dict] = (body or {}).get('messages') or []
    if not isinstance(messages, list) or len(messages) < 2:
        warn(f"[{idx}] Expected at least system + user messages")
        warnings += 1
    else:
        # Assume last message is user content
        content = (messages[-1] or {}).get('content') or ''
        if not isinstance(content, str) or not content.strip():
            warn(f"[{idx}] Empty user content")
            warnings += 1
        else:
            if len(content) > MAX_CONTENT_LEN:
                warn(f"[{idx}] User content appears too large: {len(content):,} chars")
                warnings += 1
            # Heuristic: catch forwarded NO-GO
            lowered = content.lower()
            if 'regex engine preliminarily classified' in lowered and 'no-go' in lowered:
                warn(f"[{idx}] Regex decision looks like NO-GO in batch input")
                warnings += 1
    return warnings

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    target = Path(sys.argv[1])
    strict = '--strict' in sys.argv[2:]

    # Gather files
    files: List[Path]
    if target.is_file():
        files = [target]
    else:
        pattern = target.name if '*' in target.name else 'batch_input_*.jsonl'
        root = target.parent if '*' in target.name else target
        files = sorted(root.glob(pattern))
    if not files:
        print("No batch_input_*.jsonl files found")
        return 2

    exit_code = 0
    for fp in files:
        warnings = 0
        count = 0
        try:
            with fp.open('r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    if not line.strip():
                        continue
                    count += 1
                    try:
                        obj = json.loads(line)
                    except Exception as e:
                        warn(f"[{i}] JSON parse error: {e}")
                        warnings += 1
                        continue
                    warnings += validate_line(i, obj)
        except Exception as e:
            print(f"ERROR: Failed to read {fp}: {e}")
            exit_code = 1
            continue
        print(f"Validated: {fp.name} | requests: {count} | warnings: {warnings}")
        if strict and warnings:
            exit_code = 1
    return exit_code

if __name__ == '__main__':
    sys.exit(main())

