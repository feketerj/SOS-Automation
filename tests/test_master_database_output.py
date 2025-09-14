#!/usr/bin/env python3
"""Ensure Master_Database CSV is updated when saving a batch."""

from enhanced_output_manager import EnhancedOutputManager
import tempfile
from pathlib import Path


def test_master_database_files_created():
    assessments = [{
        'result': 'GO',
        'solicitation_id': 'ID1',
        'solicitation_title': 'Title 1'
    }]
    with tempfile.TemporaryDirectory() as tmp:
        m = EnhancedOutputManager(base_path=tmp)
        outdir = m.save_assessment_batch('TESTSID', assessments, metadata={'search_id': 'TESTSID'})
        # Check Master_Database exists with at least all_time csv
        master_dir = Path(tmp) / 'Master_Database'
        assert master_dir.exists()
        all_time = master_dir / 'master_all_time.csv'
        assert all_time.exists()
        # Daily file should also be present
        daily = [p for p in master_dir.glob('master_*.csv') if p.name != 'master_all_time.csv']
        assert any(daily)
