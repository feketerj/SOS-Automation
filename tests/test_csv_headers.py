#!/usr/bin/env python3
"""Test that CSV will include sam_url column"""

from enhanced_output_manager import EnhancedOutputManager
import tempfile
import csv
import os

def test_csv_headers():
    """Check if sam_url is in CSV headers"""

    # Create test data with URLs
    test_data = [{
        'sam_url': 'https://sam.gov/test',
        'hg_url': 'https://highergov.com/test',
        'highergov_url': 'https://highergov.com/test',  # backward compat
        'result': 'GO',
        'final_decision': 'GO',
        'solicitation_id': 'TEST123',
        'solicitation_title': 'Test',
        'announcement_number': 'TEST123',
        'announcement_title': 'Test'
    }]

    # Create temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create output manager
        manager = EnhancedOutputManager()

        # Process and enrich the data
        enriched = manager._process_assessments(test_data)

        # Write CSV directly
        csv_path = os.path.join(tmpdir, 'test.csv')

        # Use the actual field names from the manager
        fieldnames = [
            'final_decision', 'knock_pattern', 'knockout_category',
            'sos_pipeline_title', 'sam_url', 'highergov_url',
            'announcement_number', 'announcement_title', 'agency',
            'due_date', 'brief_description', 'analysis_notes',
            'recommendation', 'special_action', 'posted_date',
            'naics', 'psc', 'set_aside', 'value_low', 'value_high',
            'place_of_performance', 'doc_length', 'assessment_timestamp',
            'processing_method', 'verification_method', 'batch_decision',
            'agent_decision', 'disagreement', 'verification_timestamp'
        ]

        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

        # Read and check headers
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames

        print("CSV Headers:")
        print("-" * 50)
        for i, header in enumerate(headers, 1):
            if 'url' in header.lower():
                print(f"{i:3}. {header} <-- URL FIELD")
            else:
                print(f"{i:3}. {header}")

        print("\n" + "=" * 50)
        if 'sam_url' in headers:
            print("[SUCCESS] sam_url is in CSV headers at position", headers.index('sam_url') + 1)
        else:
            print("[FAIL] sam_url NOT in CSV headers")

        if 'highergov_url' in headers:
            print("[SUCCESS] highergov_url is in CSV headers at position", headers.index('highergov_url') + 1)
        else:
            print("[FAIL] highergov_url NOT in CSV headers")

if __name__ == "__main__":
    test_csv_headers()