#!/usr/bin/env python3
"""
Test script to verify that general 8130-3 capability language is properly detected as GO
and not caught in the SAR filter
"""

from sos_ingestion_gate_v419 import IngestionGateV419, Decision

def test_8130_capability_scenarios():
    """Test that any language about 8130-3 capability is treated as GO"""

    gate = IngestionGateV419()

    test_cases = [
        {
            'name': 'Anyone capable of producing 8130-3',
            'text': """
                Navy solicitation for aircraft parts repair.
                Anyone capable of producing an FAA 8130-3 certification
                is eligible to bid.
            """,
            'expected': Decision.GO,
            'reason': '8130-3 capability without Part 145 mention should be GO'
        },
        {
            'name': 'Any vendor who can provide 8130-3',
            'text': """
                Requirement for overhaul services.
                Any vendor who can provide 8130-3 documentation is eligible.
                Standard commercial practices apply.
            """,
            'expected': Decision.GO,
            'reason': 'General 8130-3 provision capability should be GO'
        },
        {
            'name': 'Must be able to issue FAA 8130-3',
            'text': """
                Boeing 737 component repair services.
                Contractor must be able to issue FAA 8130-3 airworthiness certificates.
                Commercial aircraft parts only.
            """,
            'expected': Decision.GO,
            'reason': 'Ability to issue 8130-3 should be GO'
        },
        {
            'name': 'Sources with 8130-3 capability',
            'text': """
                P-3 Orion maintenance services.
                All sources with 8130-3 capability may bid.
                No specific repair station requirements.
            """,
            'expected': Decision.GO,
            'reason': 'Sources with 8130-3 capability should be GO'
        },
        {
            'name': 'SAR with NO 8130-3 mention (should be NO-GO)',
            'text': """
                Navy parts requirement.
                Source approval request (SAR) required.
                Only approved sources may bid.
                OEM parts only.
            """,
            'expected': Decision.NO_GO,
            'reason': 'Traditional SAR without 8130-3 should still be NO-GO'
        },
        {
            'name': 'Approved sources but with 8130-3 capability',
            'text': """
                Navy aircraft parts.
                Approved source list applies.
                However, any source capable of producing 8130-3 may also bid.
            """,
            'expected': Decision.GO,
            'reason': '8130-3 capability should override approved source restriction'
        }
    ]

    print("Testing 8130-3 Capability Detection (SAR bypass)")
    print("=" * 60)

    passed = 0
    failed = 0

    for test in test_cases:
        print(f"\nTest: {test['name']}")
        print(f"Expected: {test['expected'].value}")

        result = gate.assess_opportunity({'text': test['text']})

        print(f"Actual: {result.decision.value}")
        print(f"Reasoning: {result.primary_blocker or 'None'}")

        if result.decision == test['expected']:
            print("[PASSED]")
            passed += 1
        else:
            print("[FAILED]")
            print(f"  Issue: {test['reason']}")
            failed += 1

        if result.co_contact_applicable:
            print(f"  Contact CO: {result.co_contact_reason}")

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")

    return failed == 0

if __name__ == "__main__":
    success = test_8130_capability_scenarios()
    exit(0 if success else 1)