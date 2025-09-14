#!/usr/bin/env python3
"""
Audit field name variants across the repo and saved outputs (read-only).

Usage:
  python tools/audit_field_mappings.py [root=.] [--include-outputs] [--markdown report.md]

What it does:
  - Scans source/tests for field name variants commonly used in the pipeline
    (result, decision, final_decision, classification, processing_method,
     pipeline_stage, assessment_type, rationale, reasoning, sos_pipeline_title,
     sam_url, hg_url, highergov_url)
  - Optionally scans SOS_Output when --include-outputs is set
  - Prints counts and a few example locations for each field

Notes:
  - Purely diagnostic; does not modify any files.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List, Tuple

ROOT_DEFAULT = Path.cwd()

FIELDS = [
    "result",
    "decision",
    "final_decision",
    "classification",
    "processing_method",
    "pipeline_stage",
    "assessment_type",
    "rationale",
    "reasoning",
    "sos_pipeline_title",
    "sam_url",
    "hg_url",
    "highergov_url",
]

INCLUDE_EXT = {".py", ".json", ".jsonl", ".md"}


def should_scan(path: Path, include_outputs: bool) -> bool:
    name = path.name
    if name.startswith("."):
        return False
    if not include_outputs and "SOS_Output" in path.parts:
        return False
    # Skip heavy archives
    if any(part.startswith("_ARCHIVE") for part in path.parts):
        return False
    return True


def scan_file(fp: Path, fields: List[str]) -> List[Tuple[str, int, str]]:
    results: List[Tuple[str, int, str]] = []
    try:
        text = fp.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return results
    lower = text.lower()
    for f in fields:
        idx = 0
        f_l = f.lower()
        while True:
            pos = lower.find(f_l, idx)
            if pos == -1:
                break
            # compute line number cheaply
            line_no = lower.count("\n", 0, pos) + 1
            # grab a small snippet
            start = max(0, pos - 30)
            end = min(len(text), pos + len(f) + 30)
            snippet = text[start:end].replace("\n", " ")
            results.append((f, line_no, snippet))
            idx = pos + len(f_l)
    return results


def main():
    include_outputs = "--include-outputs" in sys.argv[1:]
    md_target = None
    args_wo_flags = []
    i = 1
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == '--markdown' and i + 1 < len(sys.argv):
            md_target = sys.argv[i+1]
            i += 2
            continue
        if a == '--include-outputs':
            i += 1
            continue
        if not a.startswith('--'):
            args_wo_flags.append(a)
        i += 1
    root_arg = args_wo_flags[0] if args_wo_flags else None
    root = Path(root_arg).resolve() if root_arg else ROOT_DEFAULT

    print("=" * 60)
    print("FIELD MAPPING AUDIT (read-only)")
    print("=" * 60)
    print(f"Root: {root}")
    print(f"Include SOS_Output: {'yes' if include_outputs else 'no'}\n")

    counts: Dict[str, int] = {f: 0 for f in FIELDS}
    examples: Dict[str, List[Tuple[str, int, str]]] = {f: [] for f in FIELDS}

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in INCLUDE_EXT:
            continue
        if not should_scan(path, include_outputs):
            continue
        hits = scan_file(path, FIELDS)
        for f, ln, snip in hits:
            counts[f] += 1
            # Keep up to 5 examples per field
            if len(examples[f]) < 5:
                rel = str(path.relative_to(root))
                examples[f].append((rel, ln, snip))

    if md_target:
        lines = []
        lines.append(f"# Field Mapping Audit\n\n")
        lines.append(f"Root: {root}\n\n")
        lines.append("## Counts by Field\n")
        for f in FIELDS:
            lines.append(f"- {f}: {counts[f]}\n")
        lines.append("\n## Examples\n")
        for f in FIELDS:
            if examples[f]:
                lines.append(f"\n### {f}\n")
                for rel, ln, snip in examples[f]:
                    lines.append(f"- {rel}:{ln} :: {snip}\n")
        Path(md_target).write_text(''.join(lines), encoding='utf-8')
        print('Wrote report:', md_target)
    else:
        print("Counts by field:")
        for f in FIELDS:
            print(f"  {f:18s}: {counts[f]}")

        print("\nExamples:")
        for f in FIELDS:
            if examples[f]:
                print(f"\n[{f}]")
                for rel, ln, snip in examples[f]:
                    print(f"  - {rel}:{ln} :: {snip}")

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
