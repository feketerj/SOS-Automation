#!/usr/bin/env python3
"""
RUN_BATCH_NOW.py - Non-interactive batch processor with CORRECTED prompt
"""

import json
import os
import sys
import time
from datetime import datetime
from mistralai import Mistral

# Add parent directory to path
sys.path.append('..')

# Configuration
API_KEY = "1BPmHydlQmz81Z1edAs1ssQX3DbmW0Yf"
MODEL = "ft:mistral-medium-latest:d42144c7:20250902:908db254"  # Fine-tuned model

# Import required modules
from highergov_batch_fetcher import HigherGovBatchFetcher
from sos_ingestion_gate_v419 import IngestionGateV419

print("\n" + "="*70)
print("BATCH PROCESSOR WITH CORRECTED PROMPT")
print("="*70)

# Phase 1: Collect opportunities
print("\nPhase 1: Collecting opportunities...")
fetcher = HigherGovBatchFetcher()
regex_gate = IngestionGateV419()

# Read test endpoints
endpoints_file = '../test_endpoints.txt'
if not os.path.exists(endpoints_file):
    endpoints_file = '../endpoints.txt'

with open(endpoints_file, 'r') as f:
    search_ids = [line.strip() for line in f if line.strip() and not line.startswith('#')][:2]  # Just first 2

print(f"Processing {len(search_ids)} search IDs")

all_opportunities = []
for search_id in search_ids:
    print(f"  Fetching {search_id}...")
    raw_opps = fetcher.fetch_all_opportunities(search_id)
    for opp in raw_opps:
        processed = fetcher.process_opportunity(opp)
        processed['search_id'] = search_id
        processed['opportunity_id'] = opp.get('id', 'unknown')
        
        # Run regex
        regex_result = regex_gate.assess_opportunity(processed)
        processed['regex_decision'] = regex_result.decision.value
        
        if regex_result.decision.value != 'NO-GO':
            all_opportunities.append(processed)

print(f"\nOpportunities for AI assessment: {len(all_opportunities)}")

# Phase 2: Create batch file with CORRECTED prompt
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
jsonl_file = f"batch_corrected_{timestamp}.jsonl"

print(f"\nPhase 2: Creating batch file with CORRECTED prompt...")
with open(jsonl_file, 'w') as f:
    for i, opp in enumerate(all_opportunities):
        # CORRECTED PROMPT FORMAT
        prompt = f"""Context: You are an expert assessment specialist for Source One Spares (SOS), a small organic supplier specializing in surplus military and aviation parts.

Question: Analyze this government contracting opportunity for Source One Spares:

Title: {opp['title']}
Agency: {opp.get('agency', 'N/A')}
NAICS: {opp.get('naics', 'N/A')}
PSC: {opp.get('psc', 'N/A')}

Requirements excerpt: {opp.get('text', '')[:400000]}"""

        # NO SYSTEM MESSAGE - just user content
        batch_request = {
            "custom_id": f"opp-{i:04d}",
            "body": {
                "model": MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 2000
            }
        }
        
        f.write(json.dumps(batch_request) + '\n')

print(f"Created {jsonl_file} with {len(all_opportunities)} requests")

# Phase 3: Submit to Mistral
print("\nPhase 3: Submitting to Mistral...")
client = Mistral(api_key=API_KEY)

# Upload file
with open(jsonl_file, 'rb') as f:
    batch_data = client.files.upload(
        file={
            "file_name": jsonl_file,
            "content": f.read()
        },
        purpose="batch"
    )

print(f"File uploaded: {batch_data.id}")

# Create batch job
batch_job = client.batch.jobs.create(
    input_files=[batch_data.id],
    model=MODEL,
    endpoint="/v1/chat/completions",
    metadata={
        "job_type": "sos_corrected_prompt",
        "created": datetime.now().isoformat()
    }
)

print(f"Batch job created: {batch_job.id}")
print(f"Status: {batch_job.status}")

# Phase 4: Monitor
print("\nPhase 4: Monitoring job...")
while True:
    job = client.batch.jobs.get(batch_job.id)
    print(f"  Status: {job.status} | Progress: {job.completed_requests}/{job.total_requests}")
    
    if job.status in ["SUCCESS", "FAILED", "CANCELLED"]:
        break
    
    time.sleep(5)

if job.status == "SUCCESS":
    print("\nPhase 5: Downloading results...")
    result_file_id = job.output_file
    result_content = client.files.download(result_file_id)
    
    results_file = f"results_corrected_{timestamp}.jsonl"
    with open(results_file, 'wb') as f:
        f.write(result_content)
    
    print(f"Results saved to {results_file}")
    
    # Parse and show sample
    print("\nSample results:")
    with open(results_file, 'r') as f:
        for i, line in enumerate(f):
            if i < 3:
                result = json.loads(line)
                response = result['response']['body']['choices'][0]['message']['content']
                print(f"\n{result['custom_id']}: {response[:200]}...")
else:
    print(f"\nJob failed with status: {job.status}")

print("\n" + "="*70)
print("BATCH PROCESSING COMPLETE")
print("="*70)