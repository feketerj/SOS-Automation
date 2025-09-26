#!/usr/bin/env python3
"""
FULL_BATCH_PROCESSOR.py - Complete end-to-end batch processing pipeline
Reads endpoints.txt, applies regex filtering, batch processes with Mistral, generates output
"""

import json
import os
import sys
import time
from datetime import datetime
from mistralai import Mistral

# Add parent directory to path
sys.path.append('..')

# HARDWIRED CONFIGURATION - PRIVATE CLIENT APP
API_KEY = "2oAquITdDMiyyk0OfQuJSSqePn3SQbde"  # Mistral API key
MODEL = "ft:pixtral-12b-latest:d42144c7:20250912:f7d61150"  # Fine-tuned Pixtral model

def phase1_collect_opportunities():
    """Phase 1: Collect opportunities and apply regex filtering"""
    print("\n" + "=" * 70)
    print("PHASE 1: COLLECTING OPPORTUNITIES AND APPLYING APP FILTER")
    print("=" * 70)

    try:
        from highergov_batch_fetcher import HigherGovBatchFetcher
    except ImportError:
        print("WARNING: highergov_batch_fetcher not found, creating minimal version")
        # Create minimal fetcher class inline
        class HigherGovBatchFetcher:
            def fetch_all_opportunities(self, search_id):
                return []  # Return empty list to continue
            def fetch_document_text(self, doc_path):
                return ""  # Return empty text

    try:
        from sos_ingestion_gate_v419 import IngestionGateV419, Decision
    except ImportError:
        print("WARNING: sos_ingestion_gate_v419 not found, creating minimal version")
        # Create minimal gate class inline
        from enum import Enum

        class Decision(Enum):
            GO = "GO"
            NO_GO = "NO-GO"
            FURTHER_ANALYSIS = "FURTHER_ANALYSIS"
            CONTACT_CO = "CONTACT_CO"
        class IngestionGateV419:
            def assess_opportunity(self, opp):
                class Result:
                    decision = Decision.FURTHER_ANALYSIS
                    primary_blocker = None
                return Result()




    # Read endpoints - check for test file first
    test_endpoints_file = '../test_endpoints.txt'
    endpoints_file = '../endpoints.txt'

    if os.path.exists(test_endpoints_file):
        endpoints_file = test_endpoints_file
        print(f"Using TEST endpoints from: {test_endpoints_file}")

    if not os.path.exists(endpoints_file):
        print("ERROR: endpoints.txt not found")
        return None, None

    with open(endpoints_file, 'r') as f:
        search_ids = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    print(f"Found {len(search_ids)} search IDs to process")

    # Initialize components
    fetcher = HigherGovBatchFetcher()
    regex_gate = IngestionGateV419()

    opportunities_for_ai = []
    regex_knockouts = []

    for idx, search_id in enumerate(search_ids, 1):
        print(f"\n[{idx}/{len(search_ids)}] Processing {search_id}...")

        try:
            # Fetch opportunities
            opportunities = fetcher.fetch_all_opportunities(search_id)
            print(f"  Fetched {len(opportunities)} opportunities")

            for opp in opportunities:
                print(f"    Processing: {opp.get('title', 'Unknown')[:40]}...")
                try:
                    # Process opportunity (this handles document fetching internally)
                    processed = fetcher.process_opportunity(opp)
                    document_text = processed.get('text') or ""
                    if document_text:
                        print(f"      Document size: {len(document_text):,} chars")
                    else:
                        print("      No document text available")
                    # Apply regex filter on processed opportunity
                    regex_result = regex_gate.assess_opportunity(processed)
                except Exception as opp_error:
                    print(f"      [ERROR] Skipping opportunity due to processing failure: {opp_error}")
                    continue
                if regex_result.decision == Decision.NO_GO:
                    # Knocked out by regex - save with all metadata
                    regex_knockouts.append({
                        'search_id': search_id,
                        'opportunity_id': processed.get('id', opp.get('opportunity_id', 'unknown')),
                        'title': processed.get('title', ''),
                        'decision': Decision.NO_GO.value,
                        'regex_decision': Decision.NO_GO.value,
                        'reasoning': f"Regex knockout: {regex_result.primary_blocker}",
                        'processing_method': 'APP_ONLY',
                        'agency': processed.get('agency', 'Unknown'),
                        'announcement_number': processed.get('id', ''),
                        'announcement_title': processed.get('title', ''),
                        'due_date': processed.get('due_date', ''),
                        'posted_date': processed.get('posted_date', ''),
                        'naics': processed.get('naics', ''),
                        'psc': processed.get('psc', ''),
                        'set_aside': processed.get('set_aside', ''),
                        'value_low': processed.get('value_low', 0),
                        'value_high': processed.get('value_high', 0),
                        'place_of_performance': processed.get('place_of_performance', ''),
                        'doc_length': len(document_text) if document_text else 0
                    })
                    print(f"      APP KNOCKOUT: {regex_result.primary_blocker}")
                else:
                    # Needs AI assessment - preserve ALL opportunity data
                    opp_with_metadata = {
                        'search_id': search_id,
                        'opportunity_id': processed.get('id', opp.get('opportunity_id', 'unknown')),
                        'title': processed.get('title', ''),
                        'text': document_text[:400000],  # Limit to 400K chars
                        'regex_decision': regex_result.decision.value,
                        'agency': processed.get('agency', 'Unknown'),
                        'announcement_number': processed.get('id', ''),
                        'announcement_title': processed.get('title', ''),
                        'due_date': processed.get('due_date', ''),
                        'posted_date': processed.get('posted_date', ''),
                        'naics': processed.get('naics', ''),
                        'psc': processed.get('psc', ''),
                        'set_aside': processed.get('set_aside', ''),
                        'value_low': processed.get('value_low', 0),
                        'value_high': processed.get('value_high', 0),
                        'place_of_performance': processed.get('place_of_performance', ''),
                        'doc_length': len(document_text) if document_text else 0
                    }
                    opportunities_for_ai.append(opp_with_metadata)
                    print(f"      Needs AI assessment")

        except Exception as e:
            print(f"  ERROR processing {search_id}: {e}")

    print(f"\n" + "=" * 70)
    print(f"PHASE 1 COMPLETE:")
    print(f"  Opportunities needing AI: {len(opportunities_for_ai)}")
    print(f"  Regex knockouts: {len(regex_knockouts)}")
    print(f"  Total processed: {len(opportunities_for_ai) + len(regex_knockouts)}")
    print("=" * 70)

    return opportunities_for_ai, regex_knockouts

def phase2_create_batch_file(opportunities):
    """Phase 2: Create JSONL file for Mistral batch processing"""
    print("\n" + "=" * 70)
    print("PHASE 2: CREATING BATCH FILE WITH SYSTEM PROMPT + FEW-SHOT EXAMPLES")
    print("=" * 70)

    # Optional: respect batch size limit from centralized config
    try:
        from config.loader import get_config  # type: ignore
        _cfg = get_config()
        _limit = _cfg.get('pipeline.batch_size_limit')
        if _limit:
            try:
                lim = int(_limit)
                if lim > 0:
                    opportunities = opportunities[:lim]
                    print(f"[INFO] Applying batch size limit: {lim}")
            except Exception:
                pass
    except Exception:
        pass

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    jsonl_file = f"batch_input_{timestamp}.jsonl"

    # Load the batch-specific prompt (GO/INDETERMINATE only, no NO-GO)
    system_prompt_path = os.path.join(
        os.path.dirname(__file__),
        "Mistral-Batch-Prompts-Training-Data",
        "SOS-Batch-Triage-Prompt.md"  # Batch AI should never return NO-GO
    )

    # Read the system prompt if available
    try:
        with open(system_prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = f.read().strip()
        print(f"[OK] Loaded system prompt from {system_prompt_path}")
        print(f"     System prompt length: {len(system_prompt)} characters")
    except Exception as e:
        # Fallback to essential system prompt
        system_prompt = """You are an expert in commercial aircraft spares and government contracting at Source One Spares (SOS). Your role is to evaluate government contracting opportunities and make an evidence-based decision according to SOS rules.

You must evaluate the **entire opportunity** against the checklist, regardless of early disqualifiers."""
        print(f"! Using fallback system prompt ({e})")

    # Load few-shot examples
    try:
        few_shot_path = os.path.join(
            os.path.dirname(__file__),
            "Mistral-Batch-Prompts-Training-Data",
            "few_shot_examples.py"
        )
        import sys
        sys.path.insert(0, os.path.dirname(few_shot_path))
        from few_shot_examples import get_few_shot_messages
        few_shot_messages = get_few_shot_messages()
        print(f"[OK] Loaded {len(few_shot_messages)//2} few-shot examples")
    except Exception as e:
        print(f"! No few-shot examples loaded ({e})")
        few_shot_messages = []

    with open(jsonl_file, 'w') as f:
        for i, opp in enumerate(opportunities):
            # Create user prompt with just the opportunity data
            user_prompt = f"""Analyze this government contracting opportunity for Source One Spares:

Title: {opp['title']}
Agency: {opp.get('agency', 'N/A')}
NAICS: {opp.get('naics', 'N/A')}
PSC: {opp.get('psc', 'N/A')}

Requirements excerpt: {opp['text'][:400000]}"""

            # Build messages array with system prompt, few-shot examples, then actual query
            messages = [
                {"role": "system", "content": system_prompt}
            ]

            # Add few-shot examples if available
            if few_shot_messages:
                messages.extend(few_shot_messages)

            # Add the actual opportunity to evaluate
            messages.append({"role": "user", "content": user_prompt})

            # Create batch request with full message chain
            batch_request = {
                "custom_id": f"opp-{opp['search_id']}-{opp['opportunity_id']}-{i:04d}",
                "body": {
                    "model": MODEL,
                    "messages": messages,
                    "temperature": 0.1,
                    "max_tokens": 2000
                }
            }

            f.write(json.dumps(batch_request) + '\n')

    print(f"Created {jsonl_file} with {len(opportunities)} requests")
    print(f"  Each request contains: system prompt + {len(few_shot_messages)//2} examples + user query")
    return jsonl_file, timestamp

def phase3_submit_to_mistral(jsonl_file):
    """Phase 3: Submit batch to Mistral API"""
    print("\n" + "=" * 70)
    print("PHASE 3: SUBMITTING TO MISTRAL")
    print("=" * 70)
    
    # Show which API key source is being used
    if 'MISTRAL_API_KEY' in os.environ:
        print('API key source: environment variable MISTRAL_API_KEY')
    elif 'cfg' in locals() and isinstance(cfg, dict) and cfg.get('mistral.api_key'):
        print('API key source: config.mistral.api_key')
    else:
        print('API key source: API_KEYS.MISTRAL_API_KEY')

    client = Mistral(api_key=API_KEY)

    # Upload file
    print("Uploading file to Mistral...")
    with open(jsonl_file, 'rb') as f:
        batch_data = client.files.upload(
            file={
                "file_name": os.path.basename(jsonl_file),
                "content": f.read()
            },
            purpose="batch"
        )

    print(f"File uploaded: {batch_data.id}")

    # Create batch job
    print("Creating batch job...")
    batch_job = client.batch.jobs.create(
        input_files=[batch_data.id],
        model=MODEL,
        endpoint="/v1/chat/completions",
        metadata={
            "job_type": "sos_batch_assessment",
            "created": datetime.now().isoformat()
        }
    )

    print(f"Batch job created: {batch_job.id}")
    print(f"Status: {batch_job.status}")

    return batch_job.id, client

def phase4_monitor_and_download(batch_id, client):
    """Phase 4: Monitor batch progress and download results"""
    print("\n" + "=" * 70)
    print("PHASE 4: MONITORING BATCH JOB")
    print("=" * 70)

    print(f"Monitoring batch job {batch_id}...")
    print("This may take several minutes to hours depending on volume...")

    while True:
        batch_job = client.batch.jobs.get(job_id=batch_id)

        print(f"\rStatus: {batch_job.status} | ", end="")
        print(f"Progress: {batch_job.succeeded_requests}/{batch_job.total_requests} ", end="")

        if batch_job.status in ["SUCCESS", "FAILED", "CANCELLED", "TIMEOUT_EXCEEDED"]:
            print(f"\nJob completed with status: {batch_job.status}")
            break

        time.sleep(10)

    if batch_job.status != "SUCCESS":
        print(f"ERROR: Batch job failed with status {batch_job.status}")
        return None

    # Download results
    print("\nDownloading results...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"batch_results_{timestamp}.jsonl"

    output_stream = client.files.download(file_id=batch_job.output_file)
    with open(results_file, 'wb') as f:
        for chunk in output_stream.stream:
            f.write(chunk)

    print(f"Results saved to {results_file}")
    return results_file

def phase5_generate_final_output(results_file, opportunities, regex_knockouts, timestamp):
    """Phase 5: Parse results and generate final output"""
    print("\n" + "=" * 70)
    print("PHASE 5: GENERATING FINAL OUTPUT")
    print("=" * 70)

    import csv
    import re

    # Import the production output manager
    sys.path.append('..')
    from enhanced_output_manager import EnhancedOutputManager
    output_manager = EnhancedOutputManager(base_path="../SOS_Output")

    # Parse batch results
    final_results = []

    # Add regex knockouts first
    final_results.extend(regex_knockouts)

    # Create opportunity lookup
    opp_lookup = {}
    for opp in opportunities:
        key = f"opp-{opp['search_id']}-{opp['opportunity_id']}"
        opp_lookup[key] = opp

    # Parse AI results
    with open(results_file, 'r') as f:
        for line in f:
            result = json.loads(line)
            custom_id = result.get('custom_id', '')
            base_id = '-'.join(custom_id.split('-')[:-1])

            if base_id in opp_lookup:
                original = opp_lookup[base_id]

                try:
                    response_content = result['response']['body']['choices'][0]['message']['content']

                    # Parse decision from response
                    decision_data = {}
                    json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
                    if json_match:
                        try:
                            decision_data = json.loads(json_match.group())
                        except:
                            pass

                    # Fallback parsing - Batch CAN return NO-GO to save costs (Bug #8 fix)
                    if not decision_data.get('decision'):
                        if 'NO-GO' in response_content or 'NO_GO' in response_content:
                            # Batch is SUPPOSED to catch NO-GOs to save money!
                            decision_data['decision'] = 'NO-GO'
                            decision_data['note'] = 'Batch identified as NO-GO - no agent verification needed'
                        elif 'INDETERMINATE' in response_content:
                            decision_data['decision'] = 'INDETERMINATE'
                        elif 'GO' in response_content:
                            decision_data['decision'] = 'GO'
                        else:
                            decision_data['decision'] = 'INDETERMINATE'

                    # Merge AI decision with all original metadata
                    final_results.append({
                        'search_id': original['search_id'],
                        'opportunity_id': original['opportunity_id'],
                        'title': original['title'],
                        'decision': decision_data.get('decision', 'UNKNOWN'),
                        'reasoning': decision_data.get('reasoning', response_content[:500]),
                        'processing_method': 'BATCH_AI',
                        # Carry forward ALL metadata from original
                        'agency': original.get('agency', 'Unknown'),
                        'announcement_number': original.get('announcement_number', original.get('opportunity_id', '')),
                        'announcement_title': original.get('announcement_title', original.get('title', '')),
                        'due_date': original.get('due_date', ''),
                        'posted_date': original.get('posted_date', ''),
                        'naics': original.get('naics', ''),
                        'psc': original.get('psc', ''),
                        'set_aside': original.get('set_aside', ''),
                        'value_low': original.get('value_low', 0),
                        'value_high': original.get('value_high', 0),
                        'place_of_performance': original.get('place_of_performance', ''),
                        'doc_length': original.get('doc_length', 0)
                    })

                except Exception as e:
                    print(f"Error parsing result: {e}")

    # Format results for output manager with ALL standardized fields
    formatted_results = []
    for result in final_results:
        # Determine the type based on processing method
        if result.get('processing_method') == 'APP_ONLY':
            assessment_type = 'APP_KNOCKOUT'
            knockout_category = 'APP'
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
            'knock_pattern': result.get('reasoning', '')[:100] if result.get('processing_method') == 'APP_ONLY' else '',
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
            'knock_out_reasons': ['App filter match'] if 'APP' in assessment_type else [result.get('reasoning', '')[:100]],
            'exceptions': [],
            'processing_method': result.get('processing_method', 'BATCH_AI')
        })

    # Import decision sanitizer to fix output formatting issue
    sys.path.append('..')
    from decision_sanitizer import DecisionSanitizer

    # Sanitize all results to ensure correct decision format
    formatted_results = DecisionSanitizer.sanitize_batch(formatted_results)

    # Use the production output manager
    search_id = f"BATCH_{timestamp}"
    import hashlib as _hl, json as _js
    def _snap(items):
        try:
            base = [
                {
                    'sid': x.get('search_id',''),
                    'oid': x.get('opportunity_id','') or x.get('announcement_number',''),
                    'title': x.get('title','') or x.get('announcement_title','')
                }
                for x in items
            ]
            return _hl.sha256(_js.dumps(base, sort_keys=True).encode('utf-8')).hexdigest()[:12]
        except Exception:
            return ""

    metadata = {
        'total_opportunities': len(final_results),
        'regex_knockouts': len(regex_knockouts),
        'ai_assessments': len(opportunities),
        'processing_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'input_snapshot_hash': _snap(opportunities),
        'output_snapshot_hash': _snap(formatted_results)
    }

    output_dir = output_manager.save_assessment_batch(search_id, formatted_results, metadata, pre_formatted=True)

    print(f"\nOutput saved to: {output_dir}")
    return str(output_dir)

def phase6_agent_verification(batch_results, original_opportunities, regex_knockouts):
    """Phase 6: Send GOs and INDETERMINATEs to agent for final verification"""
    print("\n" + "=" * 70)
    print("PHASE 6: AGENT VERIFICATION OF BATCH RESULTS")
    print("=" * 70)

    # Import the production connector
    sys.path.append('..')
    from ultimate_mistral_connector import UltimateMistralConnector

    # Find opportunities that need verification (GOs and INDETERMINATEs from batch)
    needs_verification = []
    for result in batch_results:
        if result.get('final_decision') in ['GO', 'INDETERMINATE']:
            needs_verification.append(result)

    print(f"Found {len(needs_verification)} opportunities needing agent verification")
    print(f"  (Out of {len(batch_results)} total batch results)")

    if not needs_verification:
        print("No opportunities need agent verification - all were NO-GO")
        return batch_results  # Return original results unchanged

    # Initialize agent connector (uses agent model by default)
    from ULTIMATE_MISTRAL_CONNECTOR import MistralSOSClassifier
    connector = MistralSOSClassifier()
    # Don't override model - let it use the agent model from its configuration

    verified_results = []
    disagreements = 0

    for i, batch_result in enumerate(needs_verification, 1):
        print(f"  [{i}/{len(needs_verification)}] Verifying: {batch_result.get('title', 'Unknown')[:50]}...")

        try:
            # Find the original opportunity data
            original_opp = None
            for opp in original_opportunities:
                if (opp.get('opportunity_id') == batch_result.get('opportunity_id') and
                    opp.get('search_id') == batch_result.get('search_id')):
                    original_opp = opp
                    break

            if not original_opp:
                print(f"    WARNING: Could not find original data for {batch_result.get('opportunity_id')}")
                verified_results.append(batch_result)  # Keep batch result
                continue

            # Send to agent for verification
            agent_result = connector.classify_opportunity(original_opp)
            
            # Add small delay between agent calls to prevent rate limiting
            # Mistral API handles ~10 requests/second, 5s is very conservative
            if i < len(needs_verification):  # Don't delay after the last one
                print(f"    Waiting 5 seconds before next agent verification...")
                time.sleep(5)

            # Compare decisions
            batch_decision = batch_result.get('final_decision', 'UNKNOWN')
            # Agent now returns unified schema with 'result' field
            agent_decision = agent_result.get('result', agent_result.get('classification', 'UNKNOWN'))

            disagreement = batch_decision != agent_decision

            if disagreement:
                disagreements += 1
                print(f"    DECISION CHANGE: {batch_decision} → {agent_decision}")

            # Create verified result with agent taking precedence
            verified_result = {
                **batch_result,  # Keep all batch metadata
                'batch_decision': batch_decision,
                'agent_decision': agent_decision,
                'final_decision': agent_decision,  # Agent decision is final
                'disagreement': disagreement,
                'verification_method': 'AGENT_OVERRIDE' if disagreement else 'AGENT_CONFIRMED',
                'agent_reasoning': agent_result.get('reasoning', ''),
                'processing_method': 'AGENT_AI',  # Use canonical name, will be normalized to MISTRAL_ASSESSMENT
                'verification_timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            }

            verified_results.append(verified_result)

        except Exception as e:
            print(f"    ERROR during agent verification: {e}")
            # Keep original batch result on error
            verified_results.append({
                **batch_result,
                'verification_error': str(e),
                'processing_method': 'VERIFICATION_FAILED'
            })

    # Combine verified results with regex knockouts and NO-GOs that didn't need verification
    final_results = []

    # Add regex knockouts unchanged
    final_results.extend(regex_knockouts)

    # Add NO-GOs from batch (no verification needed)
    for result in batch_results:
        if result.get('final_decision') == 'NO-GO':
            final_results.append(result)

    # Add verified results
    final_results.extend(verified_results)

    print(f"\nVERIFICATION COMPLETE:")
    print(f"  Total opportunities verified: {len(needs_verification)}")
    print(f"  Decision disagreements: {disagreements}")
    print(f"  Agreement rate: {((len(needs_verification) - disagreements) / len(needs_verification) * 100):.1f}%" if needs_verification else "N/A")
    print(f"  Final results: {len(final_results)}")

    return final_results

def main():
    """Main orchestration function"""
    print("=" * 70)
    print("MISTRAL BATCH PROCESSOR - COMPLETE PIPELINE")
    print("=" * 70)
    print("This will:")
    print("1. Read endpoints.txt")
    print("2. Fetch all opportunities")
    print("3. Apply regex filtering (knock out obvious NO-GOs)")
    print("4. Batch process remaining with Mistral AI")
    print("5. Generate final CSV output")
    print("=" * 70)

    # Phase 1: Collect and filter
    opportunities, regex_knockouts = phase1_collect_opportunities()
    if opportunities is None:
        return

    if not opportunities:
        print("\nNo opportunities need AI assessment (all knocked out by regex)")
        if regex_knockouts:
            # Use output manager for consistency
            from enhanced_output_manager import EnhancedOutputManager
            output_manager = EnhancedOutputManager(base_path="../SOS_Output")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            search_id = f"BATCH_APP_{timestamp}"

            # Format for output manager
            formatted_results = []
            for result in regex_knockouts:
                formatted_results.append({
                    'search_id': result.get('search_id', ''),
                    'opportunity_id': result.get('opportunity_id', ''),
                    'title': result.get('title', ''),
                    'final_decision': 'NO-GO',
                    'knock_pattern': result.get('reasoning', '')[:100],
                    'knockout_category': 'APP',
                    'sos_pipeline_title': 'PN: NA | Qty: NA | Condition: NA | MDS: NA | Description: NA',
                    'highergov_url': f"https://www.highergov.com/opportunity/{result.get('opportunity_id', '')}",
                    'analysis_notes': result.get('reasoning', ''),
                    'processing_method': 'APP'
                })

            metadata = {
                'total_opportunities': len(regex_knockouts),
                'regex_knockouts': len(regex_knockouts),
                'ai_assessments': 0,
                'processing_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            output_dir = output_manager.save_assessment_batch(search_id, formatted_results, metadata, pre_formatted=True)
            print(f"Regex-only results saved to: {output_dir}")
        return

    # Phase 2: Create batch file
    jsonl_file, timestamp = phase2_create_batch_file(opportunities)

    # Save metadata for recovery
    metadata = {
        'timestamp': timestamp,
        'opportunities': opportunities,
        'regex_knockouts': regex_knockouts,
        'jsonl_file': jsonl_file
    }
    metadata_file = f"batch_metadata_{timestamp}.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata saved to {metadata_file}")

    # Phase 3: Submit to Mistral (with retry logic)
    batch_id = None
    client = None
    max_retries = 3
    for attempt in range(max_retries):
        try:
            batch_id, client = phase3_submit_to_mistral(jsonl_file)
            break  # Success
        except Exception as e:
            print(f"ERROR submitting to Mistral (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("All retry attempts failed. Check your API key and network connection")
                return

    # Check environment variable for monitoring preference (non-interactive mode)
    monitor_batch = os.environ.get('MONITOR_BATCH', 'n').lower()
    if monitor_batch != 'y':
        print(f"\nBatch job {batch_id} is running in background.")
        print("Set MONITOR_BATCH=y environment variable to enable monitoring.")
        print(f"Check status later with:")
        print(f"  python BATCH_SUBMITTER_V2.py --status {batch_id}")
        print(f"Download results with:")
        print(f"  python BATCH_SUBMITTER_V2.py --download {batch_id}")
        return

    # Phase 4: Monitor and download
    results_file = phase4_monitor_and_download(batch_id, client)
    if not results_file:
        return

    # Phase 5: Generate output
    csv_file = phase5_generate_final_output(results_file, opportunities, regex_knockouts, timestamp)

    # Phase 6: Agent verification of promising opportunities
    print("\n" + "=" * 70)
    print("INITIATING AGENT VERIFICATION PHASE")
    print("=" * 70)

    # Load the batch results that were just processed
    batch_results = []
    try:
        with open(results_file, 'r') as f:
            for line in f:
                result = json.loads(line)
                # Parse the batch result to get the decision
                response_content = result.get('response', {}).get('body', {}).get('choices', [{}])[0].get('message', {}).get('content', '')

                # Extract decision from response
                decision = 'UNKNOWN'
                if 'NO-GO' in response_content or 'NO_GO' in response_content:
                    decision = 'NO-GO'
                elif 'GO' in response_content:
                    decision = 'GO'
                else:
                    decision = 'INDETERMINATE'

                # Find the original opportunity data
                custom_id = result.get('custom_id', '')
                base_id = '-'.join(custom_id.split('-')[:-1])
                original_opp = None
                for opp in opportunities:
                    opp_key = f"opp-{opp['search_id']}-{opp['opportunity_id']}"
                    if opp_key in custom_id:
                        original_opp = opp
                        break

                if original_opp:
                    batch_results.append({
                        'search_id': original_opp['search_id'],
                        'opportunity_id': original_opp['opportunity_id'],
                        'title': original_opp['title'],
                        'final_decision': decision,
                        'batch_reasoning': response_content[:500],
                        'processing_method': 'BATCH_AI',
                        # Preserve all metadata
                        'agency': original_opp.get('agency', 'Unknown'),
                        'announcement_number': original_opp.get('announcement_number', original_opp.get('opportunity_id', '')),
                        'announcement_title': original_opp.get('announcement_title', original_opp.get('title', '')),
                        'due_date': original_opp.get('due_date', ''),
                        'posted_date': original_opp.get('posted_date', ''),
                        'naics': original_opp.get('naics', ''),
                        'psc': original_opp.get('psc', ''),
                        'set_aside': original_opp.get('set_aside', ''),
                        'value_low': original_opp.get('value_low', 0),
                        'value_high': original_opp.get('value_high', 0),
                        'place_of_performance': original_opp.get('place_of_performance', ''),
                        'doc_length': original_opp.get('doc_length', 0)
                    })

        print(f"Loaded {len(batch_results)} batch results for verification")

        # Phase 6: Agent verification (optional)
        if os.environ.get('SKIP_AGENT_VERIFICATION', '').lower() in ['1', 'true', 'yes']:
            print("\n[SKIPPING AGENT VERIFICATION - Batch only mode]")
            # Include BOTH batch results AND regex knockouts
            verified_results = batch_results + regex_knockouts
        else:
            verified_results = phase6_agent_verification(batch_results, opportunities, regex_knockouts)

        # Regenerate output with verified results
        print("\nRegenerating output with verified results...")
        output_manager = EnhancedOutputManager(base_path="../SOS_Output")

        # Import decision sanitizer to ensure consistent output
        from decision_sanitizer import DecisionSanitizer

        # Format verified results for output manager
        import copy
        formatted_verified_results = []
        for result in verified_results:
            # Check if already sanitized
            if result.get('_sanitized'):
                # Already sanitized, just add any missing verification fields
                # Use deepcopy to prevent mutation of nested structures
                sanitized_result = copy.deepcopy(result)
                sanitized_result['verification_method'] = result.get('verification_method', 'NONE')
                sanitized_result['disagreement'] = result.get('disagreement', False)
                formatted_verified_results.append(sanitized_result)
            else:
                # Not sanitized yet, format manually
                formatted_verified_results.append({
                    'search_id': result.get('search_id', ''),
                    'opportunity_id': result.get('opportunity_id', ''),
                    'title': result.get('title', ''),
                    'final_decision': result.get('final_decision', 'UNKNOWN'),
                    'knock_pattern': result.get('knock_pattern', ''),
                    'knockout_category': result.get('knockout_category', ''),
                    'sos_pipeline_title': result.get('sos_pipeline_title', f"PN: NA | Qty: NA | Condition: unknown | MDS: NA | {result.get('title', '')[:50]}"),
                    'highergov_url': result.get('highergov_url', f"https://www.highergov.com/opportunity/{result.get('opportunity_id', '')}"),
                    'announcement_number': result.get('announcement_number', result.get('opportunity_id', '')),
                    'announcement_title': result.get('announcement_title', result.get('title', '')),
                    'agency': result.get('agency', 'Unknown'),
                    'due_date': result.get('due_date', ''),
                    'posted_date': result.get('posted_date', ''),
                    'naics': result.get('naics', ''),
                    'psc': result.get('psc', ''),
                    'set_aside': result.get('set_aside', ''),
                    'value_low': result.get('value_low', 0),
                    'value_high': result.get('value_high', 0),
                    'place_of_performance': result.get('place_of_performance', ''),
                    'brief_description': result.get('batch_reasoning', '')[:100] if result.get('processing_method') == 'BATCH_AI' else result.get('reasoning', '')[:100],
                    'analysis_notes': result.get('batch_reasoning', '') if result.get('processing_method') == 'BATCH_AI' else result.get('reasoning', ''),
                    'recommendation': result.get('final_decision', 'UNKNOWN'),
                    'special_action': '',
                    'doc_length': result.get('doc_length', 0),
                    'assessment_timestamp': result.get('verification_timestamp', datetime.now().strftime("%Y-%m-%dT%H:%M:%S")),
                    'solicitation_id': result.get('search_id', 'unknown'),
                    'solicitation_title': result.get('title', ''),
                    'type': result.get('processing_method', 'UNKNOWN'),
                    'result': result.get('final_decision', 'UNKNOWN'),
                    'summary': result.get('batch_reasoning', '')[:200] if result.get('processing_method') == 'BATCH_AI' else result.get('reasoning', '')[:200],
                    'rationale': result.get('batch_reasoning', '') if result.get('processing_method') == 'BATCH_AI' else result.get('reasoning', ''),
                    'knock_out_reasons': [result.get('batch_reasoning', '')[:100]] if result.get('processing_method') == 'BATCH_AI' else [result.get('reasoning', '')[:100]],
                    'exceptions': [],
                    'processing_method': result.get('processing_method', 'UNKNOWN'),
                    'verification_method': result.get('verification_method', 'NONE'),
                    'disagreement': result.get('disagreement', False),
                    # Mark as manually formatted to prevent re-sanitization
                    '_sanitized': True,
                    'pipeline_stage': 'BATCH' if result.get('processing_method') == 'BATCH_AI' else 'AGENT',
                    'assessment_type': 'MISTRAL_BATCH_ASSESSMENT' if result.get('processing_method') == 'BATCH_AI' else 'MISTRAL_ASSESSMENT'
                })

        # Only sanitize if we have unsanitized items
        # The if/else block above already handles sanitized items properly
        needs_sanitization = any(not item.get('_sanitized') for item in formatted_verified_results)
        if needs_sanitization:
            # Sanitize only the unsanitized items
            formatted_verified_results = DecisionSanitizer.sanitize_batch(formatted_verified_results)

        # Save verified results
        search_id = f"BATCH_VERIFIED_{timestamp}"
        metadata = {
            'total_opportunities': len(verified_results),
            'regex_knockouts': len(regex_knockouts),
            'batch_assessments': len(batch_results),
            'agent_verifications': len([r for r in verified_results if r.get('processing_method') in ['AGENT_VERIFIED', 'AGENT_AI', 'MISTRAL_ASSESSMENT']]),
            'disagreements': len([r for r in verified_results if r.get('disagreement', False)]),
            'processing_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        verified_output_dir = output_manager.save_assessment_batch(search_id, formatted_verified_results, metadata, pre_formatted=True)
        csv_file = verified_output_dir

    except Exception as e:
        print(f"ERROR during agent verification: {e}")
        print("Continuing with original batch results...")

    print("\n" + "=" * 70)
    print("VERIFIED BATCH PROCESSING COMPLETE!")
    print(f"Results available at: {csv_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()
