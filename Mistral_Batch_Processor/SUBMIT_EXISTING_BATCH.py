#!/usr/bin/env python3
"""Submit the already-created batch file to Mistral"""

import os
import time
from mistralai import Mistral

API_KEY = os.environ.get('MISTRAL_API_KEY', "1BPmHydlQmz81Z1edAs1ssQX3DbmW0Yf")
BATCH_FILE = "batch_input_20250912_090703.jsonl"
MODEL = "ft:pixtral-12b-latest:d42144c7:20250912:f7d61150"

print("Attempting to submit existing batch file...")
print(f"File: {BATCH_FILE}")
print(f"Model: {MODEL}")
print("=" * 50)

if not os.path.exists(BATCH_FILE):
    print(f"Error: {BATCH_FILE} not found")
    exit(1)

print(f"Found batch file, size: {os.path.getsize(BATCH_FILE)/1024:.1f} KB")

# Try submission with retries
for attempt in range(3):
    print(f"\nSubmission attempt {attempt + 1}/3...")
    try:
        client = Mistral(api_key=API_KEY)
        
        # Upload file
        print("  Uploading file...")
        with open(BATCH_FILE, 'rb') as f:
            batch_data = client.files.upload(
                file={
                    "file_name": BATCH_FILE,
                    "content": f.read()
                },
                purpose="batch"
            )
        print(f"  File uploaded: {batch_data.id}")
        
        # Create batch job
        print("  Creating batch job...")
        batch_job = client.batch.jobs.create(
            input_files=[batch_data.id],
            model=MODEL,
            endpoint="/v1/chat/completions"
        )
        
        print(f"\n[SUCCESS] Batch job created!")
        print(f"  Job ID: {batch_job.id}")
        print(f"  Status: {batch_job.status}")
        print(f"\nTo check status later:")
        print(f"  python CHECK_BATCH_STATUS.py {batch_job.id}")
        break
        
    except Exception as e:
        print(f"  Error: {e}")
        if attempt < 2:
            wait = (attempt + 1) * 10
            print(f"  Waiting {wait} seconds before retry...")
            time.sleep(wait)
        else:
            print("\nAll attempts failed")
            print("The API appears to be unavailable")