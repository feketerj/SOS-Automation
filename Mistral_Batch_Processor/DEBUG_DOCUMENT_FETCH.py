#!/usr/bin/env python3
"""Debug script to test document fetching"""

import sys
import os
sys.path.append('..')

from highergov_batch_fetcher import HigherGovBatchFetcher
import json

# Test with first endpoint
search_id = 'rFRK9PaP6ftzk1rokcKCT'

print("Testing document fetch...")
fetcher = HigherGovBatchFetcher()

# Get first opportunity
opportunities = fetcher.fetch_all_opportunities(search_id)
opportunities = opportunities[:1]  # Just get first one
if not opportunities:
    print("No opportunities found")
    sys.exit(1)

opp = opportunities[0]
print(f"\nOpportunity: {opp.get('title', 'N/A')}")
print(f"Has documents_api_path: {bool(opp.get('documents_api_path'))}")
print(f"Has document_path: {bool(opp.get('document_path'))}")

# Process it
processed = fetcher.process_opportunity(opp)

print(f"\nProcessed opportunity fields:")
for key in processed.keys():
    if key == 'text':
        print(f"  {key}: {len(processed[key])} chars")
        if processed[key]:
            print(f"    Preview: {processed[key][:200]}...")
    else:
        print(f"  {key}: {str(processed[key])[:50]}")

# Try fetching documents directly
doc_path = opp.get('documents_api_path') or opp.get('document_path')
if doc_path:
    print(f"\nDirect document fetch from: {doc_path[:100]}...")
    import requests
    response = requests.get(doc_path, timeout=60)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        docs = response.json()
        print(f"Found {len(docs.get('results', []))} documents")
        for i, doc in enumerate(docs.get('results', [])[:3]):
            print(f"\nDocument {i+1}:")
            print(f"  file_name: {doc.get('file_name', 'N/A')}")
            print(f"  has text_extract: {bool(doc.get('text_extract'))}")
            print(f"  text_extract length: {len(doc.get('text_extract', ''))}")
            print(f"  has text: {bool(doc.get('text'))}")
            print(f"  text length: {len(doc.get('text', ''))}")
            if doc.get('text_extract'):
                print(f"  Preview: {doc['text_extract'][:100]}...")