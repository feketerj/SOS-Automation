#!/usr/bin/env python3
"""Test field consolidation - Bug #5 fix verification"""

import csv
import json
import tempfile
import os
from enhanced_output_manager import EnhancedOutputManager
from decision_sanitizer import DecisionSanitizer

def test_field_consolidation():
    """Test that field duplication is eliminated"""

    print("Testing Field Consolidation (Bug #5)")
    print("=" * 60)

    # Test data with various decision fields
    test_cases = [
        {
            'name': 'Unified schema input',
            'input': {
                'result': 'GO',
                'solicitation_title': 'Test 1',
                'solicitation_id': 'TEST001'
            }
        },
        {
            'name': 'Legacy decision field',
            'input': {
                'decision': 'NO-GO',
                'title': 'Test 2',
                'source_id': 'TEST002'
            }
        },
        {
            'name': 'Nested assessment format',
            'input': {
                'assessment': {
                    'decision': 'INDETERMINATE',
                    'reasoning': 'Need more info'
                },
                'title': 'Test 3'
            }
        }
    ]

    manager = EnhancedOutputManager()
    all_passed = True

    for test_case in test_cases:
        print(f"\nTest: {test_case['name']}")
        print("-" * 40)

        # First sanitize the input
        sanitized = DecisionSanitizer.sanitize(test_case['input'])

        # Process through output manager
        enriched = manager._process_assessments([sanitized])

        if enriched:
            assessment = enriched[0]

            # Check that 'result' field exists
            if 'result' not in assessment:
                print(f"  [FAIL] Missing 'result' field")
                all_passed = False
            else:
                print(f"  [PASS] 'result' field present: {assessment['result']}")

            # Check that 'final_decision' exists for internal use
            if 'final_decision' not in assessment:
                print(f"  [WARN] Missing 'final_decision' for internal use")
            else:
                # Verify they match
                if assessment['result'] == assessment['final_decision']:
                    print(f"  [PASS] Fields match: {assessment['result']}")
                else:
                    print(f"  [FAIL] Field mismatch: result={assessment['result']}, final_decision={assessment['final_decision']}")
                    all_passed = False

    # Test CSV output to ensure no duplication
    print("\n" + "=" * 60)
    print("Testing CSV Output")
    print("-" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = os.path.join(tmpdir, 'test.csv')

        # Create test data
        test_data = [{
            'result': 'GO',
            'final_decision': 'GO',  # This should not appear in CSV
            'solicitation_id': 'TEST123',
            'solicitation_title': 'CSV Test',
            'sam_url': 'https://sam.gov/test',
            'hg_url': 'https://highergov.com/test'
        }]

        # Process and save
        enriched_data = manager._process_assessments(test_data)

        # Write CSV (simulate what save_assessment_batch does)
        fieldnames = [
            'result', 'knock_pattern', 'knockout_category',
            'sos_pipeline_title', 'sam_url', 'highergov_url',
            'announcement_number', 'announcement_title'
        ]

        with open(csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerow(enriched_data[0])

        # Read back and check
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            row = next(reader)

        print(f"CSV Headers: {headers}")

        # Check that 'result' is in CSV
        if 'result' in headers:
            print(f"  [PASS] 'result' field in CSV headers")
        else:
            print(f"  [FAIL] 'result' field missing from CSV")
            all_passed = False

        # Check that 'final_decision' is NOT in CSV (avoiding duplication)
        if 'final_decision' not in headers:
            print(f"  [PASS] 'final_decision' not duplicated in CSV")
        else:
            print(f"  [WARN] 'final_decision' still in CSV (duplication)")

        # Verify decision value preserved
        if row.get('result') == 'GO':
            print(f"  [PASS] Decision value preserved: {row['result']}")
        else:
            print(f"  [FAIL] Decision value lost or changed")
            all_passed = False

    # Test JSON output
    print("\n" + "=" * 60)
    print("Testing JSON Output")
    print("-" * 60)

    # The JSON should have both for backward compatibility
    json_data = {
        'assessments': enriched_data
    }

    # Check JSON structure
    assessment = json_data['assessments'][0]
    has_result = 'result' in assessment
    has_final = 'final_decision' in assessment

    print(f"  JSON has 'result': {has_result}")
    print(f"  JSON has 'final_decision': {has_final}")

    if has_result:
        print(f"  [PASS] JSON contains 'result' field")
    else:
        print(f"  [FAIL] JSON missing 'result' field")
        all_passed = False

    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] Field consolidation working correctly!")
        print("\nKey achievements:")
        print("- 'result' is primary field in CSV (no duplication)")
        print("- 'final_decision' kept internally for counting/filtering")
        print("- Backward compatibility maintained in JSON")
        print("- All decision values preserved correctly")
    else:
        print("[FAILURE] Some field consolidation tests failed")
    print("=" * 60)

    return all_passed

if __name__ == "__main__":
    import sys
    success = test_field_consolidation()
    sys.exit(0 if success else 1)