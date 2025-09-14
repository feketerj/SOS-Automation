#!/usr/bin/env python3
"""Additional normalization tests for DecisionSanitizer (no network)."""

from decision_sanitizer import DecisionSanitizer


def test_decision_normalization_variants():
    variants = [
        ({'decision': 'GO'}, 'GO'),
        ({'decision': 'go'}, 'GO'),
        ({'decision': 'NO_GO'}, 'NO-GO'),
        ({'decision': 'No Go'}, 'NO-GO'),
        ({'decision': 'CONTACT CO'}, 'INDETERMINATE'),
        ({'decision': 'FURTHER_ANALYSIS'}, 'INDETERMINATE'),
        ({'final_decision': 'no-go'}, 'NO-GO'),
        ({'assessment': {'decision': 'go'}}, 'GO'),
        ({'decision': None}, 'INDETERMINATE'),
        ({}, 'INDETERMINATE'),
    ]

    for payload, expected in variants:
        out = DecisionSanitizer.sanitize(dict(payload))
        assert out.get('result') == expected, (payload, out.get('result'))

