# Test Question 3: Technical Data Package (TDP) Binary Decision Logic
from filters.initial_checklist_v2 import InitialChecklistFilterV2, Decision

# Initialize filter
filter_logic = InitialChecklistFilterV2()

# Test cases for Question 3
test_cases = [
    {
        'name': 'BLOCKER: Drawings not available',
        'text': 'The government does not have technical drawings. Drawings are not available for this procurement.'
    },
    {
        'name': 'BLOCKER: OEM proprietary data',
        'text': 'Technical data is proprietary to the manufacturer. OEM owns technical data rights.'
    },
    {
        'name': 'GO: Government owns data',
        'text': 'Government owns technical data. Technical drawings will be provided upon contract award.'
    },
    {
        'name': 'GO: Commercially available',
        'text': 'Standard commercial drawings are available. Commercially available technical data package.'
    },
    {
        'name': 'PASS: No mention (standard)',
        'text': 'Requesting spare parts for aircraft maintenance. All qualified suppliers may submit proposals.'
    }
]

print('=== QUESTION 3: TECHNICAL DATA AVAILABILITY (Binary Decision) ===')
print('User Logic: Drawings either available (government/commercial) or OEM proprietary (OUT)')
print()

for i, case in enumerate(test_cases, 1):
    result = filter_logic.check_3_tech_data_availability(case['text'])
    print(f'{i}. {case["name"]}')
    print(f'   Decision: {result.decision.value}')
    print(f'   Reason: {result.reason}')
    print(f'   Quote: "{result.quote[:60]}..."')
    print()
