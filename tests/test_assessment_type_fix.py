#!/usr/bin/env python3
"""Test that assessment type normalization works correctly"""

from decision_sanitizer import DecisionSanitizer

def test_assessment_type_normalization():
    """Test all assessment type mappings"""

    print("Testing Assessment Type Normalization")
    print("=" * 60)

    # Test cases: (input_type, expected_output)
    test_cases = [
        # Legacy names that should be normalized
        ('AGENT_VERIFIED', 'MISTRAL_ASSESSMENT'),
        ('REGEX_KNOCKOUT', 'APP_KNOCKOUT'),
        ('REGEX_ONLY', 'APP_KNOCKOUT'),
        ('APP_ONLY', 'APP_KNOCKOUT'),
        ('AGENT_AI', 'MISTRAL_ASSESSMENT'),
        ('BATCH_AI', 'MISTRAL_BATCH_ASSESSMENT'),
        # Already canonical names
        ('APP_KNOCKOUT', 'APP_KNOCKOUT'),
        ('MISTRAL_ASSESSMENT', 'MISTRAL_ASSESSMENT'),
        ('MISTRAL_BATCH_ASSESSMENT', 'MISTRAL_BATCH_ASSESSMENT'),
        # Edge cases
        ('', ''),
        (None, ''),
        ('UNKNOWN_TYPE', 'UNKNOWN_TYPE'),  # Unknown types preserved
    ]

    all_passed = True

    for input_type, expected in test_cases:
        result = DecisionSanitizer._normalize_assessment_type(input_type)
        passed = result == expected
        all_passed = all_passed and passed

        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} '{input_type}' -> '{result}' (expected: '{expected}')")

    print("\n" + "=" * 60)

    # Test full sanitization with processing_method
    print("\nTesting Full Sanitization with processing_method field:")
    print("-" * 60)

    processing_method_tests = [
        # Test AGENT_VERIFIED gets normalized
        {
            'input': {
                'processing_method': 'AGENT_VERIFIED',
                'decision': 'GO',
                'title': 'Test Opportunity'
            },
            'expected_assessment_type': 'MISTRAL_ASSESSMENT'
        },
        # Test REGEX_ONLY gets normalized
        {
            'input': {
                'processing_method': 'REGEX_ONLY',
                'decision': 'NO-GO',
                'title': 'Test Opportunity'
            },
            'expected_assessment_type': 'APP_KNOCKOUT'
        },
        # Test direct assessment_type field
        {
            'input': {
                'assessment_type': 'AGENT_VERIFIED',
                'decision': 'GO',
                'title': 'Test Opportunity'
            },
            'expected_assessment_type': 'MISTRAL_ASSESSMENT'
        },
        # Test already normalized type
        {
            'input': {
                'assessment_type': 'MISTRAL_ASSESSMENT',
                'decision': 'INDETERMINATE',
                'title': 'Test Opportunity'
            },
            'expected_assessment_type': 'MISTRAL_ASSESSMENT'
        }
    ]

    for i, test in enumerate(processing_method_tests, 1):
        sanitized = DecisionSanitizer.sanitize(test['input'])
        actual_type = sanitized.get('assessment_type', '')
        expected_type = test['expected_assessment_type']

        passed = actual_type == expected_type
        all_passed = all_passed and passed

        status = "[PASS]" if passed else "[FAIL]"
        input_desc = test['input'].get('processing_method') or test['input'].get('assessment_type', 'N/A')
        print(f"{status} Test {i}: '{input_desc}' -> '{actual_type}' (expected: '{expected_type}')")

    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] All assessment type normalization tests passed!")
    else:
        print("[FAILURE] Some tests failed. Review output above.")
    print("=" * 60)

    return all_passed

if __name__ == "__main__":
    import sys
    success = test_assessment_type_normalization()
    sys.exit(0 if success else 1)