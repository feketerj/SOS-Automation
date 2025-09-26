#!/usr/bin/env python3
"""Test script to verify the corrected prompt format"""

import json

# Sample opportunity
opp = {
    'title': 'BOLT, MACHINE',
    'agency': 'DLA Aviation',
    'naics': '336413',
    'psc': '5306',
    'text': 'This is a test document for BOLT, MACHINE NSN 5306002062865'
}

# Generate prompt using the CORRECTED format
prompt = f"""Context: You are an expert assessment specialist for Source One Spares (SOS), a small organic supplier specializing in surplus military and aviation parts.

Question: Analyze this government contracting opportunity for Source One Spares:

Title: {opp['title']}
Agency: {opp.get('agency', 'N/A')}
NAICS: {opp.get('naics', 'N/A')}
PSC: {opp.get('psc', 'N/A')}

Requirements excerpt: {opp['text'][:400000]}"""

# Create batch request with NO SYSTEM MESSAGE
batch_request = {
    "custom_id": f"test-001",
    "body": {
        "model": "ft:mistral-medium-latest:d42144c7:20250902:908db254",  # Fine-tuned model
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.1,
        "max_tokens": 2000
    }
}

print("CORRECTED BATCH REQUEST FORMAT:")
print("="*70)
print(json.dumps(batch_request, indent=2))
print("="*70)
print("\nKEY FIXES:")
print("1. Uses SOS assessment specialist context (not procurement analyst)")
print("2. NO system message (matches training data)")
print("3. NO request for INDETERMINATE")
print("4. Uses fine-tuned model (not agent)")