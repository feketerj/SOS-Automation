#!/usr/bin/env python3
"""Ensure verification fields appear in CSV when provided (pre_formatted flow)."""

from enhanced_output_manager import EnhancedOutputManager
import tempfile
from pathlib import Path
import csv


def test_csv_contains_verification_columns_when_present():
    results = [
        {
            'result': 'GO',
            'solicitation_id': 'ID1',
            'solicitation_title': 'T1',
            'processing_method': 'AGENT_AI',
            'verification_method': 'AGENT_CONFIRMED',
            'batch_decision': 'INDETERMINATE',
            'agent_decision': 'GO',
            'disagreement': True,
            'verification_timestamp': '2025-09-13T12:00:00'
        }
    ]

    with tempfile.TemporaryDirectory() as tmp:
        m = EnhancedOutputManager(base_path=tmp)
        outdir = m.save_assessment_batch('TEST', results, metadata={'search_id': 'TEST'}, pre_formatted=True)
        csv_path = Path(outdir) / 'assessment.csv'
        assert csv_path.exists()
        with csv_path.open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
        for col in ('verification_method', 'batch_decision', 'agent_decision', 'disagreement', 'verification_timestamp'):
            assert col in headers

