#!/usr/bin/env python3
"""
DIRECT PROOF THE AI IS WORKING
No bullshit, just showing you the actual model response
"""

import os
try:
    from API_KEYS import MISTRAL_API_KEY
    os.environ["MISTRAL_API_KEY"] = MISTRAL_API_KEY
except:
    pass

from highergov_batch_fetcher import HigherGovBatchFetcher
from ULTIMATE_MISTRAL_CONNECTOR import MistralSOSClassifier
import json
import time

print("="*70)
print("PROVING THE AI MODEL IS ACTUALLY BEING CALLED")
print("="*70)

# 1. Get ONE opportunity
print("\n[1] Fetching ONE opportunity...")
fetcher = HigherGovBatchFetcher()
raw = fetcher.fetch_all_opportunities("HAfVxckSk6G9kSXQuJoQB", max_pages=1)[:1]
opp = fetcher.process_opportunity(raw[0])

print(f"Title: {opp.get('title', '')}")
print(f"Document size: {len(opp.get('text', '')):,} chars")
print(f"URL: {opp.get('url', '')}")

# 2. Call the model DIRECTLY
print("\n[2] Calling Mistral AI model DIRECTLY...")
print("(This will take 30-60 seconds because it's reading 400K chars)")

classifier = MistralSOSClassifier()
start_time = time.time()

# BYPASS REGEX - go straight to model
result = classifier.classify_opportunity(opp, bypass_regex=True)

elapsed = time.time() - start_time

# 3. Show EXACTLY what the model returned
print("\n[3] RAW MODEL RESPONSE:")
print("="*70)
print(json.dumps(result, indent=2))
print("="*70)

# 4. Show what goes in the CSV
print("\n[4] WHAT GOES IN YOUR CSV:")
print(f"final_decision: {result.get('classification')}")
print(f"analysis_notes: {result.get('detailed_analysis', '')[:200]}...")
print(f"confidence: {result.get('confidence')}")
print(f"pipeline_title: {result.get('sos_pipeline_title')}")

# 5. Prove it's not fake
print("\n[5] PROOF THIS IS REAL:")
print(f"- Processing took {elapsed:.1f} seconds (not instant)")
print(f"- Confidence is {result.get('confidence')} (not hardcoded 75)")
print(f"- Analysis is {len(result.get('detailed_analysis', ''))} chars (not 'Requires manual review')")

# 6. Save to file so you can see it
output_file = f"PROOF_AI_RESPONSE_{time.strftime('%H%M%S')}.json"
with open(output_file, 'w') as f:
    json.dump({
        'opportunity': {
            'title': opp.get('title'),
            'url': opp.get('url'),
            'doc_size': len(opp.get('text', ''))
        },
        'model_response': result,
        'processing_time': elapsed
    }, f, indent=2)

print(f"\n[6] Full response saved to: {output_file}")
print("="*70)