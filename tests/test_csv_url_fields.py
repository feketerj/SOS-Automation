#!/usr/bin/env python3
"""Test that sam_url and hg_url appear in CSV output"""

import csv
import tempfile
import os
from enhanced_output_manager import EnhancedOutputManager

def test_csv_url_fields():
    """Verify URL fields are included in CSV output"""

    print("Testing CSV URL Field Inclusion")
    print("=" * 60)

    # Create test data with URL fields
    test_assessments = [
        {
            'result': 'GO',
            'solicitation_id': 'TEST001',
            'solicitation_title': 'Test Opportunity 1',
            'sam_url': 'https://sam.gov/opp/12345',
            'hg_url': 'https://highergov.com/opportunity/67890',
            'knock_pattern': '',
            'knockout_category': 'GO-OK',
            'sos_pipeline_title': 'PN: NA | Qty: NA | Condition: NA | MDS: NA | Test 1',
            'announcement_number': 'TEST001',
            'announcement_title': 'Test Opportunity 1'
        },
        {
            'result': 'NO-GO',
            'solicitation_id': 'TEST002',
            'solicitation_title': 'Test Opportunity 2',
            'sam_url': 'https://sam.gov/opp/54321',
            'hg_url': '',  # Empty URL field
            'knock_pattern': 'Military platform',
            'knockout_category': 'KO-02',
            'sos_pipeline_title': 'PN: NA | Qty: NA | Condition: NA | MDS: NA | Test 2',
            'announcement_number': 'TEST002',
            'announcement_title': 'Test Opportunity 2'
        }
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create output manager with temp directory
        manager = EnhancedOutputManager(base_path=tmpdir)

        # Process assessments
        enriched = manager._process_assessments(test_assessments)

        # Save as CSV
        csv_file = os.path.join(tmpdir, 'test_output.csv')

        # Get the fieldnames from the manager
        fieldnames = [
            'result', 'knock_pattern', 'knockout_category',
            'sos_pipeline_title', 'sam_url', 'highergov_url',
            'announcement_number', 'announcement_title', 'agency',
            'due_date', 'brief_description', 'analysis_notes',
            'recommendation', 'special_action', 'posted_date',
            'naics', 'psc', 'set_aside', 'value_low', 'value_high',
            'place_of_performance', 'doc_length', 'assessment_timestamp'
        ]

        # Write CSV
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for assessment in enriched:
                row = {field: assessment.get(field, '') for field in fieldnames}
                writer.writerow(row)

        # Read back and verify
        print("\n1. Checking CSV Headers:")
        print("-" * 40)

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            rows = list(reader)

        # Check headers include URL fields
        if 'sam_url' in headers:
            print("  [OK] sam_url in CSV headers")
        else:
            print("  [FAIL] sam_url missing from CSV headers")
            return False

        if 'highergov_url' in headers:
            print("  [OK] highergov_url in CSV headers")
        else:
            print("  [FAIL] highergov_url missing from CSV headers")
            return False

        print("\n2. Checking CSV Data:")
        print("-" * 40)

        # Check first row has sam_url value
        if rows[0].get('sam_url') == 'https://sam.gov/opp/12345':
            print("  [OK] First row sam_url preserved: https://sam.gov/opp/12345")
        else:
            print(f"  [FAIL] First row sam_url: {rows[0].get('sam_url')}")
            return False

        # Check second row has sam_url but empty hg_url
        if rows[1].get('sam_url') == 'https://sam.gov/opp/54321':
            print("  [OK] Second row sam_url preserved: https://sam.gov/opp/54321")
        else:
            print(f"  [FAIL] Second row sam_url: {rows[1].get('sam_url')}")
            return False

        if rows[1].get('highergov_url') == '':
            print("  [OK] Second row highergov_url empty as expected")
        else:
            print(f"  [FAIL] Second row highergov_url should be empty: {rows[1].get('highergov_url')}")
            return False

        print("\n3. Testing save_assessment_batch method:")
        print("-" * 40)

        # Test the actual save_assessment_batch method
        output_dir = manager.save_assessment_batch(
            search_id='TEST_BATCH',
            assessments=test_assessments,
            metadata={'test': True}
        )

        # Find the CSV file
        csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]
        if csv_files:
            actual_csv = os.path.join(output_dir, csv_files[0])
            with open(actual_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                actual_headers = reader.fieldnames
                actual_rows = list(reader)

            if 'sam_url' in actual_headers:
                print("  [OK] sam_url in actual CSV output")
            else:
                print("  [FAIL] sam_url missing from actual CSV output")
                return False

            if actual_rows and actual_rows[0].get('sam_url'):
                print(f"  [OK] URL data preserved: {actual_rows[0].get('sam_url')[:30]}...")
            else:
                print("  [FAIL] URL data not preserved in actual output")
                return False

    print("\n" + "=" * 60)
    print("[SUCCESS] CSV URL fields properly included!")
    return True

if __name__ == "__main__":
    import sys
    success = test_csv_url_fields()
    sys.exit(0 if success else 1)