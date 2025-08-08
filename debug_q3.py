# Debug Question 3 pattern matching
from filters.initial_checklist_v2 import InitialChecklistFilterV2
import re

filter_logic = InitialChecklistFilterV2()

# Test the problematic case
test_text = 'The government does not have technical drawings. Drawings are not available for this procurement.'

print("Debug TDP Pattern Matching:")
print(f"Test text: {test_text}")
print()

# Check if the regex finds a match
match = filter_logic.tech_data_regex.search(test_text)
print(f"Regex match found: {match is not None}")
if match:
    print(f"Match text: '{match.group()}'")
    print(f"Match position: {match.start()}-{match.end()}")

print()
print("Testing individual patterns:")
test_patterns = [
    'drawings not available',
    'technical data not available',
    'government does not have'
]

for pattern in test_patterns:
    if pattern in test_text.lower():
        print(f"✓ Found: '{pattern}'")
    else:
        print(f"✗ Missing: '{pattern}'")
