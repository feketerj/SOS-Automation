#!/usr/bin/env python3
"""Test UI with real endpoint data"""

import os
import sys
import time

def test_ui_with_real_endpoint():
    """Test the UI with a real endpoint that has known results"""

    print("Testing UI with real endpoint")
    print("=" * 60)

    # Create a test endpoints file
    test_endpoint = "AR1yyM0PV54_Ila0ZV6J6"  # Known endpoint with 8(a) set-aside knockouts

    print(f"1. Setting up test endpoint: {test_endpoint}")
    with open('endpoints.txt', 'w') as f:
        f.write(f"{test_endpoint}\n")
    print("   OK: endpoints.txt created")

    print("\n2. Running pipeline to generate real data...")
    # Import and run the pipeline directly
    sys.path.insert(0, 'ui_service')
    from run_pipeline_import import run_pipeline_direct

    try:
        code, output = run_pipeline_direct([test_endpoint])
        if code == 0:
            print("   OK: Pipeline completed successfully")
        else:
            print(f"   WARNING: Pipeline returned code {code}")

        # Show a snippet of the output
        if output:
            lines = output.split('\n')
            print("\n   Pipeline output summary:")
            # Look for key indicators
            for line in lines:
                if 'Total processed' in line or 'GO:' in line or 'NO-GO:' in line or 'INDETERMINATE:' in line:
                    print(f"     {line.strip()}")
                elif 'Saved to:' in line:
                    print(f"     {line.strip()}")

    except Exception as e:
        print(f"   ERROR: Pipeline failed - {e}")
        return False

    print("\n3. Checking output files...")
    # Find the latest output directory
    from pathlib import Path
    output_root = Path('SOS_Output')

    if not output_root.exists():
        print("   ERROR: No SOS_Output directory found")
        return False

    # Get latest run
    latest_dir = None
    latest_time = 0
    for month_dir in output_root.iterdir():
        if month_dir.is_dir():
            for run_dir in month_dir.iterdir():
                if run_dir.is_dir() and run_dir.name.startswith('Run_'):
                    try:
                        stat = run_dir.stat()
                        if stat.st_mtime > latest_time:
                            latest_time = stat.st_mtime
                            latest_dir = run_dir
                    except:
                        pass

    if not latest_dir:
        print("   ERROR: No run directories found")
        return False

    print(f"   Found latest run: {latest_dir}")

    # Check for assessment.csv
    csv_file = latest_dir / 'assessment.csv'
    if not csv_file.exists():
        print("   ERROR: assessment.csv not found")
        return False

    print("   OK: assessment.csv exists")

    # Read and verify CSV content
    import pandas as pd
    try:
        df = pd.read_csv(csv_file)
        print(f"   OK: CSV loaded with {len(df)} rows")

        # Check columns
        print("\n4. Verifying CSV structure...")
        required_cols = ['result', 'announcement_number', 'announcement_title', 'agency']
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            print(f"   WARNING: Missing columns: {missing_cols}")
        else:
            print("   OK: All required columns present")

        # Show sample data
        print("\n5. Sample data from CSV:")
        for idx, row in df.head(3).iterrows():
            result = row.get('result', 'UNKNOWN')
            title = row.get('announcement_title', 'Unknown')
            agency = row.get('agency', 'Unknown')
            print(f"   Row {idx+1}:")
            print(f"     Title: {title[:50]}...")
            print(f"     Agency: {agency}")
            print(f"     Result: {result}")

        # Check for expected knockouts (8(a) set-aside)
        print("\n6. Verifying expected results...")
        if len(df) > 0:
            # Should have NO-GOs for 8(a) set-aside
            no_go_count = len(df[df['result'] == 'NO-GO']) if 'result' in df.columns else 0
            if no_go_count > 0:
                print(f"   OK: Found {no_go_count} NO-GO results (expected for 8(a) set-aside)")
            else:
                print("   WARNING: No NO-GO results found (expected some for 8(a) set-aside)")

    except Exception as e:
        print(f"   ERROR: Failed to read CSV - {e}")
        return False

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("\nTo view in UI:")
    print("1. Run: streamlit run ui_service/app.py")
    print("2. The UI should display the results from this test")
    print(f"3. Latest data in: {latest_dir}")

    return True

if __name__ == "__main__":
    success = test_ui_with_real_endpoint()
    sys.exit(0 if success else 1)