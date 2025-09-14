#!/usr/bin/env python3
"""Test that URL fields are properly preserved through the pipeline"""

import sys
import os
from highergov_batch_fetcher import HigherGovBatchFetcher
from decision_sanitizer import DecisionSanitizer
from enhanced_output_manager import EnhancedOutputManager

def test_url_preservation():
    """Test that both sam_url and hg_url are preserved"""

    print("Testing URL field preservation...")
    print("-" * 50)

    # Test 1: HigherGov fetcher outputs both URLs
    print("\n1. Testing HigherGovBatchFetcher...")
    test_data = {
        'source_path': 'https://sam.gov/opp/test123',
        'path': 'https://www.highergov.com/opportunity/test123',
        'title': 'Test Opportunity',
        'source_id': 'TEST123'
    }

    fetcher = HigherGovBatchFetcher()
    processed = fetcher.process_opportunity(test_data)

    assert 'sam_url' in processed, "sam_url not found in fetcher output"
    assert 'hg_url' in processed, "hg_url not found in fetcher output"
    assert processed['sam_url'] == 'https://sam.gov/opp/test123', f"Wrong sam_url: {processed['sam_url']}"
    assert processed['hg_url'] == 'https://www.highergov.com/opportunity/test123', f"Wrong hg_url: {processed['hg_url']}"
    print(f"  [OK] Fetcher outputs sam_url: {processed['sam_url']}")
    print(f"  [OK] Fetcher outputs hg_url: {processed['hg_url']}")

    # Test 2: Decision sanitizer preserves URLs
    print("\n2. Testing DecisionSanitizer...")
    test_assessment = {
        'sam_url': 'https://sam.gov/opp/test123',
        'hg_url': 'https://www.highergov.com/opportunity/test123',
        'decision': 'GO',
        'title': 'Test Opportunity'
    }

    sanitized = DecisionSanitizer.sanitize(test_assessment)

    assert 'sam_url' in sanitized, "sam_url not preserved by sanitizer"
    assert 'hg_url' in sanitized, "hg_url not preserved by sanitizer"
    assert sanitized['sam_url'] == 'https://sam.gov/opp/test123', f"Sanitizer changed sam_url: {sanitized['sam_url']}"
    assert sanitized['hg_url'] == 'https://www.highergov.com/opportunity/test123', f"Sanitizer changed hg_url: {sanitized['hg_url']}"
    print(f"  [OK] Sanitizer preserves sam_url: {sanitized['sam_url']}")
    print(f"  [OK] Sanitizer preserves hg_url: {sanitized['hg_url']}")

    # Test 3: Output manager includes URLs in enriched data
    print("\n3. Testing EnhancedOutputManager...")
    manager = EnhancedOutputManager()

    test_assessments = [{
        'sam_url': 'https://sam.gov/opp/test123',
        'hg_url': 'https://www.highergov.com/opportunity/test123',
        'result': 'GO',
        'solicitation_title': 'Test Opportunity',
        'solicitation_id': 'TEST123'
    }]

    enriched = manager._process_assessments(test_assessments)

    assert len(enriched) == 1, "Expected 1 enriched assessment"
    enriched_item = enriched[0]

    assert 'sam_url' in enriched_item, "sam_url not in enriched output"
    assert 'highergov_url' in enriched_item, "highergov_url not in enriched output"
    assert enriched_item['sam_url'] == 'https://sam.gov/opp/test123', f"Wrong sam_url in output: {enriched_item['sam_url']}"
    print(f"  [OK] Output manager includes sam_url: {enriched_item['sam_url']}")
    print(f"  [OK] Output manager includes highergov_url: {enriched_item['highergov_url']}")

    print("\n" + "=" * 50)
    print("[SUCCESS] ALL URL PRESERVATION TESTS PASSED")
    print("=" * 50)

    return True

if __name__ == "__main__":
    try:
        test_url_preservation()
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)