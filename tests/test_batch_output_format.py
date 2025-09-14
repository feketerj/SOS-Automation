#!/usr/bin/env python3
"""
Test script to verify batch processor output standardization
"""

import json
import os
from pathlib import Path

def check_batch_output_format():
    """Check if batch processor outputs are properly standardized"""
    
    # Find recent batch output folders
    sos_output = Path("SOS_Output/2025-09")
    batch_folders = sorted([f for f in sos_output.glob("Run_*_BATCH") if f.is_dir()])
    
    if not batch_folders:
        print("No batch output folders found")
        return
    
    # Check the most recent batch folder
    latest_batch = batch_folders[-1]
    print(f"Checking: {latest_batch}")
    print("=" * 70)
    
    # Check JSON format
    json_file = latest_batch / "assessment.json"
    if json_file.exists():
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        print(f"Total assessments: {len(data)}")
        
        # Check first few records for required fields
        required_fields = [
            'type',
            'solicitation_id', 
            'solicitation_title',
            'result',
            'summary',
            'rationale',
            'recommendation',
            'knock_out_reasons',
            'exceptions'
        ]
        
        # Count types
        type_counts = {}
        missing_fields = set()
        
        for i, record in enumerate(data[:5]):  # Check first 5
            print(f"\nRecord {i+1}:")
            print(f"  Title: {record.get('solicitation_title', 'MISSING')[:50]}")
            print(f"  Type: {record.get('type', 'MISSING')}")
            print(f"  Result: {record.get('result', 'MISSING')}")
            
            # Track types
            rec_type = record.get('type', 'MISSING')
            type_counts[rec_type] = type_counts.get(rec_type, 0) + 1
            
            # Check for missing fields
            for field in required_fields:
                if field not in record:
                    missing_fields.add(field)
                    print(f"  WARNING: Missing field '{field}'")
        
        # Overall statistics
        print("\n" + "=" * 70)
        print("STATISTICS:")
        print("-" * 40)
        
        # Count all types
        for record in data:
            rec_type = record.get('type', 'MISSING')
            type_counts[rec_type] = type_counts.get(rec_type, 0) + 1
        
        print("\nAssessment Types:")
        for type_name, count in sorted(type_counts.items()):
            print(f"  {type_name}: {count}")
        
        # Decision breakdown
        decision_counts = {}
        for record in data:
            decision = record.get('result', record.get('final_decision', 'UNKNOWN'))
            decision_counts[decision] = decision_counts.get(decision, 0) + 1
        
        print("\nDecisions:")
        for decision, count in sorted(decision_counts.items()):
            print(f"  {decision}: {count}")
        
        if missing_fields:
            print(f"\nWARNING: Some records missing fields: {missing_fields}")
        else:
            print("\nSUCCESS: All required fields present in sample")
        
        # Check for proper type labeling
        print("\n" + "=" * 70)
        print("TYPE VALIDATION:")
        print("-" * 40)
        
        has_regex = 'REGEX_KNOCKOUT' in type_counts
        has_batch = 'MISTRAL_BATCH_ASSESSMENT' in type_counts
        has_mistral = 'MISTRAL_ASSESSMENT' in type_counts
        
        if has_regex:
            print("PASS: REGEX_KNOCKOUT type found")
        else:
            print("FAIL: REGEX_KNOCKOUT type missing")
            
        if has_batch or has_mistral:
            print(f"PASS: Mistral assessment types found: {[t for t in type_counts if 'MISTRAL' in t]}")
        else:
            print(f"WARNING: No Mistral assessment types found, checking for AI_ASSESSMENT")
            if 'AI_ASSESSMENT' in type_counts:
                print(f"  Found AI_ASSESSMENT type (legacy format) - count: {type_counts['AI_ASSESSMENT']}")
        
        # Validate a sample Mistral assessment
        mistral_samples = [r for r in data if 'MISTRAL' in r.get('type', '')]
        if mistral_samples:
            sample = mistral_samples[0]
            print(f"\nSample Mistral Assessment:")
            print(f"  Type: {sample.get('type')}")
            print(f"  Result: {sample.get('result')}")
            print(f"  Summary: {sample.get('summary', '')[:100]}")
            print(f"  Rationale: {sample.get('rationale', '')[:100]}")
    else:
        print(f"ERROR: {json_file} not found")
    
    # Check CSV format
    csv_file = latest_batch / "assessment.csv"
    if csv_file.exists():
        print(f"\nPASS: CSV file exists: {csv_file}")
    else:
        print(f"\nFAIL: CSV file missing: {csv_file}")
    
    # Check MD format
    md_file = latest_batch / "assessment.md"
    if md_file.exists():
        print(f"PASS: Markdown file exists: {md_file}")
    else:
        print(f"FAIL: Markdown file missing: {md_file}")

if __name__ == "__main__":
    check_batch_output_format()