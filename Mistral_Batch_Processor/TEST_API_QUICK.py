#!/usr/bin/env python3
"""Quick test of HigherGov API to verify document fetching"""

import sys
import requests
import json
sys.path.append('..')

print("Testing HigherGov API Integration...")

# Test parameters
API_KEY = '9874995194174018881c567d92a2c4d2'
SEARCH_ID = 'rFRK9PaP6ftzk1rokcKCT'  # First endpoint

# Fetch opportunities
print(f"\n1. Fetching opportunities for search ID: {SEARCH_ID}")
params = {
    'api_key': API_KEY,
    'search_id': SEARCH_ID,
    'page_size': 3,  # Just get a few
    'page_number': 1
}

response = requests.get('https://www.highergov.com/api-external/opportunity/', params=params, timeout=30)
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    results = data.get('results', [])
    print(f"   Found {len(results)} opportunities")
    
    # Check first opportunity
    if results:
        opp = results[0]
        print(f"\n2. First opportunity:")
        print(f"   Title: {opp.get('title', 'N/A')[:60]}")
        print(f"   ID: {opp.get('opportunity_id', 'N/A')}")
        
        # Check for document path fields
        print(f"\n3. Document path fields present:")
        print(f"   documents_api_path: {'YES' if opp.get('documents_api_path') else 'NO'}")
        print(f"   document_path: {'YES' if opp.get('document_path') else 'NO'}")
        print(f"   document_url: {'YES' if opp.get('document_url') else 'NO'}")
        
        # Try to fetch documents
        doc_path = opp.get('documents_api_path') or opp.get('document_path')
        if doc_path:
            print(f"\n4. Fetching documents from: {doc_path[:100]}...")
            doc_response = requests.get(doc_path, timeout=30)
            print(f"   Status: {doc_response.status_code}")
            
            if doc_response.status_code == 200:
                docs = doc_response.json()
                doc_results = docs.get('results', [])
                print(f"   Found {len(doc_results)} documents")
                
                if doc_results:
                    first_doc = doc_results[0]
                    print(f"\n5. First document:")
                    print(f"   File name: {first_doc.get('file_name', 'N/A')}")
                    print(f"   Has text_extract: {'YES' if first_doc.get('text_extract') else 'NO'}")
                    print(f"   Has text: {'YES' if first_doc.get('text') else 'NO'}")
                    
                    if first_doc.get('text_extract'):
                        print(f"   Text preview: {first_doc['text_extract'][:200]}...")
                else:
                    print("   No documents in response")
            else:
                print(f"   Failed to fetch documents: {doc_response.text[:200]}")
        else:
            print("\n4. No document path found in opportunity")
else:
    print(f"Failed to fetch opportunities: {response.text[:200]}")

print("\nTest complete!")