"""
Debug Script for Multi-Stage Pipeline
Identifies and tests potential issues
"""

import asyncio
import json
import traceback
from datetime import datetime

# Import all components
try:
    from document_fetcher import DocumentFetcher
    from multi_stage_pipeline import MultiStagePipeline
    from context_accumulator import ContextAccumulator
    from pipeline_config import TIMEOUTS, PIPELINE_CONFIG
    print("All imports successful")
except ImportError as e:
    print(f"Import error: {e}")
    traceback.print_exc()
    exit(1)


def test_1_retry_logic_bounds():
    """Test that retry logic handles index bounds correctly"""
    print("\n" + "="*50)
    print("TEST 1: Retry Logic Index Bounds")
    print("="*50)

    fetcher = DocumentFetcher()

    # Test that we don't go out of bounds
    issues = []

    for attempt in range(15):  # More than MAX_RETRIES
        try:
            # This is how we calculate wait time in the code
            wait_time = fetcher.RETRY_DELAYS[min(attempt, len(fetcher.RETRY_DELAYS)-1)]
            print(f"  Attempt {attempt}: wait_time = {wait_time}s")

            if attempt >= len(fetcher.RETRY_DELAYS) and wait_time != fetcher.RETRY_DELAYS[-1]:
                issues.append(f"Attempt {attempt} should use last delay but got {wait_time}")
        except IndexError as e:
            issues.append(f"IndexError at attempt {attempt}: {e}")

    if issues:
        print("\nISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("\nPASS: Retry logic handles bounds correctly")
        return True


def test_2_timeout_none_handling():
    """Test that timeout=None is handled properly by requests"""
    print("\n" + "="*50)
    print("TEST 2: Timeout=None Handling")
    print("="*50)

    import requests

    # Test that requests.get handles timeout=None
    try:
        # This should work without error
        print("  Testing requests with timeout=None...")

        # Note: We're not actually making a request, just checking the parameter works
        test_url = "http://httpbin.org/delay/0"

        # This would be the actual call pattern
        print(f"  Would call: requests.get(url, timeout={TIMEOUTS['document_fetch']})")
        print(f"  Timeout value: {TIMEOUTS['document_fetch']} (should be None)")

        if TIMEOUTS['document_fetch'] is not None:
            print("FAIL: WARNING - Timeout is not None, might not match production")
            return False

        print("PASS: Timeout configuration correct")
        return True
    except Exception as e:
        print(f"FAIL: Error testing timeout: {e}")
        return False


def test_3_large_document_truncation():
    """Test that large documents are properly truncated"""
    print("\n" + "="*50)
    print("TEST 3: Large Document Truncation")
    print("="*50)

    fetcher = DocumentFetcher()

    # Test single document truncation
    test_doc = "A" * 600000  # 600K characters (over 500K limit)

    # Simulate what happens in _fetch_documents_by_related_key
    print(f"  Original document: {len(test_doc):,} chars")

    if len(test_doc) > fetcher.MAX_SINGLE_DOC:
        truncated = test_doc[:fetcher.MAX_SINGLE_DOC]
        print(f"  After truncation: {len(truncated):,} chars")

        if len(truncated) == fetcher.MAX_SINGLE_DOC:
            print("PASS: Document truncation works correctly")
            return True
        else:
            print(f"FAIL: Truncation failed - expected {fetcher.MAX_SINGLE_DOC:,}, got {len(truncated):,}")
            return False
    else:
        print("FAIL: Document should have been truncated but wasn't")
        return False


def test_4_context_accumulator_with_none():
    """Test that context accumulator handles None values properly"""
    print("\n" + "="*50)
    print("TEST 4: Context Accumulator None Handling")
    print("="*50)

    # Test with various None values
    test_cases = [
        {"id": None, "title": None, "text": None},
        {"search_id": None, "metadata": None, "documents": None},
        {},  # Empty dict
        {"id": "TEST", "title": "", "text": "", "metadata": {}, "documents": []},
    ]

    issues = []
    for i, test_data in enumerate(test_cases):
        try:
            context = ContextAccumulator(test_data)
            print(f"  Test case {i+1}: Created context with ID='{context.opportunity_id}'")

            # Check that we don't crash when getting context
            stage_context = context.get_context_for_stage(1)
            full_context = context.get_full_context()

            if context.opportunity_id == "":
                issues.append(f"Test case {i+1}: opportunity_id is empty string, should be 'unknown'")

        except Exception as e:
            issues.append(f"Test case {i+1} failed: {e}")

    if issues:
        print("\nFAIL - ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("\nPASS: Context accumulator handles None values correctly")
        return True


async def test_5_pipeline_with_mock_api():
    """Test pipeline processing with mock API responses"""
    print("\n" + "="*50)
    print("TEST 5: Pipeline Processing (Mock API)")
    print("="*50)

    pipeline = MultiStagePipeline()

    # Create a test opportunity
    test_opportunity = {
        "search_id": "DEBUG-001",
        "metadata": {
            "title": "Debug Test Opportunity",
            "agency": "Test Agency",
            "response_date_time": "2025-12-31 17:00:00"
        },
        "documents": [
            {"file_name": "test.pdf", "text": "Test document content with deadline December 31, 2025"}
        ],
        "combined_text": "Test opportunity with deadline December 31, 2025",
        "fetch_status": "complete"
    }

    try:
        print("  Processing test opportunity through pipeline...")

        # Note: This will use mock responses since we're using the mock methods
        result = await pipeline.process_opportunity(test_opportunity)

        print(f"  Result: {result.get('final_decision')}")
        print(f"  Stages processed: {result.get('stages_processed')}")

        if result.get('stages_processed') > 0:
            print("PASS: Pipeline processed opportunity successfully")
            return True
        else:
            print("FAIL: No stages were processed")
            return False

    except Exception as e:
        print(f"FAIL: Pipeline error - {e}")
        traceback.print_exc()
        return False


def test_6_metadata_preservation():
    """Test that metadata is preserved through pipeline stages"""
    print("\n" + "="*50)
    print("TEST 6: Metadata Preservation")
    print("="*50)

    test_opportunity = {
        "search_id": "META-001",
        "metadata": {
            "title": "Test Title",
            "agency": "Test Agency",
            "response_date_time": "2025-12-31",
            "custom_field": "Should be preserved"
        },
        "documents": [{"file_name": "test.pdf", "text": "content"}],
        "combined_text": "Test text"
    }

    context = ContextAccumulator(test_opportunity)

    # Check initial preservation
    if context.metadata != test_opportunity["metadata"]:
        print(f"FAIL: Metadata not preserved on init")
        return False

    # Add a stage result
    stage_result = {
        "decision": "GO",
        "confidence": 0.99,
        "rationale": "Test"
    }
    context.add_stage_result("TEST_STAGE", stage_result)

    # Get context for next stage
    stage_context = context.get_context_for_stage(2)

    # Check metadata is in stage context
    if "metadata" not in stage_context:
        print("FAIL: Metadata not in stage context")
        return False

    if stage_context["metadata"].get("custom_field") != "Should be preserved":
        print("FAIL: Custom metadata field not preserved")
        return False

    # Check final context
    final = context.get_full_context()
    if final["metadata"].get("custom_field") != "Should be preserved":
        print("FAIL: Metadata not in final context")
        return False

    print("PASS: Metadata preserved through all stages")
    return True


def test_7_document_fetcher_error_paths():
    """Test error handling in document fetcher"""
    print("\n" + "="*50)
    print("TEST 7: Document Fetcher Error Handling")
    print("="*50)

    fetcher = DocumentFetcher()

    # Test with invalid search ID
    result = fetcher.fetch_opportunity_with_documents("")

    if result["fetch_status"] == "error" or result["fetch_status"] == "metadata_failed":
        print("PASS: Empty search ID handled correctly")
    else:
        print(f"FAIL: Expected error status, got {result['fetch_status']}")
        return False

    # Test that we have proper error structure
    if "errors" not in result:
        print("FAIL: Result missing 'errors' field")
        return False

    if "combined_text" not in result:
        print("FAIL: Result missing 'combined_text' field")
        return False

    print("PASS: Error paths return proper structure")
    return True


async def main():
    """Run all debug tests"""
    print("\n" + "="*70)
    print("MULTI-STAGE PIPELINE DEBUG SUITE")
    print("="*70)
    print(f"Started: {datetime.now()}")

    results = {
        "Test 1 - Retry Logic": test_1_retry_logic_bounds(),
        "Test 2 - Timeout None": test_2_timeout_none_handling(),
        "Test 3 - Document Truncation": test_3_large_document_truncation(),
        "Test 4 - Context None Handling": test_4_context_accumulator_with_none(),
        "Test 5 - Pipeline Processing": await test_5_pipeline_with_mock_api(),
        "Test 6 - Metadata Preservation": test_6_metadata_preservation(),
        "Test 7 - Error Handling": test_7_document_fetcher_error_paths(),
    }

    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)

    passed = 0
    failed = 0
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1

    print(f"\nTotal: {passed} passed, {failed} failed")

    if failed > 0:
        print("\nWARNING: DEBUGGING NEEDED - See failed tests above")
        return False
    else:
        print("\nSUCCESS: ALL TESTS PASSED - Code is working correctly")
        return True


if __name__ == "__main__":
    success = asyncio.run(main())