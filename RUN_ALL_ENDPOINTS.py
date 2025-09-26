#!/usr/bin/env python3
"""
Run batch processor on all endpoints without prompts
"""

import os
import sys
import subprocess
from datetime import datetime

def main():
    print("=" * 80)
    print("RUNNING BATCH PROCESSOR ON ALL ENDPOINTS")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Set environment to skip agent verification (batch only mode)
    os.environ['SKIP_AGENT_VERIFICATION'] = '1'
    
    # Change to batch processor directory
    os.chdir('Mistral_Batch_Processor')
    
    # Check if endpoints.txt exists
    if not os.path.exists('../endpoints.txt'):
        print("ERROR: endpoints.txt not found")
        return 1
    
    # Count endpoints
    with open('../endpoints.txt', 'r') as f:
        endpoints = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"Found {len(endpoints)} search IDs in endpoints.txt")
    print("-" * 80)
    
    # Import and run the batch processor directly
    sys.path.insert(0, '.')
    
    # Monkey-patch input to auto-answer 'n' to monitoring prompt
    original_input = __builtins__.input
    def mock_input(prompt):
        if "Monitor" in prompt:
            print(prompt + "n")  # Show what we're answering
            return "n"
        return original_input(prompt)
    
    __builtins__.input = mock_input
    
    try:
        # Import and run
        import FULL_BATCH_PROCESSOR
        
    except Exception as e:
        print(f"ERROR: {e}")
        return 1
    finally:
        # Restore original input
        __builtins__.input = original_input
    
    print("\n" + "=" * 80)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 80)
    
    return 0

if __name__ == "__main__":
    exit(main())