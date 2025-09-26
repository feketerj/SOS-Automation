#!/usr/bin/env python3
"""Quick batch test with minimal opportunities to verify Pixtral model works"""

import json
import os
import sys
from datetime import datetime
from mistralai import Mistral

# Configuration
API_KEY = "2oAquITdDMiyyk0OfQuJSSqePn3SQbde"
MODEL = "ft:pixtral-12b-latest:d42144c7:20250912:f7d61150"  # New Pixtral model

# System prompt and few-shot examples
SYSTEM_PROMPT = """You are an expert government contract analyst specializing in SOS assessments."""

def create_batch_request(opp_id, title, description):
    """Create a single batch request"""
    return {
        "custom_id": f"test-{opp_id}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Assess this opportunity:\n\nTitle: {title}\n\nDescription: {description}\n\nProvide GO/NO-GO decision."}
            ],
            "temperature": 0.1,
            "max_tokens": 500
        }
    }

def main():
    print("="*60)
    print("QUICK BATCH TEST - PIXTRAL MODEL")
    print("="*60)
    
    # Create test opportunities
    test_opps = [
        ("001", "Boeing 737 Part", "Commercial aircraft part for Boeing 737"),
        ("002", "F-16 Component", "Military fighter jet component for F-16"),
        ("003", "Generic O-Ring", "Standard O-ring, NSN 5331-00-123-4567")
    ]
    
    # Create batch file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_file = f"test_batch_{timestamp}.jsonl"
    
    print(f"\nCreating batch file: {batch_file}")
    with open(batch_file, 'w') as f:
        for opp_id, title, desc in test_opps:
            request = create_batch_request(opp_id, title, desc)
            f.write(json.dumps(request) + '\n')
    
    print(f"Created batch file with {len(test_opps)} requests")
    
    # Upload and submit batch
    print("\nUploading to Mistral...")
    client = Mistral(api_key=API_KEY)
    
    with open(batch_file, 'rb') as f:
        batch_data = client.files.upload(
            file={"file_name": batch_file, "content": f.read()},
            purpose="batch"
        )
    
    print(f"File uploaded: {batch_data.id}")
    
    # Submit batch job
    print("\nSubmitting batch job...")
    job = client.batch.jobs.create(
        input_files=[batch_data.id],
        model=MODEL,
        endpoint="/v1/chat/completions",
        metadata={"type": "quick_test", "model": "pixtral"}
    )
    
    print(f"\nBatch job submitted successfully!")
    print(f"Job ID: {job.id}")
    print(f"Status: {job.status}")
    print(f"\nTo check status: python CHECK_BATCH_STATUS.py {job.id}")
    
    # Clean up
    os.remove(batch_file)
    print(f"\nCleaned up temporary file: {batch_file}")

if __name__ == "__main__":
    main()