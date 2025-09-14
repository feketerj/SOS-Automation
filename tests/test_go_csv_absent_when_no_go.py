#!/usr/bin/env python3
"""GO-only CSV should not be created when there are no GO results."""

from enhanced_output_manager import EnhancedOutputManager
import tempfile
from pathlib import Path


def test_go_csv_not_created_without_go():
    assessments = [
        {'result': 'NO-GO', 'solicitation_id': 'ID1', 'solicitation_title': 'T1'},
        {'result': 'INDETERMINATE', 'solicitation_id': 'ID2', 'solicitation_title': 'T2'},
    ]
    with tempfile.TemporaryDirectory() as tmp:
        m = EnhancedOutputManager(base_path=tmp)
        outdir = m.save_assessment_batch('TEST', assessments, metadata={'search_id': 'TEST'})
        go_csv = Path(outdir) / 'GO_opportunities.csv'
        assert not go_csv.exists()

