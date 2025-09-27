#!/usr/bin/env python3
"""
COMPLETE THREE-STAGE PIPELINE

The PROPER assessment flow:
1. Fetch all opportunities with metadata and documents
2. Stage 1: Regex filtering (FREE)
   - NO-GO → Stop here, save as NO-GO
   - GO/INDETERMINATE → Continue to Stage 2
3. Stage 2: Batch Model with prompt injection
   - NO-GO → Stop here, save as NO-GO
   - GO/INDETERMINATE → Continue to Stage 3
4. Stage 3: Agent verification
   - Final decision (GO/NO-GO/INDETERMINATE)
5. Generate complete report with all stages tracked
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Add necessary paths
sys.path.insert(0, 'Mistral_Batch_Processor')
sys.path.insert(0, '.')

# HARDCODED CONFIGURATION - CLIENT APP ONLY
MISTRAL_API_KEY = '2oAquITdDMiyyk0OfQuJSSqePn3SQbde'  # Hardcoded for client use
BATCH_MODEL = 'ft:pixtral-12b-latest:d42144c7:20250912:f7d61150'  # Fine-tuned Pixtral
AGENT_ID = 'ag:d42144c7:20250911:untitled-agent:15489fc1'  # Production agent
HIGHERGOV_API_KEY = '2c38090f3cb0c56026e17fb3e464f22cf637e2ee'  # Hardcoded for client use

def run_assessment():
    """Run the complete three-stage pipeline"""

    print("=" * 70)
    print("COMPLETE THREE-STAGE PIPELINE")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Stages: Regex → Batch Model → Agent Verification")
    print("-" * 70)

    # Import what we need
    from highergov_batch_fetcher import HigherGovBatchFetcher
    from sos_ingestion_gate_v419 import IngestionGateV419, Decision
    from pipeline_output_manager import PipelineOutputManager
    from ULTIMATE_MISTRAL_CONNECTOR import UltimateMistralConnector

    # Check endpoints.txt
    if not Path('endpoints.txt').exists():
        print("ERROR: endpoints.txt not found")
        return False

    with open('endpoints.txt', 'r') as f:
        search_ids = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    if not search_ids:
        print("ERROR: No search IDs in endpoints.txt")
        return False

    print(f"Processing {len(search_ids)} search IDs...\n")

    # Initialize components
    fetcher = HigherGovBatchFetcher()
    regex_gate = IngestionGateV419()
    mistral_connector = UltimateMistralConnector()

    # Track all results through pipeline
    all_results = []
    pipeline_stats = {
        'stage1_regex': {'no_go': 0, 'continue': 0},
        'stage2_batch': {'no_go': 0, 'continue': 0},
        'stage3_agent': {'go': 0, 'no_go': 0, 'indeterminate': 0}
    }

    # STAGE 1: FETCH AND REGEX FILTER
    print("\n" + "=" * 50)
    print("STAGE 1: FETCHING OPPORTUNITIES & REGEX FILTERING")
    print("=" * 50)

    opportunities_for_batch = []

    for search_id in search_ids:
        print(f"\nFetching: {search_id}")

        try:
            # Fetch opportunities with full metadata and documents
            opportunities = fetcher.fetch_all_opportunities(search_id)
            print(f"  Found {len(opportunities)} opportunities")

            for opp in opportunities:
                # Fetch document text
                doc_text = ""
                if opp.get('document_path'):
                    try:
                        doc_text = fetcher.fetch_document_text(opp['document_path'])
                        print(f"    Fetched {len(doc_text):,} chars of documents")
                    except:
                        print(f"    No documents fetched")

                # Combine all text for regex assessment
                combined_text = f"{opp.get('title', '')} {opp.get('description', '')} {doc_text}"

                # Apply regex filtering
                regex_result = regex_gate.assess_opportunity({'text': combined_text, **opp})

                # Build complete opportunity record
                opp_record = {
                    'opportunity_id': opp.get('id'),
                    'announcement_number': opp.get('id', f"OPP_{datetime.now().strftime('%H%M%S%f')[:10]}"),
                    'announcement_title': opp.get('title', 'Unknown'),
                    'agency': opp.get('agency', opp.get('issuing_agency', 'Unknown')),
                    'description': opp.get('description', ''),
                    'document_text': doc_text[:50000],  # Cap at 50k chars
                    'metadata': opp,
                    'pipeline_tracking': {
                        'stage1_regex': regex_result.decision.value,
                        'stage1_reason': getattr(regex_result, 'primary_reason', getattr(regex_result, 'primary_blocker', '')),
                        'stage2_batch': None,
                        'stage2_reason': None,
                        'stage3_agent': None,
                        'stage3_reason': None
                    },
                    'knock_pattern': getattr(regex_result, 'primary_reason', getattr(regex_result, 'primary_blocker', '')),
                    'knockout_category': getattr(regex_result, 'knockout_category', ''),
                    'highergov_url': f"https://www.highergov.com/opportunity/{opp.get('id', '')}",
                    'assessment_timestamp': datetime.now().isoformat()
                }

                print(f"    • {opp['title'][:50]}: {regex_result.decision.value}")

                # Check regex decision
                if regex_result.decision == Decision.NO_GO:
                    # Stop here for NO-GO
                    opp_record['result'] = 'NO-GO'
                    opp_record['pipeline_stage'] = 'REGEX'
                    opp_record['assessment_type'] = 'REGEX_KNOCKOUT'
                    all_results.append(opp_record)
                    pipeline_stats['stage1_regex']['no_go'] += 1
                else:
                    # Continue to batch for GO/INDETERMINATE/FURTHER_ANALYSIS
                    opportunities_for_batch.append(opp_record)
                    pipeline_stats['stage1_regex']['continue'] += 1

        except Exception as e:
            print(f"  ERROR processing {search_id}: {e}")
            continue

    print(f"\nStage 1 Complete:")
    print(f"  Knocked out: {pipeline_stats['stage1_regex']['no_go']}")
    print(f"  Continuing: {pipeline_stats['stage1_regex']['continue']}")

    # STAGE 2: BATCH MODEL PROCESSING
    if opportunities_for_batch:
        print("\n" + "=" * 50)
        print("STAGE 2: BATCH MODEL PROCESSING")
        print("=" * 50)
        print(f"Processing {len(opportunities_for_batch)} opportunities through batch model...")

        opportunities_for_agent = []

        # Prepare batch requests with system prompt
        from mistralai import Mistral
        client = Mistral(api_key=MISTRAL_API_KEY)

        # Load system prompt
        system_prompt = """You are an SOS assessment expert. Evaluate if this opportunity is:
- GO: Suitable for SOS sourcing
- NO-GO: Not suitable (military-only, weapons, etc.)
- INDETERMINATE: Needs further review

Consider FAA 8130 exceptions for commercial Navy platforms (P-8, E-6, C-40).
Be strict about military restrictions but allow commercial equivalents."""

        batch_requests = []
        for i, opp in enumerate(opportunities_for_batch):
            request = {
                "custom_id": f"opp_{i}_{opp['opportunity_id']}",
                "body": {
                    "model": BATCH_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"""Opportunity: {opp['announcement_title']}
Agency: {opp['agency']}
Description: {opp['description'][:2000]}
Documents: {opp['document_text'][:3000]}

Assess if this is GO, NO-GO, or INDETERMINATE for SOS sourcing."""}
                    ]
                }
            }
            batch_requests.append(request)

        # Submit batch
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        batch_file = f'Mistral_Batch_Processor/batch_input_{timestamp}.jsonl'

        with open(batch_file, 'w') as f:
            for req in batch_requests:
                f.write(json.dumps(req) + '\n')

        print(f"Submitting batch of {len(batch_requests)} requests...")

        # Upload and submit batch
        try:
            with open(batch_file, 'rb') as f:
                batch_data = client.files.upload(
                    file=(batch_file, f.read()),
                    purpose="batch"
                )

            batch_job = client.batch.jobs.create(
                input_files=[batch_data.id],
                model=BATCH_MODEL,
                endpoint="/v1/chat/completions",
                metadata={"description": f"Pipeline Stage 2 - {timestamp}"}
            )

            print(f"Batch submitted! Job ID: {batch_job.id}")
            print("Waiting for completion (this may take several minutes)...")

            # Poll for completion - NO TIMEOUT
            # Batch jobs can take a long time with document processing
            poll_count = 0
            max_polls = 1000  # Very high limit, essentially no timeout

            while poll_count < max_polls:
                job = client.batch.jobs.get(job_id=batch_job.id)

                if job.status == 'SUCCEEDED':
                    print("Batch complete! Downloading results...")

                    # Download results
                    if job.output_file:
                        result_content = client.files.download(file_id=job.output_file)
                        results_file = f'Mistral_Batch_Processor/batch_results_{timestamp}.jsonl'

                        with open(results_file, 'wb') as f:
                            f.write(result_content)

                        # Parse results
                        with open(results_file, 'r') as f:
                            for line_num, line in enumerate(f):
                                try:
                                    result = json.loads(line)
                                    custom_id = result.get('custom_id', '')
                                    content = result.get('response', {}).get('body', {}).get('choices', [{}])[0].get('message', {}).get('content', '')

                                    # Match result to opportunity
                                    opp = opportunities_for_batch[line_num]

                                    # Extract decision and reason
                                    if 'NO-GO' in content:
                                        batch_decision = 'NO-GO'
                                        # Try to extract reason from content
                                        reason_start = content.find('Reason:')
                                        if reason_start > -1:
                                            reason = content[reason_start:reason_start+100].split('\n')[0]
                                        else:
                                            reason = 'Batch model assessment'
                                    elif 'GO' in content and 'NO-GO' not in content:
                                        batch_decision = 'GO'
                                        reason = 'Passed batch assessment'
                                    else:
                                        batch_decision = 'INDETERMINATE'
                                        reason = 'Needs further review'

                                    opp['pipeline_tracking']['stage2_batch'] = batch_decision
                                    opp['pipeline_tracking']['stage2_reason'] = reason

                                    print(f"  {opp['announcement_title'][:50]}: {batch_decision}")

                                    if batch_decision == 'NO-GO':
                                        # Stop here for NO-GO
                                        opp['result'] = 'NO-GO'
                                        opp['pipeline_stage'] = 'BATCH'
                                        opp['assessment_type'] = 'MISTRAL_BATCH_ASSESSMENT'
                                        all_results.append(opp)
                                        pipeline_stats['stage2_batch']['no_go'] += 1
                                    else:
                                        # Continue to agent for GO/INDETERMINATE
                                        opportunities_for_agent.append(opp)
                                        pipeline_stats['stage2_batch']['continue'] += 1

                                except Exception as e:
                                    print(f"  Error parsing result: {e}")
                                    continue
                    break

                elif job.status == 'FAILED':
                    print("Batch failed!")
                    # Add all to agent verification as fallback
                    opportunities_for_agent = opportunities_for_batch
                    break

                else:
                    print(f"  Status: {job.status} ({job.succeeded_requests}/{job.total_requests} complete)")
                    poll_count += 1
                    time.sleep(15)  # Check every 15 seconds instead of 10

        except Exception as e:
            print(f"Batch processing error: {e}")
            # Continue all to agent as fallback
            opportunities_for_agent = opportunities_for_batch

        print(f"\nStage 2 Complete:")
        print(f"  Knocked out: {pipeline_stats['stage2_batch']['no_go']}")
        print(f"  Continuing: {pipeline_stats['stage2_batch']['continue']}")

        # STAGE 3: AGENT VERIFICATION
        if opportunities_for_agent:
            print("\n" + "=" * 50)
            print("STAGE 3: AGENT VERIFICATION")
            print("=" * 50)
            print(f"Verifying {len(opportunities_for_agent)} opportunities with agent...")

            for opp in opportunities_for_agent:
                print(f"\n  Verifying: {opp['announcement_title'][:50]}")

                try:
                    # Prepare full context for agent
                    agent_input = {
                        'title': opp['announcement_title'],
                        'agency': opp['agency'],
                        'description': opp['description'],
                        'document_text': opp['document_text'][:10000],  # Give agent more context
                        'stage1_decision': opp['pipeline_tracking']['stage1_regex'],
                        'stage2_decision': opp['pipeline_tracking']['stage2_batch']
                    }

                    # Get agent assessment
                    agent_result = mistral_connector.assess_opportunity(agent_input)

                    # Extract final decision and reason
                    if isinstance(agent_result, dict):
                        final_decision = agent_result.get('classification', agent_result.get('decision', 'INDETERMINATE'))
                        final_reason = agent_result.get('rationale', agent_result.get('reasoning', 'Agent verification'))
                    else:
                        final_decision = 'INDETERMINATE'
                        final_reason = 'Unable to determine'

                    opp['pipeline_tracking']['stage3_agent'] = final_decision
                    opp['pipeline_tracking']['stage3_reason'] = final_reason
                    opp['result'] = final_decision
                    opp['pipeline_stage'] = 'AGENT'
                    opp['assessment_type'] = 'MISTRAL_ASSESSMENT'

                    print(f"    Final: {final_decision}")

                    # Update stats
                    if 'NO-GO' in final_decision:
                        pipeline_stats['stage3_agent']['no_go'] += 1
                    elif 'GO' in final_decision:
                        pipeline_stats['stage3_agent']['go'] += 1
                    else:
                        pipeline_stats['stage3_agent']['indeterminate'] += 1

                    all_results.append(opp)

                    # Rate limiting
                    time.sleep(2)

                except Exception as e:
                    print(f"    Error: {e}")
                    opp['result'] = 'INDETERMINATE'
                    opp['pipeline_stage'] = 'AGENT'
                    opp['assessment_type'] = 'MISTRAL_ASSESSMENT'
                    all_results.append(opp)

            print(f"\nStage 3 Complete:")
            print(f"  GO: {pipeline_stats['stage3_agent']['go']}")
            print(f"  NO-GO: {pipeline_stats['stage3_agent']['no_go']}")
            print(f"  INDETERMINATE: {pipeline_stats['stage3_agent']['indeterminate']}")

    # SAVE COMPLETE RESULTS
    if all_results:
        print("\n" + "=" * 70)
        print("SAVING COMPLETE PIPELINE RESULTS")
        print("=" * 70)

        output_manager = PipelineOutputManager(base_path="SOS_Output")

        metadata = {
            'search_ids': search_ids,
            'total_opportunities': len(all_results),
            'pipeline_stats': pipeline_stats,
            'timestamp': datetime.now().isoformat()
        }

        output_dir = output_manager.save_pipeline_results(
            search_ids,
            all_results,
            pipeline_stats,
            metadata
        )

        print(f"Results saved to: {output_dir}")
        print("\n" + "=" * 70)
        print("COMPLETE PIPELINE SUMMARY")
        print("=" * 70)
        print(f"Total Opportunities: {len(all_results)}")
        print(f"\nStage 1 (Regex):")
        print(f"  Knocked out: {pipeline_stats['stage1_regex']['no_go']}")
        print(f"  Passed through: {pipeline_stats['stage1_regex']['continue']}")
        print(f"\nStage 2 (Batch Model):")
        print(f"  Knocked out: {pipeline_stats['stage2_batch']['no_go']}")
        print(f"  Passed through: {pipeline_stats['stage2_batch']['continue']}")
        print(f"\nStage 3 (Agent):")
        print(f"  Final GO: {pipeline_stats['stage3_agent']['go']}")
        print(f"  Final NO-GO: {pipeline_stats['stage3_agent']['no_go']}")
        print(f"  Final INDETERMINATE: {pipeline_stats['stage3_agent']['indeterminate']}")
        print("=" * 70)

        return True
    else:
        print("\nNo results to save")
        return False

if __name__ == "__main__":
    success = run_assessment()
    sys.exit(0 if success else 1)