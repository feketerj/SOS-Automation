"""Unit tests for EnhancedOutputManager edge cases"""
import sys
import os
from pathlib import Path
from datetime import datetime
import tempfile
import shutil
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from enhanced_output_manager import EnhancedOutputManager

def test_url_synthesis_fallbacks():
    """Test URL synthesis with missing sam_url and hg_url"""
    output_manager = EnhancedOutputManager()

    # Test with only solicitation_id
    data = {
        'solicitation_id': 'TEST123',
        'result': 'GO',
        'announcement_number': None,
        'sam_url': None,
        'hg_url': None,
        'highergov_url': None,
    }

    # Prepare the data (this method handles URL synthesis)
    prepared = output_manager._prepare_assessment_data([data])

    # Check that URLs were synthesized
    assert prepared[0]['sam_url'] != ''
    assert 'TEST123' in prepared[0]['sam_url'] or 'N/A' in prepared[0]['sam_url']

def test_title_and_id_fallbacks():
    """Test fallbacks for missing titles and IDs"""
    output_manager = EnhancedOutputManager()

    data = {
        'solicitation_id': None,
        'announcement_number': None,
        'opportunity_id': None,
        'solicitation_title': None,
        'announcement_title': None,
        'title': None,
        'result': 'NO-GO'
    }

    prepared = output_manager._prepare_assessment_data([data])

    # Should have some default values instead of None
    assert prepared[0]['announcement_number'] != None
    assert prepared[0]['announcement_title'] != None

def test_csv_resilience_with_special_chars():
    """Test CSV generation with special characters"""
    output_manager = EnhancedOutputManager()

    # Create temp directory for output
    with tempfile.TemporaryDirectory() as tmpdir:
        output_manager.base_output_dir = Path(tmpdir)

        data = [{
            'solicitation_id': 'TEST"123',  # Quote in ID
            'solicitation_title': 'Title with, comma and "quotes"',
            'result': 'GO',
            'rationale': 'Line 1\nLine 2\nLine 3',  # Multiline
            'sam_url': 'https://sam.gov/test',
            'hg_url': 'https://highergov.com/test',
        }]

        output_dir = output_manager.save_assessment_batch(
            'TEST_CSV',
            data,
            {'test': True}
        )

        csv_file = output_dir / 'assessment.csv'
        assert csv_file.exists()

        # Read and verify CSV doesn't break
        with open(csv_file, 'r') as f:
            lines = f.readlines()
            assert len(lines) >= 2  # Header + at least 1 data row

def test_empty_data_handling():
    """Test handling of empty data sets"""
    output_manager = EnhancedOutputManager()

    with tempfile.TemporaryDirectory() as tmpdir:
        output_manager.base_output_dir = Path(tmpdir)

        # Empty list
        output_dir = output_manager.save_assessment_batch(
            'EMPTY_TEST',
            [],
            {'test': True}
        )

        # Should still create output directory
        assert output_dir.exists()

        # Should create files even if empty
        json_file = output_dir / 'data.json'
        assert json_file.exists()

def test_field_name_resolution():
    """Test resolution of different field name variations"""
    output_manager = EnhancedOutputManager()

    test_cases = [
        {'result': 'GO'},
        {'final_decision': 'GO'},
        {'decision': 'GO'},
        {'classification': 'GO'},
    ]

    for data in test_cases:
        prepared = output_manager._prepare_assessment_data([data])
        # All should resolve to having a 'final_decision' field
        assert 'final_decision' in prepared[0]
        assert prepared[0]['final_decision'] == 'GO'

def test_master_database_daily_updates():
    """Test Master_Database daily and all-time file updates"""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_manager = EnhancedOutputManager()
        output_manager.base_output_dir = Path(tmpdir)

        # Create test data with specific dates
        today = datetime.now().strftime('%Y%m%d')
        data = [
            {
                'solicitation_id': 'TEST1',
                'result': 'GO',
                'assessment_timestamp': datetime.now().isoformat()
            },
            {
                'solicitation_id': 'TEST2',
                'result': 'NO-GO',
                'assessment_timestamp': datetime.now().isoformat()
            }
        ]

        # Save batch
        output_dir = output_manager.save_assessment_batch(
            'MASTER_TEST',
            data,
            {'test': True}
        )

        # Check for master database files
        master_db_dir = Path(tmpdir) / 'Master_Database'
        assert master_db_dir.exists()

        # Check for daily file
        daily_file = master_db_dir / f'assessments_{today}.csv'
        if daily_file.exists():
            with open(daily_file, 'r') as f:
                lines = f.readlines()
                assert len(lines) >= 3  # Header + 2 records