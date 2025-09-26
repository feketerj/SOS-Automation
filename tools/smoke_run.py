#!/usr/bin/env python3
"""
Smoke run: minimal end-to-end preflight without changing pipeline code.

Default behavior (no paid API calls):
  - Runs setup checks
  - Uses HigherGov fetcher on the first search ID with max_pages=1
  - Applies Regex gate; writes a batch_input JSONL + metadata for later
  - Optionally runs validators on the produced files

Usage:
  python tools/smoke_run.py [--validate]

Options:
  --validate   Run handoff validators on produced files (warn-only)

Note: This wrapper does NOT submit batch jobs or call the agent. Use RUN_BATCH_AGENT.bat for full pipeline.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def run_setup_check() -> None:
    print("\n[1/5] Running setup check...")
    try:
        subprocess.run([sys.executable, str(ROOT / 'CHECK_SETUP.py')], check=False)
    except Exception as e:
        print(f"WARN: Could not run setup check: {e}")

def read_first_endpoint() -> str:
    ep = ROOT / 'endpoints.txt'
    if not ep.exists():
        raise FileNotFoundError("endpoints.txt not found at repo root")
    for line in ep.read_text(encoding='utf-8').splitlines():
        s = line.strip()
        if s and not s.startswith('#'):
            return s
    raise ValueError("No search IDs found in endpoints.txt")

def collect_minimal(search_id: str, max_pages: int = 1):
    print("\n[2/5] Collecting minimal set from HigherGov...")
    sys.path.insert(0, str(ROOT))
    from highergov_batch_fetcher import HigherGovBatchFetcher
    from sos_ingestion_gate_v419 import IngestionGateV419, Decision

    fetcher = HigherGovBatchFetcher()
    regex_gate = IngestionGateV419()

    try:
        raw = fetcher.fetch_all_opportunities(search_id, max_pages=max_pages)
    except Exception as e:
        print(f"ERROR: Failed to fetch from HigherGov: {e}")
        return [], []

    collected = []
    knockouts = []
    for opp in raw:
        try:
            processed = fetcher.process_opportunity(opp)
            regex_result = regex_gate.assess_opportunity(processed)
            if regex_result.decision != Decision.NO_GO:
                # Prepare minimal record for batching
                title = processed.get('title', '')
                text = processed.get('text', '') or processed.get('description', '')
                collected.append({
                    'search_id': search_id,
                    'opportunity_id': processed.get('id', opp.get('opportunity_id', 'unknown')),
                    'title': title,
                    'text': (text or '')[:400_000],
                    'regex_decision': regex_result.decision.value,
                    'regex_reason': regex_result.primary_blocker or 'None'
                })
            else:
                knockouts.append({
                    'search_id': search_id,
                    'opportunity_id': processed.get('id', opp.get('opportunity_id', 'unknown')),
                    'title': processed.get('title', ''),
                    'decision': Decision.NO_GO.value,
                    'regex_decision': Decision.NO_GO.value,
                    'reasoning': f"Regex knockout: {regex_result.primary_blocker}",
                    'processing_method': 'REGEX_ONLY'
                })
        except Exception as e:
            print(f"WARN: Failed to process an opportunity: {e}")
            continue

    print(f"  Opportunities for batch: {len(collected)}")
    print(f"  Regex knockouts:        {len(knockouts)}")
    return collected, knockouts

def write_batch_files(opportunities, knockouts):
    print("\n[3/5] Writing batch input + metadata...")
    out_dir = ROOT / 'Mistral_Batch_Processor'
    out_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    jsonl_file = out_dir / f"batch_input_{timestamp}_SMOKE.jsonl"

    # Optional: load config for model id and text limit
    model_id = "ag:d42144c7:20250902:sos-triage-agent:73e9cddd"
    text_limit = 400_000
    try:
        from config.loader import get_config  # type: ignore
        cfg = get_config()
        model_id = cfg.get('mistral.model_id', model_id)
        text_limit = int(cfg.get('pipeline.text_extraction_char_limit', text_limit))
    except Exception:
        pass

    # Create JSONL file similar to BATCH_COLLECTOR
    with jsonl_file.open('w', encoding='utf-8') as f:
        for i, opp in enumerate(opportunities):
            prompt = (
                f"Analyze this opportunity for sole-source potential:\n\n"
                f"TITLE: {opp['title']}\n\nDOCUMENT TEXT (first 400K chars):\n{opp['text']}\n\n"
                f"The regex engine preliminarily classified this as: {opp['regex_decision']}\n"
                f"Provide your final assessment in JSON with fields: result, rationale."
            )
            batch_request = {
                "custom_id": f"opp-{opp['search_id']}-{opp['opportunity_id']}-{i:04d}",
                "body": {
                    "model": model_id,
                    "messages": [
                        {"role": "system", "content": "You are an expert procurement analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 2000
                }
            }
            f.write(json.dumps(batch_request) + '\n')

    metadata = {
        'timestamp': timestamp,
        'search_ids': list({o['search_id'] for o in opportunities} | {k['search_id'] for k in knockouts}),
        'total_opportunities': len(opportunities),
        'total_regex_knockouts': len(knockouts),
        'jsonl_file': jsonl_file.name,
        'opportunities': opportunities,
        'regex_knockouts': knockouts
    }
    meta_file = out_dir / f"batch_metadata_{timestamp}_SMOKE.json"
    meta_file.write_text(json.dumps(metadata, indent=2), encoding='utf-8')

    print(f"  Wrote: {jsonl_file}")
    print(f"  Wrote: {meta_file}")
    return jsonl_file, meta_file

def maybe_run_validators(jsonl_path: Path, meta_path: Path, run: bool):
    if not run:
        return
    print("\n[4/5] Running validators (warn-only)...")
    try:
        subprocess.run([sys.executable, str(ROOT / 'tools' / 'validate_batch_input.py'), str(jsonl_path)], check=False)
    except Exception as e:
        print(f"WARN: batch input validator failed: {e}")
    try:
        subprocess.run([sys.executable, str(ROOT / 'tools' / 'validate_batch_metadata.py'), str(meta_path)], check=False)
    except Exception as e:
        print(f"WARN: batch metadata validator failed: {e}")

def main():
    validate = '--validate' in sys.argv[1:]
    print("=" * 70)
    print("SOS SMOKE RUN (no batch/agent submission)")
    print("=" * 70)

    run_setup_check()
    try:
        sid = read_first_endpoint()
    except Exception as e:
        print(f"ERROR: {e}")
        return 1

    opps, knocks = collect_minimal(sid, max_pages=1)
    jsonl, meta = write_batch_files(opps, knocks)

    maybe_run_validators(jsonl, meta, validate)

    print("\n[5/5] Summary")
    print("-" * 40)
    print(f"Search ID:           {sid}")
    print(f"To Batch (count):    {len(opps)}")
    print(f"Regex Knockouts:     {len(knocks)}")
    print(f"Batch input JSONL:   {jsonl}")
    print(f"Batch metadata JSON: {meta}")
    print("\nNext steps:")
    print("  - For full pipeline: RUN_BATCH_AGENT.bat (Regex -> Batch -> Agent)")
    print("  - Or submit the smoke JSONL to create a small batch job")
    return 0

if __name__ == '__main__':
    sys.exit(main())
