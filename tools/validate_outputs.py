#!/usr/bin/env python3
"""
Validate saved pipeline outputs without affecting runtime.

Usage:
  python tools/validate_outputs.py <path-to-run-folder-or-data.json> [--strict]

Behavior:
  - Loads data.json from a run folder (or a direct file path)
  - Performs lightweight schema checks and prints WARN lines
  - Returns 0 on success even with warnings (unless --strict)
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List

ALLOWED_RESULTS = {"GO", "NO-GO", "INDETERMINATE", "FURTHER_ANALYSIS", "CONTACT_CO"}

REQUIRED_FIELDS = [
    "result",
    "announcement_number",
    "announcement_title",
    "agency",
]

URL_FIELDS = ["sam_url", "highergov_url"]

def load_data_json(target: Path) -> Dict:
    if target.is_dir():
        candidate = target / "data.json"
    else:
        candidate = target
    if not candidate.exists():
        raise FileNotFoundError(f"data.json not found at: {candidate}")
    with open(candidate, "r", encoding="utf-8") as f:
        return json.load(f)

def warn(msg: str):
    print(f"WARN: {msg}")

def validate_assessment(idx: int, a: Dict) -> int:
    warnings = 0
    # Decision present and valid
    res = str(a.get("result", "")).upper()
    if not res:
        warn(f"[{idx}] Missing result")
        warnings += 1
    elif res not in ALLOWED_RESULTS:
        warn(f"[{idx}] Unexpected result value: {res}")
        warnings += 1

    # Required non-empty fields
    for k in REQUIRED_FIELDS:
        v = a.get(k)
        if v is None or (isinstance(v, str) and not v.strip()):
            warn(f"[{idx}] Missing or empty field: {k}")
            warnings += 1

    # At least one URL present
    if not any(bool(a.get(u)) for u in URL_FIELDS):
        warn(f"[{idx}] Neither sam_url nor highergov_url present")
        warnings += 1

    # Types that should be strings (best effort)
    stringish = [
        "announcement_number", "announcement_title", "agency",
        "sos_pipeline_title", "rationale", "brief_description",
    ]
    for k in stringish:
        if k in a and a[k] is not None and not isinstance(a[k], str):
            warn(f"[{idx}] Field {k} should be a string (got {type(a[k]).__name__})")
            warnings += 1

    return warnings

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    target = Path(sys.argv[1]).resolve()
    strict = "--strict" in sys.argv[2:]

    try:
        payload = load_data_json(target)
    except Exception as e:
        print(f"ERROR: {e}")
        return 2

    assessments: List[Dict] = payload.get("assessments", [])
    meta = payload.get("metadata", {})
    print(f"Validating: {target}")
    print(f"Total assessments: {len(assessments)} | Search ID: {meta.get('search_id', 'N/A')}")

    total_warnings = 0
    for i, a in enumerate(assessments, 1):
        total_warnings += validate_assessment(i, a)

    print("\nSummary")
    print("-" * 40)
    print(f"Warnings: {total_warnings}")
    if strict and total_warnings:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())

