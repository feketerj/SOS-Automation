#!/usr/bin/env python3
"""Quick test with corrected prompt - just 3 opportunities"""

import json
from datetime import datetime
from mistralai import Mistral

# Sample opportunities (no INDETERMINATE expected)
opportunities = [
    {
        'title': 'BOLT, MACHINE',
        'agency': 'DLA Aviation',
        'naics': '336413',
        'psc': '5306',
        'text': 'NSN 5306002062865 BOLT, MACHINE. Full and open competition.'
    },
    {
        'title': 'F-16 FIGHTER JET PARTS',
        'agency': 'Air Force',
        'naics': '336413',
        'psc': '1560',
        'text': 'F-16 specific military components. No civilian equivalent.'
    },
    {
        'title': 'UH-60 BLACK HAWK PARTS',
        'agency': 'Army',
        'naics': '336413',
        'psc': '1615',
        'text': 'UH-60 Black Hawk parts. Has S-70 civilian variant. Surplus acceptable.'
    }
]

# Create batch file with CORRECTED prompt
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
jsonl_file = f"test_corrected_{timestamp}.jsonl"

with open(jsonl_file, 'w') as f:
    for i, opp in enumerate(opportunities):
        # CORRECTED PROMPT - NO INDETERMINATE
        prompt = f"""Context: You are an expert assessment specialist for Source One Spares (SOS), a small organic supplier specializing in surplus military and aviation parts.

Question: Analyze this government contracting opportunity for Source One Spares:

Title: {opp['title']}
Agency: {opp['agency']}
NAICS: {opp['naics']}
PSC: {opp['psc']}

Requirements excerpt: {opp['text']}"""

        batch_request = {
            "custom_id": f"test-{i:03d}",
            "body": {
                "model": "ft:mistral-medium-latest:d42144c7:20250902:908db254",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 500
            }
        }
        f.write(json.dumps(batch_request) + '\n')

print(f"Created {jsonl_file}")
print("\nExpected results:")
print("1. BOLT, MACHINE - Should be GO (open competition)")
print("2. F-16 PARTS - Should be NO-GO (military only)")
print("3. UH-60 PARTS - Should be GO (has civilian S-70)")
print("\nNO INDETERMINATE EXPECTED!")
print(f"\nTo submit: python BATCH_SUBMITTER_V2.py {jsonl_file}")