#!/usr/bin/env python3
"""
BATCH_RESULTS_PARSER.py - Parses Mistral batch results and creates final CSVs
Completes the batch processing pipeline
"""

import json
import csv
import os
from datetime import datetime
from typing import List, Dict

def parse_results_without_metadata(results_file: str) -> List[Dict]:
    """
    Parse batch results without metadata (no regex knockout info)
    """
    parsed_results = []
    
    with open(results_file, 'r') as f:
        for line in f:
            result = json.loads(line)
            
            # Extract custom_id
            custom_id = result.get('custom_id', '')
            
            # Extract model response
            try:
                response_content = result['response']['body']['choices'][0]['message']['content']
                
                # Try to parse JSON from response
                decision_data = {}
                try:
                    # Look for JSON in response
                    import re
                    json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
                    if json_match:
                        decision_data = json.loads(json_match.group())
                except:
                    # Fallback to text parsing
                    if 'NO-GO' in response_content or 'NO_GO' in response_content:
                        decision_data['decision'] = 'NO-GO'
                    elif 'INDETERMINATE' in response_content:
                        decision_data['decision'] = 'INDETERMINATE'
                    elif 'GO' in response_content:
                        decision_data['decision'] = 'GO'
                    else:
                        decision_data['decision'] = 'UNKNOWN'
                    
                    decision_data['reasoning'] = response_content[:500]
                
                # Extract IDs from custom_id
                parts = custom_id.split('-')
                search_id = parts[1] if len(parts) > 1 else 'unknown'
                opp_id = parts[2] if len(parts) > 2 else 'unknown'
                
                parsed_results.append({
                    'search_id': search_id,
                    'opportunity_id': opp_id,
                    'title': 'No metadata available',
                    'regex_decision': 'N/A',
                    'model_decision': decision_data.get('decision', 'UNKNOWN'),
                    'reasoning': decision_data.get('reasoning', ''),
                    'knockout_patterns': ', '.join(decision_data.get('knockout_patterns', [])),
                    'confidence': decision_data.get('confidence', 0),
                    'full_response': response_content
                })
                
            except Exception as e:
                print(f"Error parsing result for {custom_id}: {e}")
    
    return parsed_results

def parse_batch_results(results_file: str, metadata_file: str) -> List[Dict]:
    """
    Parse batch results and match with original opportunities
    """
    # Load metadata
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    
    # Start with regex knockouts from metadata
    parsed_results = metadata.get('regex_knockouts', [])
    
    # Create lookup for opportunities
    opp_lookup = {}
    for opp in metadata['opportunities']:
        key = f"opp-{opp['search_id']}-{opp['opportunity_id']}"
        opp_lookup[key] = opp
    
    with open(results_file, 'r') as f:
        for line in f:
            result = json.loads(line)
            
            # Extract custom_id to match with original
            custom_id = result.get('custom_id', '')
            # Remove trailing number for matching
            base_id = '-'.join(custom_id.split('-')[:-1])
            
            if base_id in opp_lookup:
                original = opp_lookup[base_id]
                
                # Extract model response
                try:
                    response_content = result['response']['body']['choices'][0]['message']['content']
                    
                    # Try to parse JSON from response
                    decision_data = {}
                    try:
                        # Look for JSON in response
                        import re
                        json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
                        if json_match:
                            decision_data = json.loads(json_match.group())
                    except:
                        # Fallback to text parsing
                        if 'NO-GO' in response_content or 'NO_GO' in response_content:
                            decision_data['decision'] = 'NO-GO'
                        elif 'INDETERMINATE' in response_content:
                            decision_data['decision'] = 'INDETERMINATE'
                        elif 'GO' in response_content:
                            decision_data['decision'] = 'GO'
                        else:
                            decision_data['decision'] = 'UNKNOWN'
                        
                        decision_data['reasoning'] = response_content[:500]
                    
                    # Combine with original data
                    parsed_results.append({
                        'search_id': original['search_id'],
                        'opportunity_id': original['opportunity_id'],
                        'title': original['title'],
                        'regex_decision': original['regex_decision'],
                        'model_decision': decision_data.get('decision', 'UNKNOWN'),
                        'reasoning': decision_data.get('reasoning', ''),
                        'knockout_patterns': ', '.join(decision_data.get('knockout_patterns', [])),
                        'confidence': decision_data.get('confidence', 0),
                        'full_response': response_content
                    })
                    
                except Exception as e:
                    print(f"Error parsing result for {custom_id}: {e}")
    
    return parsed_results

def create_output_csv(results: List[Dict], output_file: str = None, metadata: Dict = None):
    """
    Create CSV output matching main system format
    """
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Create in standard SOS_Output location - EXACT SAME AS PRODUCTION
        month_folder = datetime.now().strftime("%Y-%m")
        output_dir = f"../SOS_Output/{month_folder}/Run_{timestamp}_BATCH"
        os.makedirs(output_dir, exist_ok=True)
        output_file = f"{output_dir}/assessment.csv"  # Same filename as production
    
    # EXACT SAME COLUMNS AS PRODUCTION
    fieldnames = [
        'final_decision',           # GO/NO-GO/INDETERMINATE
        'knock_pattern',            # Pattern that triggered decision
        'knockout_category',        # Category code (KO-01, GO-OK, FA-00, etc.)
        'sos_pipeline_title',       # SOS Pipeline Title
        'highergov_url',           # Link to opportunity
        'announcement_number',      # Solicitation number
        'announcement_title',       # Title
        'agency',                  # Agency name
        'due_date',                # Response due date
        'brief_description',       # Short description
        'analysis_notes',          # Analysis reasoning/notes
        'recommendation',          # Recommended action
        'special_action',          # Any special action needed
        'posted_date',             # When posted
        'naics',                   # NAICS code
        'psc',                     # Product/Service code
        'set_aside',               # Small business set-aside
        'value_low',               # Min value
        'value_high',              # Max value
        'place_of_performance',    # Location
        'doc_length',              # Document size
        'assessment_timestamp'     # When we assessed it
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in results:
            # Map to production format
            decision = result.get('model_decision', result.get('decision', 'UNKNOWN'))
            row = {
                'final_decision': decision,
                'knock_pattern': result.get('reasoning', '')[:100] if result.get('reasoning') else '',
                'knockout_category': 'KO-REGEX' if result.get('processing_method') == 'REGEX_ONLY' else 'BATCH',
                'sos_pipeline_title': f"PN: NA | Qty: NA | Condition: unknown | MDS: NA | {result.get('title', '')}",
                'highergov_url': '',
                'announcement_number': result.get('opportunity_id', ''),
                'announcement_title': result.get('title', ''),
                'agency': '',
                'due_date': '',
                'brief_description': result.get('reasoning', ''),
                'analysis_notes': result.get('reasoning', ''),
                'recommendation': '',
                'special_action': '',
                'posted_date': '',
                'naics': '',
                'psc': '',
                'set_aside': '',
                'value_low': '',
                'value_high': '',
                'place_of_performance': '',
                'doc_length': 0,
                'assessment_timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            }
            writer.writerow(row)
    
    print(f"Created {output_file}")
    
    # Also save a local copy for reference
    local_copy = f"batch_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    import shutil
    shutil.copy(output_file, local_copy)
    print(f"Local copy: {local_copy}")
    
    return output_file

def generate_summary_report(results: List[Dict]):
    """
    Generate summary statistics
    """
    total = len(results)
    go_count = sum(1 for r in results if r['model_decision'] == 'GO')
    nogo_count = sum(1 for r in results if r['model_decision'] == 'NO-GO')
    indeterminate_count = sum(1 for r in results if r['model_decision'] == 'INDETERMINATE')
    unknown_count = sum(1 for r in results if r['model_decision'] == 'UNKNOWN')
    
    print("\n" + "=" * 60)
    print("BATCH PROCESSING SUMMARY")
    print("=" * 60)
    print(f"Total Processed: {total}")
    print(f"  GO: {go_count} ({go_count/total*100:.1f}%)")
    print(f"  NO-GO: {nogo_count} ({nogo_count/total*100:.1f}%)")
    print(f"  INDETERMINATE: {indeterminate_count} ({indeterminate_count/total*100:.1f}%)")
    if unknown_count > 0:
        print(f"  UNKNOWN: {unknown_count} ({unknown_count/total*100:.1f}%)")
    print("=" * 60)

def main():
    """
    Main parsing flow
    """
    print("=" * 60)
    print("BATCH RESULTS PARSER")
    print("=" * 60)
    
    # Find results and metadata files
    results_files = [f for f in os.listdir('.') if f.startswith('batch_results_') and f.endswith('.jsonl')]
    metadata_files = [f for f in os.listdir('.') if f.startswith('batch_metadata_') and f.endswith('.json')]
    
    if not results_files:
        print("No batch_results_*.jsonl files found")
        print("Download results first using:")
        print("  python BATCH_SUBMITTER.py --download [batch_id]")
        return
    
    if not metadata_files:
        print("WARNING: No batch_metadata_*.json files found")
        print("Processing without regex knockout information")
        latest_metadata = None
    else:
        # Use most recent metadata
        latest_metadata = sorted(metadata_files)[-1]
        print(f"Using metadata: {latest_metadata}")
    
    # Use most recent results
    latest_results = sorted(results_files)[-1]
    print(f"Using results: {latest_results}")
    
    # Parse results (with or without metadata)
    if latest_metadata:
        results = parse_batch_results(latest_results, latest_metadata)
    else:
        results = parse_results_without_metadata(latest_results)
    
    if not results:
        print("No results parsed")
        return
    
    # Create CSV output
    csv_file = create_output_csv(results)
    
    # Generate summary
    generate_summary_report(results)
    
    # Save full results as JSON too
    json_file = csv_file.replace('.csv', '.json')
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nFull results saved to {json_file}")

if __name__ == "__main__":
    main()