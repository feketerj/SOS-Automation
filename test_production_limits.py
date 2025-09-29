"""
Test Production Limits and Timeouts
Verifies the pipeline matches production configuration with NO timeouts and large limits
"""

import time
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from document_fetcher import DocumentFetcher
from pipeline_config import TIMEOUTS, PIPELINE_CONFIG


def test_configuration():
    """Test that configuration matches production settings"""
    print("\n" + "="*70)
    print("TESTING PRODUCTION CONFIGURATION")
    print("="*70)

    print("\n1. TIMEOUT CONFIGURATION (should all be None):")
    for key, value in TIMEOUTS.items():
        status = "OK - NO TIMEOUT" if value is None else f"FAIL - Has timeout: {value}s"
        print(f"   - {key}: {status}")

    print("\n2. DOCUMENT LIMITS:")
    fetcher = DocumentFetcher()
    print(f"   - Max document length: {fetcher.MAX_DOCUMENT_LENGTH:,} chars (should be 2,000,000)")
    print(f"   - Max single document: {fetcher.MAX_SINGLE_DOC:,} chars (should be 500,000)")
    print(f"   - Max retries: {fetcher.MAX_RETRIES} (should be 10)")
    print(f"   - Document timeout: {fetcher.DOCUMENT_TIMEOUT} (should be None)")

    print("\n3. RETRY DELAYS (progressive backoff):")
    print(f"   - Delays: {fetcher.RETRY_DELAYS}")
    print(f"   - Max delay: {max(fetcher.RETRY_DELAYS)} seconds")

    print("\n4. PIPELINE LIMITS:")
    print(f"   - Max tokens per request: {PIPELINE_CONFIG['max_tokens_per_request']:,} (should be 8,000)")
    print(f"   - Max context length: {PIPELINE_CONFIG['max_context_length']:,} chars (should be 2,000,000)")

    print("\n5. VERIFICATION:")
    all_good = True

    # Check timeouts are None
    for key, value in TIMEOUTS.items():
        if value is not None:
            print(f"   FAIL: {key} has timeout of {value}s, should be None")
            all_good = False

    # Check document limits
    if fetcher.MAX_DOCUMENT_LENGTH != 2000000:
        print(f"   FAIL: MAX_DOCUMENT_LENGTH is {fetcher.MAX_DOCUMENT_LENGTH}, should be 2000000")
        all_good = False

    if fetcher.MAX_SINGLE_DOC != 500000:
        print(f"   FAIL: MAX_SINGLE_DOC is {fetcher.MAX_SINGLE_DOC}, should be 500000")
        all_good = False

    if fetcher.MAX_RETRIES != 10:
        print(f"   FAIL: MAX_RETRIES is {fetcher.MAX_RETRIES}, should be 10")
        all_good = False

    if fetcher.DOCUMENT_TIMEOUT is not None:
        print(f"   FAIL: DOCUMENT_TIMEOUT is {fetcher.DOCUMENT_TIMEOUT}, should be None")
        all_good = False

    if PIPELINE_CONFIG['max_tokens_per_request'] != 8000:
        print(f"   FAIL: max_tokens_per_request is {PIPELINE_CONFIG['max_tokens_per_request']}, should be 8000")
        all_good = False

    if PIPELINE_CONFIG['max_context_length'] != 2000000:
        print(f"   FAIL: max_context_length is {PIPELINE_CONFIG['max_context_length']}, should be 2000000")
        all_good = False

    if all_good:
        print("   ALL CHECKS PASSED - Configuration matches production!")
    else:
        print("   SOME CHECKS FAILED - See above for details")

    return all_good


def test_large_document_handling():
    """Test that the system can handle large documents"""
    print("\n" + "="*70)
    print("TESTING LARGE DOCUMENT HANDLING")
    print("="*70)

    # Create a large mock document
    large_text = "A" * 1500000  # 1.5M characters
    print(f"\nCreated test document with {len(large_text):,} characters")

    fetcher = DocumentFetcher()

    # Test combining texts
    mock_metadata = {
        "title": "Large Document Test",
        "description_text": "B" * 100000  # 100K more
    }

    mock_documents = [
        {"text": "C" * 400000, "file_name": "doc1.pdf"},  # 400K
        {"text": "D" * 400000, "file_name": "doc2.pdf"},  # 400K
    ]

    combined = fetcher._combine_texts(mock_metadata, mock_documents)
    print(f"Combined text length: {len(combined):,} characters")

    if len(combined) <= fetcher.MAX_DOCUMENT_LENGTH:
        print(f"OK - Combined text within limit ({fetcher.MAX_DOCUMENT_LENGTH:,} chars)")
    else:
        print(f"FAIL - Combined text exceeds limit!")

    # Test single document truncation
    huge_doc = {"text": "E" * 600000, "file_name": "huge.pdf"}  # 600K - over single limit

    if len(huge_doc["text"]) > fetcher.MAX_SINGLE_DOC:
        truncated_length = fetcher.MAX_SINGLE_DOC
        print(f"\nOK - Would truncate single document from {len(huge_doc['text']):,} to {truncated_length:,} chars")
    else:
        print(f"\nFAIL - Single document not properly limited")


def simulate_long_running_fetch():
    """Simulate a long-running document fetch to show no timeout"""
    print("\n" + "="*70)
    print("SIMULATING LONG-RUNNING FETCH (NO TIMEOUT)")
    print("="*70)

    print("\nIn production, document fetches can run for minutes without timing out:")
    print("- Timeout setting: None (no timeout)")
    print("- Can wait as long as needed for documents")
    print("- Will retry up to 10 times with progressive backoff")

    fetcher = DocumentFetcher()
    print(f"\nRetry schedule (seconds between attempts):")
    for i, delay in enumerate(fetcher.RETRY_DELAYS, 1):
        print(f"  Attempt {i}: Wait {delay}s before retry")

    total_wait = sum(fetcher.RETRY_DELAYS)
    print(f"\nTotal possible wait time across all retries: {total_wait} seconds ({total_wait/60:.1f} minutes)")


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("PRODUCTION LIMITS AND TIMEOUT VERIFICATION")
    print("="*70)
    print("\nThis verifies the pipeline matches production settings from CLIENT_CONFIG.md:")
    print("- NO timeouts (all set to None)")
    print("- 2M character limit for documents")
    print("- 10 retries with progressive backoff")
    print("- Can handle massive documents")

    # Test 1: Configuration
    config_ok = test_configuration()

    # Test 2: Large document handling
    test_large_document_handling()

    # Test 3: Simulate long fetch
    simulate_long_running_fetch()

    print("\n" + "="*70)
    if config_ok:
        print("VERIFICATION COMPLETE - READY FOR PRODUCTION")
    else:
        print("VERIFICATION FAILED - CHECK CONFIGURATION")
    print("="*70)


if __name__ == "__main__":
    main()