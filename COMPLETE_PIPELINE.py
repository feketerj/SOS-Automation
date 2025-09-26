#!/usr/bin/env python3
"""Complete the pipeline - download batch results and run agent verification"""

import json
import time
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.append('.')
sys.path.append('Mistral_Batch_Processor')

print("=" * 70)
print("COMPLETING PIPELINE - BATCH RESULTS TO AGENT VERIFICATION")
print("=" * 70)

# Step 1: Download batch results
print("\nSTEP 1: DOWNLOADING BATCH RESULTS")
print("-" * 40)

from mistralai import Mistral
from API_KEYS import MISTRAL_API_KEY

client = Mistral(api_key=MISTRAL_API_KEY)
job_id = "9d1d5895-d144-45af-a3a9-11d070b52222"  # Latest batch job

# Get job and download results
job = client.batch.jobs.get(job_id=job_id)
print(f"Job status: {job.status}")
print(f"Completed: {job.succeeded_requests}/{job.total_requests}")

if job.status != "SUCCESS":
    print("Job not complete!")
    sys.exit(1)

# Download results
print(f"Downloading from: {job.output_file}")
output = client.files.download(file_id=job.output_file)
content = output.read()

# Save batch results
batch_file = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
with open(batch_file, 'wb') as f:
    f.write(content)
print(f"Saved to: {batch_file}")

# Step 2: Parse batch results
print("\nSTEP 2: PARSING BATCH RESULTS")
print("-" * 40)

batch_results = []
with open(batch_file, 'r') as f:
    for line in f:
        if line.strip():
            data = json.loads(line)
            custom_id = data.get('custom_id', '')
            
            # Extract opportunity ID
            # Format is: opp-{search_id}-{opportunity_id}-{index}
            # Search ID contains hyphen, so need careful parsing
            if custom_id.startswith('opp-'):
                remaining = custom_id[4:]  # Remove 'opp-'
                # Find the search ID (bBJ9cylAtDJ9Q-KCZfhu6)
                if 'bBJ9cylAtDJ9Q-KCZfhu6' in remaining:
                    search_id = 'bBJ9cylAtDJ9Q-KCZfhu6'
                    # Everything after search ID and next hyphen is opportunity ID
                    after_search = remaining[len(search_id)+1:]  # Skip search ID and hyphen
                    # Opportunity ID is everything before the last hyphen
                    parts = after_search.rsplit('-', 1)
                    opp_id = parts[0] if parts else after_search
                else:
                    parts = remaining.split('-')
                    search_id = '-'.join(parts[:2]) if len(parts) >= 2 else parts[0]
                    opp_id = parts[2] if len(parts) > 2 else 'unknown'
            else:
                search_id = 'unknown'
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
                        
                        # Convert NO-GO to INDETERMINATE (batch shouldn't return NO-GO)
                        if result.get('recommendation') == 'NO-GO':
                            result['recommendation'] = 'INDETERMINATE'
                            result['batch_note'] = 'Converted from NO-GO'
                        
                        batch_results.append({
                            'search_id': search_id,
                            'opportunity_id': opp_id,
                            'batch_result': result
                        })

print(f"Parsed {len(batch_results)} results")

# Count decisions
decisions = {}
for r in batch_results:
    dec = r['batch_result'].get('recommendation', 'UNKNOWN')
    decisions[dec] = decisions.get(dec, 0) + 1

print("Decision breakdown:")
for dec, count in decisions.items():
    print(f"  {dec}: {count}")

# Step 3: Load original opportunities
print("\nSTEP 3: LOADING ORIGINAL OPPORTUNITIES")
print("-" * 40)

metadata_file = "Mistral_Batch_Processor/batch_metadata_20250912_174557.json"
with open(metadata_file, 'r') as f:
    metadata = json.load(f)

original_opps = metadata['opportunities']
regex_knockouts = metadata['regex_knockouts']

print(f"Loaded {len(original_opps)} opportunities")
print(f"Loaded {len(regex_knockouts)} regex knockouts")

# Step 4: Filter for agent verification
print("\nSTEP 4: SELECTING OPPORTUNITIES FOR AGENT VERIFICATION")
print("-" * 40)

needs_verification = []
for br in batch_results:
    if br['batch_result'].get('recommendation') in ['GO', 'INDETERMINATE']:
        # Find original opportunity
        for opp in original_opps:
            if opp.get('opportunity_id') == br['opportunity_id']:
                needs_verification.append({
                    'batch_result': br,
                    'original_opp': opp
                })
                break

print(f"Need agent verification: {len(needs_verification)}")

# Step 5: Run agent verification (with timing delays)
print("\nSTEP 5: AGENT VERIFICATION")
print("-" * 40)
print("NOTE: This will take approximately {} minutes (1 min per opportunity)".format(len(needs_verification)))

if len(needs_verification) > 0:
    response = input("\nProceed with agent verification? (y/n): ").strip().lower()
    if response != 'y':
        print("Skipping agent verification")
        sys.exit(0)
    
    from ULTIMATE_MISTRAL_CONNECTOR import MistralSOSClassifier
    connector = MistralSOSClassifier()
    
    verified_results = []
    for i, item in enumerate(needs_verification, 1):
        opp = item['original_opp']
        batch = item['batch_result']
        
        print(f"\n[{i}/{len(needs_verification)}] Verifying: {opp.get('title', '')[:50]}...")
        print(f"  Batch decision: {batch['batch_result'].get('recommendation')}")
        
        try:
            # Call agent
            agent_result = connector.classify_opportunity(opp)
            
            print(f"  Agent decision: {agent_result.get('decision', 'UNKNOWN')}")
            
            if agent_result.get('decision') != batch['batch_result'].get('recommendation'):
                print(f"  DISAGREEMENT! Batch: {batch['batch_result'].get('recommendation')} -> Agent: {agent_result.get('decision')}")
            
            verified_results.append({
                'opportunity_id': opp.get('opportunity_id'),
                'title': opp.get('title'),
                'batch_decision': batch['batch_result'].get('recommendation'),
                'agent_decision': agent_result.get('decision'),
                'final_decision': agent_result.get('decision'),  # Agent is authoritative
                'disagreement': agent_result.get('decision') != batch['batch_result'].get('recommendation')
            })
            
            # Add delay between calls (except after last one)
            if i < len(needs_verification):
                print("  Waiting 60 seconds before next verification...")
                time.sleep(60)
                
        except Exception as e:
            print(f"  ERROR: {e}")
            verified_results.append({
                'opportunity_id': opp.get('opportunity_id'),
                'error': str(e),
                'final_decision': batch['batch_result'].get('recommendation')  # Keep batch decision on error
            })
    
    # Step 6: Generate final output
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE")
    print("=" * 70)
    
    # Summary
    disagreements = sum(1 for v in verified_results if v.get('disagreement'))
    print(f"\nVerification Summary:")
    print(f"  Total verified: {len(verified_results)}")
    print(f"  Disagreements: {disagreements}")
    print(f"  Agreement rate: {(len(verified_results) - disagreements) / len(verified_results) * 100:.1f}%")
    
    # Save results
    output_file = f"pipeline_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'regex_knockouts': len(regex_knockouts),
            'batch_processed': len(batch_results),
            'agent_verified': len(verified_results),
            'disagreements': disagreements,
            'results': verified_results
        }, f, indent=2)
    
    print(f"\nFinal results saved to: {output_file}")

else:
    print("No opportunities need agent verification (all were NO-GO)")

print("\nPIPELINE COMPLETE!")
