#!/usr/bin/env python3
"""
Enhanced Output Manager with comprehensive CSV and rolling database
"""

import os
import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib

class EnhancedOutputManager:
    """
    Enhanced output with:
    1. Comprehensive CSV format (all fields requested)
    2. Rolling master database that captures everything
    """

    def __init__(self, base_path: str = "SOS_Output"):
        """Initialize with database support"""
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

        # Master database location
        self.master_db_path = self.base_path / "Master_Database"
        self.master_db_path.mkdir(exist_ok=True)

    def create_run_folder(self, search_id: str) -> Path:
        """Create folder for this run"""
        now = datetime.now()
        month_folder = self.base_path / now.strftime("%Y-%m")
        month_folder.mkdir(exist_ok=True)

        timestamp = now.strftime("%Y%m%d_%H%M%S")
        run_folder = month_folder / f"Run_{timestamp}_{search_id[:8]}"
        run_folder.mkdir(exist_ok=True)

        return run_folder

    def save_assessment_batch(self,
                            search_id: str,
                            assessments: List[Dict],
                            metadata: Optional[Dict] = None,
                            pre_formatted: bool = False) -> Path:
        """
        Save comprehensive assessment data
        """

        # Create the run folder
        run_folder = self.create_run_folder(search_id)

        # Process and enrich assessments (skip if pre-formatted)
        if pre_formatted:
            enriched_assessments = assessments  # Use as-is
        else:
            enriched_assessments = self._process_assessments(assessments)

        # 1. Save comprehensive CSV (with all requested fields)
        csv_path = self._save_comprehensive_csv(run_folder / "assessment.csv", enriched_assessments)

        # 2. Append to rolling master database
        self._append_to_master_database(enriched_assessments, search_id)

        # 3. Save other formats
        self._save_report(run_folder / "report.md", enriched_assessments, metadata)
        self._save_json(run_folder / "data.json", enriched_assessments, metadata)
        self._save_summary(run_folder / "summary.txt", enriched_assessments, search_id)

        # 3b. SAVE FULL MODEL REPORTS
        self._save_model_reports(run_folder / "mistral_full_reports.md", assessments)

        # 4. Save GO-only CSV if any
        go_opps = [a for a in enriched_assessments if a['final_decision'] == 'GO']
        if go_opps:
            self._save_go_csv(run_folder / "GO_opportunities.csv", go_opps)

        # Print summary
        self._print_results(run_folder, enriched_assessments)

        return run_folder

    def _get_knockout_category(self, knock_pattern: str) -> str:
        """
        Map knock patterns to category codes

        KNOCKOUT LEGEND:
        KO-01: Timing (expired deadline)
        KO-02: Domain (non-aviation)
        KO-03: Security/Clearance required
        KO-04: Set-asides (wrong type)
        KO-05: Source restrictions (sole source, OEM only)
        KO-06: Technical data (no drawings/TDP)
        KO-07: Export controls
        KO-08: AMC/AMSC codes
        KO-09: SAR requirement
        KO-10: Military platform/engine
        KO-11: Procurement restrictions (new manufacture without data)
        KO-12: Competition status (bridge/follow-on)
        KO-13: Subcontracting prohibited
        KO-14: Contract vehicle restrictions
        KO-15: Non-standard acquisition (OTA, BAA, SBIR)
        KO-16: IT system access required
        KO-17: Special certification required
        KO-18: Direct maintenance obligations
        KO-19: Native CAD format required
        GO-OK: Approved (civilian platform, commercial item)
        FA-00: Further analysis needed
        """
        if not knock_pattern:
            return "FA-00"

        pattern_lower = knock_pattern.lower()

        # Timing
        if 'expired' in pattern_lower or 'deadline' in pattern_lower:
            return "KO-01"
        # Domain
        elif 'non-aviation' in pattern_lower or 'playground' in pattern_lower:
            return "KO-02"
        # Security
        elif 'clearance' in pattern_lower or 'classified' in pattern_lower:
            return "KO-03"
        # Set-asides
        elif any(x in pattern_lower for x in ['8(a)', 'sdvosb', 'wosb', 'hubzone']):
            return "KO-04"
        # Source restrictions
        elif any(x in pattern_lower for x in ['sole source', 'oem only', 'intent to award']):
            return "KO-05"
        # Technical data
        elif 'no government drawings' in pattern_lower or 'no tdp' in pattern_lower:
            return "KO-06"
        # Export controls
        elif 'export control' in pattern_lower:
            return "KO-07"
        # AMC/AMSC
        elif 'amc' in pattern_lower or 'amsc' in pattern_lower:
            return "KO-08"
        # SAR
        elif 'sar' in pattern_lower:
            return "KO-09"
        # Military platforms
        elif any(x in pattern_lower for x in ['f-15', 'f-16', 'f-22', 'f-35', 'b-52', 'military aircraft']):
            return "KO-10"
        # Procurement restrictions
        elif 'new manufacture' in pattern_lower and 'without' in pattern_lower:
            return "KO-11"
        # Competition status
        elif 'bridge contract' in pattern_lower or 'follow-on' in pattern_lower:
            return "KO-12"
        # Subcontracting
        elif 'subcontracting prohibited' in pattern_lower:
            return "KO-13"
        # Contract vehicles
        elif any(x in pattern_lower for x in ['idiq', 'gwac', 'gsa schedule']):
            return "KO-14"
        # Non-standard
        elif any(x in pattern_lower for x in ['ota', 'baa', 'sbir', 'sttr']):
            return "KO-15"
        # IT access
        elif 'jedmics' in pattern_lower or 'etims' in pattern_lower:
            return "KO-16"
        # Certifications
        elif 'certification required' in pattern_lower:
            return "KO-17"
        # Maintenance
        elif 'depot' in pattern_lower or 'warranty' in pattern_lower:
            return "KO-18"
        # CAD formats
        elif any(x in pattern_lower for x in ['solidworks', 'catia', 'native cad']):
            return "KO-19"
        # GO patterns
        elif any(x in pattern_lower for x in ['civilian platform', 'commercial item', 'bell aircraft']):
            return "GO-OK"
        # Default
        else:
            return "FA-00"

    def _extract_value(self, value):
        """Extract value from dict or return as string"""
        if isinstance(value, dict):
            # If it's a dict like {'naics_code': '336413'}, extract the value
            if 'naics_code' in value:
                return str(value['naics_code'])
            elif 'psc_code' in value:
                return str(value['psc_code'])
            # Return first value if dict has any
            elif value:
                return str(list(value.values())[0])
        return str(value) if value else ''

    def _process_assessments(self, assessments: List[Dict]) -> List[Dict]:
        """
        Process and enrich assessments with all required fields
        Now expects unified Agent schema with 'result' field
        """
        processed = []

        for assessment in assessments:
            # Check if this is already in unified schema (has 'result' field)
            if 'result' in assessment:
                # Already in unified format - use directly
                final_decision = assessment['result']
                assessment_data = assessment  # Fields are at top level
            else:
                # Check multiple possible field names for the decision
                # Priority: result > final_decision > decision > nested assessment.decision
                assessment_data = assessment.get('assessment', {})

                # Try all possible field names
                decision = (
                    assessment.get('result') or
                    assessment.get('final_decision') or
                    assessment.get('decision') or
                    assessment_data.get('decision') or
                    assessment_data.get('result') or
                    assessment_data.get('final_decision') or
                    'INDETERMINATE'
                ).upper()

                if 'GO' == decision:
                    final_decision = 'GO'
                elif 'NO' in decision or 'NO-GO' in decision:
                    final_decision = 'NO-GO'
                elif 'FURTHER' in decision or 'CONTACT' in decision:
                    final_decision = 'INDETERMINATE'
                else:
                    final_decision = 'INDETERMINATE'

            # Extract agency info
            agency = assessment.get('agency', {})
            if isinstance(agency, dict):
                agency_name = str(agency.get('agency_name', 'Unknown')).replace('\n', ' ').replace('\r', ' ').strip()
            else:
                agency_name = str(agency).replace('\n', ' ').replace('\r', ' ').strip()

            # Handle knock_out_reasons (unified schema at top level, legacy in assessment_data)
            if 'result' in assessment:
                # Unified schema - knock_out_reasons at top level
                knock_out_reasons = assessment.get('knock_out_reasons', [])
            else:
                # Legacy format - in assessment_data
                knock_out_reasons = assessment_data.get('knock_out_reasons', [])

            if isinstance(knock_out_reasons, list):
                knock_pattern = '; '.join(str(r).replace('\n', ' ').replace('\r', ' ') for r in knock_out_reasons) if knock_out_reasons else str(assessment_data.get('rationale', assessment_data.get('reasoning', 'No pattern specified'))).replace('\n', ' ').replace('\r', ' ')
            else:
                knock_pattern = str(assessment_data.get('rationale', assessment_data.get('reasoning', 'No pattern specified'))).replace('\n', ' ').replace('\r', ' ')

            # Generate URLs (check unified schema first)
            sam_url = assessment.get('sam_url', '')  # SAM.gov/DIBBS source URL
            highergov_url = assessment.get('hg_url', assessment.get('url', ''))
            opp_id = assessment.get('solicitation_id', assessment.get('id', assessment.get('opp_key', '')))
            if not highergov_url and opp_id:
                highergov_url = f"https://app.highergov.com/opportunities/{opp_id}"

            # Get brief description (check unified schema 'summary' first)
            brief_desc = ''
            if assessment.get('summary'):
                brief_desc = assessment['summary'][:500].replace('\n', ' ').replace('\r', ' ').strip()
            elif assessment.get('description'):
                brief_desc = assessment['description'][:500].replace('\n', ' ').replace('\r', ' ').strip()
            elif assessment.get('description_text'):
                brief_desc = assessment['description_text'][:500].replace('\n', ' ').replace('\r', ' ').strip()
            elif assessment.get('ai_summary'):
                brief_desc = assessment['ai_summary'][:500].replace('\n', ' ').replace('\r', ' ').strip()
            elif assessment.get('full_text'):
                brief_desc = assessment['full_text'][:500].replace('\n', ' ').replace('\r', ' ').strip()
            elif assessment.get('text'):
                brief_desc = assessment['text'][:500].replace('\n', ' ').replace('\r', ' ').strip()

            # Determine knockout category code
            knockout_category = self._get_knockout_category(knock_pattern)

            # Get pipeline stage and assessment type (from unified schema)
            pipeline_stage = assessment.get('pipeline_stage', '')
            assessment_type = assessment.get('assessment_type', '')

            # Build enriched record
            enriched = {
                # Core decision fields - use 'result' as primary for output
                'result': final_decision,  # Primary field following unified schema
                'final_decision': final_decision,  # Internal use for counting/filtering (not duplicated in CSV)
                'knock_pattern': knock_pattern,
                'knockout_category': knockout_category,
                'sos_pipeline_title': assessment.get('sos_pipeline_title', assessment_data.get('sos_pipeline_title', '')),
                # Use clean reasoning text, not JSON blob (check unified 'rationale' first)
                'analysis_notes': str(assessment.get('rationale', assessment_data.get('reasoning', assessment_data.get('primary_blocker', ''))))[:1000].replace('\n', ' ').replace('\r', ' ').replace('"', "'"),
                # Removed confidence - we don't calculate it
                'recommendation': assessment.get('recommendation', assessment_data.get('recommendation', '')),
                'special_action': assessment.get('special_action', assessment_data.get('special_action', '')),

                # Opportunity details (check unified schema fields first)
                'sam_url': sam_url,
                'highergov_url': highergov_url,
                'announcement_number': assessment.get('solicitation_id', assessment.get('solicitation_number', assessment.get('announcement_number', assessment.get('source_id', '')))),
                'announcement_title': str(assessment.get('solicitation_title', assessment.get('title', ''))).replace('\n', ' ').replace('\r', ' ').strip(),
                'agency': agency_name,
                'due_date': assessment.get('due_date', assessment.get('response_date', '')),
                'brief_description': brief_desc,

                # Additional metadata - handle both field name formats
                'posted_date': assessment.get('posted_date', assessment.get('publish_date', '')),
                'naics': self._extract_value(assessment.get('naics', assessment.get('naics_code', ''))),
                'psc': self._extract_value(assessment.get('psc', assessment.get('psc_code', ''))),
                'set_aside': assessment.get('set_aside', assessment.get('setAside', '')),
                'value_low': assessment.get('value_low', assessment.get('valueLow', assessment.get('val_est_low', 0))),
                'value_high': assessment.get('value_high', assessment.get('valueHigh', assessment.get('val_est_high', 0))),
                'place_of_performance': assessment.get('place_of_performance', assessment.get('popCity', assessment.get('pop_city', ''))),
                'doc_length': len(assessment.get('full_text', assessment.get('text', assessment.get('description_text', '')))),

                # Tracking fields (include pipeline stage info)
                'assessment_timestamp': datetime.now().isoformat(),
                'opportunity_id': opp_id,
                'pipeline_stage': pipeline_stage,
                'assessment_type': assessment_type,

                # Keep full data for other uses
                '_full_data': assessment
            }

            processed.append(enriched)

        return processed

    def _save_comprehensive_csv(self, filepath: Path, assessments: List[Dict]) -> Path:
        """
        Save comprehensive CSV with all requested fields
        Column order as requested:
        1. GO/NO-GO/INDETERMINATE
        2. Knock pattern triggered
        3. HigherGov URL
        4. Announcement number
        5. Announcement title
        6. Agency
        7. Due date
        8. Brief description
        9. Model says
        10. Additional useful fields
        """

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            # Define columns in requested order
            fieldnames = [
                'result',                   # GO/NO-GO/INDETERMINATE (unified schema field)
                'knock_pattern',            # Pattern that triggered decision
                'knockout_category',        # Category code (KO-01, GO-OK, FA-00, etc.)
                'sos_pipeline_title',       # SOS Pipeline Title (PN | Qty | Condition | MDS | Description)
                'sam_url',                 # SAM.gov/DIBBS source URL
                'highergov_url',           # HigherGov platform URL
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
                'assessment_timestamp',    # When we assessed it
                # New verification fields
                'processing_method',       # REGEX_ONLY, BATCH_AI, AGENT_VERIFIED
                'verification_method',     # AGENT_CONFIRMED, AGENT_OVERRIDE, NONE
                'batch_decision',          # Original batch decision
                'agent_decision',          # Agent verification decision
                'disagreement',            # Whether batch and agent disagreed
                'verification_timestamp'   # When verification occurred
            ]

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for assessment in assessments:
                # Write only the fields we want in the CSV
                row = {field: assessment.get(field, '') for field in fieldnames}
                writer.writerow(row)

        return filepath

    def _append_to_master_database(self, assessments: List[Dict], search_id: str):
        """
        Append to rolling master database
        This captures EVERYTHING for later analytics or database import
        """

        # Daily master file
        today = datetime.now().strftime("%Y-%m-%d")
        master_file = self.master_db_path / f"master_{today}.csv"

        # All-time master file
        all_time_file = self.master_db_path / "master_all_time.csv"

        # Extended fieldnames for master database (everything we track)
        master_fieldnames = [
            'run_id',                  # Unique run identifier
            'search_id',                # HigherGov search ID
            'result',                   # Decision (GO/NO-GO/INDETERMINATE)
            'knock_pattern',
            'knockout_category',        # Category code
            'sos_pipeline_title',       # NEW: Pipeline title for SOS tracking
            'highergov_url',
            'announcement_number',
            'announcement_title',
            'agency',
            'due_date',
            'brief_description',
            'analysis_notes',
            'recommendation',
            'special_action',
            'posted_date',
            'naics',
            'psc',
            'set_aside',
            'value_low',
            'value_high',
            'place_of_performance',
            'doc_length',
            'assessment_timestamp',
            'opportunity_id',
            'run_timestamp'            # When this batch was run
        ]

        run_timestamp = datetime.now().isoformat()
        run_id = f"{search_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Prepare rows with run metadata
        rows_to_write = []
        for assessment in assessments:
            row = {field: assessment.get(field, '') for field in master_fieldnames}
            row['run_id'] = run_id
            row['search_id'] = search_id
            row['run_timestamp'] = run_timestamp
            rows_to_write.append(row)

        # Write to daily master
        daily_exists = master_file.exists()
        with open(master_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=master_fieldnames)
            if not daily_exists:
                writer.writeheader()
            writer.writerows(rows_to_write)

        # Write to all-time master
        all_time_exists = all_time_file.exists()
        with open(all_time_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=master_fieldnames)
            if not all_time_exists:
                writer.writeheader()
            writer.writerows(rows_to_write)

        # Also save as JSONL for easier database import
        jsonl_file = self.master_db_path / f"master_{today}.jsonl"
        with open(jsonl_file, 'a', encoding='utf-8') as f:
            for row in rows_to_write:
                f.write(json.dumps(row, default=str) + '\n')

    def _save_report(self, filepath: Path, assessments: List[Dict], metadata: Optional[Dict]):
        """Save executive report"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# SOS ASSESSMENT REPORT\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            if metadata:
                f.write(f"**Search ID:** {metadata.get('search_id', 'N/A')}\n")
            f.write("\n")

            # Count by decision
            go_count = sum(1 for a in assessments if a['final_decision'] == 'GO')
            no_go_count = sum(1 for a in assessments if a['final_decision'] == 'NO-GO')
            indeterminate_count = sum(1 for a in assessments if a['final_decision'] == 'INDETERMINATE')
            total = len(assessments)

            f.write("## SUMMARY\n\n")
            f.write(f"- **Total Assessed:** {total}\n")
            f.write(f"- **GO:** {go_count} ({go_count/total*100:.0f}%)\n")
            f.write(f"- **NO-GO:** {no_go_count} ({no_go_count/total*100:.0f}%)\n")
            f.write(f"- **INDETERMINATE:** {indeterminate_count}\n\n")

            # GO Opportunities detail
            go_opps = [a for a in assessments if a['final_decision'] == 'GO']
            if go_opps:
                f.write("## GO OPPORTUNITIES\n\n")
                for i, opp in enumerate(go_opps, 1):
                    f.write(f"### {i}. {opp['announcement_title']}\n")
                    f.write(f"- **Agency:** {opp['agency']}\n")
                    f.write(f"- **Number:** {opp['announcement_number']}\n")
                    f.write(f"- **Due:** {opp['due_date']}\n")
                    value_low = opp.get('value_low', 0)
                    value_high = opp.get('value_high', 0)
                    if isinstance(value_low, (int, float)) and isinstance(value_high, (int, float)):
                        f.write(f"- **Value:** ${value_low:,.0f} - ${value_high:,.0f}\n")
                    else:
                        f.write(f"- **Value:** {value_low} - {value_high}\n")
                    f.write(f"- **Analysis:** {opp.get('analysis_notes', '')}\n")
                    if opp.get('recommendation'):
                        f.write(f"- **Recommendation:** {opp['recommendation']}\n")
                    if opp.get('special_action'):
                        f.write(f"- **Action Required:** {opp['special_action']}\n")
                    # Removed confidence display - we don't calculate it
                    f.write(f"- **URL:** {opp['highergov_url']}\n\n")

            # NO-GO Summary
            no_go_opps = [a for a in assessments if a['final_decision'] == 'NO-GO']
            if no_go_opps:
                f.write("## NO-GO SUMMARY\n\n")
                f.write("| Title | Knock Pattern | Agency |\n")
                f.write("|-------|--------------|--------|\n")
                for opp in no_go_opps[:20]:
                    title = opp['announcement_title'][:40]
                    pattern = opp['knock_pattern'][:30]
                    agency = opp['agency'][:25]
                    f.write(f"| {title}... | {pattern}... | {agency} |\n")

            # Indeterminate
            indeterminate_opps = [a for a in assessments if a['final_decision'] == 'INDETERMINATE']
            if indeterminate_opps:
                f.write("\n## INDETERMINATE - NEEDS REVIEW\n\n")
                for opp in indeterminate_opps:
                    f.write(f"- {opp['announcement_title']} ({opp['announcement_number']})\n")

    def _save_json(self, filepath: Path, assessments: List[Dict], metadata: Optional[Dict]):
        """Save complete data as JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'generated': datetime.now().isoformat(),
                    'total': len(assessments),
                    **(metadata or {})
                },
                'summary': {
                    'go': sum(1 for a in assessments if a['final_decision'] == 'GO'),
                    'no_go': sum(1 for a in assessments if a['final_decision'] == 'NO-GO'),
                    'indeterminate': sum(1 for a in assessments if a['final_decision'] == 'INDETERMINATE')
                },
                'assessments': [{k: v for k, v in a.items() if k not in ('_full_data', 'final_decision')} for a in assessments]
            }, f, indent=2, default=str)

    def _save_go_csv(self, filepath: Path, go_opportunities: List[Dict]):
        """Save GO-only CSV for quick action"""
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'announcement_title', 'agency', 'announcement_number',
                'value_high', 'due_date', 'highergov_url'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for opp in go_opportunities:
                writer.writerow({field: opp.get(field, '') for field in fieldnames})

    def _save_model_reports(self, filepath: Path, assessments: List[Dict]):
        """
        Save FULL MODEL REPORTS for EVERY opportunity
        This is what you've been asking for!
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# MISTRAL AI FULL ASSESSMENT REPORTS\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n")
            f.write(f"**Total Opportunities:** {len(assessments)}\n\n")
            f.write("="*70 + "\n\n")

            for i, opp in enumerate(assessments, 1):
                f.write(f"## {i}. {opp.get('title', 'UNKNOWN')}\n\n")
                f.write(f"**URL:** {opp.get('url', '')}\n")
                f.write(f"**Agency:** {opp.get('agency', '')}\n")
                f.write(f"**Document Size:** {len(opp.get('text', '')):,} chars\n\n")

                # Get the assessment
                assessment = opp.get('assessment', {})

                f.write(f"### DECISION: {assessment.get('decision', 'UNKNOWN')}\n\n")
                # Removed confidence display - we don't calculate it
                f.write("\n")

                f.write("### REASONING\n")
                f.write(assessment.get('reasoning', 'No reasoning provided') + "\n\n")

                f.write("### DETAILED ANALYSIS\n")

                # Parse and format the detailed analysis properly
                detailed = assessment.get('detailed_analysis', '')

                # Check if detailed analysis is a JSON blob
                if detailed and (detailed.strip().startswith('```json') or detailed.strip().startswith('{')):
                    try:
                        # Clean up JSON markers
                        json_text = detailed
                        if '```json' in json_text:
                            # Extract JSON between markers
                            start = json_text.find('```json') + 7
                            end = json_text.find('```', start)
                            if end > start:
                                json_text = json_text[start:end].strip()
                        elif json_text.strip().startswith('{'):
                            # Find the complete JSON object
                            brace_count = 0
                            end_pos = 0
                            for i, char in enumerate(json_text):
                                if char == '{':
                                    brace_count += 1
                                elif char == '}':
                                    brace_count -= 1
                                    if brace_count == 0:
                                        end_pos = i + 1
                                        break
                            if end_pos > 0:
                                json_text = json_text[:end_pos]

                        import json
                        data = json.loads(json_text)

                        # Format as professional report - NO RAW JSON
                        if data.get('summary'):
                            f.write(f"**Summary:** {data['summary']}\n\n")

                        if data.get('knock_out_reasons') and data['knock_out_reasons']:
                            f.write("**Knockout Reasons:**\n")
                            for reason in data['knock_out_reasons']:
                                f.write(f"- {reason}\n")
                            f.write("\n")

                        if data.get('exceptions') and data['exceptions']:
                            f.write("**Exceptions:**\n")
                            for exc in data['exceptions']:
                                f.write(f"- {exc}\n")
                            f.write("\n")

                        if data.get('recommendation'):
                            f.write(f"**Recommendation:** {data['recommendation']}\n\n")

                        if data.get('special_action') and data['special_action'] != 'None':
                            f.write(f"**Special Action Required:** {data['special_action']}\n\n")

                    except Exception as e:
                        # If JSON parsing fails, extract key information from text
                        if 'NO-GO' in detailed or 'no-go' in detailed:
                            f.write("This opportunity was marked as NO-GO by the assessment model.\n")
                        elif 'GO' in detailed:
                            f.write("This opportunity was marked as GO by the assessment model.\n")

                        # Try to extract the rationale from the text
                        if 'rationale' in detailed.lower():
                            try:
                                import re
                                rationale_match = re.search(r'"rationale":\s*"([^"]+)"', detailed)
                                if rationale_match:
                                    f.write(f"\n{rationale_match.group(1)}\n\n")
                            except:
                                pass
                else:
                    # Not JSON - write clean text
                    if detailed:
                        f.write(f"{detailed}\n\n")

                f.write("### PIPELINE TITLE\n")
                f.write(assessment.get('sos_pipeline_title', 'Not generated') + "\n\n")

                # Don't show redundant model output - we already parsed and displayed it cleanly above
                f.write("\n" + "-"*70 + "\n\n")

            f.write("\n" + "="*70 + "\n")
            f.write("END OF MODEL REPORTS\n")
            f.write("="*70 + "\n")

    def _save_summary(self, filepath: Path, assessments: List[Dict], search_id: str):
        """Save quick summary"""
        go_count = sum(1 for a in assessments if a['final_decision'] == 'GO')
        no_go_count = sum(1 for a in assessments if a['final_decision'] == 'NO-GO')
        indeterminate_count = sum(1 for a in assessments if a['final_decision'] == 'INDETERMINATE')

        with open(filepath, 'w') as f:
            f.write(f"SOS Assessment Summary\n")
            f.write(f"={'='*30}\n")
            f.write(f"Search: {search_id}\n")
            f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"\nResults:\n")
            f.write(f"  GO: {go_count}\n")
            f.write(f"  NO-GO: {no_go_count}\n")
            f.write(f"  INDETERMINATE: {indeterminate_count}\n")
            f.write(f"  TOTAL: {len(assessments)}\n")

    def _print_results(self, run_folder: Path, assessments: List[Dict]):
        """Print results summary"""
        go_count = sum(1 for a in assessments if a['final_decision'] == 'GO')
        no_go_count = sum(1 for a in assessments if a['final_decision'] == 'NO-GO')
        indeterminate_count = sum(1 for a in assessments if a['final_decision'] == 'INDETERMINATE')

        print("\n" + "="*60)
        print("ASSESSMENT COMPLETE")
        print("="*60)
        print(f"\nSaved to: {run_folder}")
        print("\nFiles generated:")
        for file in run_folder.glob("*"):
            print(f"  - {file.name}")

        print("\nResults:")
        print(f"  GO: {go_count}")
        print(f"  NO-GO: {no_go_count}")
        print(f"  INDETERMINATE: {indeterminate_count}")
        print(f"  TOTAL: {len(assessments)}")

        print("\nMaster Database Updated:")
        print(f"  Daily: Master_Database/master_{datetime.now().strftime('%Y-%m-%d')}.csv")
        print(f"  All-Time: Master_Database/master_all_time.csv")
        print("="*60)

    def get_master_stats(self) -> Dict:
        """Get statistics from master database"""
        all_time_file = self.master_db_path / "master_all_time.csv"
        if not all_time_file.exists():
            return {'error': 'No master database found'}

        stats = {
            'total_assessed': 0,
            'total_go': 0,
            'total_no_go': 0,
            'total_indeterminate': 0,
            'unique_agencies': set(),
            'date_range': {'first': None, 'last': None}
        }

        with open(all_time_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                stats['total_assessed'] += 1
                if row['final_decision'] == 'GO':
                    stats['total_go'] += 1
                elif row['final_decision'] == 'NO-GO':
                    stats['total_no_go'] += 1
                else:
                    stats['total_indeterminate'] += 1

                stats['unique_agencies'].add(row.get('agency', ''))

                # Track date range
                timestamp = row.get('assessment_timestamp', '')
                if timestamp:
                    if not stats['date_range']['first'] or timestamp < stats['date_range']['first']:
                        stats['date_range']['first'] = timestamp
                    if not stats['date_range']['last'] or timestamp > stats['date_range']['last']:
                        stats['date_range']['last'] = timestamp

        stats['unique_agencies'] = len(stats['unique_agencies'])
        stats['go_rate'] = (stats['total_go'] / stats['total_assessed'] * 100) if stats['total_assessed'] > 0 else 0

        return stats


def integrate_enhanced_output(assessments: List[Dict], search_id: str, metadata: Optional[Dict] = None) -> Path:
    """
    Drop-in replacement for output manager with enhanced CSV and database
    """
    manager = EnhancedOutputManager()
    return manager.save_assessment_batch(search_id, assessments, metadata)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "stats":
        # Show master database statistics
        manager = EnhancedOutputManager()
        stats = manager.get_master_stats()

        print("\nMASTER DATABASE STATISTICS")
        print("="*40)
        print(f"Total Assessed: {stats.get('total_assessed', 0)}")
        print(f"GO: {stats.get('total_go', 0)}")
        print(f"NO-GO: {stats.get('total_no_go', 0)}")
        print(f"INDETERMINATE: {stats.get('total_indeterminate', 0)}")
        print(f"GO Rate: {stats.get('go_rate', 0):.1f}%")
        print(f"Unique Agencies: {stats.get('unique_agencies', 0)}")
        if stats.get('date_range'):
            print(f"Date Range: {stats['date_range']['first']} to {stats['date_range']['last']}")
    else:
        print("Enhanced Output Manager")
        print("Features:")
        print("  - Comprehensive CSV with all requested fields")
        print("  - Rolling master database for analytics")
        print("  - Daily and all-time tracking")
        print("\nUsage:")
        print("  python enhanced_output_manager.py stats  # View database statistics")
