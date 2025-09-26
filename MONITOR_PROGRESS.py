#!/usr/bin/env python3
"""
Monitor batch processing progress
"""

import os
import glob
import json
from datetime import datetime
import time

def check_progress():
    """Check current processing progress"""
    
    # Check for batch metadata files
    os.chdir('Mistral_Batch_Processor')
    metadata_files = sorted(glob.glob('batch_metadata_*.json'))
    
    if not metadata_files:
        print("⏳ Waiting for batch to start...")
        return
    
    # Get latest metadata
    latest_metadata = metadata_files[-1]
    timestamp = latest_metadata.split('_')[-1].replace('.json', '')
    
    with open(latest_metadata, 'r') as f:
        metadata = json.load(f)
    
    total_endpoints = metadata.get('total_endpoints', 0)
    total_opportunities = metadata.get('total_opportunities', 0)
    regex_knockouts = metadata.get('regex_knockouts', 0)
    ai_needed = metadata.get('ai_assessments_needed', 0)
    
    # Check for batch input file
    batch_input = f'batch_input_{timestamp}.jsonl'
    if os.path.exists(batch_input):
        with open(batch_input, 'r') as f:
            batch_size = sum(1 for line in f)
    else:
        batch_size = 0
    
    # Display progress
    print("=" * 60)
    print("BATCH PROCESSING PROGRESS")
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    if total_endpoints > 0:
        print(f"📊 Endpoints: {total_endpoints}")
        print(f"📄 Total Opportunities: {total_opportunities}")
        print(f"❌ Regex Knockouts: {regex_knockouts} ({regex_knockouts*100//max(1,total_opportunities)}%)")
        print(f"🤖 Sent to AI: {ai_needed}")
        
        if batch_size > 0:
            print(f"\n✅ BATCH CREATED: {batch_size} requests")
            print("   Status: Submitted to Mistral API")
            print("   Check job status with CHECK_BATCH_STATUS.py")
        else:
            print(f"\n⏳ Creating batch file...")
            estimated_complete = ai_needed * 2  # ~2 seconds per opportunity
            print(f"   Estimated time: {estimated_complete//60} minutes")
    
    print("=" * 60)

def main():
    """Monitor progress continuously"""
    print("Monitoring batch processing progress...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            check_progress()
            time.sleep(10)  # Check every 10 seconds
            print("\n")
    except KeyboardInterrupt:
        print("\nMonitoring stopped")

if __name__ == "__main__":
    main()