#!/usr/bin/env python3
"""Verify EnhancedOutputManager handles missing/legacy fields gracefully."""

from enhanced_output_manager import EnhancedOutputManager
import tempfile
from pathlib import Path


def test_resilience_with_partial_records():
    # Missing URLs and using legacy decision fields should not crash
    assessments = [
        {'decision': 'GO', 'title': 'Legacy A', 'solicitation_id': 'A'},
        {'final_decision': 'NO-GO', 'announcement_title': 'Legacy B', 'announcement_number': 'B'},
        {'assessment': {'decision': 'INDETERMINATE'}, 'solicitation_title': 'Legacy C', 'solicitation_id': 'C'},
    ]

    with tempfile.TemporaryDirectory() as tmp:
        m = EnhancedOutputManager(base_path=tmp)
        outdir = m.save_assessment_batch('TEST', assessments, metadata={'search_id': 'TEST'})
        assert Path(outdir).exists()

