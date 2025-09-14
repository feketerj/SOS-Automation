#!/usr/bin/env python3
"""Ensure GO-only CSV is created and contains GO rows only when applicable."""

from enhanced_output_manager import EnhancedOutputManager
import tempfile
from pathlib import Path
import csv


def test_go_only_csv_creation():
    assessments = [
        {'result': 'GO', 'solicitation_id': 'ID1', 'solicitation_title': 'T1'},
        {'result': 'NO-GO', 'solicitation_id': 'ID2', 'solicitation_title': 'T2'},
        {'result': 'INDETERMINATE', 'solicitation_id': 'ID3', 'solicitation_title': 'T3'},
    ]

    with tempfile.TemporaryDirectory() as tmp:
        m = EnhancedOutputManager(base_path=tmp)
        outdir = m.save_assessment_batch('TEST', assessments, metadata={'search_id': 'TEST'})
        go_csv = Path(outdir) / 'GO_opportunities.csv'
        assert go_csv.exists()

        with go_csv.open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        # Expect only GO items present
        assert len(rows) == 1

