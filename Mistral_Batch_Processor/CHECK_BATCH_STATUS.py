#!/usr/bin/env python3
"""Check status of Mistral batch job"""

import sys
import os
from mistralai import Mistral

# Add parent directory to path
sys.path.append('..')
from API_KEYS import MISTRAL_API_KEY

def check_batch_status(job_id):
    """Check the status of a batch job"""
    client = Mistral(api_key=MISTRAL_API_KEY)
    
    try:
        job = client.batch.jobs.get(job_id=job_id)
        
        print("=" * 70)
        print(f"BATCH JOB STATUS: {job_id}")
        print("=" * 70)
        print(f"Status: {job.status}")
        print(f"Model: {job.model}")
        print(f"Total requests: {job.total_requests}")
        print(f"Succeeded: {job.succeeded_requests}")
        print(f"Failed: {job.failed_requests}")
        print(f"Created: {job.created_at}")
        
        if job.status == "SUCCESS":
            print(f"\nOutput file: {job.output_file}")
            print("Job complete! Use DOWNLOAD_BATCH_RESULTS.py to get results")
        elif job.status == "FAILED":
            if job.errors:
                print(f"\nErrors: {job.errors}")
        else:
            completion_rate = (job.succeeded_requests / job.total_requests * 100) if job.total_requests > 0 else 0
            print(f"\nProgress: {completion_rate:.1f}%")
            
    except Exception as e:
        print(f"Error checking job status: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        job_id = sys.argv[1]
        check_batch_status(job_id)
    else:
        # List all recent jobs
        client = Mistral(api_key=MISTRAL_API_KEY)
        print("=" * 70)
        print("RECENT BATCH JOBS")
        print("=" * 70)
        
        try:
            jobs = client.batch.jobs.list()
            for job in jobs.data[:10]:  # Show last 10
                print(f"{job.id}: {job.status} ({job.succeeded_requests}/{job.total_requests})")
        except Exception as e:
            print(f"Error listing jobs: {e}")