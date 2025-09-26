#!/usr/bin/env python3
"""
STANDARDIZED_OUTPUT_GENERATOR.py - Creates CSV that mirrors model JSON output exactly
Ensures complete standardization between model response and spreadsheet
"""

import json
import csv
import os
from datetime import datetime
from typing import List, Dict

def parse_model_response(response_content: str) -> Dict:
    """Parse model response and return standardized dict matching model format"""
    
    # Default structure matching model output
    standardized = {
        "solicitation_id": None,
        "solicitation_title": None,
        "type": None,
        "summary": None,
        "result": "INDETERMINATE",  # GO | NO-GO | INDETERMINATE
        "knock_out_reasons": [],
        "exceptions": [],
        "special_action": None,
        "rationale": None,
        "recommendation": "NO-GO",  # GO | NO-GO
        "sos_pipeline_title": "PN: NA | Qty: NA | Condition: unknown | MDS: NA | Description: NA",
        "highergov_link": "",
        "sam_link": ""
    }
    
    try:
        # Clean up response if needed
        if response_content.startswith('```json'):
            response_content = response_content.replace('```json', '').replace('```', '').strip()
        
        parsed = json.loads(response_content)
        
        # Map parsed data to standardized format
        # Handle both old format (decision/reasoning) and new format (result/rationale)
        if 'decision' in parsed:
            standardized['result'] = parsed.get('decision', 'INDETERMINATE')
            standardized['rationale'] = parsed.get('reasoning', '')
            standardized['recommendation'] = 'GO' if parsed.get('decision') == 'GO' else 'NO-GO'
        
        if 'result' in parsed:
            standardized['result'] = parsed['result']
        if 'rationale' in parsed:
            standardized['rationale'] = parsed['rationale']
        if 'recommendation' in parsed:
            standardized['recommendation'] = parsed['recommendation']
        if 'knock_out_reasons' in parsed:
            standardized['knock_out_reasons'] = parsed['knock_out_reasons']
        if 'sos_pipeline_title' in parsed:
            standardized['sos_pipeline_title'] = parsed['sos_pipeline_title']
        
        # Copy over any other fields that exist
        for key in ['solicitation_id', 'solicitation_title', 'type', 'summary', 
                   'exceptions', 'special_action', 'highergov_link', 'sam_link']:
            if key in parsed:
                standardized[key] = parsed[key]
                
    except Exception as e:
        print(f"Parse error: {e}")
        standardized['rationale'] = response_content[:500]  # Use raw content as rationale
    
    return standardized

def create_standardized_csv(batch_results_file: str, metadata_file: str = None, output_dir: str = None):
    """Create CSV that exactly mirrors model JSON output"""
    
    # Setup output directory
    if not output_dir:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        month_folder = datetime.now().strftime("%Y-%m")
        output_dir = f"../SOS_Output/{month_folder}/Run_{timestamp}_BATCH"
        os.makedirs(output_dir, exist_ok=True)
    
    # Load metadata if available
    metadata = {}
    opportunities_lookup = {}
    if metadata_file and os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
            # Create lookup for opportunities
            for opp in metadata.get('opportunities', []):
                key = f"opp-{opp['search_id']}-{opp['opportunity_id']}"
                opportunities_lookup[key] = opp
    
    # Process batch results
    all_results = []
    
    # Add regex knockouts first (if in metadata)
    for knockout in metadata.get('regex_knockouts', []):
        standardized = {
            "solicitation_id": knockout.get('opportunity_id'),
            "solicitation_title": knockout.get('title'),
            "type": "REGEX_KNOCKOUT",
            "summary": knockout.get('reasoning', ''),
            "result": "NO-GO",
            "knock_out_reasons": [knockout.get('knockout_patterns', 'Regex pattern match')],
            "exceptions": [],
            "special_action": None,
            "rationale": knockout.get('reasoning', ''),
            "recommendation": "NO-GO",
            "sos_pipeline_title": f"PN: NA | Qty: NA | Condition: unknown | MDS: NA | {knockout.get('title', '')}",
            "highergov_link": "",
            "sam_link": ""
        }
        all_results.append(standardized)
    
    # Process AI results
    with open(batch_results_file, 'r') as f:
        for line in f:
            result = json.loads(line)
            custom_id = result.get('custom_id', '')
            
            # Get original opportunity data
            base_id = '-'.join(custom_id.split('-')[:-1])
            opp_data = opportunities_lookup.get(base_id, {})
            
            # Extract and parse model response
            response_content = result['response']['body']['choices'][0]['message']['content']
            standardized = parse_model_response(response_content)
            
            # Add opportunity metadata
            standardized['solicitation_id'] = opp_data.get('opportunity_id', custom_id)
            standardized['solicitation_title'] = opp_data.get('title', '')
            standardized['type'] = "AI_ASSESSMENT"
            
            # Update pipeline title if we have title
            if opp_data.get('title'):
                standardized['sos_pipeline_title'] = f"PN: NA | Qty: NA | Condition: unknown | MDS: NA | {opp_data['title']}"
            
            all_results.append(standardized)
    
    # Write to CSV - columns match JSON structure exactly
    csv_file = f"{output_dir}/assessment.csv"
    fieldnames = [
        'solicitation_id',
        'solicitation_title', 
        'type',
        'summary',
        'result',  # GO | NO-GO | INDETERMINATE
        'knock_out_reasons',  # Will be stringified list
        'exceptions',  # Will be stringified list
        'special_action',
        'rationale',
        'recommendation',  # GO | NO-GO
        'sos_pipeline_title',
        'highergov_link',
        'sam_link'
    ]
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in all_results:
            # Convert lists to strings for CSV
            row = result.copy()
            row['knock_out_reasons'] = ', '.join(result.get('knock_out_reasons', []))
            row['exceptions'] = ', '.join(result.get('exceptions', []))
            writer.writerow(row)
    
    print(f"\nStandardized output saved to: {csv_file}")
    
    # Also save as JSON for perfect fidelity
    json_file = f"{output_dir}/assessment.json"
    with open(json_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"JSON output saved to: {json_file}")
    
    # Create Markdown report for NotebookLM and executive review
    md_file = f"{output_dir}/assessment.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("# SOS Opportunity Assessment Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Opportunities Assessed:** {len(all_results)}\n\n")
        
        # Executive Summary
        go_count = sum(1 for r in all_results if r['result'] == 'GO')
        nogo_count = sum(1 for r in all_results if r['result'] == 'NO-GO')
        indeterminate_count = sum(1 for r in all_results if r['result'] == 'INDETERMINATE')
        
        f.write("## Executive Summary\n\n")
        f.write(f"- **GO Opportunities:** {go_count}\n")
        f.write(f"- **NO-GO Opportunities:** {nogo_count}\n")
        f.write(f"- **Indeterminate (Needs Review):** {indeterminate_count}\n\n")
        
        # Quick Stats
        f.write("### Assessment Breakdown\n\n")
        f.write("| Result | Count | Percentage |\n")
        f.write("|--------|-------|------------|\n")
        f.write(f"| GO | {go_count} | {go_count/len(all_results)*100:.1f}% |\n")
        f.write(f"| NO-GO | {nogo_count} | {nogo_count/len(all_results)*100:.1f}% |\n")
        f.write(f"| INDETERMINATE | {indeterminate_count} | {indeterminate_count/len(all_results)*100:.1f}% |\n\n")
        
        # GO Opportunities (High Priority)
        go_opps = [r for r in all_results if r['result'] == 'GO']
        if go_opps:
            f.write("## 🟢 GO Opportunities (High Priority)\n\n")
            for i, opp in enumerate(go_opps, 1):
                f.write(f"### {i}. {opp['solicitation_title'] or 'Untitled'}\n\n")
                f.write(f"- **Solicitation ID:** {opp['solicitation_id'] or 'N/A'}\n")
                f.write(f"- **Recommendation:** {opp['recommendation']}\n")
                f.write(f"- **Rationale:** {opp['rationale'] or 'N/A'}\n")
                if opp['special_action']:
                    f.write(f"- **Special Action Required:** {opp['special_action']}\n")
                f.write(f"- **Pipeline Title:** {opp['sos_pipeline_title']}\n")
                if opp['highergov_link']:
                    f.write(f"- **HigherGov Link:** [{opp['solicitation_id']}]({opp['highergov_link']})\n")
                f.write("\n---\n\n")
        
        # Indeterminate (Needs Review)
        indeterminate_opps = [r for r in all_results if r['result'] == 'INDETERMINATE']
        if indeterminate_opps[:10]:  # Show first 10
            f.write("## 🟡 INDETERMINATE Opportunities (Needs Review)\n\n")
            f.write(f"*Showing first 10 of {len(indeterminate_opps)} opportunities requiring further analysis*\n\n")
            for i, opp in enumerate(indeterminate_opps[:10], 1):
                f.write(f"### {i}. {opp['solicitation_title'] or 'Untitled'}\n\n")
                f.write(f"- **Solicitation ID:** {opp['solicitation_id'] or 'N/A'}\n")
                f.write(f"- **Rationale:** {opp['rationale'] or 'Insufficient information for assessment'}\n")
                f.write(f"- **Pipeline Title:** {opp['sos_pipeline_title']}\n")
                f.write("\n")
        
        # NO-GO Summary
        nogo_opps = [r for r in all_results if r['result'] == 'NO-GO']
        if nogo_opps:
            f.write(f"\n## 🔴 NO-GO Opportunities Summary\n\n")
            f.write(f"Total NO-GO opportunities: {len(nogo_opps)}\n\n")
            
            # Group by knockout reason
            knockout_reasons = {}
            for opp in nogo_opps:
                reasons = opp.get('knock_out_reasons', ['Other'])
                for reason in reasons:
                    if reason not in knockout_reasons:
                        knockout_reasons[reason] = 0
                    knockout_reasons[reason] += 1
            
            if knockout_reasons:
                f.write("### Knockout Reasons Distribution\n\n")
                f.write("| Reason | Count |\n")
                f.write("|--------|-------|\n")
                for reason, count in sorted(knockout_reasons.items(), key=lambda x: x[1], reverse=True):
                    f.write(f"| {reason} | {count} |\n")
                f.write("\n")
        
        # Processing Notes
        f.write("## Processing Notes\n\n")
        f.write("- **Processing Method:** Mistral Batch API with Regex Pre-filtering\n")
        f.write("- **Model:** Fine-tuned SOS Assessment Model\n")
        f.write("- **Regex Patterns:** 497 patterns across 19 categories\n")
        f.write("- **Document Coverage:** Up to 400K characters per opportunity\n\n")
        
        # Footer
        f.write("---\n\n")
        f.write("*This report was automatically generated by the SOS Assessment Automation Tool.*\n")
        f.write("*For questions or concerns, please contact the assessment team.*\n")
    
    print(f"Markdown report saved to: {md_file}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("STANDARDIZED OUTPUT SUMMARY")
    print("=" * 60)
    print(f"Total records: {len(all_results)}")
    go_count = sum(1 for r in all_results if r['result'] == 'GO')
    nogo_count = sum(1 for r in all_results if r['result'] == 'NO-GO')
    indeterminate_count = sum(1 for r in all_results if r['result'] == 'INDETERMINATE')
    print(f"Results: GO={go_count}, NO-GO={nogo_count}, INDETERMINATE={indeterminate_count}")
    print("=" * 60)
    
    return csv_file

def main():
    """Process most recent batch results with standardized output"""
    import glob
    
    # Find most recent batch results
    results_files = glob.glob('batch_results_*.jsonl')
    if not results_files:
        print("No batch results files found")
        return
    
    latest_results = sorted(results_files)[-1]
    print(f"Processing: {latest_results}")
    
    # Find corresponding metadata
    timestamp = latest_results.replace('batch_results_', '').replace('.jsonl', '')
    metadata_files = glob.glob(f'batch_metadata_*.json')
    latest_metadata = None
    if metadata_files:
        latest_metadata = sorted(metadata_files)[-1]
        print(f"Using metadata: {latest_metadata}")
    
    # Create standardized output
    create_standardized_csv(latest_results, latest_metadata)

if __name__ == "__main__":
    main()