#!/usr/bin/env python3
"""
Test script for the enhanced InitialChecklistFilterV2
Demonstrates the improvements based on SOS documentation analysis
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from filters.initial_checklist_v2 import InitialChecklistFilterV2, Decision

def test_enhanced_filter():
    """Test the enhanced filter with sample opportunities."""
    
    filter_instance = InitialChecklistFilterV2()
    
    # Test Case 1: Military SAR - Should be NO-GO
    test_opportunity_1 = {
        'source_id': 'TEST-001',
        'title': 'F-16 Engine Parts - Source Approval Required',
        'description_text': 'This procurement requires engineering source approval by the design control activity. Only approved sources may submit proposals.',
        'due_date': '2025-12-01',
        'documents': []
    }
    
    print("=" * 60)
    print("TEST CASE 1: Military SAR Detection")
    print("=" * 60)
    
    decision_1, results_1 = filter_instance.assess_opportunity(test_opportunity_1)
    print(f"Decision: {decision_1.value}")
    print("\nDetailed Results:")
    for result in results_1:
        if result.decision != Decision.PASS or result.quote:
            print(f"  {result.check_name}: {result.decision.value}")
            print(f"    Reason: {result.reason}")
            if result.quote:
                print(f"    Quote: {result.quote[:100]}...")
            print()
    
    # Test Case 2: Commercial opportunity - Should be GO
    test_opportunity_2 = {
        'source_id': 'TEST-002', 
        'title': 'Boeing 737 Hydraulic Pump Overhaul',
        'description_text': 'Commercial item acquisition under FAR Part 12. Refurbished parts acceptable. P/N: 123-4567, Qty: 5. For Boeing 737-800 aircraft maintenance.',
        'due_date': '2025-12-15',
        'documents': []
    }
    
    print("=" * 60)
    print("TEST CASE 2: Commercial Opportunity")
    print("=" * 60)
    
    decision_2, results_2 = filter_instance.assess_opportunity(test_opportunity_2)
    print(f"Decision: {decision_2.value}")
    if decision_2 == Decision.GO:
        # Generate a simple pipeline title (pipeline_title method not available in standard filter)
        pipeline_title = f"{test_opportunity_2.get('source_id', 'Unknown')} - {decision_2.value} - {test_opportunity_2.get('title', 'Unknown Title')[:50]}"
        print(f"Pipeline Title: {pipeline_title}")
    
    print("\nKey Results:")
    for result in results_2:
        if result.decision != Decision.PASS or result.quote:
            print(f"  {result.check_name}: {result.decision.value}")
            if result.quote:
                print(f"    Quote: {result.quote[:100]}...")
            print()
    
    # Test Case 3: Mixed signals - Should be NEEDS_ANALYSIS
    test_opportunity_3 = {
        'source_id': 'TEST-003',
        'title': 'KC-46 Parts with Intent to Sole Source',
        'description_text': 'Intent to sole source to Boeing for KC-46 Pegasus spare parts. Brand name or equal may be acceptable. ITAR compliance required.',
        'due_date': '2025-11-30',
        'documents': []
    }
    
    print("=" * 60)
    print("TEST CASE 3: Mixed Signals")
    print("=" * 60)
    
    decision_3, results_3 = filter_instance.assess_opportunity(test_opportunity_3)
    print(f"Decision: {decision_3.value}")
    print("\nKey Results:")
    for result in results_3:
        if result.decision != Decision.PASS:
            print(f"  {result.check_name}: {result.decision.value}")
            print(f"    Reason: {result.reason}")
            if result.quote:
                print(f"    Quote: {result.quote[:100]}...")
            print()

    # Generate comprehensive report for Test Case 1
    print("=" * 60)
    print("COMPREHENSIVE REPORT - TEST CASE 1")
    print("=" * 60)
    
    # Generate a simple report (comprehensive report method not available in standard filter)
    decision_1_report, results_1_report = filter_instance.assess_opportunity(test_opportunity_1)
    print(f"Opportunity ID: {test_opportunity_1.get('source_id', 'Unknown')}")
    print(f"Final Decision: {decision_1_report.value}")
    print(f"Summary: Filter assessment completed using standardized InitialChecklistFilterV2")
    next_actions = ["Manual review required" if decision_1_report == Decision.NEEDS_ANALYSIS else "Proceed with assessment" if decision_1_report == Decision.GO else "Do not pursue"]
    print(f"Next Actions: {', '.join(next_actions)}")

if __name__ == "__main__":
    test_enhanced_filter()
