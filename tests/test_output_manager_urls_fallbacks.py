#!/usr/bin/env python3
"""Ensure EnhancedOutputManager populates URL fields via fallbacks."""

from enhanced_output_manager import EnhancedOutputManager


def test_url_fallbacks_from_source_fields():
    manager = EnhancedOutputManager()
    assessments = [
        {
            'result': 'GO',
            'solicitation_id': 'X1',
            'solicitation_title': 'A',
            'source_path': 'https://sam.gov/example',
            'path': 'https://app.highergov.com/opportunities/ABC'
        },
        {
            'result': 'GO',
            'solicitation_id': 'Y2',
            'solicitation_title': 'B',
            # No path, but should fall back using solicitation_id into HigherGov URL
        }
    ]

    enriched = manager._process_assessments(assessments)
    # First item should carry both URLs from source fields
    a0 = enriched[0]
    assert a0.get('sam_url') == 'https://sam.gov/example'
    assert a0.get('highergov_url') == 'https://app.highergov.com/opportunities/ABC'

    # Second should synthesize highergov_url using solicitation_id
    a1 = enriched[1]
    assert a1.get('highergov_url', '').startswith('https://app.highergov.com/opportunities/')

