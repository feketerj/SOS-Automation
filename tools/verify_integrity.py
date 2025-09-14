#!/usr/bin/env python3
"""
Verify data integrity between batch metadata (pre‑AI) and saved run outputs (post‑pipeline).

Usage:
  python tools/verify_integrity.py --meta Mistral_Batch_Processor/batch_metadata_*.json --run SOS_Output/YYYY-MM/Run_*/

Checks (warn-only):
  - Ensures each opportunity forwarded to AI (from metadata.opportunities) appears in data.json assessments
  - Compares critical fields (announcement_number/title, URLs) for drift
  - Produces simple hashes for before/after to detect mutations

No runtime changes; purely diagnostic.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Tuple


def stable_hash(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, ensure_ascii=False).encode('utf-8')
    return hashlib.sha256(data).hexdigest()[:12]


def key_from_opp(opp: Dict[str, Any]) -> Tuple[str, str]:
    return (str(opp.get('search_id', '')), str(opp.get('opportunity_id', opp.get('id', ''))))


def collect_meta(path: Path) -> Dict[Tuple[str, str], Dict[str, Any]]:
    meta = json.loads(path.read_text(encoding='utf-8'))
    index: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for opp in meta.get('opportunities', []):
        index[key_from_opp(opp)] = opp
    return index


def collect_run(path: Path) -> Dict[Tuple[str, str], Dict[str, Any]]:
    data = json.loads((path / 'data.json').read_text(encoding='utf-8'))
    index: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for a in data.get('assessments', []):
        key = (str(a.get('search_id', '')), str(a.get('opportunity_id', a.get('solicitation_id', a.get('id', '')))))
        index[key] = a
    return index


def compare(meta_idx: Dict[Tuple[str, str], Dict[str, Any]], run_idx: Dict[Tuple[str, str], Dict[str, Any]]) -> None:
    missing = []
    drifts = 0
    checked = 0

    for key, m in meta_idx.items():
        r = run_idx.get(key)
        if not r:
            missing.append(key)
            continue
        checked += 1
        # Compare critical fields
        fields = [
            ('announcement_number', ('announcement_number', 'solicitation_id', 'source_id')),
            ('announcement_title', ('announcement_title', 'solicitation_title', 'title')),
            ('sam_url', ('sam_url', 'source_path')),
            ('highergov_url', ('highergov_url', 'hg_url', 'path', 'url')),
        ]
        for label, candidates in fields:
            pre = next((m.get(c) for c in candidates if m.get(c)), None)
            post = next((r.get(c) for c in candidates if r.get(c)), None)
            if pre and post and str(pre) != str(post):
                drifts += 1
                print(f"WARN: Drift in {label} for {key}: pre='{pre}' post='{post}'")

        # Hash snapshots (subset)
        pre_hash = stable_hash({
            'id': m.get('opportunity_id') or m.get('id'),
            'title': m.get('title'),
            'urls': [m.get('source_path'), m.get('path')],
        })
        post_hash = stable_hash({
            'id': r.get('opportunity_id') or r.get('solicitation_id') or r.get('id'),
            'title': r.get('announcement_title') or r.get('solicitation_title') or r.get('title'),
            'urls': [r.get('sam_url'), r.get('highergov_url'), r.get('hg_url')],
        })
        if pre_hash != post_hash:
            # Not necessarily an error, but helpful signal
            print(f"INFO: Snapshot hash changed for {key}: {pre_hash} -> {post_hash}")

    print("\nSummary")
    print("-" * 40)
    print(f"Meta forwarded opportunities: {len(meta_idx)}")
    print(f"Found in run:                {checked}")
    print(f"Missing from run:            {len(missing)}")
    print(f"Field drifts flagged:        {drifts}")
    if missing:
        for key in missing[:10]:
            print("  Missing:", key)


def main() -> int:
    p = argparse.ArgumentParser(description='Verify integrity between metadata and run outputs (warn-only)')
    p.add_argument('--meta', required=True, help='Path to batch_metadata_*.json')
    p.add_argument('--run', required=True, help='Path to SOS_Output/YYYY-MM/Run_*/')
    args = p.parse_args()

    meta_path = next((Path(m) for m in glob.glob(args.meta)), None)
    if not meta_path or not meta_path.exists():
        print('Metadata file not found:', args.meta)
        return 2
    run_dir = Path(args.run)
    if not (run_dir.exists() and (run_dir / 'data.json').exists()):
        print('Run folder invalid:', run_dir)
        return 2

    meta_idx = collect_meta(meta_path)
    run_idx = collect_run(run_dir)
    compare(meta_idx, run_idx)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

