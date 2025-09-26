#!/usr/bin/env python3
"""
TEST_OUTPUT_LOCATION.py - Verify output goes to the right place
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Add parent directory
sys.path.append('..')
from enhanced_output_manager import EnhancedOutputManager

def test_output_location():
    """Test that output goes to ../SOS_Output not ./SOS_Output"""
    
    # Create a single test result
    test_result = [{
        'search_id': 'LOCATION_TEST',
        'opportunity_id': 'TEST001',
        'title': 'Location Test',
        'final_decision': 'GO',
        'knock_pattern': '',
        'knockout_category': 'GO-OK',
        'sos_pipeline_title': 'PN: TEST | Qty: 1 | Condition: NEW | MDS: TEST | Description: Testing location',
        'highergov_url': 'https://test.com',
        'announcement_number': 'TEST001',
        'announcement_title': 'Location Test',
        'agency': 'TEST',
        'due_date': '2025-09-15',
        'brief_description': 'Testing output location',
        'analysis_notes': 'This should go to ../SOS_Output',
        'recommendation': 'GO',
        'assessment_timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    }]
    
    # Create output manager with explicit path to parent SOS_Output
    output_manager = EnhancedOutputManager(base_path="../SOS_Output")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    search_id = f"LOCATION_{timestamp}"
    
    output_dir = output_manager.save_assessment_batch(
        search_id, 
        test_result, 
        {'test': True}, 
        pre_formatted=True
    )
    
    print(f"Output created at: {output_dir}")
    
    # Check if it's in the right place
    expected_parent = Path("../SOS_Output").resolve()
    actual_parent = Path(output_dir).parent.parent.resolve()
    
    if actual_parent == expected_parent:
        print(f"SUCCESS: Output is in the correct location!")
        print(f"  Expected: {expected_parent}")
        print(f"  Actual:   {actual_parent}")
    else:
        print(f"FAIL: Output is in the WRONG location!")
        print(f"  Expected: {expected_parent}")
        print(f"  Actual:   {actual_parent}")
    
    # Check the CSV exists and has correct format
    csv_path = output_dir / "assessment.csv"
    if csv_path.exists():
        with open(csv_path, 'r') as f:
            header = f.readline().strip()
            if 'final_decision' in header and 'knock_pattern' in header:
                print(f"SUCCESS: assessment.csv has correct format")
            else:
                print(f"FAIL: assessment.csv has wrong format")
                print(f"  Header: {header[:100]}...")

if __name__ == "__main__":
    test_output_location()