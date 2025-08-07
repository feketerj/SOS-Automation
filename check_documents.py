#!/usr/bin/env python3
import json
import glob

# Load one of our JSON files to see the structure
json_files = glob.glob('output/*.json')
if json_files:
    with open(json_files[0], 'r') as f:
        data = json.load(f)
    
    # Check if documents are included
    opp = data.get('original_opportunity', {})
    print('Keys in opportunity data:')
    print(list(opp.keys()))
    
    if 'documents' in opp:
        print(f'\nDocuments found: {len(opp["documents"])}')
        if opp['documents']:
            print('First document structure:')
            print(json.dumps(opp['documents'][0], indent=2)[:500])
    else:
        print('\nNo documents field found')
        
    # Check what text data we have
    text_fields = ['description', 'description_text', 'synopsis', 'full_text']
    for field in text_fields:
        if field in opp:
            print(f'\n{field}: {len(str(opp[field]))} characters')
            if len(str(opp[field])) > 0:
                print(f'{field} sample: {str(opp[field])[:200]}...')
else:
    print("No JSON files found")
