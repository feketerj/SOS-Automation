#!/usr/bin/env python3
"""
Run batch processor test with test endpoints
"""

import os
import sys
import subprocess
from datetime import datetime

def main():
    print("=" * 80)
    print("BATCH PROCESSOR TEST")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Mode: BATCH ONLY (No agent verification)")
    print("=" * 80)
    
    # Set environment for batch only mode
    os.environ['SKIP_AGENT_VERIFICATION'] = '1'
    
    # Change to batch processor directory
    os.chdir('Mistral_Batch_Processor')
    
    print("\nStarting batch processor...")
    print("This will:")
    print("  1. Fetch opportunities from test_endpoints.txt")
    print("  2. Apply regex filtering (FREE)")
    print("  3. Batch process remainder with Mistral (50% off)")
    print("  4. Generate output files")
    print("\nExpected time: 5-10 minutes")
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
    
    # Track if we've answered the prompt
    answered = False
    
    # Read output and auto-answer prompt
    while True:
        line = process.stdout.readline()
        if not line:
            break
        print(line.rstrip())
        
        # Auto-answer monitoring prompt
        if "Monitor batch job progress?" in line and not answered:
            process.stdin.write("n\n")
            process.stdin.flush()
            print("[AUTO-ANSWERED: n]")
            answered = True
    
    process.wait()
    
    print("\n" + "=" * 80)
    print("BATCH TEST COMPLETE")
    print("Batch job submitted to Mistral API")
    print("Results will appear in ../SOS_Output/2025-09/ when complete")
    print("=" * 80)
    
    return process.returncode

if __name__ == "__main__":
    exit(main())