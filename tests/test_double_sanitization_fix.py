#!/usr/bin/env python3
"""Test that double sanitization is prevented"""

from decision_sanitizer import DecisionSanitizer
import json

def test_double_sanitization_prevention():
    """Test that already-sanitized data is not re-processed"""

    print("Testing Double Sanitization Prevention")
    print("=" * 60)

    # Test data
    original_data = {
        'decision': 'GO',
        'title': 'Test Opportunity',
        'source_id': 'TEST001',
        'reasoning': 'This is a test',
        'source_path': 'https://sam.gov/test',
        'path': 'https://highergov.com/test'
    }

    # First sanitization
    print("\n1. First Sanitization:")
    print("-" * 40)
    first_sanitized = DecisionSanitizer.sanitize(original_data)

    # Check it was sanitized correctly
    assert first_sanitized['result'] == 'GO', "Decision not normalized"
    assert first_sanitized['_sanitized'] == True, "Not marked as sanitized"
    assert first_sanitized['pipeline_stage'] != '', "Pipeline stage not set"
    assert first_sanitized['assessment_type'] != '', "Assessment type not set"
    assert first_sanitized.get('sam_url') == 'https://sam.gov/test', "SAM URL not preserved"
    assert first_sanitized.get('hg_url') == 'https://highergov.com/test', "HG URL not preserved"

    print(f"  [OK] Correctly sanitized:")
    print(f"       result: {first_sanitized['result']}")
    print(f"       _sanitized: {first_sanitized['_sanitized']}")
    print(f"       pipeline_stage: {first_sanitized['pipeline_stage']}")
    print(f"       assessment_type: {first_sanitized['assessment_type']}")

    # Store original values for comparison
    original_values = {
        'result': first_sanitized['result'],
        'rationale': first_sanitized['rationale'],
        'sam_url': first_sanitized['sam_url'],
        'hg_url': first_sanitized['hg_url'],
        'pipeline_stage': first_sanitized['pipeline_stage'],
        'assessment_type': first_sanitized['assessment_type']
    }

    # Second sanitization (should be skipped)
    print("\n2. Second Sanitization Attempt:")
    print("-" * 40)

    # Check if already sanitized
    is_sanitized = DecisionSanitizer.is_already_sanitized(first_sanitized)
    print(f"  is_already_sanitized(): {is_sanitized}")
    assert is_sanitized == True, "Should detect as already sanitized"

    second_sanitized = DecisionSanitizer.sanitize(first_sanitized)

    # Should be identical (same object or same values)
    if second_sanitized is first_sanitized:
        print("  [OK] Returned same object (reference equality)")
    else:
        print("  [OK] Returned new object, checking values...")
        for key, expected_value in original_values.items():
            assert second_sanitized[key] == expected_value, f"{key} was modified!"
            print(f"       {key}: preserved correctly")

    # Test batch sanitization
    print("\n3. Batch Sanitization:")
    print("-" * 40)

    batch_data = [
        {'decision': 'NO-GO', 'title': 'Test 1'},  # Not sanitized
        first_sanitized,  # Already sanitized
        {'decision': 'INDETERMINATE', 'title': 'Test 3'}  # Not sanitized
    ]

    batch_sanitized = DecisionSanitizer.sanitize_batch(batch_data)

    # Check first item was sanitized
    assert batch_sanitized[0]['result'] == 'NO-GO', "First item not sanitized"
    assert batch_sanitized[0]['_sanitized'] == True, "First item not marked"

    # Check second item was preserved
    assert batch_sanitized[1]['result'] == 'GO', "Second item modified"
    assert batch_sanitized[1]['_sanitized'] == True, "Second item marker lost"

    # Check third item was sanitized
    assert batch_sanitized[2]['result'] == 'INDETERMINATE', "Third item not sanitized"
    assert batch_sanitized[2]['_sanitized'] == True, "Third item not marked"

    print("  [OK] Batch processing:")
    print(f"       Item 1: Sanitized (NO-GO)")
    print(f"       Item 2: Preserved (GO)")
    print(f"       Item 3: Sanitized (INDETERMINATE)")

    # Test edge cases
    print("\n4. Edge Cases:")
    print("-" * 40)

    # Test with missing _sanitized marker but has other markers
    edge_case1 = {
        'result': 'GO',
        'pipeline_stage': 'APP',
        'assessment_type': 'APP_KNOCKOUT'
        # Missing _sanitized
    }

    is_sanitized = DecisionSanitizer.is_already_sanitized(edge_case1)
    print(f"  Missing _sanitized marker: {is_sanitized}")
    assert is_sanitized == False, "Should not be considered sanitized without marker"

    # Test with _sanitized but invalid result
    edge_case2 = {
        '_sanitized': True,
        'pipeline_stage': 'APP',
        'assessment_type': 'APP_KNOCKOUT',
        'result': 'MAYBE'  # Invalid value
    }

    is_sanitized = DecisionSanitizer.is_already_sanitized(edge_case2)
    print(f"  Invalid result value: {is_sanitized}")
    assert is_sanitized == False, "Should not be considered sanitized with invalid result"

    print("\n" + "=" * 60)
    print("[SUCCESS] Double sanitization prevention working correctly!")
    print("\nKey achievements:")
    print("- Already-sanitized data is detected and preserved")
    print("- _sanitized marker prevents re-processing")
    print("- Batch sanitization handles mixed data correctly")
    print("- Invalid data is properly re-sanitized")

    return True

if __name__ == "__main__":
    import sys
    success = test_double_sanitization_prevention()
    sys.exit(0 if success else 1)