#!/usr/bin/env python3
"""Verify UI can properly display assessment data"""

import sys
import pandas as pd
from pathlib import Path

# Add ui_service to path
sys.path.insert(0, 'ui_service')
from field_mapper import FieldMapper

def verify_ui_display():
    """Test that the UI can properly read and display assessment data"""

    print("Verifying UI Display Functionality")
    print("=" * 60)

    # Find latest assessment.csv
    output_root = Path('SOS_Output')
    latest_csv = None
    latest_time = 0

    for month_dir in output_root.glob('*'):
        for run_dir in month_dir.glob('Run_*'):
            csv_file = run_dir / 'assessment.csv'
            if csv_file.exists():
                if csv_file.stat().st_mtime > latest_time:
                    latest_time = csv_file.stat().st_mtime
                    latest_csv = csv_file

    if not latest_csv:
        print("ERROR: No assessment.csv found")
        return False

    print(f"1. Found latest CSV: {latest_csv}")

    # Load the CSV
    try:
        df = pd.read_csv(latest_csv)
        print(f"   Loaded {len(df)} assessments")
    except Exception as e:
        print(f"   ERROR: Failed to load CSV - {e}")
        return False

    # Test field mapper
    print("\n2. Testing Field Mapper...")
    mapper = FieldMapper()

    success = True
    for idx, row in df.iterrows():
        print(f"\n   Assessment {idx + 1}:")

        # Test each field type
        title = mapper.get_field(row, 'title', 'Unknown')
        result = mapper.get_field(row, 'result', 'UNKNOWN')
        agency = mapper.get_field(row, 'agency', 'Unknown')
        sid = mapper.get_field(row, 'id', 'N/A')
        stage = mapper.get_field(row, 'stage', 'N/A')

        print(f"     Title: {title[:40]}...")
        icon = mapper.format_result_color(result)
        # Convert emoji to text for console output
        icon_text = {'🟢': '(GO)', '🔴': '(NO-GO)', '🟡': '(IND)', '⚪': '(?)'}
        icon_display = icon_text.get(icon, icon)
        print(f"     Result: {result} {icon_display}")
        print(f"     Agency: {agency}")
        print(f"     ID: {sid}")
        print(f"     Stage: {mapper.get_stage_description(stage)}")

        # Verify we got real values (not all defaults)
        if title == 'Unknown' and agency == 'Unknown' and sid == 'N/A':
            print("     WARNING: All fields returned defaults!")
            success = False

    # Test result counting
    print("\n3. Testing Result Counting...")
    go_count = 0
    no_go_count = 0
    indeterminate_count = 0

    for _, row in df.iterrows():
        result = mapper.get_field(row, 'result', 'UNKNOWN')
        if 'GO' in result.upper() and 'NO' not in result.upper():
            go_count += 1
        elif 'NO' in result.upper():
            no_go_count += 1
        elif 'INDETERMINATE' in result.upper():
            indeterminate_count += 1

    print(f"   GO: {go_count}")
    print(f"   NO-GO: {no_go_count}")
    print(f"   INDETERMINATE: {indeterminate_count}")
    print(f"   Total: {len(df)}")

    if go_count + no_go_count + indeterminate_count != len(df):
        print("   WARNING: Counts don't add up to total!")
        success = False

    # Verify column mapping
    print("\n4. Checking Column Availability...")
    expected_mappings = {
        'announcement_title': 'Title field',
        'result': 'Decision field',
        'agency': 'Agency field',
        'announcement_number': 'ID field'
    }

    for col, desc in expected_mappings.items():
        if col in df.columns:
            print(f"   OK: {desc} ({col}) present")
        else:
            print(f"   WARNING: {desc} ({col}) missing")

    print("\n" + "=" * 60)

    if success:
        print("SUCCESS: UI field mapping working correctly!")
        print("\nUI should now display:")
        print("- Real titles instead of 'Unknown Title'")
        print("- Actual agency names")
        print("- Correct GO/NO-GO/INDETERMINATE counts")
        print("- Color-coded results with icons")
    else:
        print("ISSUES FOUND: Check warnings above")

    return success

if __name__ == "__main__":
    success = verify_ui_display()
    sys.exit(0 if success else 1)