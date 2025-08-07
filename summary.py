import json
import os
from collections import Counter

# Count results by decision
decisions = []
go_opportunities = []

# Scan all JSON files in output directory
for filename in os.listdir('output'):
    if filename.endswith('.json'):
        try:
            with open(os.path.join('output', filename), 'r') as f:
                data = json.load(f)
                decision = data.get('final_decision', '')
                decisions.append(decision)
                if decision == 'GO':
                    go_opportunities.append(data)
        except:
            continue

# Print summary
counter = Counter(decisions)
print('=' * 60)
print('OFFICIAL SOS FILTER ASSESSMENT SUMMARY')
print('=' * 60)
print(f'Total Processed: {len(decisions)}')
print(f'GO Decisions: {counter.get("GO", 0)}')
print(f'NO-GO Decisions: {counter.get("NO-GO", 0)}')
print(f'NEEDS ANALYSIS: {counter.get("NEEDS ANALYSIS", 0)}')
print()
print('GO OPPORTUNITIES:')
print('-' * 30)
for i, opp in enumerate(go_opportunities, 1):
    print(f'{i:2d}. {opp.get("opportunity_title", "No title")[:60]}')
    print(f'    ID: {opp.get("opportunity_id", "No ID")}')
    phase_0 = opp.get('phase_0', {})
    platform = phase_0.get('platform_viability', 'Unknown')
    print(f'    Platform: {platform[:50]}')
    print()
