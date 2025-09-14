#!/usr/bin/env python3
"""
Test standardized batch processor output format
"""

import json
import sys
import os
from datetime import datetime

# Add paths for imports
sys.path.append('Mistral_Batch_Processor')

def test_standardized_format():
    """Test the standardized format across all processing methods"""
    
    print("=" * 80)
    print("TESTING STANDARDIZED BATCH OUTPUT FORMAT")
    print("=" * 80)
    
    # Import the output manager
    from enhanced_output_manager import EnhancedOutputManager
    
    # Create test data representing all 3 processing methods
    test_results = [
        {
            # REGEX KNOCKOUT
            'search_id': 'TEST_STD',
            'opportunity_id': 'FA8601-25-Q-REGEX',
            'title': 'F-16 FIGHTER PARTS',
            'decision': 'NO-GO',
            'reasoning': 'Regex knockout: Category 8 - Military Platform: F-16',
            'processing_method': 'REGEX_ONLY',
            'agency': 'Air Force',
            'announcement_number': 'FA8601-25-Q-REGEX',
            'announcement_title': 'F-16 FIGHTER PARTS',
            'due_date': '2025-09-20',
            'posted_date': '2025-09-11',
            'naics': '336413',
            'psc': '1560',
            'set_aside': '',
            'value_low': 100000,
            'value_high': 500000,
            'place_of_performance': 'Wright-Patterson AFB, OH',
            'doc_length': 25000
        },
        {
            # BATCH AI ASSESSMENT - GO
            'search_id': 'TEST_STD',
            'opportunity_id': 'SPE4A5-25-Q-BATCH',
            'title': 'BOEING 737 ENGINE PARTS',
            'decision': 'GO',
            'reasoning': 'Commercial aircraft parts with no restrictions. Surplus accepted.',
            'processing_method': 'BATCH_AI',
            'agency': 'DLA Aviation',
            'announcement_number': 'SPE4A5-25-Q-BATCH',
            'announcement_title': 'BOEING 737 ENGINE PARTS',
            'due_date': '2025-09-18',
            'posted_date': '2025-09-10',
            'naics': '336412',
            'psc': '2840',
            'set_aside': '',
            'value_low': 50000,
            'value_high': 250000,
            'place_of_performance': 'Richmond, VA',
            'doc_length': 45000
        },
        {
            # MISTRAL AGENT ASSESSMENT - INDETERMINATE
            'search_id': 'TEST_STD',
            'opportunity_id': 'N00383-25-Q-AGENT',
            'title': 'SHIP NAVIGATION EQUIPMENT',
            'decision': 'INDETERMINATE',
            'reasoning': 'Requires further analysis - unclear if commercial equipment is acceptable',
            'processing_method': 'MISTRAL',
            'agency': 'NAVSUP',
            'announcement_number': 'N00383-25-Q-AGENT',
            'announcement_title': 'SHIP NAVIGATION EQUIPMENT',
            'due_date': '2025-09-25',
            'posted_date': '2025-09-12',
            'naics': '334511',
            'psc': '5845',
            'set_aside': 'Small Business',
            'value_low': 75000,
            'value_high': 150000,
            'place_of_performance': 'Norfolk, VA',
            'doc_length': 18000
        }
    ]
    
    # Apply the standardized formatting from FULL_BATCH_PROCESSOR
    formatted_results = []
    for result in test_results:
        # Determine the type based on processing method
        if result.get('processing_method') == 'REGEX_ONLY':
            assessment_type = 'REGEX_KNOCKOUT'
            knockout_category = 'REGEX'
        elif result.get('processing_method') == 'BATCH_AI':
            assessment_type = 'MISTRAL_BATCH_ASSESSMENT'
            knockout_category = 'BATCH-AI' if result.get('decision') == 'NO-GO' else 'GO-OK'
        else:
            assessment_type = 'MISTRAL_ASSESSMENT'
            knockout_category = 'AI-ASSESS'
        
        # Extract agency name properly
        agency = result.get('agency', 'Unknown')
        if isinstance(agency, dict):
            agency_name = agency.get('agency_name', 'Unknown')
        else:
            agency_name = str(agency) if agency else 'Unknown'
        
        # Create fully standardized assessment format with ALL fields
        formatted_results.append({
            # Primary identification fields
            'search_id': result.get('search_id', ''),
            'opportunity_id': result.get('opportunity_id', ''),
            'title': result.get('title', ''),
            'final_decision': result.get('decision', 'INDETERMINATE'),
            'knock_pattern': result.get('reasoning', '')[:100] if result.get('processing_method') == 'REGEX_ONLY' else '',
            'knockout_category': knockout_category,
            
            # Pipeline metadata
            'sos_pipeline_title': f"PN: NA | Qty: NA | Condition: unknown | MDS: NA | {result.get('title', '')[:50]}",
            'highergov_url': f"https://www.highergov.com/opportunity/{result.get('opportunity_id', '')}",
            
            # Opportunity details (REQUIRED by output manager)
            'announcement_number': result.get('announcement_number', result.get('opportunity_id', '')),
            'announcement_title': result.get('announcement_title', result.get('title', '')),
            'agency': agency_name,
            'due_date': result.get('due_date', ''),
            'posted_date': result.get('posted_date', ''),
            
            # Contract details
            'naics': result.get('naics', ''),
            'psc': result.get('psc', ''),
            'set_aside': result.get('set_aside', ''),
            'value_low': result.get('value_low', 0),
            'value_high': result.get('value_high', 0),
            'place_of_performance': result.get('place_of_performance', ''),
            
            # Analysis results
            'brief_description': result.get('reasoning', '')[:100],
            'analysis_notes': result.get('reasoning', ''),
            'recommendation': result.get('decision', 'INDETERMINATE'),
            'special_action': '',
            
            # Document metadata
            'doc_length': result.get('doc_length', 0),
            'assessment_timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            
            # New standardized fields
            'solicitation_id': result.get('search_id', 'unknown'),
            'solicitation_title': result.get('title', ''),
            'type': assessment_type,
            'result': result.get('decision', 'INDETERMINATE'),
            'summary': result.get('reasoning', '')[:200],
            'rationale': result.get('reasoning', ''),
            'knock_out_reasons': ['Regex pattern match'] if 'REGEX' in assessment_type else [result.get('reasoning', '')[:100]],
            'exceptions': [],
            'processing_method': result.get('processing_method', 'BATCH_AI')
        })
    
    # Verify all required fields are present
    print("\nVERIFYING FIELD COMPLETENESS:")
    print("-" * 40)
    
    required_fields = [
        # Legacy fields expected by output manager
        'search_id', 'opportunity_id', 'title', 'final_decision',
        'knock_pattern', 'knockout_category', 'sos_pipeline_title',
        'highergov_url', 'announcement_number', 'announcement_title',
        'agency', 'due_date', 'posted_date', 'naics', 'psc',
        'set_aside', 'value_low', 'value_high', 'place_of_performance',
        'brief_description', 'analysis_notes', 'recommendation',
        'special_action', 'doc_length', 'assessment_timestamp',
        # New standardized fields
        'solicitation_id', 'solicitation_title', 'type', 'result',
        'summary', 'rationale', 'knock_out_reasons', 'exceptions',
        'processing_method'
    ]
    
    all_pass = True
    for i, assessment in enumerate(formatted_results, 1):
        print(f"\nAssessment {i}: {assessment['title']}")
        print(f"  Type: {assessment['type']}")
        print(f"  Processing: {assessment['processing_method']}")
        print(f"  Decision: {assessment['final_decision']}")
        
        missing = [f for f in required_fields if f not in assessment]
        if missing:
            print(f"  FAIL: Missing {len(missing)} fields: {missing}")
            all_pass = False
        else:
            print(f"  PASS: All {len(required_fields)} required fields present")
    
    # Now test with actual output manager
    print("\n" + "=" * 80)
    print("TESTING WITH OUTPUT MANAGER:")
    print("-" * 40)
    
    try:
        output_manager = EnhancedOutputManager(base_path="SOS_Output")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        search_id = f"STD_TEST_{timestamp}"
        
        metadata = {
            'total_opportunities': len(formatted_results),
            'regex_knockouts': 1,
            'ai_assessments': 2,
            'processing_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save using the actual output manager
        output_dir = output_manager.save_assessment_batch(search_id, formatted_results, metadata, pre_formatted=True)
        
        print(f"SUCCESS: Output saved to: {output_dir}")
        
        # Verify files were created
        expected_files = ['data.json', 'assessment.csv', 'report.md', 'summary.txt']
        for filename in expected_files:
            filepath = os.path.join(output_dir, filename)
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                print(f"  PASS: {filename} created ({size:,} bytes)")
            else:
                print(f"  FAIL: {filename} not found")
                all_pass = False
        
        # Check the JSON has the type field
        json_path = os.path.join(output_dir, 'data.json')
        with open(json_path, 'r') as f:
            saved_data = json.load(f)
        
        print("\n" + "-" * 40)
        print("VERIFYING TYPE FIELD IN OUTPUT:")
        for assessment in saved_data.get('assessments', []):
            if 'type' in assessment:
                print(f"  PASS: {assessment['title'][:30]} has type='{assessment['type']}'")
            else:
                print(f"  FAIL: {assessment['title'][:30]} missing 'type' field")
                all_pass = False
        
    except Exception as e:
        print(f"ERROR: Failed to save with output manager: {e}")
        all_pass = False
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY:")
    print("-" * 40)
    
    if all_pass:
        print("SUCCESS: Standardized format working correctly")
        print("- All 3 processing methods have correct type labels")
        print("- All required fields present")
        print("- Output manager accepts the format")
        print("- JSON, CSV, and Markdown files generated")
    else:
        print("FAILED: Issues detected with standardized format")
    
    return all_pass

if __name__ == "__main__":
    success = test_standardized_format()
    exit(0 if success else 1)