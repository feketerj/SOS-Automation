#!/usr/bin/env python3
"""Simple assessment runner that actually works"""

import json
import os
from datetime import datetime
from pathlib import Path
from highergov_batch_fetcher import HigherGovBatchFetcher
from sos_ingestion_gate_v419 import IngestionGateV419, Decision
from enhanced_output_manager import EnhancedOutputManager

# Read endpoint from endpoints.txt
endpoints_file = Path("endpoints.txt")
if not endpoints_file.exists():
    print("No endpoints.txt file found")
    exit(1)

search_id = endpoints_file.read_text().strip()
if not search_id:
    print("endpoints.txt is empty")
    exit(1)

print(f"Processing search ID: {search_id}")

# Initialize components
fetcher = HigherGovBatchFetcher()
gate = IngestionGateV419()
output_manager = EnhancedOutputManager()

# Fetch opportunities
print("Fetching opportunities from HigherGov...")
opportunities = fetcher.fetch_all_opportunities(search_id, max_pages=1)
print(f"Found {len(opportunities)} opportunities")

# Process each opportunity
results = []
for i, opp in enumerate(opportunities):
    print(f"Processing {i+1}/{len(opportunities)}...")

    # Get basic info
    title = opp.get('announcement_title', opp.get('title', 'Unknown'))
    agency = opp.get('agency', {})
    if isinstance(agency, dict):
        agency_name = agency.get('agency_name', 'Unknown')
    else:
        agency_name = str(agency)

    # Get document text
    doc_path = opp.get('document_path') or opp.get('source_id_version')
    doc_text = ""
    if doc_path:
        doc_text = fetcher.fetch_document_text(doc_path)

    # Create opportunity dict for assessment
    opp_dict = {
        'title': title,
        'text': doc_text,
        'id': opp.get('opportunity_id', search_id)
    }

    # Run through regex
    assessment = gate.assess_opportunity(opp_dict)

    # Map decision to GO/NO-GO/INDETERMINATE
    if assessment.decision == Decision.NO_GO:
        result_value = 'NO-GO'
    elif assessment.decision == Decision.GO:
        result_value = 'GO'
    else:
        result_value = 'INDETERMINATE'

    # Build result
    result = {
        'solicitation_id': opp.get('opportunity_id', search_id),
        'solicitation_title': title,
        'agency': agency_name,
        'result': result_value,
        'pipeline_stage': 'REGEX',
        'assessment_type': 'REGEX_ASSESSMENT',
        'knock_out_reasons': [],
        'rationale': getattr(assessment, 'analysis_notes', ''),
        'sam_url': opp.get('sam_url', ''),
        'hg_url': f"https://www.highergov.com/opportunity/{opp.get('opportunity_id', '')}",
        'doc_length': len(doc_text)
    }

    if result_value == 'NO-GO':
        result['knock_out_reasons'] = [assessment.primary_blocker] if assessment.primary_blocker else []
        result['rationale'] = f"Knocked out by regex: {assessment.knockout_category}"
    elif result_value == 'GO':
        # Would normally send to Mistral here
        result['rationale'] = "Passed all regex filters - ready for Mistral assessment"
        result['pipeline_stage'] = 'BATCH'
        result['assessment_type'] = 'MISTRAL_BATCH_ASSESSMENT'
    else:
        result['rationale'] = "Needs further analysis"

    results.append(result)

# Create output directory
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
run_id = "REAL_RUN"
output_dir = Path(f"SOS_Output/2025-09/Run_{timestamp}_{run_id}")
output_dir.mkdir(parents=True, exist_ok=True)

# Save data.json
data = {
    'metadata': {
        'generated': datetime.now().isoformat(),
        'total': len(results),
        'total_opportunities': len(results),
        'regex_knockouts': sum(1 for r in results if r['result'] == 'NO-GO'),
        'ai_assessments': sum(1 for r in results if r['result'] == 'GO'),
        'processing_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    'summary': {
        'go': sum(1 for r in results if r['result'] == 'GO'),
        'no_go': sum(1 for r in results if r['result'] == 'NO-GO'),
        'indeterminate': sum(1 for r in results if r['result'] == 'INDETERMINATE')
    },
    'assessments': results
}

with open(output_dir / 'data.json', 'w') as f:
    json.dump(data, f, indent=2)

# Save CSV
import csv
csv_file = output_dir / 'assessment.csv'
if results:
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

print(f"\nResults saved to: {output_dir}")
print(f"  GO: {data['summary']['go']}")
print(f"  NO-GO: {data['summary']['no_go']}")
print(f"  INDETERMINATE: {data['summary']['indeterminate']}")