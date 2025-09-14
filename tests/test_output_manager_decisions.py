#!/usr/bin/env python3
"""Test why output manager shows all decisions as INDETERMINATE"""

from enhanced_output_manager import EnhancedOutputManager
from decision_sanitizer import DecisionSanitizer
import tempfile
import json
import os

def test_decision_recognition():
    """Test that output manager correctly recognizes decisions"""

    print("Testing Output Manager Decision Recognition")
    print("=" * 60)

    # Create test data simulating pipeline output
    test_cases = [
        # 1. Direct from Regex stage
        {
            'name': 'Regex Knockout',
            'data': {
                'decision': 'NO-GO',
                'knock_pattern': 'Military platform',
                'processing_method': 'APP_ONLY',
                'title': 'F-16 Parts',
                'source_id': 'TEST001'
            }
        },
        # 2. From Batch API
        {
            'name': 'Batch GO',
            'data': {
                'decision': 'GO',
                'final_decision': 'GO',
                'processing_method': 'BATCH_AI',
                'title': 'Boeing 737 Parts',
                'source_id': 'TEST002',
                'batch_reasoning': 'Commercial aircraft parts'
            }
        },
        # 3. From Agent Verification
        {
            'name': 'Agent NO-GO',
            'data': {
                'final_decision': 'NO-GO',
                'processing_method': 'AGENT_AI',
                'title': 'Classified System',
                'source_id': 'TEST003',
                'reasoning': 'Requires clearance'
            }
        },
        # 4. Already sanitized format
        {
            'name': 'Unified Schema GO',
            'data': {
                'result': 'GO',
                'solicitation_id': 'TEST004',
                'solicitation_title': 'Commercial Parts',
                'rationale': 'COTS items',
                '_sanitized': True
            }
        },
        # 5. Nested assessment format (legacy)
        {
            'name': 'Legacy Nested',
            'data': {
                'assessment': {
                    'decision': 'INDETERMINATE',
                    'reasoning': 'Need more info'
                },
                'title': 'Unclear Requirements',
                'source_id': 'TEST005'
            }
        }
    ]

    print("\n1. Testing Raw Decision Recognition:")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        manager = EnhancedOutputManager(base_path=tmpdir)

        all_passed = True

        for test_case in test_cases:
            print(f"\nTest: {test_case['name']}")

            # First sanitize the data
            sanitized = DecisionSanitizer.sanitize(test_case['data'])
            print(f"  Sanitized result field: {sanitized.get('result')}")

            # Process through output manager
            enriched = manager._process_assessments([sanitized])

            if enriched:
                assessment = enriched[0]

                # Check what decision the output manager sees
                result_field = assessment.get('result')
                final_decision_field = assessment.get('final_decision')

                print(f"  Output manager sees:")
                print(f"    - result: {result_field}")
                print(f"    - final_decision: {final_decision_field}")

                # The issue: Is it recognizing the decision correctly?
                if result_field == 'INDETERMINATE' and sanitized.get('result') != 'INDETERMINATE':
                    print(f"  [FAIL] Decision lost! Was {sanitized.get('result')}, became INDETERMINATE")
                    all_passed = False
                elif result_field == sanitized.get('result'):
                    print(f"  [OK] Decision preserved: {result_field}")
                else:
                    print(f"  [WARN] Decision changed: {sanitized.get('result')} -> {result_field}")
                    all_passed = False

        print("\n2. Testing Batch Processing:")
        print("-" * 40)

        # Test with a batch of mixed decisions
        batch_data = [
            {'decision': 'GO', 'title': 'Test GO', 'source_id': 'B001'},
            {'decision': 'NO-GO', 'title': 'Test NO-GO', 'source_id': 'B002'},
            {'decision': 'INDETERMINATE', 'title': 'Test INDETERMINATE', 'source_id': 'B003'}
        ]

        # Sanitize batch
        sanitized_batch = DecisionSanitizer.sanitize_batch(batch_data)

        # Process through output manager
        enriched_batch = manager._process_assessments(sanitized_batch)

        # Count decisions
        go_count = sum(1 for a in enriched_batch if a.get('result') == 'GO')
        nogo_count = sum(1 for a in enriched_batch if a.get('result') == 'NO-GO')
        indeterminate_count = sum(1 for a in enriched_batch if a.get('result') == 'INDETERMINATE')

        print(f"Expected: 1 GO, 1 NO-GO, 1 INDETERMINATE")
        print(f"Actual: {go_count} GO, {nogo_count} NO-GO, {indeterminate_count} INDETERMINATE")

        if go_count == 1 and nogo_count == 1 and indeterminate_count == 1:
            print("[OK] Batch counts correct")
        else:
            print("[FAIL] Batch counts incorrect")
            all_passed = False

        # Test the save and summary generation
        print("\n3. Testing Save and Summary:")
        print("-" * 40)

        output_dir = manager.save_assessment_batch(
            search_id='TEST_BATCH',
            assessments=sanitized_batch,
            metadata={'test': True}
        )

        # Check the JSON output
        json_file = os.path.join(output_dir, 'data.json')
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                json_data = json.load(f)

            summary = json_data.get('summary', {})
            print(f"JSON Summary: GO={summary.get('go')}, NO-GO={summary.get('no_go')}, INDETERMINATE={summary.get('indeterminate')}")

            if summary.get('go') == 1 and summary.get('no_go') == 1 and summary.get('indeterminate') == 1:
                print("[OK] JSON summary correct")
            else:
                print("[FAIL] JSON summary incorrect")
                all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] Output manager correctly recognizes decisions")
    else:
        print("[FAILURE] Output manager has issues with decision recognition")

    return all_passed

if __name__ == "__main__":
    import sys
    success = test_decision_recognition()
    sys.exit(0 if success else 1)