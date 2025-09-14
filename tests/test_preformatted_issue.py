#!/usr/bin/env python3
"""Test the pre_formatted=True issue with output manager"""

from enhanced_output_manager import EnhancedOutputManager
from decision_sanitizer import DecisionSanitizer
import tempfile
import json
import os

def test_preformatted_issue():
    """Test what happens with pre_formatted=True"""

    print("Testing Pre-Formatted Data Issue")
    print("=" * 60)

    # Simulate what FULL_BATCH_PROCESSOR does
    batch_results = [
        {
            'decision': 'GO',
            'title': 'Boeing 737 Parts',
            'search_id': 'TEST001',
            'reasoning': 'Commercial aircraft',
            'processing_method': 'BATCH_AI'
        },
        {
            'decision': 'NO-GO',
            'title': 'F-16 Components',
            'search_id': 'TEST002',
            'reasoning': 'Military platform',
            'processing_method': 'BATCH_AI'
        },
        {
            'decision': 'INDETERMINATE',
            'title': 'Unclear Requirements',
            'search_id': 'TEST003',
            'reasoning': 'Need more information',
            'processing_method': 'BATCH_AI'
        }
    ]

    print("\n1. Simulating FULL_BATCH_PROCESSOR flow:")
    print("-" * 40)

    # Format like FULL_BATCH_PROCESSOR does
    formatted_results = []
    for result in batch_results:
        formatted_results.append({
            'search_id': result.get('search_id', ''),
            'opportunity_id': result.get('opportunity_id', ''),
            'title': result.get('title', ''),
            'final_decision': result.get('decision', 'INDETERMINATE'),
            'knock_pattern': '',
            'knockout_category': '',
            'sos_pipeline_title': f"PN: NA | Qty: NA | Condition: NA | MDS: NA | {result.get('title', '')[:50]}",
            'highergov_url': f"https://www.highergov.com/opportunity/{result.get('search_id', '')}",
            'announcement_number': result.get('search_id', ''),
            'announcement_title': result.get('title', ''),
            'agency': 'Unknown',
            'due_date': '',
            'posted_date': '',
            'naics': '',
            'psc': '',
            'set_aside': '',
            'value_low': 0,
            'value_high': 0,
            'place_of_performance': '',
            'brief_description': result.get('reasoning', '')[:100],
            'analysis_notes': result.get('reasoning', ''),
            'recommendation': result.get('decision', 'INDETERMINATE'),
            'special_action': '',
            'doc_length': 0,
            'assessment_timestamp': '2025-09-13T12:00:00',
            'solicitation_id': result.get('search_id', 'unknown'),
            'solicitation_title': result.get('title', ''),
            'type': 'BATCH_AI',
            'result': result.get('decision', 'INDETERMINATE'),
            'summary': result.get('reasoning', '')[:200],
            'rationale': result.get('reasoning', ''),
            'knock_out_reasons': [result.get('reasoning', '')[:100]],
            'exceptions': [],
            'processing_method': 'BATCH_AI'
        })

    # Sanitize like FULL_BATCH_PROCESSOR does
    print("Before sanitization:")
    print(f"  First item 'result': {formatted_results[0].get('result')}")
    print(f"  First item 'final_decision': {formatted_results[0].get('final_decision')}")

    formatted_results = DecisionSanitizer.sanitize_batch(formatted_results)

    print("\nAfter sanitization:")
    print(f"  First item 'result': {formatted_results[0].get('result')}")
    print(f"  First item 'final_decision': {formatted_results[0].get('final_decision')}")

    # Now test with output manager
    print("\n2. Testing with output manager:")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        manager = EnhancedOutputManager(base_path=tmpdir)

        # Test with pre_formatted=True (like pipeline does)
        print("\nWith pre_formatted=True:")
        output_dir = manager.save_assessment_batch(
            search_id='TEST_PREFORMATTED',
            assessments=formatted_results,
            metadata={'test': True},
            pre_formatted=True
        )

        # Check JSON output
        json_file = os.path.join(output_dir, 'data.json')
        with open(json_file, 'r') as f:
            json_data = json.load(f)

        summary = json_data.get('summary', {})
        print(f"  Summary: GO={summary.get('go')}, NO-GO={summary.get('no_go')}, INDETERMINATE={summary.get('indeterminate')}")

        # Check actual assessment data
        assessments = json_data.get('assessments', [])
        if assessments:
            print(f"  First assessment 'result': {assessments[0].get('result')}")
            print(f"  First assessment 'final_decision': {assessments[0].get('final_decision')}")

        # Test with pre_formatted=False (normal flow)
        print("\nWith pre_formatted=False:")
        output_dir2 = manager.save_assessment_batch(
            search_id='TEST_NORMAL',
            assessments=formatted_results,
            metadata={'test': True},
            pre_formatted=False
        )

        json_file2 = os.path.join(output_dir2, 'data.json')
        with open(json_file2, 'r') as f:
            json_data2 = json.load(f)

        summary2 = json_data2.get('summary', {})
        print(f"  Summary: GO={summary2.get('go')}, NO-GO={summary2.get('no_go')}, INDETERMINATE={summary2.get('indeterminate')}")

    print("\n3. Diagnosis:")
    print("-" * 40)

    if summary.get('go') == 0 and summary.get('no_go') == 0:
        print("[PROBLEM FOUND] With pre_formatted=True, decisions not being counted!")
        print("The issue is that the summary counts use 'final_decision' field")
        print("But when pre_formatted=True, _process_assessments is skipped")
        return False
    else:
        print("[OK] Decisions are being counted correctly")
        return True

if __name__ == "__main__":
    import sys
    success = test_preformatted_issue()
    sys.exit(0 if success else 1)