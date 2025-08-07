#!/usr/bin/env python3
"""
Analysis script to identify potential logic strengthening opportunities
"""

from filters.initial_checklist_v2 import InitialChecklistFilterV2, Decision

def analyze_current_filter():
    """Analyze current filter capabilities against SOS documentation"""
    
    filter_obj = InitialChecklistFilterV2()
    
    print("=== CURRENT FILTER ANALYSIS ===")
    print()
    
    # Check SAR patterns coverage
    print("SAR Detection Patterns:")
    sar_pattern = filter_obj.sar_regex.pattern
    print(f"- Pattern complexity: {len(sar_pattern)} characters")
    print(f"- Includes AMC codes: {'AMC' in sar_pattern}")
    print(f"- Includes AMSC codes: {'AMSC' in sar_pattern}")
    print(f"- Includes QPL/QML: {'QPL' in sar_pattern and 'QML' in sar_pattern}")
    print()
    
    # Platform coverage
    print("Platform Coverage:")
    print(f"- Pure military platforms: {len(filter_obj.platform_guide['pure_military'])}")
    print(f"- Civilian equivalent platforms: {len(filter_obj.platform_guide['civilian_equivalent'])}")
    print()
    
    print("=== TESTING POTENTIAL GAPS ===")
    print()
    
    # Test cases based on SOS documentation that might not be covered
    test_cases = [
        # AMSC codes from the bid matrix that might not be covered
        ("AMSC H detection", "This item has AMSC H requirements"),
        ("AMSC T detection", "QPL required with AMSC T designation"),
        ("AMSC G detection", "Item classified as AMSC G"),
        
        # Additional SAR indicators from documentation
        ("First article testing", "First article test and approval required"),
        ("Design control activity", "Approval by design control activity required"),
        ("Manufacturing source approval", "Manufacturing source approval by government required"),
        
        # Critical safety/flight critical items
        ("Critical safety item", "This is a critical safety item requiring special handling"),
        ("Flight critical component", "Flight critical component requiring certification"),
        ("Life limited part", "Life limited part requiring tracking and certification"),
        
        # Technical data nuances
        ("Drawing authentication", "Authenticated drawings required from design authority"),
        ("Government furnished data", "No government furnished data available"),
        ("Proprietary technical data", "Technical data is proprietary to OEM"),
        
        # Certification edge cases
        ("FAR 145 repair station", "FAR 145 repair station certification required"),
        ("PMA approval", "PMA (Parts Manufacturer Approval) required"),
        ("STC requirement", "STC (Supplemental Type Certificate) required"),
        
        # Export control specifics
        ("ITAR registration", "ITAR registration and compliance required"),
        ("Export license specific", "Specific export license required for this item"),
        ("ECCN classification", "Export controlled under ECCN classification"),
        
        # OEM authorization nuances
        ("Factory authorization letter", "Factory authorization letter required"),
        ("OEM supply chain", "Must be sourced through OEM authorized supply chain"),
        ("Direct OEM purchase", "Direct purchase from OEM required only"),
    ]
    
    for description, test_text in test_cases:
        # Test against all major filter methods
        sar_match = filter_obj.sar_regex.search(test_text)
        tech_data_match = filter_obj.tech_data_regex.search(test_text)
        cert_match = filter_obj.prohibited_certs_regex.search(test_text)
        oem_match = filter_obj.oem_regex.search(test_text)
        
        detected = any([sar_match, tech_data_match, cert_match, oem_match])
        match_type = ""
        if sar_match:
            match_type += "SAR "
        if tech_data_match:
            match_type += "TECH_DATA "
        if cert_match:
            match_type += "CERT "
        if oem_match:
            match_type += "OEM "
        
        status = "DETECTED" if detected else "NOT DETECTED"
        if detected:
            status += f" ({match_type.strip()})"
        
        print(f"{description}: {status}")
    
    print()
    print("=== RECOMMENDATIONS BASED ON SOS DOCUMENTATION ===")
    print()
    
    # Based on SOS Initial Assessment Logic v4.0 and AMC/AMSC Bid Matrix
    recommendations = [
        "1. AMSC Code Coverage: Current filter covers C,D,P,R but SOS Bid Matrix shows H,T,Z need specific handling",
        "2. Critical Safety Items: Flight-critical and life-limited parts often have additional SAR requirements", 
        "3. Technical Data Granularity: Distinguish between 'no TDP' vs 'limited TDP' vs 'proprietary TDP'",
        "4. OEM Authorization Levels: Different levels from 'authorized dealer' to 'direct OEM only'",
        "5. Export Control Specificity: ITAR registration vs specific export licenses have different implications",
        "6. Certification Depth: FAR 145, PMA, STC requirements vs manufacturing certifications",
        "7. Design Authority Approval: Specific patterns for design control activity requirements",
        "8. First Article/Qualification: Manufacturing qualification requirements beyond standard SAR"
    ]
    
    for rec in recommendations:
        print(rec)
    
    return filter_obj

if __name__ == "__main__":
    analyze_current_filter()
