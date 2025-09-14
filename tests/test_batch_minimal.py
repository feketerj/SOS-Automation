#!/usr/bin/env python3
"""
Minimal test of batch processor to verify output format
"""

import json
import sys
from datetime import datetime

# Add path for imports
sys.path.append('Mistral_Batch_Processor')

def test_minimal_batch():
    """Test batch processor with minimal simulated data"""
    
    print("=" * 80)
    print("MINIMAL BATCH PROCESSOR TEST")
    print("=" * 80)
    
    # Import the output manager
    from enhanced_output_manager import EnhancedOutputManager
    
    # Simulate what FULL_BATCH_PROCESSOR does with results
    final_results = [
        {
            'search_id': 'TEST_MINIMAL',
            'opportunity_id': 'FA8601-25-Q-TEST1',
            'title': 'C-130 AIRCRAFT PARTS',
            'decision': 'NO-GO',
            'reasoning': 'Regex knockout: Category 8 - Military Platform: C-130',
            'processing_method': 'REGEX_ONLY'
        },
        {
            'search_id': 'TEST_MINIMAL',
            'opportunity_id': 'SPE4A5-25-Q-TEST2',
            'title': 'BOEING 737 ENGINE PARTS',
            'decision': 'GO',
            'reasoning': 'Commercial aircraft parts, no restrictions',
            'processing_method': 'BATCH_AI'
        }
    ]
    
    # Apply exact formatting from FULL_BATCH_PROCESSOR.py lines 363-406
    formatted_results = []
    for result in final_results:
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
    
    # Use the output manager to save
    output_manager = EnhancedOutputManager(base_path="SOS_Output")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    search_id = f"BATCH_TEST_{timestamp}"
    
    metadata = {
        'total_opportunities': len(final_results),
        'regex_knockouts': 1,
        'ai_assessments': 1,
        'processing_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save using the actual output manager
    output_dir = output_manager.save_assessment_batch(search_id, formatted_results, metadata, pre_formatted=True)
    
    print(f"\nOutput saved to: {output_dir}")
    
    # Read back and verify
    data_file = f"{output_dir}/data.json"
    with open(data_file, 'r') as f:
        saved_data = json.load(f)
    
    print("\n" + "=" * 80)
    print("VERIFICATION OF SAVED OUTPUT:")
    print("-" * 40)
    
    # Check assessments
    for i, assessment in enumerate(saved_data.get('assessments', []), 1):
        print(f"\nAssessment {i}: {assessment.get('title', 'UNKNOWN')}")
        
        # Check for type field
        if 'type' in assessment:
            print(f"  SUCCESS: 'type' field present = '{assessment['type']}'")
        else:
            print(f"  FAIL: 'type' field is MISSING!")
        
        # Check other critical fields
        critical_fields = ['solicitation_id', 'solicitation_title', 'result', 
                          'summary', 'rationale', 'recommendation']
        missing = [f for f in critical_fields if f not in assessment]
        if missing:
            print(f"  WARNING: Missing fields: {missing}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    
    return output_dir

if __name__ == "__main__":
    test_minimal_batch()