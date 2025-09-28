#!/usr/bin/env python3
"""
Test script to verify Part 145 repair station logic works correctly
"""

from sos_ingestion_gate_v419 import IngestionGateV419, Decision

def test_part_145_scenarios():
    """Test that Part 145 language is treated as GO, not as approved source restriction"""

    gate = IngestionGateV419()

    test_cases = [
        {
            'name': 'Part 145 capable of 8130-3',
            'text': """
                Navy solicitation for aircraft parts repair.
                Any FAA Part 145 repair station capable of producing 8130-3 certification
                is eligible to bid. Must provide FAA 8130-3 tags with all repairs.
            """,
            'expected': Decision.GO,
            'reason': 'Part 145 with 8130-3 capability should be GO'
        },
        {
            'name': 'Any FAA certified repair station',
            'text': """
                Requirement for overhaul services.
                Any FAA certified repair station that can issue 8130-3 documentation.
                No specific approved source list required.
            """,
            'expected': Decision.GO,
            'reason': 'Any FAA repair station language should be GO'
        },
        {
            'name': 'Part 145 MRO',
            'text': """
                Boeing 737 component repair services.
                Must be FAA Part 145 MRO capable of providing airworthiness certificates.
                Commercial aircraft parts only.
            """,
            'expected': Decision.GO,
            'reason': 'Part 145 MRO requirement should be GO'
        },
        {
            'name': 'Traditional approved source (should be NO-GO)',
            'text': """
                F-16 engine parts required.
                Only approved sources on QPL may bid.
                OEM only, no alternatives accepted.
            """,
            'expected': Decision.NO_GO,
            'reason': 'QPL/OEM only should still be NO-GO'
        },
        {
            'name': 'Approved sources WITH FAA 8130 (Contact CO)',
            'text': """
                Navy P-8 Poseidon parts.
                Approved source list applies.
                FAA 8130-3 certification required for all parts.
                Commercial equivalents may be considered.
            """,
            'expected': Decision.FURTHER_ANALYSIS,
            'reason': 'Approved sources + FAA 8130 should trigger Contact CO'
        }
    ]

    print("Testing Part 145 Repair Station Logic")
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
    success = test_part_145_scenarios()
    exit(0 if success else 1)