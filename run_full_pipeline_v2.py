#!/usr/bin/env python3
"""
Full Pipeline v2: Proper folder structure and human-readable outputs
"""

import os
import json
import csv
from datetime import datetime
from highergov_batch_fetcher import HigherGovBatchFetcher
from mistral_api_connector import MistralSOSClassifier

def ensure_folder_structure():
    """Create the proper folder hierarchy"""
    base_folders = [
        "Results",
        "Results/Regex_Results",
        "Results/Model_Results"
    ]
    for folder in base_folders:
        os.makedirs(folder, exist_ok=True)
    return "Results"

def run_full_pipeline_v2(search_id: str, use_mistral: bool = True):
    """
    Complete pipeline with proper folder structure
    """
    
    print("="*60)
    print("SOS ASSESSMENT PIPELINE v2.1")
    print("="*60)
    print(f"Search ID: {search_id}")
    print(f"Mistral: {'ENABLED' if use_mistral else 'DISABLED'}")
    print("="*60)
    
    # Setup folders
    base_dir = ensure_folder_structure()
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    timestamp = now.strftime("%H%M%S")
    
    # Create dated subfolders: Results/[Type]/YYYY/MM/DD/
    if use_mistral:
        output_dir = f"{base_dir}/Model_Results/{year}/{month}/{day}"
    else:
        output_dir = f"{base_dir}/Regex_Results/{year}/{month}/{day}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Fetch from HigherGov
    print("\n[1/4] Fetching opportunities from HigherGov...")
    fetcher = HigherGovBatchFetcher()
    opportunities = fetcher.fetch_all_opportunities(search_id, max_pages=1)
    print(f"  -> Found {len(opportunities)} opportunities")
    
    if not opportunities:
        print("No opportunities found!")
        return
    
    # Step 2: Document fetching
    print("\n[2/4] Fetching full documents...")
    enriched = []
    for opp in opportunities[:10]:  # Limit for testing
        doc_text = fetcher.fetch_document_text(opp.get('id'))
        if doc_text:
            opp['full_text'] = doc_text
        enriched.append(opp)
    print(f"  -> Enriched {len(enriched)} opportunities with documents")
    
    # Step 3: Assessment
    print("\n[3/4] Running assessments...")
    
    if use_mistral and os.environ.get("MISTRAL_API_KEY"):
        classifier = MistralSOSClassifier(use_dummy=False)
        print("  -> Using hybrid Regex + SOS Agent")
    else:
        classifier = None
        print("  -> Using Regex only")
    
    results = {
        'go': [],
        'no_go': [],
        'further': [],
        'contact': []
    }
    
    all_assessments = []
    
    for opp in enriched:
        if classifier:
            # Hybrid assessment
            assessment = classifier.classify_opportunity(opp)
            decision = assessment['classification']
            reasoning = assessment['reasoning']
            confidence = assessment.get('confidence', 0)
            source = assessment['model_used']
        else:
            # Regex only
            from sos_ingestion_gate_v419 import IngestionGateV419
            gate = IngestionGateV419()
            regex_result = gate.assess_opportunity(opp)
            decision = regex_result.decision.value
            reasoning = regex_result.primary_blocker or "Pattern match"
            confidence = 75
            source = "REGEX_V14"
        
        # Store assessment
        opp['assessment'] = {
            'decision': decision,
            'reasoning': reasoning,
            'confidence': confidence,
            'source': source
        }
        
        all_assessments.append(opp)
        
        # Categorize
        if decision == 'GO':
            results['go'].append(opp)
        elif decision in ['NO-GO', 'NO_GO']:
            results['no_go'].append(opp)
        elif decision == 'CONTACT_CO':
            results['contact'].append(opp)
        else:
            results['further'].append(opp)
    
    # Step 4: Generate ALL outputs
    print("\n[4/4] Generating reports...")
    
    # 1. CSV FILE (ALWAYS GENERATED)
    csv_file = f"{output_dir}/Assessment_{search_id}_{timestamp}.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['decision', 'title', 'agency', 'confidence', 'reasoning', 
                     'naics', 'psc', 'set_aside', 'value_low', 'value_high', 
                     'doc_length', 'model_used']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for opp in all_assessments:
            agency_name = opp.get('agency', {}).get('agency_name', 'N/A') if isinstance(opp.get('agency'), dict) else opp.get('agency', 'N/A')
            writer.writerow({
                'decision': opp['assessment']['decision'],
                'title': opp.get('title', 'N/A'),
                'agency': agency_name,
                'confidence': opp['assessment']['confidence'],
                'reasoning': opp['assessment']['reasoning'][:200],
                'naics': opp.get('naics', ''),
                'psc': opp.get('psc', ''),
                'set_aside': opp.get('set_aside', ''),
                'value_low': opp.get('value_low', 0),
                'value_high': opp.get('value_high', 0),
                'doc_length': len(opp.get('full_text', '')),
                'model_used': opp['assessment']['source']
            })
    print(f"  -> CSV saved: {csv_file}")
    
    # 2. HUMAN READABLE REPORT (Markdown)
    report_file = f"{output_dir}/REPORT_{search_id}_{timestamp}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"# SOS Assessment Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Search ID:** {search_id}\n")
        f.write(f"**Assessment Type:** {'AI-Enhanced (Mistral)' if use_mistral else 'Regex Only'}\n\n")
        
        f.write("## Executive Summary\n\n")
        f.write(f"- **Total Assessed:** {len(all_assessments)}\n")
        f.write(f"- **GO:** {len(results['go'])} ({len(results['go'])/len(all_assessments)*100:.1f}%)\n")
        f.write(f"- **NO-GO:** {len(results['no_go'])} ({len(results['no_go'])/len(all_assessments)*100:.1f}%)\n")
        f.write(f"- **FURTHER ANALYSIS:** {len(results['further'])}\n")
        f.write(f"- **CONTACT CO:** {len(results['contact'])}\n\n")
        
        # GO Opportunities
        if results['go']:
            f.write("## 🟢 GO OPPORTUNITIES\n\n")
            for i, opp in enumerate(results['go'], 1):
                agency_name = opp.get('agency', {}).get('agency_name', 'N/A') if isinstance(opp.get('agency'), dict) else opp.get('agency', 'N/A')
                f.write(f"### {i}. {opp.get('title', 'N/A')}\n")
                f.write(f"- **Agency:** {agency_name}\n")
                f.write(f"- **Confidence:** {opp['assessment']['confidence']}%\n")
                f.write(f"- **Value Range:** ${opp.get('value_low', 0):,} - ${opp.get('value_high', 0):,}\n")
                f.write(f"- **Reasoning:** {opp['assessment']['reasoning']}\n\n")
        
        # NO-GO Opportunities (summary only)
        if results['no_go']:
            f.write("## 🔴 NO-GO OPPORTUNITIES\n\n")
            f.write("| Title | Agency | Reason |\n")
            f.write("|-------|--------|--------|\n")
            for opp in results['no_go']:
                agency_name = opp.get('agency', {}).get('agency_name', 'N/A') if isinstance(opp.get('agency'), dict) else opp.get('agency', 'N/A')
                reason = opp['assessment']['reasoning'][:100] + "..." if len(opp['assessment']['reasoning']) > 100 else opp['assessment']['reasoning']
                f.write(f"| {opp.get('title', 'N/A')} | {agency_name} | {reason} |\n")
            f.write("\n")
        
        # Further Analysis
        if results['further']:
            f.write("## ⚠️ REQUIRES FURTHER ANALYSIS\n\n")
            for opp in results['further']:
                agency_name = opp.get('agency', {}).get('agency_name', 'N/A') if isinstance(opp.get('agency'), dict) else opp.get('agency', 'N/A')
                f.write(f"- **{opp.get('title', 'N/A')}** ({agency_name})\n")
            f.write("\n")
    
    print(f"  -> Report saved: {report_file}")
    
    # 3. JSON for technical use
    json_file = f"{output_dir}/data_{search_id}_{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump({
            'metadata': {
                'search_id': search_id,
                'timestamp': datetime.now().isoformat(),
                'total_assessed': len(all_assessments),
                'model_used': use_mistral
            },
            'summary': {
                'go': len(results['go']),
                'no_go': len(results['no_go']),
                'further': len(results['further']),
                'contact': len(results['contact'])
            },
            'assessments': all_assessments
        }, f, indent=2, default=str)
    print(f"  -> JSON saved: {json_file}")
    
    # Print results
    print(f"\n{'='*60}")
    print("ASSESSMENT COMPLETE")
    print(f"{'='*60}")
    print(f"Total Assessed: {len(all_assessments)}")
    print(f"  GO: {len(results['go'])} ({len(results['go'])/len(all_assessments)*100:.1f}%)")
    print(f"  NO-GO: {len(results['no_go'])} ({len(results['no_go'])/len(all_assessments)*100:.1f}%)")
    print(f"  FURTHER: {len(results['further'])}")
    print(f"  CONTACT: {len(results['contact'])}")
    
    print(f"\nFiles saved to: {output_dir}/")
    print(f"  - {os.path.basename(csv_file)} (spreadsheet)")
    print(f"  - {os.path.basename(report_file)} (human readable)")
    print(f"  - {os.path.basename(json_file)} (technical data)")
    
    return results

def main():
    """Main entry point"""
    
    # Check setup
    if not os.environ.get("MISTRAL_API_KEY"):
        print("WARNING: MISTRAL_API_KEY not set - will use regex only")
        use_mistral = False
    else:
        use_mistral = True
    
    # Get search ID
    import sys
    if len(sys.argv) > 1:
        search_id = sys.argv[1]
    else:
        search_id = "gvCo0-K8fEbyI367g_HYp"
        print(f"No search ID provided, using test: {search_id}")
    
    # Run pipeline
    results = run_full_pipeline_v2(search_id, use_mistral=use_mistral)
    
    print("\n[OK] Pipeline complete!")

if __name__ == "__main__":
    main()