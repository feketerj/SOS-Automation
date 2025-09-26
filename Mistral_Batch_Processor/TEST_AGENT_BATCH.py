#!/usr/bin/env python3
"""Test if batch API accepts agent ID"""

import json
from datetime import datetime
from mistralai import Mistral

# Create minimal batch file with AGENT ID
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
jsonl_file = f"test_agent_{timestamp}.jsonl"

batch_request = {
    "custom_id": "test-agent",
    "body": {
        "model": "ag:d42144c7:20250902:sos-triage-agent:73e9cddd",  # AGENT ID
        "messages": [
            {"role": "user", "content": "Test"}
        ],
        "temperature": 0.1,
        "max_tokens": 100
    }
}

with open(jsonl_file, 'w') as f:
    f.write(json.dumps(batch_request) + '\n')

print(f"Created {jsonl_file} with AGENT model ID")
print("Attempting to submit to batch API...")

try:
    client = Mistral(api_key="1BPmHydlQmz81Z1edAs1ssQX3DbmW0Yf")
    
    # Upload file
    with open(jsonl_file, 'rb') as f:
        batch_data = client.files.upload(
            file={"file_name": jsonl_file, "content": f.read()},
            purpose="batch"
        )
    print(f"File uploaded: {batch_data.id}")
    
    # Try to create batch job with agent model
    batch_job = client.batch.jobs.create(
        input_files=[batch_data.id],
        model="ag:d42144c7:20250902:sos-triage-agent:73e9cddd",  # AGENT ID
        endpoint="/v1/chat/completions",
        metadata={"test": "agent_batch"}
    )
    print(f"SUCCESS?! Batch job created: {batch_job.id}")
    print(f"Status: {batch_job.status}")
    
except Exception as e:
    print(f"FAILED (as expected): {e}")