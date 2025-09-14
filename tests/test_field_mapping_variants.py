#!/usr/bin/env python3
"""Validation tests for field mapping variants (warn-only style).

Covers TODO Priority 2.2 Step 2: Validation Tests
- Ensures varied field names normalize to unified 'result'
- Verifies EnhancedOutputManager respects unified fields
"""

from decision_sanitizer import DecisionSanitizer
from enhanced_output_manager import EnhancedOutputManager


def test_result_field_variants_normalize():
    variants = [
        ({'result': 'GO'}, 'GO'),
        ({'decision': 'NO_GO'}, 'NO-GO'),
        ({'final_decision': 'indeterminate'}, 'INDETERMINATE'),
        ({'assessment': {'decision': 'go'}}, 'GO'),
    ]

    for payload, expected in variants:
        out = DecisionSanitizer.sanitize(dict(payload))
        assert out.get('result') == expected, f"Expected {expected} for {payload}, got {out.get('result')}"


def test_output_manager_uses_unified_result():
    manager = EnhancedOutputManager()
    assessments = [
        {'decision': 'GO', 'solicitation_title': 'A', 'solicitation_id': '1'},
        {'final_decision': 'NO-GO', 'solicitation_title': 'B', 'solicitation_id': '2'},
        {'assessment': {'decision': 'INDETERMINATE'}, 'solicitation_title': 'C', 'solicitation_id': '3'},
        {'result': 'GO', 'solicitation_title': 'D', 'solicitation_id': '4'},
    ]

    enriched = manager._process_assessments(assessments)
    results = [e.get('result') for e in enriched]
    assert results == ['GO', 'NO-GO', 'INDETERMINATE', 'GO']

