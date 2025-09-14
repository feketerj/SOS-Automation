#!/usr/bin/env python3
"""
Test weapons systems, electronic warfare, and rocket systems blocking
"""

from sos_ingestion_gate_v419 import IngestionGateV419, Decision

def test_weapons_ew_systems():
    """Test that weapons, EW, and rocket systems are properly blocked"""
    
    gate = IngestionGateV419()
    
    test_cases = [
        # WEAPONS SYSTEMS - Should all be NO-GO
        ("Weapon system components", "Weapon system", False),
        ("Fire control system upgrade", "Fire control", False),
        ("Targeting system maintenance", "Targeting system", False),
        ("Ordnance system parts", "Ordnance system", False),
        ("Missile system components", "Missile system", False),
        ("Torpedo system maintenance", "Torpedo system", False),
        ("Bombing system upgrade", "Bombing system", False),
        ("Gunnery system parts", "Gunnery system", False),
        
        # ELECTRONIC WARFARE - Should all be NO-GO
        ("Electronic warfare system", "EW system", False),
        ("EW system components", "EW abbreviation", False),
        ("Jamming system upgrade", "Jamming", False),
        ("Countermeasure system parts", "Countermeasures", False),
        ("Radar warning receiver", "RWR full", False),
        ("RWR components", "RWR abbreviation", False),
        ("ECM pod maintenance", "ECM", False),
        ("ESM system upgrade", "ESM", False),
        ("SIGINT equipment", "SIGINT", False),
        ("ELINT systems", "ELINT", False),
        ("EA-6B Prowler parts", "EA-6B", False),
        ("EA-18G Growler components", "EA-18G", False),
        ("RC-135 reconnaissance", "RC-135", False),
        ("EP-3 ARIES systems", "EP-3", False),
        
        # ROCKET/MISSILE SYSTEMS - Should all be NO-GO
        ("Rocket system components", "Rocket system", False),
        ("MLRS parts", "MLRS", False),
        ("HIMARS maintenance", "HIMARS", False),
        ("Patriot missile system", "Patriot", False),
        ("THAAD components", "THAAD", False),
        ("Aegis combat system", "Aegis", False),
        ("SM-2 missile parts", "SM-2", False),
        ("SM-3 missile components", "SM-3", False),
        ("AIM-120 AMRAAM", "AIM-120", False),
        ("AIM-9 Sidewinder", "AIM-9", False),
        ("AGM-65 Maverick", "AGM-65", False),
        ("AGM-88 HARM", "AGM-88", False),
        ("Tomahawk missile", "Tomahawk", False),
        ("Hellfire missile parts", "Hellfire", False),
        ("JDAM kit components", "JDAM", False),
        ("GBU-31 guided bomb", "GBU-31", False),
        ("Mk 48 torpedo parts", "Mk torpedo", False),
        
        # WITH AMSC OVERRIDE - Should PASS
        ("Weapon system with AMSC Z", "Weapon + AMSC Z", True),
        ("Electronic warfare AMSC Code G", "EW + AMSC G", True),
        ("Missile system AMSC A", "Missile + AMSC A", True),
        ("HIMARS parts AMC 1", "HIMARS + AMC 1", True),
        
        # CIVILIAN SYSTEMS - Should PASS
        ("Commercial radar system", "Commercial radar", True),
        ("Weather radar components", "Weather radar", True),
        ("Air traffic control system", "ATC system", True),
        ("Boeing 737 parts", "Boeing 737", True),
    ]
    
    print("=" * 80)
    print("WEAPONS/EW/ROCKET SYSTEMS TEST")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    print("\nWEAPONS SYSTEMS:")
    print("-" * 40)
    for text, description, should_pass in test_cases[:8]:
        opportunity = {
            'id': f"TEST-{description}",
            'title': text,
            'description': text,
            'combined_text': text
        }
        result = gate.assess_opportunity(opportunity)
        is_go = result.decision in [Decision.GO, Decision.FURTHER_ANALYSIS]
        
        if is_go == should_pass:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"
            failed += 1
        
        print(f"{status:4} {description:20} -> {result.decision.value}")
        if status == "FAIL" and result.primary_blocker:
            print(f"     ERROR: {result.primary_blocker}")
    
    print("\nELECTRONIC WARFARE SYSTEMS:")
    print("-" * 40)
    for text, description, should_pass in test_cases[8:22]:
        opportunity = {
            'id': f"TEST-{description}",
            'title': text,
            'description': text,
            'combined_text': text
        }
        result = gate.assess_opportunity(opportunity)
        is_go = result.decision in [Decision.GO, Decision.FURTHER_ANALYSIS]
        
        if is_go == should_pass:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"
            failed += 1
        
        print(f"{status:4} {description:20} -> {result.decision.value}")
        if status == "FAIL" and result.primary_blocker:
            print(f"     ERROR: {result.primary_blocker}")
    
    print("\nROCKET/MISSILE SYSTEMS:")
    print("-" * 40)
    for text, description, should_pass in test_cases[22:40]:
        opportunity = {
            'id': f"TEST-{description}",
            'title': text,
            'description': text,
            'combined_text': text
        }
        result = gate.assess_opportunity(opportunity)
        is_go = result.decision in [Decision.GO, Decision.FURTHER_ANALYSIS]
        
        if is_go == should_pass:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"
            failed += 1
        
        print(f"{status:4} {description:20} -> {result.decision.value}")
        if status == "FAIL" and result.primary_blocker:
            print(f"     ERROR: {result.primary_blocker}")
    
    print("\nAMSC OVERRIDES:")
    print("-" * 40)
    for text, description, should_pass in test_cases[40:44]:
        opportunity = {
            'id': f"TEST-{description}",
            'title': text,
            'description': text,
            'combined_text': text
        }
        result = gate.assess_opportunity(opportunity)
        is_go = result.decision in [Decision.GO, Decision.FURTHER_ANALYSIS]
        
        if is_go == should_pass:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"
            failed += 1
        
        print(f"{status:4} {description:20} -> {result.decision.value}")
        if status == "FAIL" and result.primary_blocker:
            print(f"     ERROR: {result.primary_blocker}")
    
    print("\nCIVILIAN SYSTEMS (Should Pass):")
    print("-" * 40)
    for text, description, should_pass in test_cases[44:]:
        opportunity = {
            'id': f"TEST-{description}",
            'title': text,
            'description': text,
            'combined_text': text
        }
        result = gate.assess_opportunity(opportunity)
        is_go = result.decision in [Decision.GO, Decision.FURTHER_ANALYSIS]
        
        if is_go == should_pass:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"
            failed += 1
        
        print(f"{status:4} {description:20} -> {result.decision.value}")
        if status == "FAIL" and result.primary_blocker:
            print(f"     ERROR: {result.primary_blocker}")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("-" * 40)
    print(f"Passed: {passed}/{len(test_cases)}")
    print(f"Failed: {failed}/{len(test_cases)}")
    
    if failed == 0:
        print("\nSUCCESS: All weapons/EW/rocket systems properly blocked!")
    else:
        print(f"\nFAILURE: {failed} tests failed")
    
    return failed == 0

if __name__ == "__main__":
    test_weapons_ew_systems()