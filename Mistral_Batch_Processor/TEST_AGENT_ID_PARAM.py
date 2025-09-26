#!/usr/bin/env python3
"""Test batch API with agent_id parameter (not model field)"""

import json
from datetime import datetime
from mistralai import Mistral

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
jsonl_file = f"test_agent_param_{timestamp}.jsonl"

# Create batch file - agent models might not need model field in JSONL
batch_request = {
    "custom_id": "test-agent-param",
    "body": {
        # Don't specify model here for agents
        "messages": [
            {"role": "user", "content": "Test with agent"}
        ],
        "temperature": 0.1,
        "max_tokens": 100
    }
}

with open(jsonl_file, 'w') as f:
    f.write(json.dumps(batch_request) + '\n')

print(f"Created {jsonl_file}")
print("Attempting batch with agent_id parameter...")

try:
    client = Mistral(api_key="1BPmHydlQmz81Z1edAs1ssQX3DbmW0Yf")
    
    # Upload file
    with open(jsonl_file, 'rb') as f:
        batch_data = client.files.upload(
            file={"file_name": jsonl_file, "content": f.read()},
            purpose="batch"
        )
    print(f"File uploaded: {batch_data.id}")
    
    # Try using agent_id PARAMETER (not model)
    batch_job = client.batch.jobs.create(
        input_files=[batch_data.id],
        agent_id="ag:d42144c7:20250902:sos-triage-agent:73e9cddd",  # Use agent_id param!
        endpoint="/v1/chat/completions",
        metadata={"test": "agent_via_param"}
    )
    print(f"SUCCESS! Batch job created with agent_id: {batch_job.id}")
    print(f"Status: {batch_job.status}")
    
except Exception as e:
    print(f"FAILED: {e}")