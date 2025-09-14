#!/usr/bin/env python3
"""Ensure data.json has expected top-level structure after save."""

from enhanced_output_manager import EnhancedOutputManager
import tempfile
from pathlib import Path
import json


def test_data_json_top_level_fields():
    assessments = [{
        'result': 'GO',
        'solicitation_id': 'ID1',
        'solicitation_title': 'Title 1'
    }]
    with tempfile.TemporaryDirectory() as tmp:
        m = EnhancedOutputManager(base_path=tmp)
        outdir = m.save_assessment_batch('TESTSID', assessments, metadata={'search_id': 'TESTSID'})
        data_path = Path(outdir) / 'data.json'
        assert data_path.exists()
        data = json.loads(data_path.read_text(encoding='utf-8'))
        assert 'metadata' in data and 'assessments' in data
        assert isinstance(data['assessments'], list) and len(data['assessments']) == 1
        assert data['metadata'].get('search_id') == 'TESTSID'

