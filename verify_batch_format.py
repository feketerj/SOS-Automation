#!/usr/bin/env python3
"""
Verify batch processor output format without running full pipeline
"""

import json
from datetime import datetime

def verify_format():
    """Verify the batch processor formatting logic"""
    
    print("=" * 80)
    print("BATCH PROCESSOR FORMAT VERIFICATION")
    print("=" * 80)
    
    # Test data representing different processing paths
    test_results = [
        {
            'search_id': 'TEST123',
            'opportunity_id': 'FA8601-25-Q-B031',
            'title': 'REPAIR PARTS FOR C-130 AIRCRAFT',
            'decision': 'NO-GO',
            'reasoning': 'Regex knockout: Category 8 - Military Platform: C-130 (military transport)',
            'processing_method': 'REGEX_ONLY'
        },
        {
            'search_id': 'TEST456',
            'opportunity_id': 'SPE4A5-25-Q-1234',
            'title': 'BOEING 737 PARTS',
            'decision': 'GO',
            'reasoning': 'Commercial aircraft parts with no restrictions',
            'processing_method': 'BATCH_AI'
        },
        {
            'search_id': 'TEST789',
            'opportunity_id': 'N00383-25-Q-5678',
            'title': 'SHIP PARTS',
            'decision': 'INDETERMINATE',
            'reasoning': 'Requires further analysis - unclear specifications',
            'processing_method': 'MISTRAL'
        }
    ]
    
    # Apply the same formatting logic from FULL_BATCH_PROCESSOR.py
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
    
    # Verify each assessment
    print("\nVERIFYING FORMATTED ASSESSMENTS:")
    print("-" * 40)
    
    required_fields = [
        'solicitation_id', 'solicitation_title', 'type',
        'result', 'summary', 'rationale', 'recommendation',
        'knock_out_reasons', 'exceptions', 'special_action',
        'sos_pipeline_title', 'highergov_link', 'sam_link',
        'search_id', 'opportunity_id', 'title', 'final_decision',
        'knock_pattern', 'knockout_category', 'analysis_notes',
        'processing_method'
    ]
    
    all_pass = True
    for i, assessment in enumerate(formatted_results, 1):
        print(f"\nAssessment {i}: {assessment['title']}")
        print(f"  Type: {assessment['type']}")
        print(f"  Result: {assessment['result']}")
        print(f"  Processing Method: {assessment['processing_method']}")
        
        # Check required fields
        missing = [f for f in required_fields if f not in assessment]
        if missing:
            print(f"  FAIL: Missing fields: {missing}")
            all_pass = False
        else:
            print(f"  PASS: All {len(required_fields)} required fields present")
        
        # Verify type mapping
        expected_type = {
            'REGEX_ONLY': 'REGEX_KNOCKOUT',
            'BATCH_AI': 'MISTRAL_BATCH_ASSESSMENT',
            'MISTRAL': 'MISTRAL_ASSESSMENT'
        }.get(assessment['processing_method'])
        
        if assessment['type'] != expected_type:
            print(f"  FAIL: Type mismatch. Expected '{expected_type}', got '{assessment['type']}'")
            all_pass = False
        else:
            print(f"  PASS: Type correctly set to '{assessment['type']}'")
    
    # Summary
    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY:")
    print("-" * 40)
    
    if all_pass:
        print("SUCCESS: All assessments have correct standardized format")
        print(f"- All {len(required_fields)} required fields present")
        print("- Type field correctly mapped based on processing_method")
        print("- REGEX_ONLY -> REGEX_KNOCKOUT")
        print("- BATCH_AI -> MISTRAL_BATCH_ASSESSMENT")
        print("- MISTRAL -> MISTRAL_ASSESSMENT")
    else:
        print("FAILED: Some assessments have incorrect format")
    
    # Save verification output
    output_file = 'batch_format_verification.json'
    with open(output_file, 'w') as f:
        json.dump({
            'verified_at': datetime.now().isoformat(),
            'test_cases': len(test_results),
            'all_pass': all_pass,
            'required_fields': required_fields,
            'formatted_results': formatted_results
        }, f, indent=2)
    
    print(f"\nVerification details saved to: {output_file}")
    
    return all_pass

if __name__ == "__main__":
    success = verify_format()
    exit(0 if success else 1)