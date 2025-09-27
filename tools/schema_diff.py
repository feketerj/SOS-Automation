#!/usr/bin/env python3
"""
Schema diff summary tool - compare two data.json files and list field differences (read-only).

Usage:
  python tools/schema_diff.py file1.json file2.json
  python tools/schema_diff.py SOS_Output/2025-09/Run_1/data.json SOS_Output/2025-09/Run_2/data.json

Outputs a summary of:
  - Missing fields in each file
  - Type differences for common fields
  - First assessment with invalid/missing required fields
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Set, Any

REQUIRED_FIELDS = {
    'solicitation_id', 'result', 'announcement_number',
    'announcement_title', 'agency'
}

URL_FIELDS = {'sam_url', 'hg_url', 'highergov_url'}

def load_json_file(path: Path) -> Dict:
    """Load JSON file safely"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return {}

def get_field_types(data: Dict) -> Dict[str, str]:
    """Extract field types from first assessment"""
    assessments = data.get('assessments', [])
    if not assessments:
        return {}

    first_assessment = assessments[0]
    field_types = {}

    for key, value in first_assessment.items():
        if value is None:
            field_types[key] = 'null'
        elif isinstance(value, bool):
            field_types[key] = 'boolean'
        elif isinstance(value, int):
            field_types[key] = 'integer'
        elif isinstance(value, float):
            field_types[key] = 'float'
        elif isinstance(value, str):
            field_types[key] = 'string'
        elif isinstance(value, list):
            field_types[key] = 'array'
        elif isinstance(value, dict):
            field_types[key] = 'object'
        else:
            field_types[key] = 'unknown'

    return field_types

def find_invalid_assessments(data: Dict) -> List[Dict]:
    """Find assessments missing required fields"""
    invalid = []
    assessments = data.get('assessments', [])

    for i, assessment in enumerate(assessments):
        missing = []
        for field in REQUIRED_FIELDS:
            if field not in assessment or assessment[field] is None or assessment[field] == '':
                missing.append(field)

        # Check for at least one URL
        has_url = any(assessment.get(field) for field in URL_FIELDS)
        if not has_url:
            missing.append('(no URL fields)')

        if missing:
            invalid.append({
                'index': i,
                'id': assessment.get('solicitation_id', 'UNKNOWN'),
                'missing_fields': missing
            })

    return invalid[:5]  # Return first 5 invalid

def compare_schemas(file1: Path, file2: Path) -> None:
    """Compare two JSON schema files and print differences"""
    print("=" * 60)
    print("SCHEMA DIFF SUMMARY")
    print("=" * 60)
    print(f"File 1: {file1}")
    print(f"File 2: {file2}")
    print("-" * 60)

    # Load both files
    data1 = load_json_file(file1)
    data2 = load_json_file(file2)

    if not data1 or not data2:
        print("Failed to load one or both files")
        return

    # Get assessment counts
    count1 = len(data1.get('assessments', []))
    count2 = len(data2.get('assessments', []))
    print(f"\nAssessment counts:")
    print(f"  File 1: {count1}")
    print(f"  File 2: {count2}")

    # Get field sets and types
    types1 = get_field_types(data1)
    types2 = get_field_types(data2)

    fields1 = set(types1.keys())
    fields2 = set(types2.keys())

    # Find differences
    only_in_1 = fields1 - fields2
    only_in_2 = fields2 - fields1
    common = fields1 & fields2

    if only_in_1:
        print(f"\nFields only in File 1 ({len(only_in_1)}):")
        for field in sorted(only_in_1)[:10]:  # Show first 10
            print(f"  - {field} ({types1[field]})")

    if only_in_2:
        print(f"\nFields only in File 2 ({len(only_in_2)}):")
        for field in sorted(only_in_2)[:10]:  # Show first 10
            print(f"  - {field} ({types2[field]})")

    # Check type differences
    type_diffs = []
    for field in common:
        if types1[field] != types2[field]:
            type_diffs.append((field, types1[field], types2[field]))

    if type_diffs:
        print(f"\nType differences ({len(type_diffs)}):")
        for field, type1, type2 in type_diffs[:10]:  # Show first 10
            print(f"  - {field}: {type1} -> {type2}")

    # Check for invalid assessments
    invalid1 = find_invalid_assessments(data1)
    invalid2 = find_invalid_assessments(data2)

    if invalid1:
        print(f"\nInvalid assessments in File 1 (first {len(invalid1)}):")
        for inv in invalid1:
            print(f"  - Index {inv['index']}: {inv['id']} missing: {', '.join(inv['missing_fields'])}")

    if invalid2:
        print(f"\nInvalid assessments in File 2 (first {len(invalid2)}):")
        for inv in invalid2:
            print(f"  - Index {inv['index']}: {inv['id']} missing: {', '.join(inv['missing_fields'])}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("-" * 60)
    print(f"Total fields in File 1: {len(fields1)}")
    print(f"Total fields in File 2: {len(fields2)}")
    print(f"Common fields: {len(common)}")
    print(f"Unique to File 1: {len(only_in_1)}")
    print(f"Unique to File 2: {len(only_in_2)}")
    print(f"Type differences: {len(type_diffs)}")
    print(f"Invalid in File 1: {len(invalid1)}")
    print(f"Invalid in File 2: {len(invalid2)}")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(
        description='Compare schema differences between two data.json files (read-only)'
    )
    parser.add_argument('file1', help='Path to first data.json file')
    parser.add_argument('file2', help='Path to second data.json file')

    args = parser.parse_args()

    file1 = Path(args.file1)
    file2 = Path(args.file2)

    if not file1.exists():
        print(f"Error: File not found: {file1}")
        return 1

    if not file2.exists():
        print(f"Error: File not found: {file2}")
        return 1

    compare_schemas(file1, file2)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())