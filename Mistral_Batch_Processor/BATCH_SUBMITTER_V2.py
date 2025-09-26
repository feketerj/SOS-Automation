#!/usr/bin/env python3
"""
BATCH_SUBMITTER_V2.py - Enhanced Mistral batch submission using SDK
Follows the official Mistral batch API documentation
"""

import json
import os
import sys
import time
from datetime import datetime
from mistralai import Mistral

# API configuration
API_KEY = "1BPmHydlQmz81Z1edAs1ssQX3DbmW0Yf"
MODEL = "ft:mistral-medium-latest:d42144c7:20250902:908db254"  # Using accessible fine-tuned model

def create_client():
    """Create Mistral client"""
    return Mistral(api_key=API_KEY)

def upload_batch_file(client, filepath):
    """Upload JSONL file to Mistral"""
    print(f"Uploading {filepath}...")
    
    try:
        with open(filepath, 'rb') as f:
            batch_data = client.files.upload(
                file={
                    "file_name": os.path.basename(filepath),
                    "content": f.read()
                },
                purpose="batch"
            )
        
        print(f"File uploaded successfully: {batch_data.id}")
        print(f"  Filename: {batch_data.filename}")
        # Size attribute may not exist in batch file upload
        return batch_data.id
    
    except Exception as e:
        print(f"Upload failed: {e}")
        return None

def create_batch_job(client, file_id):
    """Create batch job with uploaded file"""
    print(f"\nCreating batch job...")
    
    try:
        batch_job = client.batch.jobs.create(
            input_files=[file_id],
            model=MODEL,
            endpoint="/v1/chat/completions",
            metadata={
                "job_type": "sos_assessment",
                "created": datetime.now().isoformat()
            }
        )
        
        print(f"Batch job created successfully!")
        print(f"  Job ID: {batch_job.id}")
        print(f"  Status: {batch_job.status}")
        print(f"  Created: {batch_job.created_at}")
        return batch_job
    
    except Exception as e:
        print(f"Batch creation failed: {e}")
        return None

def check_batch_status(client, batch_id):
    """Check status of batch job"""
    try:
        batch_job = client.batch.jobs.get(job_id=batch_id)
        
        print(f"\nBatch Job Status: {batch_id}")
        print(f"  Status: {batch_job.status}")
        print(f"  Total requests: {batch_job.total_requests}")
        print(f"  Succeeded: {batch_job.succeeded_requests}")
        print(f"  Failed: {batch_job.failed_requests}")
        
        if batch_job.total_requests > 0:
            percent_done = ((batch_job.succeeded_requests + batch_job.failed_requests) / 
                          batch_job.total_requests) * 100
            print(f"  Progress: {percent_done:.1f}%")
        
        if batch_job.status == "SUCCESS":
            print(f"  Output file: {batch_job.output_file}")
            if batch_job.error_file:
                print(f"  Error file: {batch_job.error_file}")
        
        return batch_job
    
    except Exception as e:
        print(f"Status check failed: {e}")
        return None

def monitor_batch_progress(client, batch_id, check_interval=10):
    """Monitor batch job until completion"""
    print(f"\nMonitoring batch job {batch_id}...")
    print("Press Ctrl+C to stop monitoring (job will continue running)")
    
    try:
        while True:
            batch_job = check_batch_status(client, batch_id)
            
            if not batch_job:
                break
            
            if batch_job.status in ["SUCCESS", "FAILED", "CANCELLED", "TIMEOUT_EXCEEDED"]:
                print(f"\nJob completed with status: {batch_job.status}")
                return batch_job
            
            time.sleep(check_interval)
    
    except KeyboardInterrupt:
        print("\nStopped monitoring. Job continues running in background.")
        print(f"Check status later with: python BATCH_SUBMITTER_V2.py --status {batch_id}")
        return None

def download_batch_results(client, batch_id, output_dir="."):
    """Download results from completed batch"""
    batch_job = client.batch.jobs.get(job_id=batch_id)
    
    if batch_job.status != "SUCCESS":
        print(f"Job not complete. Status: {batch_job.status}")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Download output file
    if batch_job.output_file:
        print(f"Downloading results...")
        output_stream = client.files.download(file_id=batch_job.output_file)
        
        output_filename = f"batch_results_{timestamp}.jsonl"
        output_path = os.path.join(output_dir, output_filename)
        
        with open(output_path, 'wb') as f:
            for chunk in output_stream.stream:
                f.write(chunk)
        
        print(f"Results saved to: {output_path}")
        
        # Download error file if exists
        if batch_job.error_file:
            print(f"Downloading error file...")
            error_stream = client.files.download(file_id=batch_job.error_file)
            
            error_filename = f"batch_errors_{timestamp}.jsonl"
            error_path = os.path.join(output_dir, error_filename)
            
            with open(error_path, 'wb') as f:
                for chunk in error_stream.stream:
                    f.write(chunk)
            
            print(f"Errors saved to: {error_path}")
        
        return output_path
    
    return None

def submit_and_monitor(jsonl_file):
    """Complete submission and monitoring workflow"""
    client = create_client()
    
    # Upload file
    file_id = upload_batch_file(client, jsonl_file)
    if not file_id:
        return None
    
    # Create batch job
    batch_job = create_batch_job(client, file_id)
    if not batch_job:
        return None
    
    # Save batch info for reference
    batch_info = {
        'batch_id': batch_job.id,
        'file_id': file_id,
        'model': MODEL,
        'jsonl_file': jsonl_file,
        'submitted': datetime.now().isoformat(),
        'status': batch_job.status
    }
    
    info_file = f"batch_info_{batch_job.id[:8]}.json"
    with open(info_file, 'w') as f:
        json.dump(batch_info, f, indent=2)
    
    print(f"\nBatch info saved to: {info_file}")
    
    # Option to monitor
    response = input("\nMonitor progress? (y/n): ").strip().lower()
    if response == 'y':
        final_job = monitor_batch_progress(client, batch_job.id)
        if final_job and final_job.status == "SUCCESS":
            download_batch_results(client, batch_job.id)
    else:
        print(f"\nBatch job running in background.")
        print(f"Check status: python BATCH_SUBMITTER_V2.py --status {batch_job.id}")
        print(f"Download results: python BATCH_SUBMITTER_V2.py --download {batch_job.id}")
    
    return batch_job.id

def main():
    """Main entry point"""
    print("=" * 60)
    print("MISTRAL BATCH SUBMITTER V2 - Using SDK")
    print("=" * 60)
    
    if len(sys.argv) > 2:
        client = create_client()
        
        if sys.argv[1] == '--status':
            check_batch_status(client, sys.argv[2])
        
        elif sys.argv[1] == '--download':
            download_batch_results(client, sys.argv[2])
        
        elif sys.argv[1] == '--monitor':
            monitor_batch_progress(client, sys.argv[2])
    
    elif len(sys.argv) > 1 and sys.argv[1].endswith('.jsonl'):
        # Submit specific file
        submit_and_monitor(sys.argv[1])
    
    else:
        # Find most recent batch_input file
        jsonl_files = [f for f in os.listdir('.') 
                      if f.startswith('batch_input_') and f.endswith('.jsonl')]
        
        if not jsonl_files:
            print("No batch_input_*.jsonl files found")
            print("Run BATCH_COLLECTOR.py first to create input file")
            return
        
        latest_jsonl = sorted(jsonl_files)[-1]
        print(f"Found input file: {latest_jsonl}")
        
        # Count requests in file
        with open(latest_jsonl, 'r') as f:
            request_count = sum(1 for line in f if line.strip())
        print(f"Requests in file: {request_count}")
        
        submit_and_monitor(latest_jsonl)

if __name__ == "__main__":
    main()