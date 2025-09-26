#!/usr/bin/env python3
"""
TEST_DOCUMENT_FETCH.py - Quick test of document fetching for first 2 endpoints
"""

import sys
import json
sys.path.append('..')

print("=" * 70)
print("TESTING DOCUMENT FETCH FOR FIRST 2 ENDPOINTS")
print("=" * 70)

# Import the fetcher
try:
    from highergov_batch_fetcher import HigherGovBatchFetcher
    print("[OK] HigherGovBatchFetcher imported successfully")
except ImportError as e:
    print(f"[X] Failed to import HigherGovBatchFetcher: {e}")
    sys.exit(1)

# Test endpoints
test_endpoints = [
    "rFRK9PaP6ftzk1rokcKCT",
    "u912_Lb64wa9wH2GuKXTu"
]

fetcher = HigherGovBatchFetcher()

for idx, search_id in enumerate(test_endpoints, 1):
    print(f"\n[{idx}/2] Testing search ID: {search_id}")
    print("-" * 50)
    
    try:
        # Fetch opportunities
        opportunities = fetcher.fetch_all_opportunities(search_id)
        print(f"  Found {len(opportunities)} opportunities")
        
        # Show first 3 opportunities
        for i, opp in enumerate(opportunities[:3], 1):
            print(f"\n  Opportunity {i}:")
            print(f"    Title: {opp.get('title', 'N/A')[:60]}")
            print(f"    ID: {opp.get('opportunity_id', 'N/A')}")
            
            # Check which document field exists
            doc_path = None
            if 'document_path' in opp:
                doc_path = opp['document_path']
                print(f"    Has document_path: {doc_path[:50] if doc_path else 'None'}")
            if 'documents_api_path' in opp:
                doc_path = opp['documents_api_path']
                print(f"    Has documents_api_path: {doc_path[:50] if doc_path else 'None'}")
            if 'document_url' in opp:
                doc_path = opp['document_url']
                print(f"    Has document_url: {doc_path[:50] if doc_path else 'None'}")
            
            # Try to fetch document
            if doc_path:
                print(f"    Fetching document...")
                try:
                    doc_text = fetcher.fetch_document_text(doc_path)
                    print(f"    [OK] Document fetched: {len(doc_text):,} characters")
                    print(f"    Preview: {doc_text[:200]}...")
                except Exception as e:
                    print(f"    [X] Failed to fetch document: {e}")
            else:
                print(f"    [X] No document path found")
                
    except Exception as e:
        print(f"  ERROR: {e}")

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)