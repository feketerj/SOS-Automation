#!/usr/bin/env python3
"""Debug what patterns are actually loaded in the regex engine"""

from sos_ingestion_gate_v419 import IngestionGateV419

# Initialize the gate
gate = IngestionGateV419()

print("Loaded Patterns in Regex Engine")
print("=" * 60)

# Check what pattern families are loaded
print("\nPattern families in compiled_patterns:")
for family_name in sorted(gate.compiled_patterns.keys()):
    patterns = gate.compiled_patterns[family_name]
    print(f"  {family_name}: {len(patterns)} patterns")

# Check specific patterns we expect
print("\n" + "=" * 60)
print("Checking for expected knockout patterns:")

expected = {
    'sole_source_patterns': ['sole source', 'only known source'],
    'approved_source_only_patterns': ['approved source', 'OEM only'],
    'tdp_negative_patterns': ['TDP not available', 'drawings not available'],
}

for family, keywords in expected.items():
    if family in gate.compiled_patterns:
        print(f"\n{family}: FOUND")
        # Show first few patterns
        for i, pattern in enumerate(gate.compiled_patterns[family][:3]):
            print(f"  Pattern {i+1}: {pattern.pattern[:60]}...")
    else:
        print(f"\n{family}: NOT FOUND in compiled patterns!")

# Check the category mapping
print("\n" + "=" * 60)
print("Pattern to Category Mapping:")
for pattern_name, category_id in gate.categories.PATTERN_TO_CATEGORY.items():
    exists = pattern_name in gate.compiled_patterns
    status = "EXISTS" if exists else "MISSING"
    print(f"  {pattern_name} -> Category {category_id} [{status}]")