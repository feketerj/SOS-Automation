#!/usr/bin/env python3
"""Direct pipeline runner that actually works"""

import sys
import os
from pathlib import Path

def run_pipeline_for_real(endpoints_list):
    """Actually run the pipeline with given endpoints"""

    # Get root directory
    root = Path(__file__).resolve().parents[1]

    # Write endpoints to file
    endpoints_file = root / "endpoints.txt"
    with open(endpoints_file, "w") as f:
        for endpoint in endpoints_list:
            f.write(f"{endpoint}\n")

    print(f"Wrote {len(endpoints_list)} endpoints to {endpoints_file}")

    # Change to root directory
    os.chdir(str(root))

    # Run the batch processor directly - THIS WORKS
    cmd = f"{sys.executable} Mistral_Batch_Processor\\FULL_BATCH_PROCESSOR.py"
    print(f"Running: {cmd}")

    result = os.system(cmd)

    return result

if __name__ == "__main__":
    # Test with provided endpoints
    test_endpoints = sys.argv[1:] if len(sys.argv) > 1 else ["AR1yyM0PV54_Ila0ZV6J6"]
    result = run_pipeline_for_real(test_endpoints)
    print(f"\nPipeline completed with code: {result}")