#!/usr/bin/env python3
"""
BATCH_SUBMITTER.py - Submits JSONL file to Mistral for batch processing
Uses Mistral's batch API for efficient bulk processing
"""

import json
import requests
import sys
import os
from datetime import datetime

# Hardcoded API key (same as main system)
API_KEY = "1BPmHydlQmz81Z1edAs1ssQX3DbmW0Yf"
BASE_URL = "https://api.mistral.ai/v1"

def upload_file(filepath: str) -> str:
    """
    Upload JSONL file to Mistral
    Returns file_id for batch creation
    """
    print(f"Uploading {filepath}...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    with open(filepath, 'rb') as f:
        files = {
            'file': (os.path.basename(filepath), f, 'application/jsonl'),
            'purpose': (None, 'batch')
        }
        
        response = requests.post(
            f"{BASE_URL}/files",
            headers=headers,
            files=files
        )
    
    if response.status_code == 200:
        file_data = response.json()
        file_id = file_data['id']
        print(f"File uploaded successfully: {file_id}")
        return file_id
    else:
        print(f"Upload failed: {response.status_code}")
        print(response.text)
        return None

def create_batch_job(file_id: str, description: str = "SOS Assessment Batch") -> str:
    """
    Create batch job with uploaded file
    Returns batch_id for tracking
    """
    print(f"Creating batch job...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    batch_data = {
        "input_file_id": file_id,
        "endpoint": "/v1/chat/completions",
        "completion_window": "24h",
        "metadata": {
            "description": description,
            "created": datetime.now().isoformat()
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/batch/jobs",
        headers=headers,
        json=batch_data
    )
    
    if response.status_code == 200:
        batch = response.json()
        batch_id = batch['id']
        print(f"Batch created successfully: {batch_id}")
        print(f"Status: {batch.get('status', 'unknown')}")
        return batch_id
    else:
        print(f"Batch creation failed: {response.status_code}")
        print(response.text)
        return None

def check_batch_status(batch_id: str) -> dict:
    """
    Check status of batch job
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    response = requests.get(
        f"{BASE_URL}/batches/{batch_id}",
        headers=headers
    )
    
    if response.status_code == 200:
        batch = response.json()
        print(f"Batch {batch_id}:")
        print(f"  Status: {batch.get('status')}")
        print(f"  Progress: {batch.get('request_counts', {})}")
        
        if batch.get('status') == 'completed':
            print(f"  Output file: {batch.get('output_file_id')}")
            return batch
    else:
        print(f"Status check failed: {response.status_code}")
    
    return None

def download_results(output_file_id: str, save_as: str = None) -> str:
    """
    Download batch results
    """
    if not save_as:
        save_as = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    response = requests.get(
        f"{BASE_URL}/files/{output_file_id}/content",
        headers=headers
    )
    
    if response.status_code == 200:
        with open(save_as, 'wb') as f:
            f.write(response.content)
        print(f"Results saved to {save_as}")
        return save_as
    else:
        print(f"Download failed: {response.status_code}")
        return None

def main():
    """
    Main submission flow
    """
    print("=" * 60)
    print("MISTRAL BATCH SUBMITTER")
    print("=" * 60)
    
    # Find most recent JSONL file
    jsonl_files = [f for f in os.listdir('.') if f.startswith('batch_input_') and f.endswith('.jsonl')]
    
    if not jsonl_files:
        print("No batch_input_*.jsonl files found")
        print("Run BATCH_COLLECTOR.py first")
        return
    
    latest_jsonl = sorted(jsonl_files)[-1]
    print(f"Using: {latest_jsonl}")
    
    # Upload file
    file_id = upload_file(latest_jsonl)
    if not file_id:
        return
    
    # Create batch
    batch_id = create_batch_job(file_id)
    if not batch_id:
        return
    
    # Save batch info
    batch_info = {
        'batch_id': batch_id,
        'file_id': file_id,
        'jsonl_file': latest_jsonl,
        'submitted': datetime.now().isoformat()
    }
    
    with open(f"batch_info_{batch_id}.json", 'w') as f:
        json.dump(batch_info, f, indent=2)
    
    print("\n" + "=" * 60)
    print("BATCH SUBMITTED!")
    print(f"Batch ID: {batch_id}")
    print("\nTo check status:")
    print(f"  python BATCH_SUBMITTER.py --status {batch_id}")
    print("\nTo download results when complete:")
    print(f"  python BATCH_SUBMITTER.py --download {batch_id}")
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        if sys.argv[1] == '--status':
            check_batch_status(sys.argv[2])
        elif sys.argv[1] == '--download':
            batch = check_batch_status(sys.argv[2])
            if batch and batch.get('output_file_id'):
                download_results(batch['output_file_id'])
    else:
        main()