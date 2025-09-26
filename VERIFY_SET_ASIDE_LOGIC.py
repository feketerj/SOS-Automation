#!/usr/bin/env python3
"""Verify what set-asides are being checked"""

import re

# The patterns from _check_set_aside
ineligible_patterns = [
    (r'\b8\s*\(\s*a\s*\)', '8(a) minority-owned business'),
    (r'\b8a\b', '8(a) minority-owned business'),
    (r'\bwosb\b', 'women-owned small business'),
    (r'\bedwosb\b', 'economically disadvantaged women-owned'),
    (r'\bsdvosb\b', 'service-disabled veteran-owned'),
    (r'\bhubzone\b', 'HUBZone small business'),
    (r'\bvosb\b', 'veteran-owned small business')
]

# Test text that contains "TOTAL SMALL BUSINESS SET-ASIDE"
test_text = "NOTICE OF TOTAL SMALL BUSINESS SET-ASIDE (OCT 2020)(DEVIATION 2020-O0008)"

print("Testing set-aside patterns")
print("=" * 60)
print(f"Test text: {test_text}")
print()

# Check each pattern
print("Checking ineligible patterns:")
matched = False
for pattern, description in ineligible_patterns:
    if re.search(pattern, test_text, re.IGNORECASE):
        print(f"  MATCHED: {pattern} -> {description}")
        matched = True
    else:
        print(f"  No match: {pattern}")

if not matched:
    print("\nRESULT: No patterns matched!")
    print("This text would NOT be knocked out by the regex.")

print("\n" + "=" * 60)
print("ANALYSIS:")
print("The regex is only looking for SPECIFIC set-aside types:")
print("  - 8(a) minority-owned")
print("  - Women-owned (WOSB/EDWOSB)")
print("  - Veteran-owned (VOSB/SDVOSB)")
print("  - HUBZone")
print("")
print("It does NOT check for:")
print("  - Total Small Business Set-Aside")
print("  - Small Business Set-Aside")
print("  - 100% Small Business")
print("")
print("This appears to be BY DESIGN - SOS might be eligible for")
print("regular small business set-asides but not the special categories.")