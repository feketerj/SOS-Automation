# Test Questions 1, 2, and 3 together in full scenarios
from filters.initial_checklist_v2 import InitialChecklistFilterV2, Decision

filter_logic = InitialChecklistFilterV2()

# Full scenario test cases
test_scenarios = [
    {
        'name': 'GO: Aviation, Open Competition, Gov Owns Data',
        'text': 'RFQ for C-130 aircraft spare parts. All responsible sources may submit quotes. Government owns technical data and will provide upon award.'
    },
    {
        'name': 'NO-GO: Tech Data Not Available',  
        'text': 'Request for F-16 engine components. Open competition. Technical drawings are not available for this procurement.'
    },
    {
        'name': 'NO-GO: OEM Proprietary Data',
        'text': 'Boeing 737 parts needed urgently. Competitive solicitation. Technical data is proprietary to the manufacturer and will not be provided.'
    },
    {
        'name': 'GO: Commercial Aviation with Standard Data',
        'text': 'Commercial aircraft component procurement for Boeing fleet. Standard commercial drawings available. All qualified suppliers welcome.'
    }
]

print('=== QUESTIONS 1-3 INTEGRATION TEST ===')
print('Testing Aviation (Q1) + Sole Source (Q2) + Tech Data (Q3)')
print()

for i, scenario in enumerate(test_scenarios, 1):
    # Create mock opportunity object
    mock_opp = {
        'title': scenario['name'],
        'description_text': scenario['text'],
        'full_analysis_text': scenario['text']
    }
    
    final_decision, detailed_results = filter_logic.assess_opportunity(mock_opp)
    
    print(f'{i}. {scenario["name"]}')
    print(f'   FINAL DECISION: {final_decision.value}')
    print(f'   Key Checks:')
    
    for result in detailed_results:
        if result.decision != Decision.PASS or 'Aviation' in result.reason:
            print(f'     - {result.check_name}: {result.decision.value} ({result.reason})')
    print()
