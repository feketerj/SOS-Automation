#!/usr/bin/env python3
"""Verify Master_Database updates are working correctly"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from enhanced_output_manager import EnhancedOutputManager
import tempfile
from pathlib import Path
import csv

def verify_master_database():
    """Test Master_Database creation and updates"""
    print("Testing Master_Database functionality")
    print("=" * 50)

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create output manager with temp base path
        manager = EnhancedOutputManager(base_path=tmp_dir)

        # Test data
        assessments = [
            {
                'result': 'GO',
                'solicitation_id': 'TEST001',
                'solicitation_title': 'Test Equipment Purchase',
                'agency': 'Test Agency',
                'announcement_number': 'ANN-001'
            },
            {
                'result': 'NO-GO',
                'solicitation_id': 'TEST002',
                'solicitation_title': 'Military System',
                'agency': 'DOD',
                'announcement_number': 'ANN-002'
            }
        ]

        # Save the batch
        print("Saving assessment batch...")
        output_dir = manager.save_assessment_batch(
            'TESTRUN',
            assessments,
            metadata={'search_id': 'TESTRUN', 'total_opportunities': 2}
        )
        print(f"Saved to: {output_dir}")

        # Check Master_Database exists
        master_dir = Path(tmp_dir) / 'Master_Database'
        print(f"\nChecking Master_Database at: {master_dir}")

        if not master_dir.exists():
            print("ERROR: Master_Database directory not created!")
            return False

        print("OK: Master_Database directory exists")

        # Check for all-time file
        all_time_file = master_dir / 'master_all_time.csv'
        if not all_time_file.exists():
            print("ERROR: master_all_time.csv not created!")
            return False

        print("OK: master_all_time.csv exists")

        # Check for daily file
        from datetime import datetime
        daily_file = master_dir / f"master_{datetime.now().strftime('%Y-%m-%d')}.csv"
        if not daily_file.exists():
            print(f"ERROR: Daily file not created: {daily_file.name}")
            return False

        print(f"OK: Daily file exists: {daily_file.name}")

        # Read and verify content
        print("\nVerifying content...")
        with open(all_time_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if len(rows) != 2:
            print(f"ERROR: Expected 2 rows, found {len(rows)}")
            return False

        print(f"OK: Found {len(rows)} assessments in master database")

        # Verify data
        for i, row in enumerate(rows):
            print(f"\nRow {i+1}:")
            print(f"  Result: {row.get('result', 'N/A')}")
            print(f"  ID: {row.get('announcement_number', 'N/A')}")
            print(f"  Title: {row.get('announcement_title', 'N/A')}")

            # Check required fields
            if not row.get('result'):
                print(f"  ERROR: Missing result field!")
                return False

        print("\n" + "=" * 50)
        print("SUCCESS: Master_Database updates working correctly!")
        return True

if __name__ == "__main__":
    success = verify_master_database()
    sys.exit(0 if success else 1)