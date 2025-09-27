#!/usr/bin/env python3
"""Test failure scenarios in pipeline runner"""

import sys
import os
from pathlib import Path
import tempfile

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ui_service'))
from run_pipeline_import import run_pipeline_direct

def test_malformed_endpoints():
    """Test with various malformed inputs"""
    print("Testing malformed endpoints...")

    test_cases = [
        ([""], "empty string"),
        (["   "], "whitespace only"),
        ([None], "None value"),
        (["valid", None, "valid2"], "mixed with None"),
        (["a" * 1000], "very long string"),
        (["\n\r\t"], "special characters"),
        (["<script>alert('xss')</script>"], "potential XSS"),
        (["'; DROP TABLE;"], "SQL injection attempt"),
    ]

    for endpoints, description in test_cases:
        try:
            code, output = run_pipeline_direct(endpoints)
            print(f"  [{description}] Code: {code}")
        except Exception as e:
            print(f"  [{description}] Exception: {str(e)[:50]}")

def test_filesystem_issues():
    """Test filesystem permission and space issues"""
    print("\nTesting filesystem issues...")

    # Test read-only directory
    original_file = Path(__file__).parent.parent / "endpoints.txt"

    # Try to write to a path that might not exist
    try:
        # Temporarily change permissions if on Windows
        if os.name == 'nt':
            import stat
            original_mode = original_file.stat().st_mode if original_file.exists() else None
            if original_file.exists():
                os.chmod(original_file, stat.S_IREAD)

        code, output = run_pipeline_direct(["TEST"])
        print(f"  [Read-only test] Code: {code}")

    except Exception as e:
        print(f"  [Read-only test] Exception: {str(e)[:100]}")
    finally:
        # Restore permissions
        if os.name == 'nt' and original_file.exists() and 'original_mode' in locals():
            os.chmod(original_file, original_mode)

def test_import_failures():
    """Test what happens if imports fail"""
    print("\nTesting import failures...")

    # Temporarily mess with sys.path
    original_path = sys.path.copy()

    try:
        # Remove all paths except standard library
        sys.path = [p for p in sys.path if 'site-packages' not in p][:2]

        from run_pipeline_import import run_pipeline_direct
        code, output = run_pipeline_direct(["IMPORT_TEST"])
        print(f"  [Limited path] Code: {code}")

    except Exception as e:
        print(f"  [Import failure] Exception: {str(e)[:100]}")
    finally:
        sys.path = original_path

def test_concurrent_execution():
    """Test concurrent execution issues"""
    print("\nTesting concurrent execution...")

    import threading
    results = []

    def run_pipeline(id):
        try:
            code, output = run_pipeline_direct([f"CONCURRENT_{id}"])
            results.append((id, code, "success"))
        except Exception as e:
            results.append((id, -1, str(e)[:50]))

    threads = []
    for i in range(3):
        t = threading.Thread(target=run_pipeline, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    for id, code, status in results:
        print(f"  [Thread {id}] Code: {code}, Status: {status}")

def test_memory_stress():
    """Test with large data that might cause memory issues"""
    print("\nTesting memory stress...")

    # Create a large number of endpoints
    large_endpoints = [f"ENDPOINT_{i}" for i in range(1000)]

    try:
        code, output = run_pipeline_direct(large_endpoints)
        print(f"  [1000 endpoints] Code: {code}")
    except Exception as e:
        print(f"  [Memory stress] Exception: {str(e)[:100]}")

if __name__ == "__main__":
    print("="*60)
    print("FAILURE SCENARIO TESTING")
    print("="*60)

    test_malformed_endpoints()
    test_filesystem_issues()
    test_import_failures()
    test_concurrent_execution()
    test_memory_stress()

    print("="*60)
    print("Failure testing complete")