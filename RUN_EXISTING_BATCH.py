#!/usr/bin/env python3
"""Run pipeline using existing batch results - no new batch job"""

import json
import time
import sys
import os
from datetime import datetime

print("=" * 70)
print("RUNNING PIPELINE WITH EXISTING BATCH RESULTS")
print("=" * 70)

# Optional: load centralized configuration to populate env vars if missing
try:
    from config.loader import get_config  # type: ignore
    _cfg = get_config()
    os.environ.setdefault('MISTRAL_API_KEY', str(_cfg.get('mistral.api_key', '') or os.environ.get('MISTRAL_API_KEY', '')))
    os.environ.setdefault('HIGHERGOV_API_KEY', str(_cfg.get('highergov.api_key', '') or os.environ.get('HIGHERGOV_API_KEY', '')))
    os.environ.setdefault('HG_API_BASE_URL', str(_cfg.get('highergov.base_url', '') or os.environ.get('HG_API_BASE_URL', '')))
    os.environ.setdefault('MISTRAL_API_BASE_URL', str(_cfg.get('mistral.base_url', '') or os.environ.get('MISTRAL_API_BASE_URL', '')))
except Exception:
    pass

# Use existing files
batch_file = "Mistral_Batch_Processor/batch_results_20250912_201234.jsonl"
metadata_file = "Mistral_Batch_Processor/batch_metadata_20250912_174557.json"

print(f"\nUsing existing batch results:")
print(f"  Batch file: {batch_file}")
print(f"  Metadata: {metadata_file}")

# Parse batch results
print("\nParsing batch results...")
batch_results = []
with open(batch_file, 'r') as f:
    for line in f:
        if line.strip():
            data = json.loads(line)
            custom_id = data.get('custom_id', '')
            
            # Extract opportunity ID
            if custom_id.startswith('opp-'):
                remaining = custom_id[4:]
                if 'bBJ9cylAtDJ9Q-KCZfhu6' in remaining:
                    search_id = 'bBJ9cylAtDJ9Q-KCZfhu6'
                    after_search = remaining[len(search_id)+1:]
                    parts = after_search.rsplit('-', 1)
                    opp_id = parts[0] if parts else after_search
                else:
                    opp_id = custom_id
            else:
                opp_id = custom_id
            
            # Parse response
            response = data.get('response', {})
            if response.get('status_code') == 200:
                body = response.get('body', {})
                choices = body.get('choices', [])
                if choices:
                    content = choices[0]['message']['content']
                    
                    # Extract JSON
                    if '```json' in content:
                        json_str = content.split('```json')[1].split('```')[0]
                        result = json.loads(json_str)
                        
                        batch_results.append({
                            'opportunity_id': opp_id,
                            'batch_result': result
                        })

print(f"Parsed {len(batch_results)} batch results")

# Count decisions
decisions = {}
for r in batch_results:
    dec = r['batch_result'].get('recommendation', 'UNKNOWN')
    decisions[dec] = decisions.get(dec, 0) + 1

print("\nBatch decision breakdown:")
for dec, count in decisions.items():
    print(f"  {dec}: {count}")

# Load original opportunities
print("\nLoading original opportunities...")
with open(metadata_file, 'r') as f:
    metadata = json.load(f)

original_opps = metadata['opportunities']
regex_knockouts = metadata['regex_knockouts']

print(f"  Found {len(original_opps)} opportunities")
print(f"  Found {len(regex_knockouts)} regex knockouts")

# Prepare all results for unified output
all_results = []

# Add regex knockouts
print("\nProcessing regex knockouts...")
for ko in regex_knockouts:
    ko['assessment_type'] = 'REGEX_KNOCKOUT'
    ko['decision'] = 'NO-GO'
    ko['pipeline_stage'] = 'REGEX'
    all_results.append(ko)
print(f"  Added {len(regex_knockouts)} regex knockouts")

# Process batch results
print("\nProcessing batch results...")
batch_nogo_count = 0
needs_agent = []

for br in batch_results:
    opp_id = br['opportunity_id']
    recommendation = br['batch_result'].get('recommendation', 'UNKNOWN')
    
    # Find original opportunity
    original = None
    for opp in original_opps:
        if opp.get('opportunity_id') == opp_id:
            original = opp
            break
    
    if not original:
        continue
    
    if recommendation == 'NO-GO':
        # Batch NO-GO - stop here
        original['assessment_type'] = 'MISTRAL_BATCH_ASSESSMENT'
        original['decision'] = 'NO-GO'
        original['pipeline_stage'] = 'BATCH'
        original['batch_decision'] = 'NO-GO'
        all_results.append(original)
        batch_nogo_count += 1
    else:
        # GO or INDETERMINATE - needs agent
        needs_agent.append({
            'batch_result': br,
            'original': original,
            'batch_decision': recommendation
        })

print(f"  Batch NO-GOs: {batch_nogo_count}")
print(f"  Need agent verification: {len(needs_agent)}")

# Agent verification
if len(needs_agent) > 0:
    print(f"\nRunning agent verification on {len(needs_agent)} opportunities...")
    print(f"This will take approximately {len(needs_agent)} minutes")
    
    from ULTIMATE_MISTRAL_CONNECTOR import MistralSOSClassifier
    connector = MistralSOSClassifier()
    
    for i, item in enumerate(needs_agent, 1):
        opp = item['original']
        batch_dec = item['batch_decision']
        
        print(f"\n[{i}/{len(needs_agent)}] {opp.get('title', '')[:50]}...")
        print(f"  Batch: {batch_dec}")
        
        try:
            # Call agent
            agent_result = connector.classify_opportunity(opp)
            agent_decision = agent_result.get('classification', 'UNKNOWN')
            print(f"  Agent: {agent_decision}")
            
            # Record result
            opp['assessment_type'] = 'MISTRAL_ASSESSMENT'
            opp['decision'] = agent_decision
            opp['pipeline_stage'] = 'AGENT'
            opp['batch_decision'] = batch_dec
            opp['agent_decision'] = agent_decision
            
            if batch_dec != agent_decision:
                print(f"  >>> DISAGREEMENT!")
                opp['disagreement'] = True
            
            all_results.append(opp)
            
            # Delay between calls
            if i < len(needs_agent):
                print("  Waiting 60 seconds...")
                time.sleep(60)
                
        except Exception as e:
            print(f"  ERROR: {e}")
            opp['assessment_type'] = 'ERROR'
            opp['decision'] = batch_dec  # Use batch decision on error
            opp['error'] = str(e)
            all_results.append(opp)

# Generate unified output
print("\n" + "=" * 70)
print("GENERATING UNIFIED OUTPUT")
print("-" * 40)

from enhanced_output_manager import EnhancedOutputManager
output_manager = EnhancedOutputManager()

output_path = output_manager.save_assessment_batch(
    search_id='bBJ9cylAtDJ9Q-KCZfhu6',
    assessments=all_results,
    metadata={
        'pipeline_stages': ['regex', 'batch', 'agent'],
        'regex_knockouts': len(regex_knockouts),
        'batch_no_gos': batch_nogo_count,
        'agent_verified': len(needs_agent)
    }
)

print(f"\nPIPELINE COMPLETE!")
print(f"Results saved to: {output_path}")
