#!/usr/bin/env python3
"""Test that sanitization preserves all critical data fields"""

from decision_sanitizer import DecisionSanitizer
import json

def test_data_integrity():
    """Test that sanitization preserves all critical fields without corruption"""

    print("Testing Data Integrity During Sanitization")
    print("=" * 60)

    # Complex test data with all possible fields
    complex_data = {
        # Decision fields (various formats)
        'decision': 'GO',
        'final_decision': 'GO',
        'recommendation': 'Proceed',

        # Nested assessment (legacy format)
        'assessment': {
            'decision': 'GO',
            'reasoning': 'Nested reasoning text'
        },

        # URL fields
        'source_path': 'https://sam.gov/opportunity/12345',
        'path': 'https://highergov.com/opportunity/67890',
        'sam_url': 'https://sam.gov/direct',  # Direct field
        'hg_url': 'https://highergov.com/direct',  # Direct field

        # Identification fields
        'solicitation_id': 'SOL-123',
        'source_id': 'SRC-456',
        'announcement_number': 'ANN-789',
        'opportunity_id': 'OPP-ABC',

        # Title fields
        'solicitation_title': 'Main Title',
        'title': 'Alternative Title',
        'announcement_title': 'Announcement Title',

        # Summary fields
        'summary': 'Primary summary text',
        'ai_summary': 'AI generated summary',
        'description_text': 'Description text',

        # Reasoning fields
        'rationale': 'Primary rationale',
        'reasoning': 'Alternative reasoning',
        'primary_blocker': 'Blocker text',

        # Metadata fields
        'agency': 'Department of Defense',
        'due_date': '2025-12-31',
        'posted_date': '2025-01-01',
        'naics': '541330',
        'psc': 'R425',
        'set_aside': 'Small Business',
        'value_low': 100000,
        'value_high': 500000,
        'place_of_performance': 'Washington, DC',
        'doc_length': 12345,

        # Processing fields
        'processing_method': 'BATCH_AI',
        'knock_pattern': 'Military platform',
        'knock_out_reasons': ['Reason 1', 'Reason 2'],
        'exceptions': ['Exception 1'],
        'special_action': 'Contact CO',
        'sos_pipeline_title': 'Pipeline Title',

        # Custom fields that should be preserved
        'custom_field_1': 'Custom Value 1',
        'custom_field_2': 12345,
        'custom_field_3': ['list', 'of', 'values']
    }

    # Sanitize the complex data
    print("\n1. Sanitizing Complex Data:")
    print("-" * 40)
    sanitized = DecisionSanitizer.sanitize(complex_data)

    # Check critical fields are preserved
    critical_checks = {
        'result': 'GO',  # Should be normalized from 'decision'
        'solicitation_id': 'SOL-123',  # Should be preserved
        'solicitation_title': 'Main Title',  # Should use primary field
        'sam_url': 'https://sam.gov/direct',  # Should use direct field first
        'hg_url': 'https://highergov.com/direct',  # Should use direct field first
        'rationale': 'Primary rationale',  # Should use primary field first
        'agency': 'Department of Defense',  # Metadata preserved
        'due_date': '2025-12-31',  # Metadata preserved
        'value_low': 100000,  # Numeric preserved
        'value_high': 500000,  # Numeric preserved
        '_sanitized': True  # Marker added
    }

    all_passed = True
    for field, expected in critical_checks.items():
        actual = sanitized.get(field)
        if actual != expected:
            print(f"  [FAIL] {field}: expected '{expected}', got '{actual}'")
            all_passed = False
        else:
            print(f"  [OK] {field}: {expected}")

    # Check that knock_out_reasons is preserved as list
    if sanitized['knock_out_reasons'] != ['Reason 1', 'Reason 2']:
        print(f"  [FAIL] knock_out_reasons not preserved as list")
        all_passed = False
    else:
        print(f"  [OK] knock_out_reasons: preserved as list")

    # Test priority fallback for URL fields
    print("\n2. Testing URL Field Priority:")
    print("-" * 40)

    url_test_cases = [
        {
            'name': 'Direct sam_url',
            'data': {'sam_url': 'https://sam.gov/direct'},
            'expected': 'https://sam.gov/direct'
        },
        {
            'name': 'Fallback to sam_gov_url',
            'data': {'sam_gov_url': 'https://sam.gov/alt'},
            'expected': 'https://sam.gov/alt'
        },
        {
            'name': 'Fallback to source_path',
            'data': {'source_path': 'https://sam.gov/source'},
            'expected': 'https://sam.gov/source'
        }
    ]

    for test_case in url_test_cases:
        sanitized = DecisionSanitizer.sanitize(test_case['data'])
        actual = sanitized.get('sam_url')
        if actual == test_case['expected']:
            print(f"  [OK] {test_case['name']}: {actual}")
        else:
            print(f"  [FAIL] {test_case['name']}: expected '{test_case['expected']}', got '{actual}'")
            all_passed = False

    # Test that second sanitization doesn't corrupt data
    print("\n3. Testing Data Preservation on Re-sanitization:")
    print("-" * 40)

    # First sanitization
    first_pass = DecisionSanitizer.sanitize(complex_data)
    first_values = {
        'result': first_pass['result'],
        'solicitation_id': first_pass['solicitation_id'],
        'sam_url': first_pass['sam_url'],
        'hg_url': first_pass['hg_url'],
        'agency': first_pass['agency']
    }

    # Second sanitization (should be skipped)
    second_pass = DecisionSanitizer.sanitize(first_pass)

    # Check values unchanged
    for field, expected in first_values.items():
        if second_pass[field] != expected:
            print(f"  [FAIL] {field} corrupted on re-sanitization")
            all_passed = False
        else:
            print(f"  [OK] {field} preserved on re-sanitization")

    # Test with minimal data
    print("\n4. Testing Minimal Data Handling:")
    print("-" * 40)

    minimal_data = {
        'decision': 'NO-GO'
    }

    minimal_sanitized = DecisionSanitizer.sanitize(minimal_data)

    # Should have default values but no errors
    if minimal_sanitized['result'] != 'NO-GO':
        print(f"  [FAIL] Minimal decision not preserved")
        all_passed = False
    else:
        print(f"  [OK] Minimal decision preserved")

    if minimal_sanitized['solicitation_id'] != '':
        print(f"  [FAIL] Should have empty solicitation_id")
        all_passed = False
    else:
        print(f"  [OK] Empty fields handled correctly")

    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] Data integrity maintained during sanitization!")
        print("\nKey achievements:")
        print("- All critical fields preserved correctly")
        print("- Priority fallback working for multi-source fields")
        print("- Re-sanitization doesn't corrupt data")
        print("- Minimal data handled without errors")
    else:
        print("[FAILURE] Some data integrity tests failed")

    return all_passed

if __name__ == "__main__":
    import sys
    success = test_data_integrity()
    sys.exit(0 if success else 1)