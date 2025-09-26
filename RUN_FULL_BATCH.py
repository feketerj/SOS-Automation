#!/usr/bin/env python3
"""
Run full batch processor on all endpoints with auto-answer
"""

import os
import sys
import subprocess
from datetime import datetime

def main():
    print("=" * 80)
    print("FULL BATCH PROCESSOR - ALL ENDPOINTS")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Mode: BATCH ONLY (No agent verification)")
    print("=" * 80)
    
    # Set environment for batch only mode
    os.environ['SKIP_AGENT_VERIFICATION'] = '1'
    
    # Copy endpoints.txt to batch processor directory
    import shutil
    if os.path.exists('endpoints.txt'):
        shutil.copy('endpoints.txt', 'Mistral_Batch_Processor/endpoints.txt')
        with open('endpoints.txt', 'r') as f:
            endpoints = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        print(f"\nProcessing {len(endpoints)} endpoints from endpoints.txt")
    else:
        print("ERROR: endpoints.txt not found!")
        return 1
    
    # Change to batch processor directory
    os.chdir('Mistral_Batch_Processor')
    
    print("\nStarting batch processor...")
    print("This will:")
    print(f"  1. Fetch opportunities from {len(endpoints)} search IDs")
    print("  2. Apply regex filtering (FREE)")
    print("  3. Batch process remainder with Mistral (50% off)")
    print("  4. Generate output files")
    print("\nEstimated time: 20-30 minutes for full run")
    print("-" * 80)
    
    # Run the batch processor with auto-answer 'n' to monitoring
    process = subprocess.Popen(
        [sys.executable, 'FULL_BATCH_PROCESSOR.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    # Track progress
    answered = False
    batch_job_id = None
    
    # Read output and auto-answer prompt
    while True:
        line = process.stdout.readline()
        if not line:
            break
        print(line.rstrip())
        
        # Extract batch job ID if created
        if "Batch job created:" in line:
            batch_job_id = line.split("Batch job created:")[1].strip()
        
        # Auto-answer monitoring prompt
        if "Monitor batch job progress?" in line and not answered:
            process.stdin.write("n\n")
            process.stdin.flush()
            print("[AUTO-ANSWERED: n]")
            answered = True
    
    process.wait()
    
    print("\n" + "=" * 80)
    print("BATCH PROCESSING COMPLETE")
    if batch_job_id:
        print(f"Batch Job ID: {batch_job_id}")
        print("\nTo check status:")
        print(f"  python CHECK_BATCH_STATUS.py {batch_job_id}")
        print("\nTo download results when ready:")
        print(f"  python DOWNLOAD_BATCH_RESULTS.py {batch_job_id}")
    print("\nResults will appear in ../SOS_Output/2025-09/ when complete")
    print("=" * 80)
    
    return process.returncode

if __name__ == "__main__":
    exit(main())