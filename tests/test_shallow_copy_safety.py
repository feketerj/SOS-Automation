#!/usr/bin/env python3
"""Test that shallow copy doesn't cause unintended mutations"""

def test_shallow_copy_safety():
    """Test that modifications to copied sanitized data don't affect original"""

    print("Testing Shallow Copy Safety")
    print("=" * 60)

    # Create a sanitized result with nested structures
    original = {
        '_sanitized': True,
        'result': 'GO',
        'pipeline_stage': 'BATCH',
        'assessment_type': 'MISTRAL_BATCH_ASSESSMENT',
        'knock_out_reasons': ['Reason 1', 'Reason 2'],  # Mutable list
        'exceptions': [],  # Mutable list
        'metadata': {  # Nested dict
            'timestamp': '2025-09-13',
            'version': '1.0'
        }
    }

    # Simulate what happens in FULL_BATCH_PROCESSOR.py line 806
    print("\n1. Testing Shallow Copy Behavior:")
    print("-" * 40)

    copied = original.copy()
    copied['verification_method'] = 'AGENT'
    copied['disagreement'] = True

    # Test 1: Top-level additions don't affect original
    assert 'verification_method' not in original, "Top-level addition affected original!"
    assert 'disagreement' not in original, "Top-level addition affected original!"
    print("  [OK] Top-level additions don't affect original")

    # Test 2: Top-level modifications don't affect original
    copied['result'] = 'NO-GO'
    assert original['result'] == 'GO', "Top-level modification affected original!"
    print("  [OK] Top-level modifications don't affect original")

    # Test 3: WARNING - List modifications DO affect original
    copied['knock_out_reasons'].append('Reason 3')
    if 'Reason 3' in original['knock_out_reasons']:
        print("  [WARNING] List modification DOES affect original!")
        print("           This is expected Python behavior with shallow copy")
    else:
        print("  [UNEXPECTED] List modification didn't affect original")

    # Test 4: WARNING - Nested dict modifications DO affect original
    copied['metadata']['modified'] = True
    if 'modified' in original.get('metadata', {}):
        print("  [WARNING] Nested dict modification DOES affect original!")
        print("           This is expected Python behavior with shallow copy")
    else:
        print("  [UNEXPECTED] Nested dict modification didn't affect original")

    # Test proper deep copy approach
    print("\n2. Testing Deep Copy Solution:")
    print("-" * 40)

    import copy

    # Reset original
    original = {
        '_sanitized': True,
        'result': 'GO',
        'knock_out_reasons': ['Reason 1', 'Reason 2'],
        'metadata': {'timestamp': '2025-09-13'}
    }

    # Use deep copy instead
    deep_copied = copy.deepcopy(original)
    deep_copied['knock_out_reasons'].append('Reason 3')
    deep_copied['metadata']['modified'] = True

    assert 'Reason 3' not in original['knock_out_reasons'], "Deep copy failed for list!"
    assert 'modified' not in original.get('metadata', {}), "Deep copy failed for nested dict!"
    print("  [OK] Deep copy prevents all mutations to original")

    # Recommendation
    print("\n3. Recommendation for FULL_BATCH_PROCESSOR.py:")
    print("-" * 40)
    print("  Current (line 806): sanitized_result = result.copy()")
    print("  Better: import copy; sanitized_result = copy.deepcopy(result)")
    print("  OR: Only copy needed fields instead of entire structure")

    print("\n" + "=" * 60)
    print("[COMPLETE] Shallow copy test reveals potential issues")
    print("\nFindings:")
    print("- Shallow copy is SAFE for top-level primitive fields")
    print("- Shallow copy is UNSAFE for lists and nested dicts")
    print("- Current code could have issues if lists/dicts are modified")
    print("- Recommend using deepcopy or selective field copying")

    return True

if __name__ == "__main__":
    import sys
    success = test_shallow_copy_safety()
    sys.exit(0 if success else 1)