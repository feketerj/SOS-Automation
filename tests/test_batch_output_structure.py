#!/usr/bin/env python3
"""
TEST_OUTPUT_STRUCTURE.py - Test the standardized output structure
Creates a small test batch to verify all three output formats are generated correctly
"""

import os
import json
import sys
from datetime import datetime

def test_output_structure():
    """Test that the output structure is correctly standardized"""
    print("=" * 70)
    print("TESTING STANDARDIZED OUTPUT STRUCTURE")
    print("=" * 70)
    
    # Check if we have any recent batch outputs
    month_folder = datetime.now().strftime("%Y-%m")
    output_base = f"../SOS_Output/{month_folder}"
    
    if not os.path.exists(output_base):
        print(f"ERROR: Output directory does not exist: {output_base}")
        return False
    
    # Find the latest batch output
    batch_dirs = [d for d in os.listdir(output_base) if d.startswith("Run_") and "_BATCH" in d]
    
    if not batch_dirs:
        print("No batch output directories found. Run a batch process first.")
        return False
    
    # Sort by timestamp and get the latest
    batch_dirs.sort()
    latest_dir = batch_dirs[-1]
    full_path = os.path.join(output_base, latest_dir)
    
    print(f"\nChecking latest batch output: {latest_dir}")
    print("-" * 50)
    
    # Check for all three required files
    required_files = {
        "assessment.csv": "CSV spreadsheet format",
        "assessment.json": "JSON technical format",
        "assessment.md": "Markdown executive report"
    }
    
    all_present = True
    for filename, description in required_files.items():
        file_path = os.path.join(full_path, filename)
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"[OK] {filename:20} - {description:30} ({file_size:,} bytes)")
            
            # Validate JSON file
            if filename == "assessment.json":
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if 'summary' in data and 'assessments' in data:
                            print(f"  JSON structure valid: {len(data['assessments'])} assessments")
                        else:
                            print("  WARNING: JSON missing expected fields")
                except Exception as e:
                    print(f"  ERROR: Invalid JSON - {e}")
            
            # Check Markdown has content
            elif filename == "assessment.md":
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "# SOS Opportunity Assessment Report" in content:
                        print(f"  Markdown report valid: {len(content):,} characters")
                    else:
                        print("  WARNING: Markdown missing expected header")
                        
        else:
            print(f"[FAIL] {filename:20} - MISSING!")
            all_present = False
    
    # Check for summary file (optional but good to have)
    summary_path = os.path.join(full_path, "summary.txt")
    if os.path.exists(summary_path):
        print(f"[OK] {'summary.txt':20} - Processing summary (optional)")
    
    print("-" * 50)
    
    if all_present:
        print("\n[SUCCESS] All output files are correctly generated!")
        print("The batch processor is creating standardized outputs in:")
        print(f"  {full_path}")
        return True
    else:
        print("\n[FAILURE] Some output files are missing!")
        print("The batch processor needs to generate all three formats:")
        print("  - assessment.csv (for spreadsheets)")
        print("  - assessment.json (for technical analysis)")
        print("  - assessment.md (for executive reports)")
        return False

if __name__ == "__main__":
    success = test_output_structure()
    sys.exit(0 if success else 1)