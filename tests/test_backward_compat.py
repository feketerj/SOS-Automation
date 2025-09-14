#!/usr/bin/env python3
"""Test backward compatibility with existing data structures"""

from decision_sanitizer import DecisionSanitizer

def test_backward_compatibility():
    """Test that existing data structures still work"""

    print("Testing Backward Compatibility")
    print("=" * 60)

    # Simulate various existing data structures from the pipeline
    test_cases = [
        # 1. From FULL_BATCH_PROCESSOR with AGENT_VERIFIED
        {
            'name': 'FULL_BATCH_PROCESSOR agent verification',
            'input': {
                'processing_method': 'AGENT_VERIFIED',
                'decision': 'GO',
                'title': 'Test Opportunity',
                'agent_reasoning': 'Looks good',
                'verification_method': 'AGENT_CONFIRMED',
                'disagreement': False
            },
            'expected': {
                'result': 'GO',
                'assessment_type': 'MISTRAL_ASSESSMENT',
                'pipeline_stage': 'AGENT'
            }
        },
        # 2. From batch processing
        {
            'name': 'Batch AI processing',
            'input': {
                'processing_method': 'BATCH_AI',
                'decision': 'NO-GO',
                'title': 'Test Batch',
                'reasoning': 'Military platform'
            },
            'expected': {
                'result': 'NO-GO',
                'assessment_type': 'MISTRAL_BATCH_ASSESSMENT',
                'pipeline_stage': 'BATCH'
            }
        },
        # 3. From regex knockout
        {
            'name': 'Regex knockout',
            'input': {
                'processing_method': 'REGEX_ONLY',
                'final_decision': 'NO-GO',
                'knock_pattern': 'Military aircraft F-16',
                'title': 'F-16 Parts'
            },
            'expected': {
                'result': 'NO-GO',
                'assessment_type': 'APP_KNOCKOUT',
                'pipeline_stage': 'APP'
            }
        },
        # 4. Legacy nested format
        {
            'name': 'Legacy nested assessment',
            'input': {
                'assessment': {
                    'decision': 'INDETERMINATE',
                    'reasoning': 'Need more info'
                },
                'title': 'Unknown Part'
            },
            'expected': {
                'result': 'INDETERMINATE',
                'assessment_type': 'MISTRAL_BATCH_ASSESSMENT',
                'pipeline_stage': 'BATCH'
            }
        },
        # 5. Direct assessment_type field (already normalized)
        {
            'name': 'Already normalized type',
            'input': {
                'assessment_type': 'MISTRAL_ASSESSMENT',
                'result': 'GO',
                'solicitation_title': 'Commercial Part'
            },
            'expected': {
                'result': 'GO',
                'assessment_type': 'MISTRAL_ASSESSMENT',
                'pipeline_stage': ''  # Not auto-detected when assessment_type present
            }
        }
    ]

    all_passed = True

    for test in test_cases:
        print(f"\nTest: {test['name']}")
        print("-" * 40)

        # Run sanitization
        sanitized = DecisionSanitizer.sanitize(test['input'])

        # Check expected fields
        for field, expected_value in test['expected'].items():
            actual_value = sanitized.get(field, '')
            passed = actual_value == expected_value

            if not passed:
                all_passed = False
                print(f"  [FAIL] {field}: '{actual_value}' (expected: '{expected_value}')")
            else:
                print(f"  [PASS] {field}: '{actual_value}'")

        # Verify core fields are present
        required_fields = ['solicitation_id', 'solicitation_title', 'result',
                          'knock_out_reasons', 'exceptions', 'assessment_type']
        for field in required_fields:
            if field not in sanitized:
                print(f"  [WARN] Missing required field: {field}")

    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] All backward compatibility tests passed!")
        print("The normalization preserves functionality for all existing data formats.")
    else:
        print("[FAILURE] Some backward compatibility tests failed.")
        print("Review the failures above.")
    print("=" * 60)

    return all_passed

if __name__ == "__main__":
    import sys
    success = test_backward_compatibility()
    sys.exit(0 if success else 1)