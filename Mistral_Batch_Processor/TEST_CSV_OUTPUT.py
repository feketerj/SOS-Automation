#!/usr/bin/env python3
"""
TEST_CSV_OUTPUT.py - Test that batch processor creates proper assessment.csv
"""

import sys
import os
from datetime import datetime

# Add parent directory
sys.path.append('..')
from enhanced_output_manager import EnhancedOutputManager

def test_csv_creation():
    """Test creating a CSV with the output manager"""
    
    # Create test data
    test_results = [
        {
            'search_id': 'TEST123',
            'opportunity_id': 'OPP001',
            'title': 'Test Opportunity 1',
            'final_decision': 'NO-GO',
            'knock_pattern': 'Set-aside: 8(a)',
            'knockout_category': 'KO-04',
            'sos_pipeline_title': 'PN: 123 | Qty: 10 | Condition: NEW | MDS: F-16 | Description: Test part',
            'highergov_url': 'https://www.highergov.com/opportunity/OPP001',
            'announcement_number': 'FA1234',
            'announcement_title': 'Test Opportunity 1',
            'agency': 'Air Force',
            'due_date': '2025-09-15',
            'brief_description': 'Test description',
            'analysis_notes': 'Knocked out by set-aside',
            'recommendation': 'NO-GO',
            'special_action': '',
            'posted_date': '2025-09-10',
            'naics': '336411',
            'psc': '1560',
            'set_aside': '8(a)',
            'value_low': '100000',
            'value_high': '500000',
            'place_of_performance': 'Wright-Patterson AFB',
            'doc_length': '5000',
            'assessment_timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        },
        {
            'search_id': 'TEST123',
            'opportunity_id': 'OPP002', 
            'title': 'Test Opportunity 2',
            'final_decision': 'GO',
            'knock_pattern': '',
            'knockout_category': 'GO-OK',
            'sos_pipeline_title': 'PN: 456 | Qty: 5 | Condition: OH | MDS: C-130 | Description: Surplus part',
            'highergov_url': 'https://www.highergov.com/opportunity/OPP002',
            'announcement_number': 'SPE123',
            'announcement_title': 'Test Opportunity 2',
            'agency': 'DLA',
            'due_date': '2025-09-20',
            'brief_description': 'Good opportunity',
            'analysis_notes': 'Surplus parts, unrestricted',
            'recommendation': 'GO',
            'special_action': 'Contact CO immediately',
            'posted_date': '2025-09-10',
            'naics': '336411',
            'psc': '1560',
            'set_aside': '',
            'value_low': '50000',
            'value_high': '150000',
            'place_of_performance': 'Richmond, VA',
            'doc_length': '3000',
            'assessment_timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        }
    ]
    
    # Create output manager
    output_manager = EnhancedOutputManager()
    
    # Save using the manager
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    search_id = f"TEST_{timestamp}"
    
    metadata = {
        'test_run': True,
        'total_opportunities': 2,
        'processing_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    output_dir = output_manager.save_assessment_batch(
        search_id, 
        test_results, 
        metadata, 
        pre_formatted=True
    )
    
    print(f"Test output created in: {output_dir}")
    
    # Verify the CSV
    csv_path = output_dir / "assessment.csv"
    if csv_path.exists():
        print(f"\n✓ assessment.csv created successfully!")
        
        # Read first few lines
        with open(csv_path, 'r') as f:
            lines = f.readlines()[:3]
            print("\nCSV Preview:")
            for line in lines:
                print(f"  {line.strip()[:100]}...")
        
        # Check fields
        header = lines[0].strip()
        expected_fields = ['final_decision', 'knock_pattern', 'knockout_category', 'sos_pipeline_title']
        
        print("\nField Check:")
        for field in expected_fields:
            if field in header:
                print(f"  ✓ {field} found")
            else:
                print(f"  ✗ {field} MISSING!")
    else:
        print(f"\n✗ ERROR: assessment.csv not created!")
    
    # List all files created
    print(f"\nAll files in output directory:")
    for file in output_dir.iterdir():
        size = file.stat().st_size
        print(f"  - {file.name} ({size:,} bytes)")

if __name__ == "__main__":
    test_csv_creation()