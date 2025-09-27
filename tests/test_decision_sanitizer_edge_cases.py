"""Unit tests for DecisionSanitizer edge cases"""
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from decision_sanitizer import DecisionSanitizer

def test_nested_legacy_format():
    """Test handling of legacy format with assessment dict"""
    # Legacy format with assessment dictionary
    data = {
        "assessment": {
            "decision": "no-go"
        }
    }

    result = DecisionSanitizer.sanitize(data)
    assert result['result'] == 'NO-GO'

    # Test deeper nested structure returns INDETERMINATE
    deeply_nested = {
        "wrapper": {
            "assessment": {
                "inner": {
                    "decision": "no-go"
                }
            }
        }
    }

    result = DecisionSanitizer.sanitize(deeply_nested)
    assert result['result'] == 'INDETERMINATE'  # Too deep to find

def test_none_and_empty_values():
    """Test handling of None and empty values"""

    # Test None (returns None for non-dict)
    assert DecisionSanitizer.sanitize(None) == None

    # Test empty dict (should return sanitized structure)
    result = DecisionSanitizer.sanitize({})
    assert result['result'] == 'INDETERMINATE'

    # Test dict with None decision
    result = DecisionSanitizer.sanitize({'decision': None})
    assert result['result'] == 'INDETERMINATE'

    # Test dict with empty string decision
    result = DecisionSanitizer.sanitize({'decision': ''})
    assert result['result'] == 'INDETERMINATE'

def test_case_variations():
    """Test various case and spacing variations"""

    test_cases = [
        ("GO", "GO"),
        ("go", "GO"),
        ("Go", "GO"),
        ("gO", "GO"),
        (" GO ", "GO"),
        ("NO-GO", "NO-GO"),
        ("no-go", "NO-GO"),
        ("No-Go", "NO-GO"),
        ("NO_GO", "NO-GO"),
        ("NOGO", "NO-GO"),
        ("no go", "NO-GO"),
        ("  no   go  ", "NO-GO"),
    ]

    for input_val, expected in test_cases:
        result = DecisionSanitizer.sanitize({'decision': input_val})
        assert result['result'] == expected, f"Failed for input: '{input_val}'"

def test_already_sanitized_detection():
    """Test that already sanitized data is not re-processed"""

    # Already sanitized data (has _sanitized marker)
    data = {
        'result': 'GO',
        '_sanitized': True,
        'rationale': 'Test rationale'
    }

    result = DecisionSanitizer.sanitize(data)
    assert result == data  # Should return unchanged
    assert result['_sanitized'] is True

def test_field_preservation():
    """Test that standard fields are preserved during sanitization"""

    data = {
        'decision': 'go',
        'rationale': 'This is a good opportunity',
        'solicitation_id': '12345',
        'sam_url': 'https://sam.gov/123',
        'hg_url': 'https://highergov.com/456'
    }

    result = DecisionSanitizer.sanitize(data)

    # Check decision was sanitized
    assert result['result'] == 'GO'
    assert result['final_decision'] == 'GO'  # Both fields set

    # Check other fields preserved
    assert result['rationale'] == 'This is a good opportunity'
    assert result['solicitation_id'] == '12345'
    assert result['sam_url'] == 'https://sam.gov/123'
    assert result['hg_url'] == 'https://highergov.com/456'

    # Check standard fields are added
    assert '_sanitized' in result
    assert 'pipeline_stage' in result
    assert 'assessment_type' in result

def test_special_decision_values():
    """Test handling of special decision values"""

    test_cases = [
        ('INDETERMINATE', 'INDETERMINATE'),
        ('indeterminate', 'INDETERMINATE'),
        ('UNKNOWN', 'INDETERMINATE'),
        ('unknown', 'INDETERMINATE'),
        ('REVIEW', 'INDETERMINATE'),
        ('review', 'INDETERMINATE'),
        ('ERROR', 'INDETERMINATE'),
        ('error', 'INDETERMINATE'),
        ('INVALID', 'INDETERMINATE'),
        ('invalid', 'INDETERMINATE'),
    ]

    for input_val, expected in test_cases:
        result = DecisionSanitizer.sanitize({'decision': input_val})
        assert result['result'] == expected, f"Failed for input: '{input_val}'"
if __name__ == '__main__':
    # Run tests directly
    print('Running DecisionSanitizer edge case tests...')

    test_nested_legacy_format()
    print('[OK] Nested legacy format test passed')

    test_none_and_empty_values()
    print('[OK] None and empty values test passed')

    test_case_variations()
    print('[OK] Case variations test passed')

    test_already_sanitized_detection()
    print('[OK] Already sanitized detection test passed')

    test_field_preservation()
    print('[OK] Field preservation test passed')

    test_special_decision_values()
    print('[OK] Special decision values test passed')

    print('\nAll DecisionSanitizer tests passed!')
