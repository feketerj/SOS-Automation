#!/usr/bin/env python3
"""
Test script to verify FAA 8130 exception fix.
Tests that the exception only applies to specific commercial Navy platforms.
"""

from sos_ingestion_gate_v419 import IngestionGateV419

def test_faa_8130_exception():
    """Test various scenarios for FAA 8130 exception"""
    gate = IngestionGateV419()

    test_cases = [
        # Should trigger exception (commercial Navy platforms)
        {
            "name": "P-8 Poseidon with FAA 8130",
            "text": "Navy P-8 Poseidon maintenance. OEM only parts required. FAA 8130-3 certification required.",
            "expected": True
        },
        {
            "name": "E-6B Mercury with FAA 8130",
            "text": "NAVSUP E-6B Mercury TACAMO. Source approval required. FAA Form 8130 needed.",
            "expected": True
        },
        {
            "name": "C-40 Clipper with FAA 8130",
            "text": "Naval C-40A Clipper support. Original equipment manufacturer. Airworthiness certificate FAA 8130.",
            "expected": True
        },

        # Should NOT trigger exception (military platforms)
        {
            "name": "F/A-18 with FAA 8130",
            "text": "Navy F/A-18 Super Hornet. OEM only parts. FAA 8130-3 required.",
            "expected": False
        },
        {
            "name": "Generic Navy with FAA 8130",
            "text": "Navy aircraft parts. Source approval required. FAA 8130 certification.",
            "expected": False
        },
        {
            "name": "MH-60 with FAA 8130",
            "text": "NAVAIR MH-60 Seahawk maintenance. OEM parts only. FAA Form 8130 required.",
            "expected": False
        },

        # Missing required components
        {
            "name": "P-8 without SAR requirement",
            "text": "Navy P-8 Poseidon maintenance. FAA 8130 certification required.",
            "expected": False  # Missing OEM/SAR requirement
        },
        {
            "name": "P-8 without FAA 8130",
            "text": "Navy P-8 Poseidon maintenance. OEM only parts required.",
            "expected": False  # Missing FAA 8130
        },
        {
            "name": "Commercial platform without Navy",
            "text": "P-8 Poseidon maintenance. OEM only. FAA 8130 required.",
            "expected": False  # Missing Navy context
        }
    ]

    print("Testing FAA 8130 Exception Fix")
    print("=" * 50)

    passed = 0
    failed = 0

    for test in test_cases:
        result = gate._has_faa_8130_exception(test["text"])
        status = "PASS" if result == test["expected"] else "FAIL"

        if result == test["expected"]:
            passed += 1
        else:
            failed += 1

        print(f"{status}: {test['name']}")
        print(f"  Expected: {test['expected']}, Got: {result}")
        if result != test["expected"]:
            print(f"  Text: {test['text'][:100]}...")
        print()

    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("SUCCESS: All tests passed! FAA 8130 exception is now properly restricted.")
    else:
        print("FAILURE: Some tests failed. Review the implementation.")

    return failed == 0

if __name__ == "__main__":
    import sys
    success = test_faa_8130_exception()
    sys.exit(0 if success else 1)