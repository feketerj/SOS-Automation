#!/usr/bin/env python3
"""Validate CSV columns and ordering produced by EnhancedOutputManager."""

from enhanced_output_manager import EnhancedOutputManager
import tempfile
from pathlib import Path
import csv


def test_csv_columns_and_ordering():
    manager = EnhancedOutputManager()
    assessments = [
        {
            'result': 'GO',
            'solicitation_id': 'ID1',
            'solicitation_title': 'Title 1',
            'sam_url': 'https://sam.gov/x',
            'hg_url': 'https://app.highergov.com/y',
        }
    ]

    with tempfile.TemporaryDirectory() as tmp:
        # Force base_path to temp to avoid touching real SOS_Output
        m = EnhancedOutputManager(base_path=tmp)
        outdir = m.save_assessment_batch('TEST', assessments, metadata={'search_id': 'TEST'})
        csv_path = Path(outdir) / 'assessment.csv'
        assert csv_path.exists()

        with csv_path.open(newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)

        # Spot-check expected column positions
        assert headers[0] == 'result'
        assert 'sos_pipeline_title' in headers
        assert 'sam_url' in headers and 'highergov_url' in headers
        # 'final_decision' should not be a CSV column (internal only)
        assert 'final_decision' not in headers
