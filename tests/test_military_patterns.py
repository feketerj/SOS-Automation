#!/usr/bin/env python3
"""
Test script to verify military platform detection in regex patterns
"""

import re
from sos_ingestion_gate_v419 import IngestionGateV419, Decision

def test_military_platforms():
    """Test various military platform mentions"""
    
    # Initialize the gate
    gate = IngestionGateV419()
    
    # Test cases with expected results
    test_cases = [
        # KC Tankers (should be NO-GO)
        ("KC-135 Stratotanker parts needed", "KC-135", True),
        ("Parts for KC135 aircraft", "KC-135 variant", True),
        ("KC-10 Extender maintenance", "KC-10", True),
        ("KC10 fuel system components", "KC-10 variant", True),
        ("KC-46 Pegasus spare parts", "KC-46", True),
        ("KC46A tanker components", "KC-46 variant", True),
        
        # C-Series Transport (should be NO-GO)
        ("C-130 Hercules parts", "C-130", True),
        ("C130J Super Hercules", "C-130 variant", True),
        ("C-17 Globemaster III components", "C-17", True),
        ("C17 cargo system", "C-17 variant", True),
        ("C-5 Galaxy spare parts", "C-5", True),
        ("C5M Super Galaxy", "C-5 variant", True),
        
        # Fighters (should be NO-GO)
        ("F-16 Fighting Falcon parts", "F-16", True),
        ("F16 engine components", "F-16 variant", True),
        ("F-15 Eagle maintenance", "F-15", True),
        ("F15EX parts", "F-15 variant", True),
        ("F-22 Raptor systems", "F-22", True),
        ("F-35 Lightning II components", "F-35", True),
        
        # Bombers (should be NO-GO)
        ("B-52 Stratofortress parts", "B-52", True),
        ("B52H components", "B-52 variant", True),
        ("B-1 Lancer maintenance", "B-1", True),
        ("B-2 Spirit spare parts", "B-2", True),
        
        # Maritime Patrol (should be NO-GO)
        ("P-3 Orion parts", "P-3", True),
        ("P3C maintenance", "P-3 variant", True),
        ("P-8 Poseidon components", "P-8", True),
        ("P8A systems", "P-8 variant", True),
        
        # AWACS/Electronic (should be NO-GO)
        ("E-3 AWACS parts", "E-3", True),
        ("E3 Sentry components", "E-3 variant", True),
        ("E-2 Hawkeye maintenance", "E-2", True),
        ("E-8 JSTARS systems", "E-8", True),
        
        # Commercial aircraft (should be GO or needs further review)
        ("Boeing 737 parts", "Boeing 737", False),
        ("Boeing 747 components", "Boeing 747", False),
        ("Airbus A320 maintenance", "Airbus A320", False),
        ("Cessna Citation parts", "Cessna Citation", False),
        
        # Edge cases - military designations in commercial context
        ("DC-10 commercial parts", "DC-10 commercial", False),
        ("Boeing 707 tanker conversion", "707 tanker", True),  # Military conversion
    ]
    
    print("=" * 80)
    print("MILITARY PLATFORM DETECTION TEST")
    print("=" * 80)
    
    # Track patterns in hardcoded check (lines 470-492) - UPDATED patterns
    hardcoded_patterns = [
        r'(?i)\bF[-\s]?(?:15|16|18|22|35)[A-Z]{0,2}\b',  # F-15, F-16, F-22, F-35 (including F15EX)
        r'(?i)\bF[-\s]?(?:4|5|14|111|117)[A-Z]{0,2}\b',   # F-4, F-5, F-14, etc.
        r'(?i)\bB[-\s]?(?:1|2|52|21)[A-Z]{0,2}\b',        # B-1, B-2, B-52
        r'(?i)\bC[-\s]?(?:130|17|5|12|27|21)[A-Z]{0,2}\b', # C-130, C-17, C-5
        r'(?i)\bKC[-\s]?(?:135|10|46)[A-Z]{0,2}\b',       # KC-135, KC-10, KC-46
        r'(?i)\bP[-\s]?(?:3|8)[A-Z]{0,2}\b',              # P-3 Orion, P-8 Poseidon
        r'(?i)\bE[-\s]?(?:2|3|4|6|8)[A-Z]{0,2}\b',        # E-2, E-3 AWACS, E-4, E-6, E-8
        r'(?i)\bAH[-\s]?(?:1|64|6)[A-Z]?\b',              # AH-1, AH-64 Apache
        r'(?i)\bUH[-\s]?(?:1|60|72)[A-Z]?\b',             # UH-1, UH-60 Black Hawk
        r'(?i)\bCH[-\s]?(?:47|53)[A-Z]?\b',               # CH-47 Chinook, CH-53
        r'(?i)\bMH[-\s]?(?:60|53|47)[A-Z]?\b',            # MH-60, MH-53, MH-47
        r'(?i)\bV[-\s]?22\b'                              # V-22 Osprey
    ]
    
    print("\nHardcoded Pattern Check:")
    print("-" * 40)
    
    for text, description, should_block in test_cases:
        matched = False
        matched_pattern = None
        
        # Check against hardcoded patterns
        for pattern in hardcoded_patterns:
            if re.search(pattern, text):
                matched = True
                matched_pattern = pattern
                break
        
        status = "PASS" if matched == should_block else "FAIL"
        result = "BLOCKED" if matched else "PASSED"
        
        print(f"{status} {description:25} - {result:8} | Text: '{text[:40]}...'")
        if matched and matched_pattern:
            print(f"   Matched pattern: {matched_pattern}")
        if matched != should_block:
            print(f"   ERROR: Expected {'BLOCKED' if should_block else 'PASSED'}")
    
    print("\n" + "=" * 80)
    print("Full Gate Assessment Check:")
    print("-" * 40)
    
    # Now test with full gate assessment
    for text, description, should_block in test_cases:
        # Create a minimal opportunity dict
        opportunity = {
            'id': f"TEST-{description}",
            'title': text,
            'description': text,
            'combined_text': text
        }
        result = gate.assess_opportunity(opportunity)
        
        is_blocked = result.decision == Decision.NO_GO
        status = "PASS" if is_blocked == should_block else "FAIL"
        
        print(f"{status} {description:25} - {result.decision.value:20}")
        
        if is_blocked and result.categories_triggered:
            print(f"   Categories triggered: {result.categories_triggered}")
            if result.primary_blocker:
                print(f"   Primary blocker: {result.primary_blocker}")
        
        if is_blocked != should_block:
            print(f"   ERROR: Expected {'NO-GO' if should_block else 'GO/FURTHER_ANALYSIS'}")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("-" * 40)
    
    # Check specific patterns that might be missing
    missing_patterns = []
    
    # Test each specific aircraft type
    specific_tests = [
        ("KC-135", r'(?i)\bKC[-\s]?135'),
        ("KC-10", r'(?i)\bKC[-\s]?10\b'),
        ("KC-46", r'(?i)\bKC[-\s]?46'),
        ("C-130", r'(?i)\bC[-\s]?130'),
        ("C-17", r'(?i)\bC[-\s]?17\b'),
        ("C-5", r'(?i)\bC[-\s]?5\b'),
        ("P-3", r'(?i)\bP[-\s]?3\b'),
        ("P-8", r'(?i)\bP[-\s]?8\b'),
        ("E-3", r'(?i)\bE[-\s]?3\b'),
    ]
    
    for aircraft, pattern in specific_tests:
        found = False
        for hp in hardcoded_patterns:
            if re.search(hp, f"{aircraft} test"):
                found = True
                break
        
        if not found:
            missing_patterns.append(aircraft)
    
    if missing_patterns:
        print(f"Missing patterns for: {', '.join(missing_patterns)}")
    else:
        print("All critical military platforms have patterns")
    
    return missing_patterns

if __name__ == "__main__":
    missing = test_military_platforms()
    
    if missing:
        print("\n" + "=" * 80)
        print("RECOMMENDATION:")
        print("-" * 40)
        print("Update the hardcoded patterns in sos_ingestion_gate_v419.py")
        print("around lines 470-492 to include missing aircraft")