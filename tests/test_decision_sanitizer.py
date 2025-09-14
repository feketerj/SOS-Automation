#!/usr/bin/env python3
"""
Test script to verify decision sanitizer fixes the output formatting issue
"""

from decision_sanitizer import DecisionSanitizer

def test_decision_normalization():
    """Test that decisions are properly normalized"""

    test_cases = [
        # Input, Expected Output
        ('GO', 'GO'),
        ('go', 'GO'),
        ('Go', 'GO'),
        ('NO-GO', 'NO-GO'),
        ('NO_GO', 'NO-GO'),
        ('no-go', 'NO-GO'),
        ('NO GO', 'NO-GO'),
        ('INDETERMINATE', 'INDETERMINATE'),
        ('indeterminate', 'INDETERMINATE'),
        ('UNKNOWN', 'INDETERMINATE'),
        ('FURTHER_ANALYSIS', 'INDETERMINATE'),
        ('CONTACT CO', 'INDETERMINATE'),
        (None, 'INDETERMINATE'),
        ('', 'INDETERMINATE'),
        ('random text', 'INDETERMINATE'),
    ]

    print("Testing decision normalization...")
    print("-" * 50)

    all_passed = True
    for input_val, expected in test_cases:
        result = DecisionSanitizer._normalize(input_val)
        passed = result == expected
        status = "PASS" if passed else "FAIL"

        if not passed:
            all_passed = False

        print(f"{status} Input: '{input_val}' -> Expected: '{expected}', Got: '{result}'")

    print("-" * 50)
    if all_passed:
        print("SUCCESS: All tests passed!")
    else:
        print("FAILURE: Some tests failed!")

    return all_passed

def test_data_sanitization():
    """Test that data dictionaries are properly sanitized"""

    test_data = [
        {
            'decision': 'go',
            'title': 'Test Opportunity'
        },
        {
            'decision': 'NO_GO',
            'recommendation': 'Do not proceed'
        },
        {
            'final_decision': 'indeterminate',
            'batch_decision': 'go',
            'agent_decision': 'no-go'
        }
    ]

    print("\nTesting data sanitization...")
    print("-" * 50)

    for i, data in enumerate(test_data):
        print(f"\nTest {i+1}:")
        print(f"  Input: {data}")

        sanitized = DecisionSanitizer.sanitize(data.copy())
        print(f"  Output: {sanitized}")

        # Check that final_decision exists and is normalized
        if 'final_decision' in sanitized:
            decision = sanitized['final_decision']
            if decision in ['GO', 'NO-GO', 'INDETERMINATE']:
                print(f"  VALID final_decision: {decision}")
            else:
                print(f"  INVALID final_decision: {decision}")
        else:
            print("  MISSING final_decision field")

    print("-" * 50)

def test_batch_sanitization():
    """Test batch processing of multiple items"""

    batch_data = [
        {'decision': 'GO', 'id': '1'},
        {'decision': 'no-go', 'id': '2'},
        {'recommendation': 'INDETERMINATE', 'id': '3'},
        {'final_decision': 'GO', 'id': '4'},
    ]

    print("\nTesting batch sanitization...")
    print("-" * 50)

    sanitized_batch = DecisionSanitizer.sanitize_batch(batch_data)

    for item in sanitized_batch:
        print(f"ID: {item.get('id')} -> final_decision: {item.get('final_decision')}")

    # Check all have normalized final_decision
    all_valid = all(
        item.get('final_decision') in ['GO', 'NO-GO', 'INDETERMINATE']
        for item in sanitized_batch
    )

    if all_valid:
        print("SUCCESS: All batch items properly sanitized!")
    else:
        print("FAILURE: Some batch items not properly sanitized!")

    print("-" * 50)

if __name__ == "__main__":
    print("=" * 50)
    print("DECISION SANITIZER TEST SUITE")
    print("=" * 50)

    # Run all tests
    test_decision_normalization()
    test_data_sanitization()
    test_batch_sanitization()

    print("\n" + "=" * 50)
    print("TEST SUITE COMPLETE")
    print("=" * 50)