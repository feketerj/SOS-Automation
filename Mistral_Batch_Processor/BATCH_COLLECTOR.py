#!/usr/bin/env python3
"""
BATCH_COLLECTOR.py - Collects all opportunities and creates JSONL for Mistral batch processing
COMPLETELY SEPARATE from main system - won't break anything
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict

# Add parent directory to path to import existing modules
sys.path.append('..')

def collect_opportunities_from_searches(search_ids: List[str]) -> List[Dict]:
    """
    Collect all opportunities from multiple search IDs
    Uses existing fetcher but doesn't process them
    """
    from highergov_batch_fetcher import HigherGovBatchFetcher
    from sos_ingestion_gate_v419 import IngestionGateV419
    
    all_opportunities = []
    regex_knockouts = []  # Track what got knocked out
    fetcher = HigherGovBatchFetcher()
    regex_gate = IngestionGateV419()
    
    total_regex_knockouts = 0

    # Optional: apply a batch size cap from centralized config across all IDs
    try:
        from config.loader import get_config  # type: ignore
        _cfg = get_config()
        _limit = _cfg.get('pipeline.batch_size_limit')
        cap = int(_limit) if _limit else None
    except Exception:
        cap = None
    
    for idx, search_id in enumerate(search_ids, 1):
        print(f"\n[{idx}/{len(search_ids)}] Fetching opportunities for {search_id}...")
        try:
            # Use existing fetcher
            opportunities = fetcher.fetch_all_opportunities(search_id)
            print(f"  Found {len(opportunities)} opportunities")
            
            collected_count = 0
            knocked_out_count = 0

            # Optional parallel document fetching (config-gated; default off)
            use_parallel = False
            max_workers = 2
            try:
                from config.loader import get_config  # type: ignore
                _cfg = get_config()
                use_parallel = bool(str(_cfg.get('pipeline.parallel_fetch.enabled', '') or ''))
                _mw = _cfg.get('pipeline.parallel_fetch.max_workers')
                if _mw:
                    max_workers = max(1, int(_mw))
            except Exception:
                pass

            if use_parallel:
                try:
                    from concurrent.futures import ThreadPoolExecutor, as_completed
                    doc_map = {}
                    tasks = {}
                    with ThreadPoolExecutor(max_workers=max_workers) as ex:
                        for idx, opp in enumerate(opportunities):
                            dpath = opp.get('document_path')
                            if dpath:
                                tasks[ex.submit(fetcher.fetch_document_text, dpath)] = idx
                    for fut in as_completed(tasks):
                        idx = tasks[fut]
                        try:
                            doc_map[idx] = fut.result()
                        except Exception:
                            doc_map[idx] = ""
                    # Attach texts
                    for i, opp in enumerate(opportunities):
                        opp['text'] = doc_map.get(i, "")
                except Exception:
                    # Fallback to sequential on any parallel failure
                    for opp in opportunities:
                        dpath = opp.get('document_path')
                        opp['text'] = fetcher.fetch_document_text(dpath) if dpath else ""
            else:
                for opp in opportunities:
                    dpath = opp.get('document_path')
                    opp['text'] = fetcher.fetch_document_text(dpath) if dpath else ""

                # Run regex to filter obvious NO-GOs
                regex_result = regex_gate.assess_opportunity(opp)
                
                # Only collect GO and FURTHER_ANALYSIS for model
                if str(regex_result.decision) != 'Decision.NO_GO':
                    all_opportunities.append({
                        'search_id': search_id,
                        'opportunity_id': opp.get('opportunity_id', 'unknown'),
                        'title': opp.get('title', ''),
                        'text': document_text[:400000],  # 400K limit  
                        'regex_decision': str(regex_result.decision),
                        'regex_reason': regex_result.primary_blocker or 'None'
                    })
                    collected_count += 1
                    print(f"  Collected: {opp.get('title', 'Unknown')[:50]}...")
                else:
                    knocked_out_count += 1
                    total_regex_knockouts += 1
                    # Save regex knockouts too!
                    regex_knockouts.append({
                        'search_id': search_id,
                        'opportunity_id': opp.get('opportunity_id', 'unknown'),
                        'title': opp.get('title', ''),
                        'decision': 'NO-GO',
                        'reasoning': f"Regex knockout: {regex_result.primary_blocker}",
                        'knockout_patterns': regex_result.primary_blocker,
                        'processing_method': 'REGEX_ONLY'
                    })
                    print(f"  Regex knocked out: {opp.get('title', 'Unknown')[:50]}...")
            # Apply cap if defined
            if cap is not None and len(all_opportunities) > cap:
                all_opportunities = all_opportunities[:cap]
                print(f"  [INFO] Applying batch size limit: {cap}")
            
            print(f"  Summary: {collected_count} for model, {knocked_out_count} knocked out by regex")
                    
        except Exception as e:
            print(f"Error fetching {search_id}: {e}")
    
    print(f"\n" + "=" * 60)
    print(f"COLLECTION SUMMARY:")
    print(f"  Total opportunities collected for model: {len(all_opportunities)}")
    print(f"  Total knocked out by regex: {total_regex_knockouts}")
    print(f"  Total processed: {len(all_opportunities) + total_regex_knockouts}")
    print("=" * 60)
    return all_opportunities, regex_knockouts

def create_batch_jsonl(opportunities: List[Dict], output_file: str = "batch_input.jsonl"):
    """
    Create JSONL file for Mistral batch processing
    """
    
    with open(output_file, 'w') as f:
        for i, opp in enumerate(opportunities):
            # Create the prompt
            prompt = f"""Analyze this opportunity for sole-source potential:

TITLE: {opp['title']}

DOCUMENT TEXT (first 400K chars):
{opp['text']}

The regex engine preliminarily classified this as: {opp['regex_decision']}

Provide your final assessment. Return a JSON response:
{{
    "decision": "GO" or "NO-GO" or "INDETERMINATE",
    "reasoning": "Brief explanation of your decision",
    "knockout_patterns": ["any specific patterns found"],
    "confidence": 0-100
}}"""

            # Create batch request format
            batch_request = {
                "custom_id": f"opp-{opp['search_id']}-{opp['opportunity_id']}-{i:04d}",
                "body": {
                    "model": "ag:d42144c7:20250902:sos-triage-agent:73e9cddd",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert procurement analyst specializing in identifying sole-source opportunities."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.1,
                    "max_tokens": 2000
                }
            }
            
            # Write as JSONL (one JSON object per line)
            f.write(json.dumps(batch_request) + '\n')
    
    print(f"Created {output_file} with {len(opportunities)} requests")
    return output_file

def main():
    """
    Main function to collect and prepare batch
    """
    print("=" * 60)
    print("MISTRAL BATCH COLLECTOR")
    print("Prepares opportunities for batch processing")
    print("=" * 60)
    
    # Read endpoints
    if os.path.exists('../endpoints.txt'):
        with open('../endpoints.txt', 'r') as f:
            search_ids = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    else:
        print("No endpoints.txt found")
        return
    
    print(f"\nFound {len(search_ids)} search IDs")
    
    # Collect all opportunities
    opportunities, regex_knockouts = collect_opportunities_from_searches(search_ids)
    
    if not opportunities and not regex_knockouts:
        print("No opportunities to process")
        return
    
    # Create JSONL file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    jsonl_file = f"batch_input_{timestamp}.jsonl"
    create_batch_jsonl(opportunities, jsonl_file)
    
    # Save metadata for later processing
    # Compute simple snapshot hashes (for integrity checks)
    import hashlib, json as _json
    def _snap(items):
        try:
            base = [
                {
                    'sid': x.get('search_id',''),
                    'oid': x.get('opportunity_id',''),
                    'title': x.get('title',''),
                    'urls': [x.get('text','')[:0]]
                }
                for x in items
            ]
            return hashlib.sha256(_json.dumps(base, sort_keys=True).encode('utf-8')).hexdigest()[:12]
        except Exception:
            return ""

    metadata = {
        'timestamp': timestamp,
        'search_ids': search_ids,
        'total_opportunities': len(opportunities),
        'total_regex_knockouts': len(regex_knockouts),
        'jsonl_file': jsonl_file,
        'opportunities': opportunities,  # Save for mapping results back
        'regex_knockouts': regex_knockouts,  # Save regex knockouts too!
        'opportunity_snapshot_hash': _snap(opportunities),
        'regex_knockouts_snapshot_hash': _snap(regex_knockouts)
    }
    
    metadata_file = f"batch_metadata_{timestamp}.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\nSaved metadata to {metadata_file}")
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("1. Upload the JSONL file to Mistral")
    print("2. Create batch job with the file")
    print("3. Download results when complete")
    print("4. Run BATCH_RESULTS_PARSER.py to process")
    print("=" * 60)

if __name__ == "__main__":
    main()
