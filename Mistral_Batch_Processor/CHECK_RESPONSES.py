#!/usr/bin/env python3
"""Check what model is actually returning"""

import json

# Check first 3 responses
with open('batch_results_20250910_104225.jsonl', 'r') as f:
    for i, line in enumerate(f):
        if i >= 3:
            break
        
        result = json.loads(line)
        custom_id = result['custom_id']
        response = result['response']['body']['choices'][0]['message']['content']
        
        print(f"\n{'='*60}")
        print(f"RESPONSE {i+1} - ID: {custom_id}")
        print("="*60)
        print("RAW MODEL OUTPUT:")
        print(response)
        
        # Try to parse it
        try:
            if response.startswith('```json'):
                response_clean = response.replace('```json', '').replace('```', '').strip()
            else:
                response_clean = response
            
            parsed = json.loads(response_clean)
            print("\nPARSED DATA:")
            print(f"  Decision: {parsed.get('decision', 'MISSING')}")
            print(f"  Confidence: {parsed.get('confidence', 'MISSING')}")
            print(f"  Reasoning: {parsed.get('reasoning', 'MISSING')[:100]}...")
        except Exception as e:
            print(f"\nPARSE ERROR: {e}")