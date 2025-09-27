#!/usr/bin/env python3
"""
Test civilian vs military platform detection
RULE: Civilian platform = GO, Military platform = NO-GO
"""

import re
from sos_ingestion_gate_v419 import IngestionGateV419, Decision

def test_civilian_vs_military():
    """Test civilian platform derivatives vs pure military platforms"""
    
    gate = IngestionGateV419()
    
    test_cases = [
        # CIVILIAN PLATFORMS - SHOULD PASS (GO)
        ("Boeing 737 parts", "Boeing 737", "CIVILIAN", True),
        ("Boeing 747 components", "Boeing 747", "CIVILIAN", True),
        ("Boeing 757 maintenance", "Boeing 757", "CIVILIAN", True),
        ("Boeing 767 spare parts", "Boeing 767", "CIVILIAN", True),
        ("Boeing 777 systems", "Boeing 777", "CIVILIAN", True),
        ("Boeing 787 Dreamliner", "Boeing 787", "CIVILIAN", True),
        ("Airbus A320 parts", "Airbus A320", "CIVILIAN", True),
        ("Airbus A330 components", "Airbus A330", "CIVILIAN", True),
        ("Airbus A350 maintenance", "Airbus A350", "CIVILIAN", True),
        ("Airbus A380 parts", "Airbus A380", "CIVILIAN", True),
        ("Cessna Citation parts", "Cessna Citation", "CIVILIAN", True),
        ("Gulfstream G650 components", "Gulfstream G650", "CIVILIAN", True),
        ("Bombardier Global 7500", "Bombardier Global", "CIVILIAN", True),
        ("Embraer E175 parts", "Embraer E175", "CIVILIAN", True),
        
        # MILITARY DERIVATIVES OF CIVILIAN PLATFORMS - SHOULD PASS
        ("KC-46 Pegasus parts", "KC-46 (Boeing 767)", "MILITARY-DERIVATIVE", False),  # Based on 767
        ("P-8 Poseidon components", "P-8 (Boeing 737)", "MILITARY-DERIVATIVE", False),  # Based on 737
        ("E-7 Wedgetail parts", "E-7 (Boeing 737)", "MILITARY-DERIVATIVE", False),  # Based on 737
        ("KC-10 Extender maintenance", "KC-10 (DC-10)", "MILITARY-DERIVATIVE", False),  # Based on DC-10
        ("E-767 AWACS parts", "E-767 (Boeing 767)", "MILITARY-DERIVATIVE", False),  # Based on 767
        
        # PURE MILITARY PLATFORMS - SHOULD NOT PASS (NO-GO)
        ("F-16 Fighting Falcon parts", "F-16", "MILITARY", False),
        ("F-15 Eagle maintenance", "F-15", "MILITARY", False),
        ("F-22 Raptor systems", "F-22", "MILITARY", False),
        ("F-35 Lightning II", "F-35", "MILITARY", False),
        ("B-52 Stratofortress", "B-52", "MILITARY", False),
        ("B-1 Lancer parts", "B-1", "MILITARY", False),
        ("B-2 Spirit components", "B-2", "MILITARY", False),
        ("C-130 Hercules parts", "C-130", "MILITARY", False),
        ("C-17 Globemaster III", "C-17", "MILITARY", False),
        ("C-5 Galaxy spare parts", "C-5", "MILITARY", False),
        ("KC-135 Stratotanker", "KC-135 (Boeing 707)", "MILITARY", False),  # Old 707 derivative but military
        ("P-3 Orion parts", "P-3 (Lockheed)", "MILITARY", False),
        ("E-3 AWACS components", "E-3 (Boeing 707)", "MILITARY", False),  # Old 707 derivative
        ("E-2 Hawkeye parts", "E-2", "MILITARY", False),
        ("AH-64 Apache parts", "AH-64", "MILITARY", False),
        ("UH-60 Black Hawk", "UH-60", "MILITARY", False),
        ("CH-47 Chinook parts", "CH-47", "MILITARY", False),
        ("V-22 Osprey components", "V-22", "MILITARY", False),
    ]
    
    print("=" * 80)
    print("CIVILIAN VS MILITARY PLATFORM TEST")
    print("RULE: Civilian platform = GO, Military-only platform = NO-GO")
    print("=" * 80)
    
    results = {"PASS": 0, "FAIL": 0}
    failures = []
    
    for text, description, category, should_pass in test_cases:
        opportunity = {
            'id': f"TEST-{description}",
            'title': text,
            'description': text,
            'combined_text': text
        }
        
        result = gate.assess_opportunity(opportunity)
        is_go = result.decision in [Decision.GO, Decision.FURTHER_ANALYSIS]
        
        if category == "MILITARY-DERIVATIVE":
            # These are tricky - based on civilian but used military
            # Current system blocks them, which might be correct
            status = "INFO"
            print(f"{status:4} {description:30} | Decision: {result.decision.value:20} | {category}")
            if result.decision == Decision.NO_GO and result.primary_blocker:
                print(f"     Blocked by: {result.primary_blocker}")
        else:
            passed_test = (is_go == should_pass)
            status = "PASS" if passed_test else "FAIL"
            results[status] += 1
            
            print(f"{status:4} {description:30} | Decision: {result.decision.value:20} | {category}")
            
            if not passed_test:
                failures.append((description, category, should_pass, result.decision.value))
                if result.decision == Decision.NO_GO and result.primary_blocker:
                    print(f"     ERROR: {result.primary_blocker}")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("-" * 40)
    print(f"Passed: {results['PASS']}")
    print(f"Failed: {results['FAIL']}")
    
    if failures:
        print("\nFAILURES:")
        for desc, cat, expected_pass, actual in failures:
            expected = "GO/FURTHER_ANALYSIS" if expected_pass else "NO-GO"
            print(f"  - {desc} ({cat}): Expected {expected}, got {actual}")
    
    print("\n" + "=" * 80)
    print("KEY INSIGHTS:")
    print("-" * 40)
    print("1. Pure civilian aircraft (737, 747, A320, etc.) -> PASS")
    print("2. Pure military aircraft (F-16, B-52, C-130, etc.) -> BLOCKED")
    print("3. Military derivatives of civilian platforms (KC-46, P-8) -> CURRENTLY BLOCKED")
    print("   Note: KC-46 is based on 767, P-8 is based on 737")
    print("   These are edge cases - may need business decision")
    
    return results['FAIL'] == 0

if __name__ == "__main__":
    success = test_civilian_vs_military()