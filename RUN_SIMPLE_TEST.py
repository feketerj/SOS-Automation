#!/usr/bin/env python3
"""
Simple test of assessment on a few endpoints
"""

import subprocess
import sys
from datetime import datetime

def main():
    print("=" * 80)
    print("RUNNING SIMPLE TEST ON FIRST 3 ENDPOINTS")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Just test first 3 endpoints
    test_ids = [
        'rFRK9PaP6ftzk1rokcKCT',
        'u912_Lb64wa9wH2GuKXTu', 
        'fWWjan2WfFQ3gojr1iAUJ'
    ]
    
    for i, search_id in enumerate(test_ids, 1):
        print(f"\n[{i}/3] Processing: {search_id}")
        print("-" * 40)
        
        result = subprocess.run(
            [sys.executable, "LOCKED_PRODUCTION_RUNNER.py", search_id],
            capture_output=False,  # Show output directly
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print(f"SUCCESS: {search_id}")
        else:
            print(f"FAILED: {search_id}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE - Check SOS_Output folder for results")
    print("=" * 80)

if __name__ == "__main__":
    main()