#!/usr/bin/env python3
"""
Test AMSC overrides and civilian platform detection
"""

from sos_ingestion_gate_v419 import IngestionGateV419, Decision

def test_amsc_and_civilian():
    """Test AMSC Z/G overrides and civilian platform equivalents"""
    
    gate = IngestionGateV419()
    
    test_cases = [
        # AMSC Z/G OVERRIDES - Should all PASS
        ("C-130 parts with AMSC Code Z", "C-130 + AMSC Z", True),
        ("F-16 components AMSC G", "F-16 + AMSC G", True),
        ("B-52 maintenance AMSC Code Z", "B-52 + AMSC Z", True),
        ("KC-135 parts AMSC Z", "KC-135 + AMSC Z", True),
        ("C-5 Galaxy AMSC Code G", "C-5 + AMSC G", True),
        ("P-3 Orion AMSC A", "P-3 + AMSC A", True),
        ("AMC 1 applies to these parts", "AMC 1", True),
        ("AMC 2 commercial equivalent", "AMC 2", True),
        
        # CIVILIAN-BASED PLATFORMS - Should PASS
        ("C-12 King Air parts", "C-12 (King Air)", True),
        ("UC-12 Huron components", "UC-12 (King Air)", True),
        ("C-20 Gulfstream parts", "C-20 (Gulfstream)", True),
        ("C-21 Learjet maintenance", "C-21 (Learjet)", True),
        ("C-26 Metro parts", "C-26 (Metro/Merlin)", True),
        ("C-32 Boeing 757", "C-32 (757)", True),
        ("C-37 Gulfstream V", "C-37 (G550)", True),
        ("C-40 Boeing 737 BBJ", "C-40 (737 BBJ)", True),
        ("UC-35 Citation parts", "UC-35 (Citation)", True),
        ("T-6 Texan II trainer", "T-6 (PC-9 based)", True),
        ("T-34 Mentor parts", "T-34 (Bonanza based)", True),
        ("T-44 King Air trainer", "T-44 (King Air 90)", True),
        ("UH-72 Lakota parts", "UH-72 (EC145)", True),
        ("UH-60 Black Hawk", "UH-60 (S-70)", True),
        ("MH-65 Dolphin parts", "MH-65 (AS365)", True),
        
        # PURE MILITARY WITHOUT AMSC - Should NOT PASS
        ("F-16 Fighting Falcon", "F-16 alone", False),
        ("C-130 Hercules parts", "C-130 alone", False),
        ("B-52 Stratofortress", "B-52 alone", False),
        ("C-5 Galaxy maintenance", "C-5 alone", False),
        ("C-17 Globemaster III", "C-17 alone", False),
        ("AH-64 Apache parts", "AH-64 alone", False),
        ("V-22 Osprey components", "V-22 alone", False),
        
        # EDGE CASES WITH L-100 (Civilian C-130) - Should PASS
        ("L-100 civilian Hercules", "L-100", True),
        ("L-382 commercial variant", "L-382", True),
        
        # KC TANKERS - Mixed based on civilian base
        ("KC-46 Pegasus parts", "KC-46 (767 based)", False),  # Currently blocks
        ("KC-10 Extender", "KC-10 (DC-10 based)", False),  # Currently blocks
        ("KC-135 Stratotanker", "KC-135 (707 based)", False),  # Currently blocks
        
        # P-8 and E-7 (737 based) 
        ("P-8 Poseidon parts", "P-8 (737 based)", False),  # Currently blocks
        ("E-7 Wedgetail components", "E-7 (737 based)", True),  # May pass
    ]
    
    print("=" * 80)
    print("AMSC OVERRIDE AND CIVILIAN PLATFORM TEST")
    print("=" * 80)
    print("\nAMSC Z/G/A OVERRIDES:")
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
        status = "PASS" if is_go == should_pass else "FAIL"
        
        print(f"{status:4} {description:25} -> {result.decision.value}")
        if status == "FAIL":
            if result.primary_blocker:
                print(f"     ERROR: {result.primary_blocker}")
    
    print("\nCIVILIAN-BASED MILITARY DESIGNATIONS:")
    print("-" * 40)
    
    for text, description, should_pass in test_cases[8:23]:
        opportunity = {
            'id': f"TEST-{description}",
            'title': text,
            'description': text,
            'combined_text': text
        }
        result = gate.assess_opportunity(opportunity)
        is_go = result.decision in [Decision.GO, Decision.FURTHER_ANALYSIS]
        status = "PASS" if is_go == should_pass else "FAIL"
        
        print(f"{status:4} {description:25} -> {result.decision.value}")
        if status == "FAIL":
            if result.primary_blocker:
                print(f"     ERROR: {result.primary_blocker}")
    
    print("\nPURE MILITARY WITHOUT OVERRIDE:")
    print("-" * 40)
    
    for text, description, should_pass in test_cases[23:30]:
        opportunity = {
            'id': f"TEST-{description}",
            'title': text,
            'description': text,
            'combined_text': text
        }
        result = gate.assess_opportunity(opportunity)
        is_go = result.decision in [Decision.GO, Decision.FURTHER_ANALYSIS]
        status = "PASS" if is_go == should_pass else "FAIL"
        
        print(f"{status:4} {description:25} -> {result.decision.value}")
        if status == "FAIL":
            if result.primary_blocker:
                print(f"     ERROR: {result.primary_blocker}")
    
    print("\nEDGE CASES:")
    print("-" * 40)
    
    for text, description, should_pass in test_cases[30:]:
        opportunity = {
            'id': f"TEST-{description}",
            'title': text,
            'description': text,
            'combined_text': text
        }
        result = gate.assess_opportunity(opportunity)
        is_go = result.decision in [Decision.GO, Decision.FURTHER_ANALYSIS]
        status = "INFO"
        
        print(f"{status:4} {description:25} -> {result.decision.value}")
        if result.decision == Decision.NO_GO and result.primary_blocker:
            print(f"     {result.primary_blocker}")

if __name__ == "__main__":
    test_amsc_and_civilian()