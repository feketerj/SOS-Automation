#!/usr/bin/env python3
"""
BATCH_RUN.py - Process multiple search IDs from a file
NO modifications to core files - just a wrapper
"""

import os
import sys
import subprocess
from datetime import datetime
import time

def _load_config_env():
    """Optionally load centralized config and set env vars if missing.
    Preserves existing behavior by only filling unset values.
    """
    try:
        from config.loader import get_config  # type: ignore
        cfg = get_config()
        os.environ.setdefault('HIGHERGOV_API_KEY', str(cfg.get('highergov.api_key', '') or os.environ.get('HIGHERGOV_API_KEY', '')))
        os.environ.setdefault('HG_API_BASE_URL', str(cfg.get('highergov.base_url', '') or os.environ.get('HG_API_BASE_URL', '')))
        os.environ.setdefault('MISTRAL_API_KEY', str(cfg.get('mistral.api_key', '') or os.environ.get('MISTRAL_API_KEY', '')))
        os.environ.setdefault('MISTRAL_API_BASE_URL', str(cfg.get('mistral.base_url', '') or os.environ.get('MISTRAL_API_BASE_URL', '')))
    except Exception:
        pass

def load_endpoints(filename="endpoints.txt"):
    """Load search IDs from file, skip comments and blank lines"""
    if not os.path.exists(filename):
        print(f"[WARNING] {filename} not found, creating example file")
        create_example_file(filename)
        return []
    
    endpoints = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and blank lines
            if line and not line.startswith('#'):
                endpoints.append(line)
    
    return endpoints

def create_example_file(filename):
    """Create example endpoints file"""
    example = """# SOS Assessment Batch Processing
# Add one HigherGov search ID per line
# Lines starting with # are ignored

# Example IDs (replace with your actual IDs):
f5KQeEYWpQ4FtgSOPd6Sm
HAfVxckSk6G9kSXQuJoQB
gvCo0-K8fEbyI367g_HYp

# Add more search IDs below:
"""
    with open(filename, 'w') as f:
        f.write(example)
    print(f"Created {filename} - add your search IDs and run again")

def run_assessment(search_id):
    """Run assessment for a single search ID"""
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Processing: {search_id}")
    print("-" * 40)
    
    try:
        result = subprocess.run(
            [sys.executable, "LOCKED_PRODUCTION_RUNNER.py", search_id],
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout per assessment
        )
        
        if result.returncode == 0:
            # Look for output location in stdout
            output_loc = None
            for line in result.stdout.split('\n'):
                if 'SOS_Output' in line and 'Run_' in line:
                    output_loc = line.strip()
                    break
            
            return {
                'status': 'SUCCESS',
                'output': output_loc or 'Check SOS_Output folder',
                'error': None
            }
        else:
            return {
                'status': 'FAILED',
                'output': None,
                'error': result.stderr[:200] if result.stderr else 'Unknown error'
            }
            
    except subprocess.TimeoutExpired:
        return {
            'status': 'TIMEOUT',
            'output': None,
            'error': 'Assessment took longer than 10 minutes'
        }
    except Exception as e:
        return {
            'status': 'ERROR',
            'output': None,
            'error': str(e)
        }

def main():
    print("=" * 60)
    print("SOS ASSESSMENT TOOL - BATCH PROCESSOR")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check if LOCKED_PRODUCTION_RUNNER exists
    if not os.path.exists('LOCKED_PRODUCTION_RUNNER.py'):
        print("[ERROR] LOCKED_PRODUCTION_RUNNER.py not found!")
        print("Make sure you're in the right directory")
        sys.exit(1)
    
    # Load optional config to set env vars for subprocesses
    _load_config_env()
    # Load endpoints
    endpoints = load_endpoints()
    
    if not endpoints:
        print("\n[INFO] No endpoints found in endpoints.txt")
        print("Add search IDs to the file and run again")
        return
    
    print(f"\nFound {len(endpoints)} search IDs to process")
    print("-" * 60)
    for i, ep in enumerate(endpoints, 1):
        print(f"  {i}. {ep}")
    
    print("-" * 60)
    # Auto-proceed without asking
    print(f"\nProcessing all {len(endpoints)} assessments...")
    
    # Process each endpoint
    start_time = datetime.now()
    results = []
    
    print("\n" + "=" * 60)
    print("STARTING BATCH PROCESSING")
    print("=" * 60)
    
    for i, search_id in enumerate(endpoints, 1):
        print(f"\n[{i}/{len(endpoints)}] " + "=" * 40)
        result = run_assessment(search_id)
        results.append({
            'search_id': search_id,
            **result
        })
        
        # Show result
        if result['status'] == 'SUCCESS':
            print(f"[SUCCESS] Completed: {search_id}")
            if result['output']:
                print(f"  Output: {result['output']}")
        else:
            print(f"[{result['status']}] Failed: {search_id}")
            if result['error']:
                print(f"  Error: {result['error']}")
        
        # Delay between assessments to avoid overwhelming APIs and ensure stability
        if i < len(endpoints):
            print("Waiting 15 seconds before next assessment...")
            time.sleep(15)
    
    # Summary report
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 60)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Total time: {duration:.1f} seconds")
    print(f"Average per assessment: {duration/len(endpoints):.1f} seconds")
    print("\nResults Summary:")
    print("-" * 60)
    
    success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
    failed_count = len(results) - success_count
    
    print(f"  Successful: {success_count}")
    print(f"  Failed: {failed_count}")
    
    if failed_count > 0:
        print("\nFailed assessments:")
        for r in results:
            if r['status'] != 'SUCCESS':
                print(f"  - {r['search_id']}: {r['status']}")
    
    # Save summary to file
    summary_file = f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(summary_file, 'w') as f:
        f.write("SOS BATCH PROCESSING SUMMARY\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Duration: {duration:.1f} seconds\n")
        f.write(f"Successful: {success_count}/{len(results)}\n")
        f.write("\nDetailed Results:\n")
        f.write("-" * 60 + "\n")
        
        for r in results:
            f.write(f"\nSearch ID: {r['search_id']}\n")
            f.write(f"Status: {r['status']}\n")
            if r['output']:
                f.write(f"Output: {r['output']}\n")
            if r['error']:
                f.write(f"Error: {r['error']}\n")
    
    print(f"\nSummary saved to: {summary_file}")
    print("\nAll outputs in: SOS_Output/2025-09/")
    print("=" * 60)

if __name__ == "__main__":
    main()
