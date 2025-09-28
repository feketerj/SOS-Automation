#!/usr/bin/env python3
"""Test script to validate pattern category integration."""

from sos_ingestion_gate_v419 import IngestionGateV419

def test_pattern_categories():
    """Test that all new pattern categories are properly integrated."""

    gate = IngestionGateV419()

    # Test cases for missing categories
    test_cases = [
        {
            'id': 'TEST-CAT16',
            'description': 'Must have JEDMICS access and ETIMS registration required',
            'expected_category': 16,
            'expected_name': 'IT_ACCESS'
        },
        {
            'id': 'TEST-CAT18',
            'description': 'Vendor must perform depot-level repair and provide warranty support directly',
            'expected_category': 18,
            'expected_name': 'WARRANTY'
        },
        {
            'id': 'TEST-CAT19',
            'description': 'Must submit native CATIA files and SolidWorks native format required',
            'expected_category': 19,
            'expected_name': 'CAD_CAM'
        },
        {
            'id': 'TEST-CAT12',
            'description': 'This is a bridge contract with incumbent advantage',
            'expected_category': 12,
            'expected_name': 'COMPETITION'
        },
        {
            'id': 'TEST-CAT15',
            'description': 'OTA prototype project under BAA with SBIR requirements',
            'expected_category': 15,
            'expected_name': 'EXPERIMENTAL'
        },
        {
            'id': 'TEST-CAT17',
            'description': 'DCMA approved supplier with NASA qualified and EPA certified',
            'expected_category': 17,
            'expected_name': 'CERTIFICATIONS'
        },
        {
            'id': 'TEST-AMSC-OVERRIDE',
            'description': 'F-16 fighter parts with AMSC Code G - government owns data',
            'expected_decision': 'GO',
            'expected_note': 'AMSC G override'
        }
    ]

    print("Testing Pattern Category Integration")
    print("=" * 50)

    passed = 0
    failed = 0

    for test_case in test_cases:
        print(f"\nTesting: {test_case['id']}")
        print(f"Description: {test_case['description'][:60]}...")

        opportunity = {
            'id': test_case['id'],
            'title': test_case['description'],
            'description': test_case['description'],
            'documents_text': test_case['description']
        }

        result = gate.assess_opportunity(opportunity)

        if 'expected_category' in test_case:
            # Check if the expected category was triggered
            if test_case['expected_category'] in result.categories_triggered:
                print(f"[PASS] Category {test_case['expected_category']} ({test_case['expected_name']}) triggered")
                passed += 1
            else:
                print(f"[FAIL] Category {test_case['expected_category']} ({test_case['expected_name']}) NOT triggered")
                print(f"  Triggered categories: {result.categories_triggered}")
                failed += 1

        if 'expected_decision' in test_case:
            # Check decision for override tests
            if result.decision.value == test_case['expected_decision']:
                print(f"[PASS] Decision: {result.decision.value} (expected {test_case['expected_decision']})")
                passed += 1
            else:
                print(f"[FAIL] Decision: {result.decision.value} (expected {test_case['expected_decision']})")
                failed += 1

    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")

    # Check that all pattern families in PATTERN_TO_CATEGORY exist in compiled patterns
    print("\n" + "=" * 50)
    print("Checking pattern family mappings...")

    missing_patterns = []
    for pattern_family in gate.categories.PATTERN_TO_CATEGORY.keys():
        if pattern_family not in gate.compiled_patterns:
            missing_patterns.append(pattern_family)
            print(f"[MISSING] Pattern family '{pattern_family}' not found in compiled patterns")

    if not missing_patterns:
        print("[OK] All pattern families in PATTERN_TO_CATEGORY are available")
    else:
        print(f"\n[ERROR] Missing {len(missing_patterns)} pattern families:")
        for pattern in missing_patterns:
            print(f"  - {pattern}")

    return passed, failed, missing_patterns

if __name__ == "__main__":
    passed, failed, missing = test_pattern_categories()

    if failed > 0 or missing:
        print("\n[TEST FAILED] - Some patterns not working correctly")
        exit(1)
    else:
        print("\n[ALL TESTS PASSED]")
        exit(0)