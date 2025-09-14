#!/usr/bin/env python3
"""
Test generic military component terms blocking
"""

from sos_ingestion_gate_v419 import IngestionGateV419, Decision

def test_generic_military_terms():
    """Test that generic military component terms are properly blocked"""
    
    gate = IngestionGateV419()
    
    test_cases = [
        # LAUNCH/TUBE SYSTEMS - Should all be NO-GO
        ("Rocket tubes for missile system", "Rocket tubes", False),
        ("Launch tubes assembly", "Launch tubes", False),
        ("Launcher tube components", "Launcher tube", False),
        ("Missile tubes maintenance", "Missile tubes", False),
        ("Torpedo tubes for submarine", "Torpedo tubes", False),
        
        # RACK/MOUNT SYSTEMS - Should all be NO-GO
        ("Bomb rack assembly", "Bomb rack", False),
        ("Missile racks for aircraft", "Missile racks", False),
        ("Weapon rack components", "Weapon rack", False),
        ("Weapons racks installation", "Weapons racks", False),
        ("Pylon assembly for fighter", "Pylon assembly", False),
        ("Pylon adapter kit", "Pylon adapter", False),
        ("Hardpoints for external stores", "Hardpoints", False),
        ("Munitions dispenser system", "Munitions dispenser", False),
        ("Ejector rack mechanism", "Ejector rack", False),
        
        # EXPLOSIVE COMPONENTS - Should all be NO-GO
        ("Warhead assembly", "Warhead", False),
        ("Warheads for missiles", "Warheads", False),
        ("Explosive device components", "Explosive device", False),
        ("Detonator assembly", "Detonator", False),
        ("Detonators for ordnance", "Detonators", False),
        ("Rocket igniter components", "Rocket igniter", False),
        ("Fuze assembly mechanism", "Fuze assembly", False),
        ("Arming mechanism parts", "Arming mechanism", False),
        ("Arming wire assembly", "Arming wire", False),
        
        # PROPULSION COMPONENTS - Should all be NO-GO
        ("Propellant grain assembly", "Propellant grain", False),
        ("Propellant charge components", "Propellant charge", False),
        ("Booster motor assembly", "Booster motor", False),
        ("Booster charge ignition", "Booster charge", False),
        ("Sustainer motor parts", "Sustainer motor", False),
        
        # GUIDANCE/CONTROL - Should all be NO-GO
        ("Guidance section assembly", "Guidance section", False),
        ("Guidance unit components", "Guidance unit", False),
        ("Seeker head assembly", "Seeker head", False),
        ("Seeker assembly parts", "Seeker assembly", False),
        ("Control surfaces for missile", "Control surfaces", False),
        ("Control fins mechanism", "Control fins", False),
        ("Canard assembly", "Canards", False),
        
        # GUN/ARTILLERY COMPONENTS - Should all be NO-GO
        ("Breech block mechanism", "Breech block", False),
        ("Breech mechanism parts", "Breech mechanism", False),
        ("Barrel assembly components", "Barrel assembly", False),
        ("Recoil mechanism buffer", "Recoil mechanism", False),
        ("Recoil buffer system", "Recoil buffer", False),
        ("Traverse mechanism motor", "Traverse mechanism", False),
        ("Elevation mechanism parts", "Elevation mechanism", False),
        ("Ammunition feed system", "Ammunition feed", False),
        ("Shell casing ejector", "Shell casing", False),
        ("Cartridge cases for ammo", "Cartridge cases", False),
        ("Powder charge assembly", "Powder charge", False),
        
        # FIRE CONTROL/TARGETING - Should all be NO-GO
        ("Ballistic computer system", "Ballistic computer", False),
        ("Ballistics calculator unit", "Ballistics calculator", False),
        ("Fire director system", "Fire director", False),
        ("Fire control computer", "Fire control", False),
        ("Laser designator assembly", "Laser designator", False),
        ("Laser rangefinder unit", "Laser rangefinder", False),
        ("Thermal sight assembly", "Thermal sight", False),
        ("Thermal imager system", "Thermal imager", False),
        ("Night vision scope", "Night vision scope", False),
        ("Night vision device", "Night vision device", False),
        
        # COUNTERMEASURES - Should all be NO-GO
        ("IFF system components", "IFF system", False),
        ("IFF transponder unit", "IFF transponder", False),
        ("Chaff dispenser cartridge", "Chaff dispenser", False),
        ("Chaff cartridge assembly", "Chaff cartridge", False),
        ("Flare dispenser system", "Flare dispenser", False),
        ("Flare cartridge mechanism", "Flare cartridge", False),
        ("Decoy launcher assembly", "Decoy launcher", False),
        ("Decoys dispenser system", "Decoys dispenser", False),
        ("Smoke grenade launcher", "Smoke grenade", False),
        ("Smoke dispenser unit", "Smoke dispenser", False),
        
        # WITH AMSC OVERRIDE - Should PASS
        ("Rocket tubes with AMSC Z", "Rocket tubes + AMSC Z", True),
        ("Warhead assembly AMSC Code G", "Warhead + AMSC G", True),
        ("Laser designator AMSC A", "Laser designator + AMSC A", True),
        
        # FALSE POSITIVES TO AVOID - Should PASS
        ("Commercial tube fittings", "Commercial tubes", True),
        ("Rack mount server equipment", "Server rack", True),
        ("Industrial igniter for furnace", "Industrial igniter", True),
        ("Commercial thermal camera", "Commercial thermal", True),
        ("Smoke detector system", "Smoke detector", True),
    ]
    
    print("=" * 80)
    print("GENERIC MILITARY COMPONENT TERMS TEST")
    print("=" * 80)
    
    passed = 0
    failed = 0
    categories = [
        ("LAUNCH/TUBE SYSTEMS", 0, 5),
        ("RACK/MOUNT SYSTEMS", 5, 14),
        ("EXPLOSIVE COMPONENTS", 14, 23),
        ("PROPULSION COMPONENTS", 23, 28),
        ("GUIDANCE/CONTROL", 28, 35),
        ("GUN/ARTILLERY COMPONENTS", 35, 46),
        ("FIRE CONTROL/TARGETING", 46, 56),
        ("COUNTERMEASURES", 56, 66),
        ("AMSC OVERRIDES", 66, 69),
        ("FALSE POSITIVES TO AVOID", 69, len(test_cases))
    ]
    
    for category_name, start, end in categories:
        print(f"\n{category_name}:")
        print("-" * 40)
        
        for text, description, should_pass in test_cases[start:end]:
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
            
            print(f"{status:4} {description:30} -> {result.decision.value}")
            if status == "FAIL":
                if result.primary_blocker:
                    print(f"     ERROR: {result.primary_blocker}")
                elif should_pass and not is_go:
                    print(f"     ERROR: Should have passed but was blocked")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("-" * 40)
    print(f"Passed: {passed}/{len(test_cases)}")
    print(f"Failed: {failed}/{len(test_cases)}")
    
    if failed == 0:
        print("\nSUCCESS: All generic military component terms properly handled!")
    else:
        print(f"\nFAILURE: {failed} tests failed")
    
    return failed == 0

if __name__ == "__main__":
    test_generic_military_terms()