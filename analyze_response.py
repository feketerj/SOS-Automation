import json
import os
from api_clients.highergov_client_enhanced import EnhancedHigherGovClient

client = EnhancedHigherGovClient()
response = client.get_saved_search_opportunities('tFDSNa5qi9S92K-bXbReY', limit=1)

# Get first opportunity for detailed analysis
if response.get('results'):
    opp = response['results'][0]
    print('=== OPPORTUNITY STRUCTURE ===')
    for key, value in opp.items():
        value_str = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
        print(f'{key}: {type(value)} - {value_str}')
        
    print('\n=== DOCUMENT RELATED FIELDS ===')
    doc_fields = [k for k in opp.keys() if 'doc' in k.lower() or 'file' in k.lower() or 'attach' in k.lower() or 'path' in k.lower()]
    for field in doc_fields:
        print(f'{field}: {opp[field]}')
        
    # Check if document_path exists and what it contains
    if 'document_path' in opp:
        print(f'\nDOCUMENT_PATH DETAILS: {opp["document_path"]}')
        
    # Check for any URL fields that might point to documents
    url_fields = [k for k in opp.keys() if 'url' in k.lower() or 'link' in k.lower()]
    if url_fields:
        print('\n=== URL FIELDS ===')
        for field in url_fields:
            print(f'{field}: {opp[field]}')
