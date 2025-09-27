#!/usr/bin/env python3
"""
THE ONE TRUE PIPELINE RUNNER

This is THE script to run assessments. It:
1. Reads endpoints.txt
2. Fetches opportunities from HigherGov
3. Applies regex filtering
4. Saves ALL results immediately to SOS_Output
5. No batch jobs, no waiting, just results

Cost: Essentially free (just regex, no AI calls)
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add necessary paths
sys.path.insert(0, 'Mistral_Batch_Processor')
sys.path.insert(0, '.')

def run_assessment():
    """The one function that does everything you need"""

    print("=" * 70)
    print("SOS ASSESSMENT PIPELINE")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 70)

    # Import what we need
    from highergov_batch_fetcher import HigherGovBatchFetcher
    from sos_ingestion_gate_v419 import IngestionGateV419
    from enhanced_output_manager import EnhancedOutputManager

    # Check endpoints.txt
    if not Path('endpoints.txt').exists():
        print("ERROR: endpoints.txt not found")
        print("Create endpoints.txt with one search ID per line")
        return False

    # Read endpoints
    with open('endpoints.txt', 'r') as f:
        search_ids = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    if not search_ids:
        print("ERROR: No search IDs in endpoints.txt")
        return False

    print(f"Processing {len(search_ids)} search IDs...\n")

    # Process each search ID
    all_results = []
    stats = {'go': 0, 'no_go': 0, 'indeterminate': 0}

    fetcher = HigherGovBatchFetcher()
    gate = IngestionGateV419()

    for search_id in search_ids:
        print(f"Fetching: {search_id}")

        try:
            # Fetch opportunities
            opportunities = fetcher.fetch_all_opportunities(search_id)
            print(f"  Found {len(opportunities)} opportunities")

            # Apply regex to each
            for opp in opportunities:
                # Get assessment from regex
                result = gate.assess_opportunity(opp)

                # Format for output
                formatted = {
                    'announcement_number': opp.get('id', f"OPP_{datetime.now().strftime('%H%M%S%f')[:10]}"),
                    'announcement_title': opp.get('title', 'Unknown'),
                    'agency': opp.get('agency', opp.get('issuing_agency', 'Unknown')),
                    'result': result.decision.value,
                    'knockout_category': getattr(result, 'knockout_category', ''),
                    'knock_pattern': getattr(result, 'primary_reason', ''),
                    'highergov_url': f"https://www.highergov.com/opportunity/{opp.get('id', '')}",
                    'assessment_timestamp': datetime.now().isoformat(),
                    'pipeline_stage': 'REGEX',
                    'assessment_type': 'REGEX_ASSESSMENT'
                }

                all_results.append(formatted)

                # Update stats
                if 'NO-GO' in formatted['result']:
                    stats['no_go'] += 1
                elif 'GO' in formatted['result']:
                    stats['go'] += 1
                else:
                    stats['indeterminate'] += 1

                # Show progress
                print(f"    • {formatted['announcement_title'][:50]}: {formatted['result']}")

        except Exception as e:
            print(f"  ERROR processing {search_id}: {e}")
            continue

    # Save everything
    if all_results:
        print(f"\nSaving {len(all_results)} assessments...")

        output_manager = EnhancedOutputManager(base_path="SOS_Output")

        metadata = {
            'search_ids': search_ids,
            'total_opportunities': len(all_results),
            'regex_knockouts': stats['no_go'],
            'timestamp': datetime.now().isoformat()
        }

        output_dir = output_manager.save_assessment_batch(
            search_ids[0][:8] if search_ids else 'ASSESS',
            all_results,
            metadata,
            pre_formatted=True
        )

        print("\n" + "=" * 70)
        print("ASSESSMENT COMPLETE")
        print("-" * 70)
        print(f"Results saved to: {output_dir}")
        print(f"\nSummary:")
        print(f"  GO: {stats['go']}")
        print(f"  NO-GO: {stats['no_go']}")
        print(f"  INDETERMINATE: {stats['indeterminate']}")
        print(f"  TOTAL: {len(all_results)}")
        print("=" * 70)

        return True
    else:
        print("\nNo results to save")
        return False

if __name__ == "__main__":
    success = run_assessment()
    sys.exit(0 if success else 1)