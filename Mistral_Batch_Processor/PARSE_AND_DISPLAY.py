#!/usr/bin/env python3
"""
Quick parser to display batch results
"""

import json
import csv
from datetime import datetime

# Load metadata
with open('batch_metadata_20250910_100512.json', 'r') as f:
    metadata = json.load(f)

# Load results
results = []
with open('batch_results_20250910_104225.jsonl', 'r') as f:
    for line in f:
        result = json.loads(line)
        
        # Extract response
        response_content = result['response']['body']['choices'][0]['message']['content']
        
        # Parse JSON from response
        try:
            # Handle responses that start with ```json
            if response_content.startswith('```json'):
                response_content = response_content.replace('```json', '').replace('```', '').strip()
            decision_data = json.loads(response_content)
        except:
            # Fallback
            decision_data = {
                'decision': 'PARSE_ERROR',
                'reasoning': response_content[:200],
                'confidence': 0
            }
        
        results.append({
            'custom_id': result['custom_id'],
            'decision': decision_data.get('decision', 'UNKNOWN'),
            'confidence': decision_data.get('confidence', 0),
            'reasoning': decision_data.get('reasoning', '')[:100]  # Truncate for display
        })

# Display summary
print("\n" + "=" * 80)
print("BATCH PROCESSING RESULTS SUMMARY")
print("=" * 80)

# Count decisions
go_count = sum(1 for r in results if r['decision'] == 'GO')
nogo_count = sum(1 for r in results if r['decision'] == 'NO-GO')
indeterminate_count = sum(1 for r in results if r['decision'] == 'INDETERMINATE')

print(f"\nTotal AI Assessments: {len(results)}")
regex_knockouts = metadata.get('total_regex_knockouts', 8)  # From test run we know it was 8
print(f"Regex Knockouts: {regex_knockouts}")
print(f"GRAND TOTAL: {len(results) + regex_knockouts}")
print(f"\nAI Assessment Breakdown:")
print(f"  GO: {go_count} ({go_count/len(results)*100:.1f}%)")
print(f"  NO-GO: {nogo_count} ({nogo_count/len(results)*100:.1f}%)")
print(f"  INDETERMINATE: {indeterminate_count} ({indeterminate_count/len(results)*100:.1f}%)")

# Show sample results
print("\nSample Results (first 10):")
print("-" * 80)
for i, r in enumerate(results[:10], 1):
    print(f"{i}. {r['decision']:15} (Conf: {r['confidence']:3}) - {r['reasoning'][:60]}...")

# Create simple CSV
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_file = f"batch_results_{timestamp}.csv"

with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['custom_id', 'decision', 'confidence', 'reasoning'])
    writer.writeheader()
    writer.writerows(results)

print(f"\n" + "=" * 80)
print(f"Results saved to: {csv_file}")
print(f"Processing from {len(metadata.get('search_ids', ['rFRK9PaP6ftzk1rokcKCT', 'u912_Lb64wa9wH2GuKXTu']))} search IDs")
print("=" * 80)