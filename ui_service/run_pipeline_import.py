#!/usr/bin/env python3
"""Direct pipeline runner using Python imports instead of subprocess"""

import sys
import os
from pathlib import Path
from io import StringIO
import traceback
import importlib

def run_pipeline_direct(endpoints_list):
    """Run the pipeline directly via Python import - no subprocess"""

    # Validate input
    if not endpoints_list:
        return 1, "ERROR: No endpoints provided. At least one endpoint is required."

    # Get root directory
    root = Path(__file__).resolve().parents[1]

    # Write endpoints to file with explicit encoding
    endpoints_file = root / "endpoints.txt"
    with open(endpoints_file, "w", encoding="utf-8") as f:
        for endpoint in endpoints_list:
            endpoint_clean = str(endpoint).strip()
            if endpoint_clean:  # Skip empty strings
                f.write(f"{endpoint_clean}\n")

    print(f"Wrote {len(endpoints_list)} endpoints to {endpoints_file}")

    # Save original directory and stdout
    original_cwd = os.getcwd()
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    original_syspath = sys.path.copy()  # Save original sys.path

    # Capture output
    output_buffer = StringIO()

    # Track paths we add to sys.path
    added_paths = []

    try:
        # Change to Mistral_Batch_Processor directory since FULL_BATCH_PROCESSOR expects endpoints.txt at ../endpoints.txt
        batch_processor_dir = root / "Mistral_Batch_Processor"
        os.chdir(str(batch_processor_dir))

        # Add necessary paths to sys.path and track them
        if str(batch_processor_dir) not in sys.path:
            sys.path.insert(0, str(batch_processor_dir))
            added_paths.append(str(batch_processor_dir))
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
            added_paths.append(str(root))

        # Redirect stdout/stderr to capture output
        sys.stdout = output_buffer
        sys.stderr = output_buffer

        # Set environment variables to prevent interactive prompts
        os.environ['MONITOR_BATCH'] = 'n'
        os.environ['SKIP_AGENT_VERIFICATION'] = '1'

        print("Starting pipeline execution via direct import...")

        # Check if module was previously imported and reload if necessary
        if 'FULL_BATCH_PROCESSOR' in sys.modules:
            # Reload to ensure we get latest code
            importlib.reload(sys.modules['FULL_BATCH_PROCESSOR'])
            from FULL_BATCH_PROCESSOR import main as batch_main
        else:
            # First time import
            from FULL_BATCH_PROCESSOR import main as batch_main

        # Run the batch processor
        batch_main()

        print("\nPipeline completed successfully")
        return 0, output_buffer.getvalue()

    except Exception as e:
        # Safely get output buffer content BEFORE any restoration
        try:
            captured_output = output_buffer.getvalue()
        except:
            captured_output = ""

        error_msg = f"Pipeline failed with error: {str(e)}\n{traceback.format_exc()}"
        return 1, captured_output + "\n" + error_msg

    finally:
        # Close output buffer FIRST before restoring streams
        try:
            output_buffer.close()
        except:
            pass

        # THEN restore original stdout/stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr

        # Remove added paths from sys.path
        for path in added_paths:
            if path in sys.path:
                try:
                    sys.path.remove(path)
                except:
                    pass  # Path might already be removed

        # Restore working directory
        try:
            os.chdir(original_cwd)
        except:
            pass  # Directory might not exist anymore


if __name__ == "__main__":
    # Test with provided endpoints or default
    test_endpoints = sys.argv[1:] if len(sys.argv) > 1 else ["AR1yyM0PV54_Ila0ZV6J6"]

    print(f"Testing direct import pipeline with endpoints: {test_endpoints}")
    result_code, output = run_pipeline_direct(test_endpoints)

    print(f"\n{'='*60}")
    print("Pipeline Output:")
    print('='*60)
    print(output)
    print('='*60)
    print(f"\nPipeline completed with code: {result_code}")