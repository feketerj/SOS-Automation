"""
Enhanced Main Pipeline with Comprehensive Logging and Error Handling
Demonstrates proper logging integration for debugging and maintenance
"""

import os
import json
import datetime
from pathlib import Path
from enhanced_logging import (
    initialize_logging, 
    FilterDecisionLogger, 
    timing_decorator, 
    error_handler,
    create_session_summary
)
from api_clients.highergov_client_enhanced import EnhancedHigherGovClient
from filters.initial_checklist_v2 import InitialChecklistFilterV2, Decision
import logging

# Initialize comprehensive logging system
initialize_logging("INFO")  # Change to "DEBUG" for more detailed logs

# Get loggers
main_logger = logging.getLogger('sos_pipeline')
api_logger = logging.getLogger('sos_pipeline.api')
filter_logger = logging.getLogger('sos_pipeline.filter')
error_logger = logging.getLogger('sos_pipeline.errors')
perf_logger = logging.getLogger('sos_pipeline.performance')

# Initialize specialized loggers
filter_decision_logger = FilterDecisionLogger()

OUTPUT_DIR = "output"
HIGHERGOV_API_KEY = os.getenv('HIGHERGOV_API_KEY')
SAVED_SEARCH_ID = os.getenv('SAVED_SEARCH_ID')

@timing_decorator
@error_handler
def initialize_components():
    """Initialize API client and filter with error handling"""
    main_logger.info("Initializing pipeline components...")
    
    if not HIGHERGOV_API_KEY:
        error_logger.error("HIGHERGOV_API_KEY not found in environment variables")
        raise ValueError("Missing HIGHERGOV_API_KEY")
    
    if not SAVED_SEARCH_ID:
        error_logger.error("SAVED_SEARCH_ID not found in environment variables")
        raise ValueError("Missing SAVED_SEARCH_ID")
    
    api_logger.info(f"Using API key: {HIGHERGOV_API_KEY[-4:]}...")
    api_logger.info(f"Using saved search ID: {SAVED_SEARCH_ID}")
    
    client = EnhancedHigherGovClient(api_key=HIGHERGOV_API_KEY)
    filter_obj = InitialChecklistFilterV2()
    
    main_logger.info("Components initialized successfully")
    return client, filter_obj

@timing_decorator  
@error_handler
def fetch_opportunities(client, limit=100):
    """Fetch opportunities with comprehensive logging"""
    main_logger.info(f"Fetching opportunities (limit: {limit})")
    api_logger.info(f"Making API call to saved search: {SAVED_SEARCH_ID}")
    
    try:
        opportunities = client.get_saved_search_opportunities(SAVED_SEARCH_ID, limit=limit)
        
        if not opportunities:
            api_logger.warning("No opportunities returned from API")
            return []
        
        api_logger.info(f"Successfully fetched {len(opportunities)} opportunities")
        
        # Log sample opportunity structure for debugging
        if opportunities:
            sample_keys = list(opportunities[0].keys())[:10]  # First 10 keys
            api_logger.debug(f"Sample opportunity structure: {sample_keys}")
        
        return opportunities
        
    except Exception as e:
        api_logger.error(f"Failed to fetch opportunities: {str(e)}")
        error_logger.error(f"API fetch failed: {str(e)}", exc_info=True)
        raise

@error_handler
def enhanced_assess_opportunity(filter_obj, opportunity):
    """Enhanced opportunity assessment with detailed logging"""
    opp_id = opportunity.get('id', 'UNKNOWN')
    opp_title = opportunity.get('title', 'NO TITLE')[:50]
    
    filter_logger.info(f"Starting assessment for {opp_id}: {opp_title}")
    
    try:
        # Run the assessment with enhanced logging - V2 API returns (decision, detailed_results)
        final_decision, detailed_results = filter_obj.assess_opportunity(opportunity)
        
        # Log detailed decision breakdown
        filter_decision_logger.log_final_decision(opp_id, final_decision.value, str([r.reason for r in detailed_results]))
        
        # Log each check result for debugging
        for result in detailed_results:
            if result.decision != Decision.PASS:
                status = result.decision == Decision.GO
                if "Phase" in result.check_name or "Aviation" in result.check_name or "Platform" in result.check_name:
                    filter_decision_logger.log_phase_0_decision(
                        opp_id, result.check_name, status, result.reason
                    )
                else:
                    filter_decision_logger.log_phase_1_decision(
                        opp_id, result.check_name, status, result.reason
                    )
        
        # Track pattern enhancement opportunities
        if final_decision == Decision.NO_GO:
            full_text = opportunity.get('description', '') + ' ' + opportunity.get('title', '')
            if len(full_text) > 100:  # Only log if substantial text available
                filter_decision_logger.log_pattern_enhancement_opportunity(
                    opp_id, "v2_no_go_pattern", "V2 assessment resulted in NO-GO", full_text[:500]
                )
        
        # Return result in compatible format for the rest of the pipeline
        class CompatResult:
            def __init__(self, decision, details):
                self.decision = decision.value
                self.detailed_results = details
                self.reasoning = [r.reason for r in details if r.decision != Decision.PASS]
        
        return CompatResult(final_decision, detailed_results)
        
    except Exception as e:
        error_logger.error(f"Assessment failed for {opp_id}: {str(e)}", exc_info=True)
        filter_logger.error(f"ASSESSMENT_ERROR | {opp_id} | {str(e)}")
        raise

@timing_decorator
@error_handler
def save_detailed_results(opportunity, result, output_dir):
    """Save results with error handling and logging"""
    opp_id = opportunity.get('id', 'UNKNOWN')
    
    try:
        # Create output directory
        Path(output_dir).mkdir(exist_ok=True)
        
        # Prepare detailed results
        detailed_results = {
            "opportunity_id": opp_id,
            "opportunity_title": opportunity.get('title', 'NO TITLE'),
            "final_decision": result.decision,
            "phase_0": result.phase_0,
            "phase_1": result.phase_1,
            "reasoning": result.reasoning,
            "full_opportunity_data": opportunity,
            "assessment_timestamp": datetime.datetime.now().isoformat(),
            "filter_version": "sos_official_filter_v1.0"
        }
        
        # Save to file
        file_path = Path(output_dir) / f"{opp_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(detailed_results, f, indent=2, ensure_ascii=False)
        
        main_logger.debug(f"Results saved to {file_path}")
        return file_path
        
    except Exception as e:
        error_logger.error(f"Failed to save results for {opp_id}: {str(e)}", exc_info=True)
        raise

@timing_decorator
def main():
    """Enhanced main pipeline with comprehensive error handling and logging"""
    session_start = datetime.datetime.now()
    main_logger.info("=" * 80)
    main_logger.info("🚀 SOS OPPORTUNITY ASSESSMENT PIPELINE - ENHANCED VERSION")
    main_logger.info("=" * 80)
    
    # Counters for session summary
    total_opportunities = 0
    go_count = 0
    no_go_count = 0
    errors_count = 0
    
    try:
        # Initialize components
        client, filter_obj = initialize_components()
        
        # Create output directory
        Path(OUTPUT_DIR).mkdir(exist_ok=True)
        main_logger.info(f"Output directory: {Path(OUTPUT_DIR).absolute()}")
        
        # Fetch opportunities
        opportunities = fetch_opportunities(client, limit=100)
        total_opportunities = len(opportunities)
        
        if not opportunities:
            main_logger.warning("No opportunities to process. Exiting.")
            return
        
        main_logger.info(f"Processing {total_opportunities} opportunities...")
        
        # Process each opportunity
        for i, opportunity in enumerate(opportunities, 1):
            opp_id = opportunity.get('id', f'UNK_{i}')
            opp_title = opportunity.get('title', 'NO TITLE')[:50]
            
            try:
                main_logger.info("=" * 80)
                main_logger.info(f"Processing {i}/{total_opportunities}: {opp_title} ({opp_id})")
                
                # Assess opportunity
                result = enhanced_assess_opportunity(filter_obj, opportunity)
                
                # Count results
                if result.decision == "GO":
                    go_count += 1
                else:
                    no_go_count += 1
                
                # Display decision summary
                print(f"FINAL DECISION: [{result.decision}]")
                print("-" * 20)
                
                # Show phase results
                print("Phase 0 (Preliminary Gates):")
                for check, outcome in result.phase_0.items():
                    status = "PASS" if "PASS" in outcome else "FAIL"
                    print(f"  - {check}: {status} - {outcome.split(' - ', 1)[-1] if ' - ' in outcome else outcome}")
                
                if any("FAIL" not in outcome for outcome in result.phase_0.values()):
                    print("Phase 1 (Hard Stops):")
                    for check, outcome in result.phase_1.items():
                        status = "PASS" if "PASS" in outcome else "FAIL"
                        print(f"  - {check}: {status} - {outcome.split(' - ', 1)[-1] if ' - ' in outcome else outcome}")
                
                print("Reasoning:")
                for reason in result.reasoning:
                    print(f"  - {reason}")
                
                # Save detailed results
                file_path = save_detailed_results(opportunity, result, OUTPUT_DIR)
                main_logger.info(f"Results saved to {file_path}")
                
            except Exception as e:
                errors_count += 1
                error_logger.error(f"Failed to process opportunity {opp_id}: {str(e)}", exc_info=True)
                main_logger.error(f"❌ Error processing {opp_id}: {str(e)}")
                continue
        
        # Create session summary
        create_session_summary(session_start, total_opportunities, go_count, no_go_count, errors_count)
        
        # Final summary
        main_logger.info("=" * 80)
        main_logger.info("📊 PIPELINE SUMMARY")
        main_logger.info(f"Total Processed: {total_opportunities}")
        main_logger.info(f"GO Decisions: {go_count}")
        main_logger.info(f"NO-GO Decisions: {no_go_count}")
        if total_opportunities > 0:
            success_rate = (go_count / total_opportunities) * 100
            main_logger.info(f"Success Rate: {success_rate:.2f}%")
        main_logger.info(f"Errors: {errors_count}")
        main_logger.info("=" * 80)
        
    except Exception as e:
        errors_count += 1
        error_logger.error(f"Pipeline failed with critical error: {str(e)}", exc_info=True)
        main_logger.error(f"💥 Critical pipeline failure: {str(e)}")
        raise
    
    finally:
        # Always log completion
        duration = datetime.datetime.now() - session_start
        main_logger.info(f"Pipeline completed in {duration}")
        main_logger.info("Check logs directory for detailed debugging information")

if __name__ == "__main__":
    main()
