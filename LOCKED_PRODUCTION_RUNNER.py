#!/usr/bin/env python3
"""
PRODUCTION RUNNER WITH FULL AI INTEGRATION
This is the CORRECT runner that uses:
1. Document fetching (700KB+ per opportunity) 
2. Regex engine v4.19 (497 patterns)
3. Mistral AI model (for non-knocked-out opportunities)
4. Proper CSV output with model analysis
"""

import os
import sys
from datetime import datetime

# Set API key
try:
    from API_KEYS import MISTRAL_API_KEY
    os.environ["MISTRAL_API_KEY"] = MISTRAL_API_KEY
except:
    pass

# Optional: load centralized configuration (env > settings > defaults)
try:
    from config.loader import get_config  # type: ignore
    _cfg = get_config()
    # Respect existing env if already set
    if not os.environ.get("MISTRAL_API_KEY") and _cfg.get("mistral.api_key"):
        os.environ["MISTRAL_API_KEY"] = str(_cfg.get("mistral.api_key"))
    if not os.environ.get("HIGHERGOV_API_KEY") and _cfg.get("highergov.api_key"):
        os.environ["HIGHERGOV_API_KEY"] = str(_cfg.get("highergov.api_key"))
    # Base URLs (optional)
    if not os.environ.get("HG_API_BASE_URL") and _cfg.get("highergov.base_url"):
        os.environ["HG_API_BASE_URL"] = str(_cfg.get("highergov.base_url"))
    if not os.environ.get("MISTRAL_API_BASE_URL") and _cfg.get("mistral.base_url"):
        os.environ["MISTRAL_API_BASE_URL"] = str(_cfg.get("mistral.base_url"))
except Exception:
    # Silent fallback to existing behavior
    pass

from highergov_batch_fetcher import HigherGovBatchFetcher
from sos_ingestion_gate_v419 import IngestionGateV419
from ULTIMATE_MISTRAL_CONNECTOR import MistralSOSClassifier
from enhanced_output_manager import EnhancedOutputManager
from pipeline_title_generator import PipelineTitleGenerator
try:
    from master_analytics_tracker import MasterAnalyticsTracker
except:
    MasterAnalyticsTracker = None

def main():
    """PRODUCTION RUNNER WITH AI"""
    
    if len(sys.argv) < 2:
        print("\n" + "="*70)
        print("PRODUCTION RUNNER WITH AI INTEGRATION")
        print("="*70)
        print("\nUsage: python PRODUCTION_RUNNER_WITH_AI.py SEARCH_ID")
        print("\nThis runner uses:")
        print("  1. Full document fetching (700KB+ per opportunity)")
        print("  2. Regex engine v4.19 (497 patterns)")
        print("  3. Mistral AI model for detailed analysis")
        print("  4. Proper CSV with model reasoning")
        print("="*70)
        return
    
    search_id = sys.argv[1]
    
    print("="*70)
    print("PRODUCTION ASSESSMENT WITH AI")
    print("="*70)
    print(f"Search ID: {search_id}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("="*70)
    
    # Step 1: Fetch opportunities with documents
    print("\n[1/5] Fetching opportunities from HigherGov...")
    fetcher = HigherGovBatchFetcher()
    raw_opportunities = fetcher.fetch_all_opportunities(search_id)
    
    if not raw_opportunities:
        print("ERROR: No opportunities found")
        return
    
    print(f"  Found {len(raw_opportunities)} opportunities")
    
    # Step 2: Process to extract documents
    print("\n[2/5] Processing documents...")
    opportunities = []
    total_text_length = 0
    docs_found = 0
    
    for opp in raw_opportunities:
        processed = fetcher.process_opportunity(opp)
        text_len = len(processed.get('text', ''))
        total_text_length += text_len
        
        if text_len > 10000:  # Has substantial docs
            docs_found += 1
        
        opportunities.append(processed)
    
    avg_text = total_text_length // len(opportunities) if opportunities else 0
    print(f"  Document coverage: {docs_found}/{len(opportunities)}")
    print(f"  Average text size: {avg_text:,} chars")
    print(f"  Total text: {total_text_length:,} chars")
    
    # Step 3: Initialize processors
    print("\n[3/5] Initializing assessment engines...")
    regex_gate = IngestionGateV419()
    mistral_classifier = MistralSOSClassifier()
    title_generator = PipelineTitleGenerator()
    
    print("  [OK] Regex engine loaded (497 patterns)")
    print("  [OK] Mistral AI connected")
    print("  [OK] Pipeline title generator ready")
    
    # Step 4: Assess each opportunity
    print("\n[4/5] Assessing opportunities...")
    results = []
    go_count = 0
    no_go_count = 0
    indeterminate_count = 0
    
    for i, opp in enumerate(opportunities):
        title = opp.get('title', '')[:60]
        
        # First: Run regex assessment
        regex_result = regex_gate.assess_opportunity(opp)
        
        # Generate pipeline title from document
        pipeline_title = title_generator.generate_title(opp)
        
        # If regex says NO-GO, use that
        if regex_result.decision.value == 'NO-GO':
            decision = 'NO-GO'
            reasoning = regex_result.primary_blocker or 'Regex knockout'
            detailed_analysis = f"Hard knockout by regex: {regex_result.primary_blocker}"
            full_response = ''  # No model call for regex knockouts
            # Removed confidence - we don't calculate it
            print(f"  [{decision}] (Regex) {title}")
            no_go_count += 1
        else:
            # Send to AI model for detailed analysis
            try:
                model_result = mistral_classifier.classify_opportunity(opp, bypass_regex=False)
                # Use unified schema fields (result, rationale) with fallback to old names
                decision = model_result.get('result', model_result.get('classification', 'INDETERMINATE'))
                reasoning = model_result.get('rationale', model_result.get('reasoning', ''))
                detailed_analysis = model_result.get('detailed_analysis', '')
                # Removed confidence - model doesn't calculate it
                full_response = model_result.get('full_model_response', '')
                
                # Use model's pipeline title if better
                if model_result.get('sos_pipeline_title') and 'NA' not in model_result.get('sos_pipeline_title'):
                    pipeline_title = model_result['sos_pipeline_title']
                
                print(f"  [{decision}] (AI) {title}")
                
                if decision == 'GO':
                    go_count += 1
                elif decision == 'NO-GO':
                    no_go_count += 1
                else:
                    indeterminate_count += 1
                    
            except Exception as e:
                print(f"  [ERROR] Model failed for {title}: {e}")
                decision = 'INDETERMINATE'
                reasoning = 'Model error - needs manual review'
                detailed_analysis = str(e)
                # Error case - no confidence
                indeterminate_count += 1
        
        # Add assessment to opportunity
        opp['assessment'] = {
            'decision': decision,
            'reasoning': reasoning,
            'detailed_analysis': detailed_analysis,  # THIS is what populates analysis_notes
            'full_model_response': full_response if 'full_response' in locals() else '',  # FULL MODEL OUTPUT
            'sos_pipeline_title': pipeline_title,
            # Removed confidence field
            'knockout_category': regex_result.primary_blocker_category if regex_result else 'MODEL',
            'timestamp': datetime.now().isoformat()
        }
        
        results.append(opp)
    
    # Step 5: Save results
    print(f"\n[5/5] Saving results...")
    output_manager = EnhancedOutputManager()
    
    # Create metadata
    metadata = {
        'search_id': search_id,
        'total': len(results),
        'go_count': go_count,
        'no_go_count': no_go_count,
        'indeterminate_count': indeterminate_count,
        'avg_doc_size': avg_text,
        'timestamp': datetime.now().isoformat()
    }
    
    # Save everything
    output_dir = output_manager.save_assessment_batch(search_id, results, metadata)
    
    # Update master analytics if available
    if MasterAnalyticsTracker:
        try:
            tracker = MasterAnalyticsTracker()
            csv_path = output_dir / "assessment.csv"
            if csv_path.exists():
                tracker.update_master_database(csv_path)
                print("  [OK] Master analytics updated")
        except Exception as e:
            print(f"  [WARNING] Could not update master analytics: {e}")
    
    # Final summary
    print("\n" + "="*70)
    print("ASSESSMENT COMPLETE")
    print("="*70)
    print(f"Results: GO={go_count}, NO-GO={no_go_count}, INDETERMINATE={indeterminate_count}")
    print(f"Output: {output_dir}")
    print(f"Document Coverage: {docs_found}/{len(opportunities)} ({avg_text:,} chars avg)")
    print("\nKey files generated:")
    print(f"  - assessment.csv - Open in Excel")
    print(f"  - mistral_full_reports.md - Full AI analysis")
    print(f"  - report.md - Summary report")
    print("="*70)

if __name__ == "__main__":
    main()
