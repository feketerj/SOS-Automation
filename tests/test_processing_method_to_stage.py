#!/usr/bin/env python3
"""Validate mapping of processing_method to pipeline_stage and assessment_type.

Low-risk checks to ensure consistent stage metadata across variants.
"""

from enhanced_output_manager import EnhancedOutputManager


def test_processing_method_stage_mapping():
    manager = EnhancedOutputManager()
    assessments = [
        {
            'processing_method': 'REGEX_ONLY',
            'final_decision': 'NO-GO',
            'solicitation_title': 'Regex KO',
            'solicitation_id': 'R1',
        },
        {
            'processing_method': 'BATCH_AI',
            'final_decision': 'GO',
            'solicitation_title': 'Batch',
            'solicitation_id': 'B1',
        },
        {
            'processing_method': 'AGENT_AI',
            'final_decision': 'GO',
            'solicitation_title': 'Agent',
            'solicitation_id': 'A1',
        },
    ]

    enriched = manager._process_assessments(assessments)
    # Expect pipeline_stage and assessment_type set consistently
    stages = [e.get('pipeline_stage') for e in enriched]
    types = [e.get('assessment_type') for e in enriched]

    assert stages == ['APP', 'BATCH', 'AGENT']
    assert types == ['APP_KNOCKOUT', 'MISTRAL_BATCH_ASSESSMENT', 'MISTRAL_ASSESSMENT']

