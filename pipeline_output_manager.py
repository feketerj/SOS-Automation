#!/usr/bin/env python3
"""
Pipeline Output Manager - Complete visibility of three-stage pipeline
Shows exactly what got knocked out where and why
"""

import os
import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class PipelineOutputManager:
    """
    Comprehensive output showing complete pipeline journey:
    - What went through each stage
    - What got knocked out and why
    - Final decisions with full tracking
    """

    def __init__(self, base_path: str = "SOS_Output"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

    def save_pipeline_results(self,
                             search_ids: List[str],
                             all_results: List[Dict],
                             pipeline_stats: Dict,
                             metadata: Optional[Dict] = None) -> Path:
        """Save comprehensive pipeline results with full visibility"""

        # Create run folder
        now = datetime.now()
        month_folder = self.base_path / now.strftime("%Y-%m")
        month_folder.mkdir(exist_ok=True)

        timestamp = now.strftime("%Y%m%d_%H%M%S")
        search_id = search_ids[0][:8] if search_ids else 'PIPELINE'
        run_folder = month_folder / f"Run_{timestamp}_{search_id}"
        run_folder.mkdir(exist_ok=True)

        # Save all formats
        self._save_pipeline_csv(run_folder / "pipeline_results.csv", all_results)
        self._save_pipeline_report(run_folder / "pipeline_report.md", all_results, pipeline_stats)
        self._save_stage_summary(run_folder / "stage_summary.txt", all_results, pipeline_stats)
        self._save_knockouts_report(run_folder / "knockouts.md", all_results)
        self._save_json_data(run_folder / "data.json", all_results, metadata)

        # Save GO-only CSV for actionable items
        go_opps = [r for r in all_results if r.get('result') == 'GO']
        if go_opps:
            self._save_go_csv(run_folder / "GO_opportunities.csv", go_opps)

        print(f"\nResults saved to: {run_folder}")
        return run_folder

    def _save_pipeline_csv(self, filepath: Path, results: List[Dict]):
        """Save comprehensive CSV with all pipeline tracking"""

        fieldnames = [
            # Final result
            'result',
            'pipeline_stage',
            'assessment_type',

            # Stage tracking
            'stage1_regex_decision',
            'stage1_regex_reason',
            'stage2_batch_decision',
            'stage2_batch_reason',
            'stage3_agent_decision',
            'stage3_agent_reason',

            # Opportunity info
            'announcement_number',
            'announcement_title',
            'agency',
            'description',

            # Knockout details
            'knockout_category',
            'knock_pattern',

            # URLs
            'highergov_url',
            'sam_url',

            # Document info
            'document_length',
            'document_fetched',

            # Additional metadata fields from HigherGov
            'source_id',
            'opp_key',
            'title',
            'description_text',
            'posted_date',
            'due_date',
            'notice_type',
            'contract_type',
            'set_aside',
            'naics_code',
            'psc_code',
            'pop_country',
            'pop_state',
            'pop_city',
            'active',
            'source_id_version',
            'issuing_agency',
            'document_path',
            'source_path',
            'path',

            # Timestamps
            'assessment_timestamp',
        ]

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for r in results:
                # Extract pipeline tracking info
                tracking = r.get('pipeline_tracking', {})

                # Extract metadata fields
                metadata = r.get('metadata', {})

                row = {
                    'result': r.get('result', 'UNKNOWN'),
                    'pipeline_stage': r.get('pipeline_stage', ''),
                    'assessment_type': r.get('assessment_type', ''),

                    'stage1_regex_decision': tracking.get('stage1_regex', ''),
                    'stage1_regex_reason': tracking.get('stage1_reason', ''),
                    'stage2_batch_decision': tracking.get('stage2_batch', ''),
                    'stage2_batch_reason': tracking.get('stage2_reason', ''),
                    'stage3_agent_decision': tracking.get('stage3_agent', ''),
                    'stage3_agent_reason': tracking.get('stage3_reason', ''),

                    'announcement_number': r.get('announcement_number', ''),
                    'announcement_title': r.get('announcement_title', '')[:100],
                    'agency': r.get('agency', ''),
                    'description': r.get('description', '')[:200],

                    'knockout_category': r.get('knockout_category', ''),
                    'knock_pattern': r.get('knock_pattern', ''),

                    'highergov_url': r.get('highergov_url', ''),
                    'sam_url': r.get('sam_url', ''),

                    'document_length': len(r.get('document_text', '')),
                    'document_fetched': 'YES' if r.get('document_text') else 'NO',

                    # Add all metadata fields
                    'source_id': metadata.get('source_id', ''),
                    'opp_key': metadata.get('opp_key', ''),
                    'title': metadata.get('title', ''),
                    'description_text': metadata.get('description_text', '')[:200],
                    'posted_date': metadata.get('posted_date', ''),
                    'due_date': metadata.get('due_date', ''),
                    'notice_type': metadata.get('notice_type', ''),
                    'contract_type': metadata.get('contract_type', ''),
                    'set_aside': metadata.get('set_aside', ''),
                    'naics_code': metadata.get('naics_code', ''),
                    'psc_code': metadata.get('psc_code', ''),
                    'pop_country': metadata.get('pop_country', ''),
                    'pop_state': metadata.get('pop_state', ''),
                    'pop_city': metadata.get('pop_city', ''),
                    'active': metadata.get('active', ''),
                    'source_id_version': metadata.get('source_id_version', ''),
                    'issuing_agency': metadata.get('issuing_agency', ''),
                    'document_path': metadata.get('document_path', ''),
                    'source_path': metadata.get('source_path', ''),
                    'path': metadata.get('path', ''),

                    'assessment_timestamp': r.get('assessment_timestamp', ''),
                }
                writer.writerow(row)

    def _save_pipeline_report(self, filepath: Path, results: List[Dict], stats: Dict):
        """Generate comprehensive markdown report showing full pipeline flow"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# COMPLETE PIPELINE REPORT\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")

            # Overview stats
            f.write("## Pipeline Statistics\n\n")
            f.write(f"**Total Opportunities:** {len(results)}\n\n")

            f.write("### Stage 1: Regex Filtering (FREE)\n")
            f.write(f"- Knocked Out: {stats['stage1_regex']['no_go']}\n")
            f.write(f"- Passed Through: {stats['stage1_regex']['continue']}\n\n")

            f.write("### Stage 2: Batch Model (50% off)\n")
            f.write(f"- Knocked Out: {stats.get('stage2_batch', {}).get('no_go', 0)}\n")
            f.write(f"- Passed Through: {stats.get('stage2_batch', {}).get('continue', 0)}\n\n")

            f.write("### Stage 3: Agent Verification (Full price)\n")
            f.write(f"- Final GO: {stats.get('stage3_agent', {}).get('go', 0)}\n")
            f.write(f"- Final NO-GO: {stats.get('stage3_agent', {}).get('no_go', 0)}\n")
            f.write(f"- Final INDETERMINATE: {stats.get('stage3_agent', {}).get('indeterminate', 0)}\n\n")

            # Detailed results by stage
            f.write("## Detailed Pipeline Flow\n\n")

            # Stage 1 knockouts
            stage1_knockouts = [r for r in results if r.get('pipeline_stage') == 'REGEX']
            if stage1_knockouts:
                f.write("### Stage 1 Knockouts (Regex)\n\n")
                for r in stage1_knockouts:
                    f.write(f"**{r['announcement_title'][:60]}**\n")
                    f.write(f"- ID: {r['announcement_number']}\n")
                    f.write(f"- Agency: {r['agency']}\n")
                    f.write(f"- Reason: {r.get('pipeline_tracking', {}).get('stage1_reason', 'Pattern match')}\n")
                    f.write(f"- Category: {r.get('knockout_category', '')}\n\n")

            # Stage 2 knockouts
            stage2_knockouts = [r for r in results if r.get('pipeline_stage') == 'BATCH']
            if stage2_knockouts:
                f.write("### Stage 2 Knockouts (Batch Model)\n\n")
                for r in stage2_knockouts:
                    f.write(f"**{r['announcement_title'][:60]}**\n")
                    f.write(f"- ID: {r['announcement_number']}\n")
                    f.write(f"- Agency: {r['agency']}\n")
                    f.write(f"- Stage 1: {r.get('pipeline_tracking', {}).get('stage1_regex', '')}\n")
                    f.write(f"- Stage 2: {r.get('pipeline_tracking', {}).get('stage2_batch', '')}\n")
                    f.write(f"- Reason: Model assessment\n\n")

            # Stage 3 final decisions
            stage3_results = [r for r in results if r.get('pipeline_stage') == 'AGENT']
            if stage3_results:
                f.write("### Stage 3 Final Decisions (Agent)\n\n")

                # Group by decision
                go_results = [r for r in stage3_results if r.get('result') == 'GO']
                nogo_results = [r for r in stage3_results if r.get('result') == 'NO-GO']
                ind_results = [r for r in stage3_results if r.get('result') not in ['GO', 'NO-GO']]

                if go_results:
                    f.write("#### FINAL GO\n\n")
                    for r in go_results:
                        f.write(f"**{r['announcement_title'][:60]}**\n")
                        f.write(f"- ID: {r['announcement_number']}\n")
                        f.write(f"- Agency: {r['agency']}\n")
                        f.write(f"- URL: {r['highergov_url']}\n")
                        f.write(f"- Journey: {r.get('pipeline_tracking', {}).get('stage1_regex', '')} → ")
                        f.write(f"{r.get('pipeline_tracking', {}).get('stage2_batch', '')} → ")
                        f.write(f"{r.get('pipeline_tracking', {}).get('stage3_agent', '')}\n\n")

                if nogo_results:
                    f.write("#### FINAL NO-GO\n\n")
                    for r in nogo_results:
                        f.write(f"**{r['announcement_title'][:60]}**\n")
                        f.write(f"- ID: {r['announcement_number']}\n")
                        f.write(f"- Journey: {r.get('pipeline_tracking', {}).get('stage1_regex', '')} → ")
                        f.write(f"{r.get('pipeline_tracking', {}).get('stage2_batch', '')} → ")
                        f.write(f"{r.get('pipeline_tracking', {}).get('stage3_agent', '')}\n\n")

                if ind_results:
                    f.write("#### FINAL INDETERMINATE\n\n")
                    for r in ind_results:
                        f.write(f"**{r['announcement_title'][:60]}**\n")
                        f.write(f"- ID: {r['announcement_number']}\n")
                        f.write(f"- Journey: {r.get('pipeline_tracking', {}).get('stage1_regex', '')} → ")
                        f.write(f"{r.get('pipeline_tracking', {}).get('stage2_batch', '')} → ")
                        f.write(f"{r.get('pipeline_tracking', {}).get('stage3_agent', '')}\n\n")

    def _save_stage_summary(self, filepath: Path, results: List[Dict], stats: Dict):
        """Save quick text summary of pipeline stages"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("PIPELINE STAGE SUMMARY\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write(f"Total Opportunities: {len(results)}\n\n")

            f.write("STAGE 1 (REGEX - FREE):\n")
            f.write(f"  Input:  {len(results)} opportunities\n")
            f.write(f"  Knocked Out: {stats['stage1_regex']['no_go']}\n")
            f.write(f"  Passed:  {stats['stage1_regex']['continue']}\n\n")

            f.write("STAGE 2 (BATCH MODEL - 50% OFF):\n")
            f.write(f"  Input:  {stats['stage1_regex']['continue']} opportunities\n")
            f.write(f"  Knocked Out: {stats.get('stage2_batch', {}).get('no_go', 0)}\n")
            f.write(f"  Passed:  {stats.get('stage2_batch', {}).get('continue', 0)}\n\n")

            f.write("STAGE 3 (AGENT - FULL PRICE):\n")
            f.write(f"  Input:  {stats.get('stage2_batch', {}).get('continue', 0)} opportunities\n")
            f.write(f"  GO:     {stats.get('stage3_agent', {}).get('go', 0)}\n")
            f.write(f"  NO-GO:  {stats.get('stage3_agent', {}).get('no_go', 0)}\n")
            f.write(f"  INDETERMINATE: {stats.get('stage3_agent', {}).get('indeterminate', 0)}\n\n")

            f.write("=" * 50 + "\n")
            f.write("COST OPTIMIZATION:\n")
            regex_savings = stats['stage1_regex']['no_go']
            batch_savings = stats.get('stage2_batch', {}).get('no_go', 0) * 0.5
            f.write(f"  Regex saved: {regex_savings} AI calls (100% savings)\n")
            f.write(f"  Batch saved: {batch_savings:.1f} full-price calls (50% savings)\n")

    def _save_knockouts_report(self, filepath: Path, results: List[Dict]):
        """Generate detailed knockouts report"""

        knockouts = [r for r in results if r.get('result') == 'NO-GO']

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# KNOCKOUT ANALYSIS\n\n")
            f.write(f"Total Knockouts: {len(knockouts)}\n\n")

            # Group by stage
            stage_groups = {}
            for ko in knockouts:
                stage = ko.get('pipeline_stage', 'UNKNOWN')
                if stage not in stage_groups:
                    stage_groups[stage] = []
                stage_groups[stage].append(ko)

            for stage, items in stage_groups.items():
                f.write(f"## {stage} Stage Knockouts ({len(items)})\n\n")

                # Group by reason/category
                reason_groups = {}
                for item in items:
                    reason = item.get('knockout_category', item.get('knock_pattern', 'Unknown'))[:50]
                    if reason not in reason_groups:
                        reason_groups[reason] = []
                    reason_groups[reason].append(item)

                for reason, opps in sorted(reason_groups.items(), key=lambda x: -len(x[1])):
                    f.write(f"### {reason} ({len(opps)} knockouts)\n")
                    for opp in opps[:5]:  # Show first 5
                        f.write(f"- {opp['announcement_title'][:60]} ({opp['announcement_number']})\n")
                    if len(opps) > 5:
                        f.write(f"- ... and {len(opps)-5} more\n")
                    f.write("\n")

    def _save_json_data(self, filepath: Path, results: List[Dict], metadata: Dict):
        """Save complete JSON data"""

        output = {
            'metadata': metadata,
            'statistics': {
                'total_opportunities': len(results),
                'final_go': len([r for r in results if r.get('result') == 'GO']),
                'final_no_go': len([r for r in results if r.get('result') == 'NO-GO']),
                'final_indeterminate': len([r for r in results if r.get('result') not in ['GO', 'NO-GO']])
            },
            'results': results
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, default=str)

    def _save_go_csv(self, filepath: Path, go_opps: List[Dict]):
        """Save actionable GO opportunities"""

        fieldnames = [
            'announcement_number',
            'announcement_title',
            'agency',
            'highergov_url',
            'pipeline_journey',
            'assessment_timestamp'
        ]

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for opp in go_opps:
                tracking = opp.get('pipeline_tracking', {})
                journey = f"{tracking.get('stage1_regex', '')}→{tracking.get('stage2_batch', '')}→{tracking.get('stage3_agent', '')}"

                row = {
                    'announcement_number': opp.get('announcement_number', ''),
                    'announcement_title': opp.get('announcement_title', ''),
                    'agency': opp.get('agency', ''),
                    'highergov_url': opp.get('highergov_url', ''),
                    'pipeline_journey': journey,
                    'assessment_timestamp': opp.get('assessment_timestamp', '')
                }
                writer.writerow(row)