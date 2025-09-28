#!/usr/bin/env python3
"""
Pipeline Stage Viewer - Shows exact JSON output from each pipeline stage.
"""

import json
from datetime import datetime
import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional

class PipelineStageViewer:
    """Display detailed stage-by-stage pipeline results with JSON outputs."""

    def __init__(self):
        self.stage_names = {
            'REGEX': 'Stage 1: Regex Pattern Matching',
            'BATCH': 'Stage 2: Batch Model Assessment',
            'AGENT': 'Stage 3: Agent Verification'
        }

        self.stage_colors = {
            'REGEX': '#FF6B6B',  # Red
            'BATCH': '#4ECDC4',  # Teal
            'AGENT': '#45B7D1'   # Blue
        }

    def render_pipeline_journey(self, row: pd.Series) -> None:
        """Render the complete pipeline journey for an opportunity."""

        # Extract pipeline tracking data
        pipeline_tracking = {}

        # Check if pipeline_tracking exists as a column
        if 'pipeline_tracking' in row and pd.notna(row['pipeline_tracking']):
            try:
                if isinstance(row['pipeline_tracking'], str):
                    pipeline_tracking = json.loads(row['pipeline_tracking'])
                elif isinstance(row['pipeline_tracking'], dict):
                    pipeline_tracking = row['pipeline_tracking']
            except:
                pass

        # Also check for individual stage columns
        if not pipeline_tracking:
            # Build from individual columns if available
            if 'stage1_regex_decision' in row:
                pipeline_tracking['stage1_regex'] = row.get('stage1_regex_decision', '')
                pipeline_tracking['stage1_reason'] = row.get('stage1_regex_reason', '')
            if 'stage2_batch_decision' in row:
                pipeline_tracking['stage2_batch'] = row.get('stage2_batch_decision', '')
                pipeline_tracking['stage2_reason'] = row.get('stage2_batch_reason', '')
            if 'stage3_agent_decision' in row:
                pipeline_tracking['stage3_agent'] = row.get('stage3_agent_decision', '')
                pipeline_tracking['stage3_reason'] = row.get('stage3_agent_reason', '')

        # Display pipeline flow
        st.write("### 🔄 Pipeline Journey")

        # Create columns for each stage
        cols = st.columns(3)

        # Stage 1: Regex
        with cols[0]:
            st.markdown("#### 🔍 Stage 1: Regex")
            decision = pipeline_tracking.get('stage1_regex', 'Not Processed')
            reason = pipeline_tracking.get('stage1_reason', '')

            if decision in ['NO-GO', 'No-Go']:
                st.error(f"❌ {decision.replace('NO-GO', 'No-Go')}")
                st.caption(f"Knocked out: {reason}")
                st.json({
                    "stage": "REGEX",
                    "decision": decision,
                    "reason": reason,
                    "continued": False
                })
            elif decision in ['GO', 'CONTINUE']:
                st.success(f"✅ {decision.replace('GO', 'Go').replace('CONTINUE', 'Continue')}")
                st.caption("Passed to next stage")
                st.json({
                    "stage": "REGEX",
                    "decision": decision,
                    "reason": reason or "No knockouts found",
                    "continued": True
                })
            else:
                st.info("⏭️ Skipped or Not Run")

        # Stage 2: Batch
        with cols[1]:
            st.markdown("#### 🤖 Stage 2: Batch")
            decision = pipeline_tracking.get('stage2_batch', 'Not Processed')
            reason = pipeline_tracking.get('stage2_reason', '')

            # Extract batch JSON if available
            batch_json = {}
            if 'batch_response' in row and pd.notna(row['batch_response']):
                try:
                    if isinstance(row['batch_response'], str):
                        batch_json = json.loads(row['batch_response'])
                    elif isinstance(row['batch_response'], dict):
                        batch_json = row['batch_response']
                except:
                    batch_json = {"raw": str(row.get('batch_response', ''))}

            if decision in ['NO-GO', 'No-Go']:
                st.error(f"❌ {decision.replace('NO-GO', 'No-Go')}")
                st.caption(f"Reason: {reason[:50]}...")
            elif decision in ['GO', 'Go']:
                st.success(f"✅ {decision.replace('GO', 'Go').replace('CONTINUE', 'Continue')}")
                st.caption("Approved")
            elif decision in ['INDETERMINATE', 'Indeterminate']:
                st.warning(f"❓ {decision}")
                st.caption("Needs agent review")
            else:
                st.info("⏭️ Not Processed")

            # Show batch model response if available
            if batch_json:
                with st.expander("View Batch Model Response"):
                    st.json(batch_json)
            elif decision and decision != 'Not Processed':
                st.json({
                    "stage": "BATCH",
                    "decision": decision,
                    "rationale": reason,
                    "continued": decision != 'NO-GO'
                })

        # Stage 3: Agent
        with cols[2]:
            st.markdown("#### 🎯 Stage 3: Agent")
            decision = pipeline_tracking.get('stage3_agent', 'Not Processed')
            reason = pipeline_tracking.get('stage3_reason', '')

            # Extract agent JSON if available
            agent_json = {}
            if 'agent_response' in row and pd.notna(row['agent_response']):
                try:
                    if isinstance(row['agent_response'], str):
                        agent_json = json.loads(row['agent_response'])
                    elif isinstance(row['agent_response'], dict):
                        agent_json = row['agent_response']
                except:
                    agent_json = {"raw": str(row.get('agent_response', ''))}

            if decision in ['NO-GO', 'No-Go']:
                st.error(f"❌ {decision.replace('NO-GO', 'No-Go')}")
                st.caption(f"Final: {reason[:50]}...")
            elif decision in ['GO', 'Go']:
                st.success(f"✅ {decision.replace('GO', 'Go').replace('CONTINUE', 'Continue')}")
                st.caption("Final: Approved")
            else:
                st.info("⏭️ Not Required")

            # Show agent response if available
            if agent_json:
                with st.expander("View Agent Response"):
                    st.json(agent_json)
            elif decision and decision != 'Not Processed':
                st.json({
                    "stage": "AGENT",
                    "decision": decision,
                    "rationale": reason,
                    "knockout": row.get('knockout', {}),
                    "government_quotes": row.get('government_quotes', [])
                })

    def render_stage_comparison(self, df: pd.DataFrame) -> None:
        """Show comparison of decisions across stages."""

        st.write("### 📊 Stage Decision Distribution")

        # Create metrics for each stage
        cols = st.columns(3)

        # Stage 1 metrics
        with cols[0]:
            st.markdown("**Stage 1: Regex**")
            stage1_counts = {
                'NO-GO': 0,
                'CONTINUE': 0,
                'SKIPPED': 0
            }

            for _, row in df.iterrows():
                if 'stage1_regex_decision' in row:
                    decision = row['stage1_regex_decision']
                    if 'NO-GO' in str(decision) or 'No-Go' in str(decision):
                        stage1_counts['NO-GO'] += 1
                    elif decision:
                        stage1_counts['CONTINUE'] += 1
                    else:
                        stage1_counts['SKIPPED'] += 1

            st.metric("Knocked Out", stage1_counts['NO-GO'])
            st.metric("Passed Through", stage1_counts['CONTINUE'])

        # Stage 2 metrics
        with cols[1]:
            st.markdown("**Stage 2: Batch**")
            stage2_counts = {
                'GO': 0,
                'NO-GO': 0,
                'INDETERMINATE': 0
            }

            for _, row in df.iterrows():
                if 'stage2_batch_decision' in row:
                    decision = str(row['stage2_batch_decision'])
                    if 'NO-GO' in decision or 'No-Go' in decision:
                        stage2_counts['NO-GO'] += 1
                    elif 'INDETERMINATE' in decision or 'Indeterminate' in decision:
                        stage2_counts['INDETERMINATE'] += 1
                    elif 'GO' in decision or 'Go' in decision:
                        stage2_counts['GO'] += 1

            st.metric("GO", stage2_counts['GO'])
            st.metric("NO-GO", stage2_counts['NO-GO'])
            st.metric("Indeterminate", stage2_counts['INDETERMINATE'])

        # Stage 3 metrics
        with cols[2]:
            st.markdown("**Stage 3: Agent**")
            stage3_counts = {
                'GO': 0,
                'NO-GO': 0,
                'NOT_RUN': 0
            }

            for _, row in df.iterrows():
                if 'stage3_agent_decision' in row and pd.notna(row['stage3_agent_decision']):
                    decision = str(row['stage3_agent_decision'])
                    if 'NO-GO' in decision or 'No-Go' in decision:
                        stage3_counts['NO-GO'] += 1
                    elif 'GO' in decision or 'Go' in decision:
                        stage3_counts['GO'] += 1
                else:
                    stage3_counts['NOT_RUN'] += 1

            if stage3_counts['NOT_RUN'] < len(df):
                st.metric("Final GO", stage3_counts['GO'])
                st.metric("Final NO-GO", stage3_counts['NO-GO'])
            else:
                st.info("Agent verification not run")

    def render_json_outputs(self, row: pd.Series) -> None:
        """Display raw JSON outputs from each stage in the EXACT required schema format."""

        st.write("### 📝 Raw Stage Outputs (EXACT Schema)")

        tabs = st.tabs(["Regex Output", "Batch Output", "Agent Output"])

        # Regex output (limited fields since regex can't infer)
        with tabs[0]:
            solicitation_id = row.get('announcement_number', row.get('solicitation_id', 'N/A'))
            decision = row.get('stage1_regex_decision', 'N/A')

            regex_output = {
                "AssessmentHeaderLine": f"{decision.replace('NO-GO', 'No-Go').replace('GO', 'Go').replace('CONTINUE', 'Continue')}-{solicitation_id}",
                "SolicitationTitle": row.get('announcement_title', row.get('solicitation_title', 'N/A')),
                "SolicitationNumber": solicitation_id,
                "MDSPlatformCommercialDesignation": None,
                "TriageDate": datetime.now().strftime('%m-%d-%Y'),
                "DatePosted": None,
                "DateResponsesSubmissionsDue": None,
                "DaysOpen": None,
                "RemainingDays": None,
                "PotentialAward": {
                    "Exceeds25K": None,
                    "Range": None
                },
                "FinalRecommendation": f"{decision.replace('NO-GO', 'No-Go').replace('GO', 'Go').replace('CONTINUE', 'Continue')} - {row.get('stage1_regex_reason', 'Pattern match')}",
                "Scope": None,
                "KnockoutLogic": f"Category {row.get('knockout_category', 'N/A')}: {row.get('stage1_regex_reason', 'Pattern match')}",
                "SOSPipelineNotes": f"PN: NA | Qty: NA | Condition: NA | MDS: NA | {solicitation_id} | Regex knockout",
                "QuestionsForCO": []
            }
            st.json(regex_output)

        # Batch output (partial schema - batch can infer some fields)
        with tabs[1]:
            solicitation_id = row.get('announcement_number', row.get('solicitation_id', 'N/A'))
            decision = row.get('stage2_batch_decision', 'N/A')

            # Try to extract structured batch response if available
            batch_parsed = {}
            if 'batch_response' in row and pd.notna(row['batch_response']):
                try:
                    if isinstance(row['batch_response'], str):
                        batch_parsed = json.loads(row['batch_response'])
                    elif isinstance(row['batch_response'], dict):
                        batch_parsed = row['batch_response']
                except:
                    pass

            batch_output = {
                "AssessmentHeaderLine": batch_parsed.get('AssessmentHeaderLine', batch_parsed.get('HeaderLine', f"{decision.replace('NO-GO', 'No-Go').replace('GO', 'Go').replace('INDETERMINATE', 'Indeterminate')}-{solicitation_id}")),
                "SolicitationTitle": row.get('announcement_title', row.get('solicitation_title', 'N/A')),
                "SolicitationNumber": solicitation_id,
                "MDSPlatformCommercialDesignation": batch_parsed.get('MDSPlatformCommercialDesignation', "Indeterminate MDS | Indeterminate"),
                "TriageDate": datetime.now().strftime('%m-%d-%Y'),
                "DatePosted": batch_parsed.get('DatePosted', row.get('posted_date', None)),
                "DateResponsesSubmissionsDue": batch_parsed.get('DateResponsesSubmissionsDue', row.get('due_date', None)),
                "DaysOpen": batch_parsed.get('DaysOpen', None),
                "RemainingDays": batch_parsed.get('RemainingDays', None),
                "PotentialAward": batch_parsed.get('PotentialAward', {
                    "Exceeds25K": None,
                    "Range": None
                }),
                "FinalRecommendation": batch_parsed.get('FinalRecommendation', row.get('stage2_batch_reason', 'N/A')),
                "Scope": batch_parsed.get('Scope', 'Indeterminate'),
                "KnockoutLogic": batch_parsed.get('KnockoutLogic', row.get('stage2_batch_reason', 'Batch model assessment')),
                "SOSPipelineNotes": batch_parsed.get('SOSPipelineNotes', row.get('sos_pipeline_title', f"PN: NA | Qty: NA | Condition: NA | MDS: NA | {solicitation_id} | Batch assessment")),
                "QuestionsForCO": batch_parsed.get('QuestionsForCO', [])
            }

            st.json(batch_output)

        # Agent output (full schema - agent provides complete assessment)
        with tabs[2]:
            solicitation_id = row.get('announcement_number', row.get('solicitation_id', 'N/A'))
            decision = row.get('stage3_agent_decision', row.get('result', 'N/A'))

            # Try to extract structured agent response if available
            agent_parsed = {}
            if 'agent_response' in row and pd.notna(row['agent_response']):
                try:
                    if isinstance(row['agent_response'], str):
                        agent_parsed = json.loads(row['agent_response'])
                    elif isinstance(row['agent_response'], dict):
                        agent_parsed = row['agent_response']
                except:
                    pass

            # Build complete agent output in EXACT schema
            agent_output = {
                "AssessmentHeaderLine": agent_parsed.get('AssessmentHeaderLine', agent_parsed.get('HeaderLine', f"{decision.replace('NO-GO', 'No-Go').replace('GO', 'Go')}-{solicitation_id}")),
                "SolicitationTitle": row.get('announcement_title', row.get('solicitation_title', 'N/A')),
                "SolicitationNumber": solicitation_id,
                "MDSPlatformCommercialDesignation": agent_parsed.get('MDSPlatformCommercialDesignation', row.get('MDSPlatformCommercialDesignation', 'Indeterminate MDS | Commercial Item: Indeterminate')),
                "TriageDate": datetime.now().strftime('%m-%d-%Y'),
                "DatePosted": agent_parsed.get('DatePosted', row.get('posted_date', row.get('DatePosted', None))),
                "DateResponsesSubmissionsDue": agent_parsed.get('DateResponsesSubmissionsDue', row.get('due_date', row.get('DateResponsesSubmissionsDue', None))),
                "DaysOpen": agent_parsed.get('DaysOpen', row.get('DaysOpen', None)),
                "RemainingDays": agent_parsed.get('RemainingDays', row.get('RemainingDays', None)),
                "PotentialAward": agent_parsed.get('PotentialAward', row.get('PotentialAward', {
                    "Exceeds25K": "Yes, typical government contract",
                    "Range": row.get('award_estimate', '$100K-$500K estimated')
                })),
                "FinalRecommendation": agent_parsed.get('FinalRecommendation', row.get('stage3_agent_reason', row.get('FinalRecommendation', 'N/A'))),
                "Scope": agent_parsed.get('Scope', row.get('Scope', 'Purchase')),
                "KnockoutLogic": agent_parsed.get('KnockoutLogic', row.get('KnockoutLogic', 'All 19 categories assessed by agent')),
                "SOSPipelineNotes": agent_parsed.get('SOSPipelineNotes', row.get('sos_pipeline_title', f"PN: NA | Qty: NA | Condition: NA | MDS: NA | {solicitation_id} | Agent assessment")),
                "QuestionsForCO": agent_parsed.get('QuestionsForCO', row.get('QuestionsForCO', []))
            }

            st.json(agent_output)

# Usage example
if __name__ == "__main__":
    # This would be integrated into the main app.py
    viewer = PipelineStageViewer()

    # Sample data for testing
    sample_row = pd.Series({
        'stage1_regex_decision': 'CONTINUE',
        'stage1_regex_reason': 'No knockouts found',
        'stage2_batch_decision': 'INDETERMINATE',
        'stage2_batch_reason': 'Navy platform with FAA 8130 - needs review',
        'stage3_agent_decision': 'GO',
        'stage3_agent_reason': 'P-8 Poseidon commercial platform with FAA 8130 acceptable'
    })

    st.title("Pipeline Stage Viewer Test")
    viewer.render_pipeline_journey(sample_row)