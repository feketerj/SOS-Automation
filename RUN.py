#!/usr/bin/env python3
"""
SIMPLE WRAPPER FOR SOS ASSESSMENT TOOL
Usage:
    python RUN.py [SEARCH_ID]  # Run single assessment
    python RUN.py              # Run batch from endpoints.txt
"""

import sys
import subprocess
import os

def main():
    print("="*60)
    print("SOS ASSESSMENT TOOL - SIMPLE RUNNER")
    print("="*60)
    
    if len(sys.argv) > 1:
        # Single assessment mode
        search_id = sys.argv[1]
        print(f"\nRunning single assessment for: {search_id}")
        print("-"*60)
        
        # Run LOCKED_PRODUCTION_RUNNER.py with the search ID
        result = subprocess.run(
            ["python", "LOCKED_PRODUCTION_RUNNER.py", search_id],
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print("\n" + "="*60)
            print("SUCCESS! Check SOS_Output/ for results")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("ERROR: Assessment failed. Check the error messages above.")
            print("="*60)
            
    else:
        # Batch mode
        if not os.path.exists("endpoints.txt"):
            print("\nERROR: endpoints.txt not found!")
            print("Create endpoints.txt with search IDs (one per line)")
            return
            
        # Count endpoints
        with open("endpoints.txt", "r") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            count = len(lines)
        
        print(f"\nRunning batch assessment for {count} endpoints from endpoints.txt")
        print("-"*60)
        
        # Run BATCH_RUN.py
        result = subprocess.run(
            ["python", "BATCH_RUN.py"],
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print("\n" + "="*60)
            print("SUCCESS! Check SOS_Output/ for results")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("ERROR: Batch processing failed. Check the error messages above.")
            print("="*60)

if __name__ == "__main__":
    main()