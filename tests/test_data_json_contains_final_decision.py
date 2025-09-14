#!/usr/bin/env python3
"""Ensure data.json includes 'final_decision' for internal analysis."""

from enhanced_output_manager import EnhancedOutputManager
import tempfile
from pathlib import Path
import json


def test_data_json_includes_final_decision():
    assessments = [{
        'result': 'NO-GO',
        'solicitation_id': 'ID9',
        'solicitation_title': 'Title 9'
    }]
    with tempfile.TemporaryDirectory() as tmp:
        m = EnhancedOutputManager(base_path=tmp)
        outdir = m.save_assessment_batch('TESTSID', assessments, metadata={'search_id': 'TESTSID'})
        data_path = Path(outdir) / 'data.json'
        data = json.loads(data_path.read_text(encoding='utf-8'))
        assert data['assessments'][0].get('final_decision') == 'NO-GO'

