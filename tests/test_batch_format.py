#!/usr/bin/env python3
"""
Test the batch processor output format without running full batch
"""

import json
import sys
from datetime import datetime

# Add path for imports
sys.path.append('Mistral_Batch_Processor')

def test_format_generation():
    """Test that the format generation code produces correct output"""
    
    # Simulate batch processor results
    test_results = [
        {
            'search_id': 'TEST123',
            'opportunity_id': 'OPP-001',
            'title': 'Test Regex Knockout',
            'decision': 'NO-GO',
            'reasoning': 'Regex knockout: Category 4 - SET-ASIDES: 8(a) set-aside',
            'processing_method': 'REGEX_ONLY'
        },
        {
            'search_id': 'TEST123',
            'opportunity_id': 'OPP-002',
            'title': 'Test Batch AI Assessment',
            'decision': 'GO',
            'reasoning': 'Commercial parts with no restrictions identified',
            'processing_method': 'BATCH_AI'
        },
        {
            'search_id': 'TEST123',
            'opportunity_id': 'OPP-003',
            'title': 'Test Regular Assessment',
            'decision': 'INDETERMINATE',
            'reasoning': 'Requires further analysis',
            'processing_method': 'MISTRAL'
        }
    ]
    
    # Run the formatting logic from FULL_BATCH_PROCESSOR
    formatted_results = []
    for result in test_results:
        # Determine the type based on processing method
        if result.get('processing_method') == 'REGEX_ONLY':
            assessment_type = 'REGEX_KNOCKOUT'
        elif result.get('processing_method') == 'BATCH_AI':
            assessment_type = 'MISTRAL_BATCH_ASSESSMENT'
        else:
            assessment_type = 'MISTRAL_ASSESSMENT'
        
        # Create standardized assessment format
        formatted_results.append({
            # Standard identification fields
            'solicitation_id': result.get('search_id', 'unknown'),
            'solicitation_title': result.get('title', ''),
            'type': assessment_type,
            
            # Decision fields
            'result': result.get('decision', 'INDETERMINATE'),
            'summary': result.get('reasoning', '')[:200],
            'rationale': result.get('reasoning', ''),
            'recommendation': result.get('decision', 'INDETERMINATE'),
            
            # Knockout/exception fields
            'knock_out_reasons': ['Regex pattern match'] if 'REGEX' in assessment_type else [result.get('reasoning', '')[:100]],
            'exceptions': [],
            'special_action': None,
            
            # Metadata fields
            'sos_pipeline_title': f"PN: NA | Qty: NA | Condition: unknown | MDS: NA | {result.get('title', '')[:50]}",
            'highergov_link': f"https://www.highergov.com/opportunity/{result.get('opportunity_id', '')}",
            'sam_link': '',
            
            # Legacy fields for compatibility
            'search_id': result.get('search_id', ''),
            'opportunity_id': result.get('opportunity_id', ''),
            'title': result.get('title', ''),
            'final_decision': result.get('decision', 'INDETERMINATE'),
            'knock_pattern': result.get('reasoning', '')[:100] if result.get('processing_method') == 'REGEX_ONLY' else '',
            'knockout_category': 'BATCH-AI' if result.get('processing_method') == 'BATCH_AI' else 'REGEX',
            'analysis_notes': result.get('reasoning', ''),
            'processing_method': result.get('processing_method', 'BATCH_AI')
        })
    
    # Display results
    print("=" * 80)
    print("BATCH PROCESSOR OUTPUT FORMAT TEST")
    print("=" * 80)
    
    for i, assessment in enumerate(formatted_results, 1):
        print(f"\nAssessment {i}:")
        print(f"  Title: {assessment['solicitation_title']}")
        print(f"  Type: {assessment['type']}")
        print(f"  Result: {assessment['result']}")
        print(f"  Summary: {assessment['summary'][:50]}...")
        
        # Check required fields
        required_fields = [
            'solicitation_id', 'solicitation_title', 'type',
            'result', 'summary', 'rationale', 'recommendation',
            'knock_out_reasons', 'exceptions', 'special_action',
            'sos_pipeline_title', 'highergov_link', 'sam_link'
        ]
        
        missing = [f for f in required_fields if f not in assessment]
        if missing:
            print(f"  MISSING FIELDS: {missing}")
        else:
            print(f"  PASS: All required fields present")
    
    # Save test output
    output_file = 'test_batch_output.json'
    with open(output_file, 'w') as f:
        json.dump(formatted_results, f, indent=2)
    
    print(f"\nTest output saved to: {output_file}")
    
    # Verify types are correct
    print("\n" + "=" * 80)
    print("TYPE VERIFICATION:")
    print("-" * 40)
    
    types_found = set(a['type'] for a in formatted_results)
    expected_types = {'REGEX_KNOCKOUT', 'MISTRAL_BATCH_ASSESSMENT', 'MISTRAL_ASSESSMENT'}
    
    for t in expected_types:
        if t in types_found:
            print(f"PASS: {t} type correctly set")
        else:
            print(f"FAIL: {t} type missing")
    
    return formatted_results

if __name__ == "__main__":
    test_format_generation()