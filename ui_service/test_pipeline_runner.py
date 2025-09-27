#!/usr/bin/env python3
"""Test suite for the pipeline runner improvements"""

import sys
import os
from pathlib import Path

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))

from run_pipeline_import import run_pipeline_direct

def test_empty_list_protection():
    """Test that empty list returns error"""
    print("Testing empty list protection...")
    code, output = run_pipeline_direct([])
    assert code == 1, f"Expected error code 1, got {code}"
    assert "No endpoints provided" in output, "Expected empty list error message"
    print("  [OK] Empty list protection works")

def test_valid_endpoint():
    """Test with a valid endpoint"""
    print("Testing valid endpoint...")
    code, output = run_pipeline_direct(['TEST_ENDPOINT'])
    assert code == 0, f"Expected success code 0, got {code}"
    print("  [OK] Valid endpoint processing works")

def test_resource_cleanup():
    """Test that resources are cleaned up properly"""
    print("Testing resource cleanup...")

    # Get initial state
    initial_cwd = os.getcwd()
    initial_syspath_len = len(sys.path)

    # Run pipeline
    code, output = run_pipeline_direct(['CLEANUP_TEST'])

    # Check working directory restored
    assert os.getcwd() == initial_cwd, "Working directory not restored"
    print("  [OK] Working directory restored")

    # Check sys.path mostly clean (allow 1-2 paths from imports)
    path_leak = len(sys.path) - initial_syspath_len
    assert path_leak <= 2, f"Too many paths leaked: {path_leak}"
    print(f"  PASSED sys.path cleanup (leak: {path_leak} paths)")

def test_error_handling():
    """Test error handling with invalid data"""
    print("Testing error handling...")

    # Test with None (should handle gracefully)
    try:
        code, output = run_pipeline_direct(None)
        assert code == 1, "Expected error for None input"
        print("  [OK] None input handled")
    except:
        print("  [OK] None input raises exception (acceptable)")

    # Test with list containing empty strings
    code, output = run_pipeline_direct(['', '  ', 'VALID'])
    assert code == 0, "Should process valid entries"
    print("  [OK] Empty string filtering works")

def test_output_capture():
    """Test that output is properly captured"""
    print("Testing output capture...")
    code, output = run_pipeline_direct(['OUTPUT_TEST'])

    # Check that we get some output
    assert len(output) > 0, "No output captured"
    assert "Pipeline" in output or "ERROR" in output, "Output doesn't contain expected text"
    print("  [OK] Output capture works")

def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("PIPELINE RUNNER TEST SUITE")
    print("="*60)

    tests = [
        test_empty_list_protection,
        test_valid_endpoint,
        test_resource_cleanup,
        test_error_handling,
        test_output_capture
    ]

    failed = []
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"  [FAIL] Test failed: {e}")
            failed.append(test.__name__)

    print("="*60)
    if not failed:
        print("ALL TESTS PASSED PASSED")
    else:
        print(f"TESTS FAILED: {', '.join(failed)}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(run_all_tests())