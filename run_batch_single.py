#!/usr/bin/env python3
"""
Run batch processor on a single search ID with progress
"""

import sys
import os
import time
from datetime import datetime

# Add paths
sys.path.append('Mistral_Batch_Processor')

def run_single_batch():
    """Process single search ID through batch pipeline"""
    
    print("=" * 70)
    print("SINGLE SEARCH ID BATCH TEST")
    print("=" * 70)
    
    # Single search ID for testing
    search_id = "rFRK9PaP6ftzk1rokcKCT"
    
    print(f"Processing search ID: {search_id}")
    print("Note: Document fetching may take 1-2 minutes per opportunity")
    print("-" * 70)
    
    # Import components
    from highergov_batch_fetcher import HigherGovBatchFetcher
    from sos_ingestion_gate_v419 import IngestionGateV419, Decision
    from enhanced_output_manager import EnhancedOutputManager
    
    # Initialize
    fetcher = HigherGovBatchFetcher()
    regex_gate = IngestionGateV419()
    output_manager = EnhancedOutputManager(base_path="SOS_Output")
    
    # Step 1: Fetch opportunities
    print(f"\n[1/4] Fetching opportunities from HigherGov...")
    start = time.time()
    
    opportunities = fetcher.fetch_all_opportunities(search_id, max_pages=1)  # Just first page
    
    elapsed = time.time() - start
    print(f"  Fetched {len(opportunities)} opportunities in {elapsed:.1f} seconds")
    
    if not opportunities:
        print("ERROR: No opportunities found")
        return False
    
    # Step 2: Process and filter
    print(f"\n[2/4] Processing opportunities and applying regex filter...")
    
    results = []
    for i, opp in enumerate(opportunities[:2], 1):  # Just process first 2
        print(f"  [{i}/{min(2, len(opportunities))}] {opp.get('title', 'Unknown')[:40]}...")
        
        # Process opportunity (fetches documents)
        start = time.time()
        processed = fetcher.process_opportunity(opp)
        elapsed = time.time() - start
        
        doc_size = len(processed.get('text', ''))
        print(f"      Processed in {elapsed:.1f}s, document: {doc_size:,} chars")
        
        # Apply regex
        regex_result = regex_gate.assess_opportunity(processed)
        
        # Build result with ALL metadata
        result = {
            'search_id': search_id,
            'opportunity_id': processed.get('id', ''),
            'title': processed.get('title', ''),
            'agency': processed.get('agency', 'Unknown'),
            'announcement_number': processed.get('announcement_number', processed.get('id', '')),
            'announcement_title': processed.get('announcement_title', processed.get('title', '')),
            'due_date': processed.get('due_date', ''),
            'posted_date': processed.get('posted_date', ''),
            'naics': processed.get('naics', ''),
            'psc': processed.get('psc', ''),
            'set_aside': processed.get('set_aside', ''),
            'value_low': processed.get('value_low', 0),
            'value_high': processed.get('value_high', 0),
            'place_of_performance': processed.get('place_of_performance', ''),
            'doc_length': doc_size
        }
        
        if regex_result.decision == Decision.NO_GO:
            print(f"      REGEX KNOCKOUT: {regex_result.primary_blocker}")
            result.update({
                'decision': 'NO-GO',
                'reasoning': f"Regex knockout: {regex_result.primary_blocker}",
                'processing_method': 'REGEX_ONLY'
            })
        else:
            print(f"      Needs AI assessment (would be sent to batch)")
            result.update({
                'decision': 'INDETERMINATE',
                'reasoning': 'Would be sent to Mistral batch API',
                'processing_method': 'BATCH_AI'
            })
        
        results.append(result)
    
    # Step 3: Format results
    print(f"\n[3/4] Formatting results with standardized fields...")
    
    formatted_results = []
    for result in results:
        # Determine type
        if result.get('processing_method') == 'REGEX_ONLY':
            assessment_type = 'REGEX_KNOCKOUT'
            knockout_category = 'REGEX'
        else:
            assessment_type = 'MISTRAL_BATCH_ASSESSMENT'
            knockout_category = 'BATCH-AI'
        
        # Extract agency name
        agency = result.get('agency', 'Unknown')
        if isinstance(agency, dict):
            agency_name = agency.get('agency_name', 'Unknown')
        else:
            agency_name = str(agency) if agency else 'Unknown'
        
        # Build standardized format
        formatted_results.append({
            # All required fields
            'search_id': result.get('search_id', ''),
            'opportunity_id': result.get('opportunity_id', ''),
            'title': result.get('title', ''),
            'final_decision': result.get('decision', 'INDETERMINATE'),
            'knock_pattern': result.get('reasoning', '')[:100] if result.get('processing_method') == 'REGEX_ONLY' else '',
            'knockout_category': knockout_category,
            'sos_pipeline_title': f"PN: NA | Qty: NA | Condition: unknown | MDS: NA | {result.get('title', '')[:50]}",
            'highergov_url': f"https://www.highergov.com/opportunity/{result.get('opportunity_id', '')}",
            'announcement_number': result.get('announcement_number', ''),
            'announcement_title': result.get('announcement_title', ''),
            'agency': agency_name,
            'due_date': result.get('due_date', ''),
            'posted_date': result.get('posted_date', ''),
            'naics': result.get('naics', ''),
            'psc': result.get('psc', ''),
            'set_aside': result.get('set_aside', ''),
            'value_low': result.get('value_low', 0),
            'value_high': result.get('value_high', 0),
            'place_of_performance': result.get('place_of_performance', ''),
            'brief_description': result.get('reasoning', '')[:100],
            'analysis_notes': result.get('reasoning', ''),
            'recommendation': result.get('decision', 'INDETERMINATE'),
            'special_action': '',
            'doc_length': result.get('doc_length', 0),
            'assessment_timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            # New standardized fields
            'solicitation_id': result.get('search_id', ''),
            'solicitation_title': result.get('title', ''),
            'type': assessment_type,
            'result': result.get('decision', 'INDETERMINATE'),
            'summary': result.get('reasoning', '')[:200],
            'rationale': result.get('reasoning', ''),
            'knock_out_reasons': ['Regex pattern match'] if 'REGEX' in assessment_type else [result.get('reasoning', '')[:100]],
            'exceptions': [],
            'processing_method': result.get('processing_method', 'BATCH_AI')
        })
    
    # Step 4: Save output
    print(f"\n[4/4] Saving standardized output...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_id = f"SINGLE_TEST_{timestamp}"
    
    metadata = {
        'total_opportunities': len(formatted_results),
        'regex_knockouts': sum(1 for r in results if r['processing_method'] == 'REGEX_ONLY'),
        'ai_assessments': sum(1 for r in results if r['processing_method'] == 'BATCH_AI'),
        'processing_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    output_dir = output_manager.save_assessment_batch(batch_id, formatted_results, metadata, pre_formatted=True)
    
    print(f"\n" + "=" * 70)
    print("TEST COMPLETE")
    print(f"Output saved to: {output_dir}")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    success = run_single_batch()
    exit(0 if success else 1)