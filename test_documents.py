import json
import os
from api_clients.highergov_client_enhanced import EnhancedHigherGovClient

client = EnhancedHigherGovClient()
response = client.get_saved_search_opportunities('tFDSNa5qi9S92K-bXbReY', limit=1)

# Get first opportunity for detailed analysis
if response.get('results'):
    opp = response['results'][0]
    print(f"Opportunity: {opp['title']}")
    print(f"Source ID: {opp['source_id']}")
    
    # Try to fetch documents
    if 'document_path' in opp and opp['document_path']:
        print(f"\nFetching documents from: {opp['document_path']}")
        documents = client.get_opportunity_documents(opp['document_path'])
        
        print(f"\nDocuments response structure:")
        for key, value in documents.items():
            value_str = str(value)[:200] + "..." if len(str(value)) > 200 else str(value)
            print(f'{key}: {type(value)} - {value_str}')
            
        if 'results' in documents and documents['results']:
            print(f"\nFound {len(documents['results'])} documents:")
            for i, doc in enumerate(documents['results'][:3]):  # Show first 3 docs
                print(f"\nDocument {i+1}:")
                for key, value in doc.items():
                    if isinstance(value, str) and len(value) > 100:
                        print(f"  {key}: {value[:100]}...")
                    else:
                        print(f"  {key}: {value}")
        else:
            print("No documents found in response")
    else:
        print("No document_path available")
