#!/usr/bin/env python3
"""Download and process Mistral batch results"""

import sys
import os
import json
from datetime import datetime
from mistralai import Mistral

# Add parent directory to path
sys.path.append('..')
from API_KEYS import MISTRAL_API_KEY

def download_batch_results(job_id):
    """Download and process batch results"""
    client = Mistral(api_key=MISTRAL_API_KEY)
    
    print("=" * 70)
    print(f"DOWNLOADING BATCH RESULTS: {job_id}")
    print("=" * 70)
    
    try:
        # Get job info
        job = client.batch.jobs.get(job_id=job_id)
        
        if job.status != "SUCCESS":
            print(f"Job not complete! Status: {job.status}")
            return
        
        # Download results
        print(f"Downloading from: {job.output_file}")
        output = client.files.download(file_id=job.output_file)
        content = output.read()
        
        # Save raw results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        raw_file = f"batch_results_{timestamp}.jsonl"
        with open(raw_file, 'wb') as f:
            f.write(content)
        print(f"Raw results saved to: {raw_file}")
        
        # Parse results
        results = []
        with open(raw_file, 'r') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    custom_id = data.get('custom_id', '')
                    
                    # Parse response
                    response = data.get('response', {})
                    if response.get('status_code') == 200:
                        body = response.get('body', {})
                        choices = body.get('choices', [])
                        if choices:
                            content = choices[0]['message']['content']
                            
                            # Extract JSON from response
                            if '```json' in content:
                                json_str = content.split('```json')[1].split('```')[0]
                                result = json.loads(json_str)
                                results.append({
                                    'id': custom_id,
                                    'recommendation': result.get('recommendation', 'UNKNOWN'),
                                    'confidence': result.get('confidence_score', 0),
                                    'reasoning': result.get('reasoning', '')
                                })
        
        # Summary
        print(f"\nProcessed {len(results)} results")
        
        # Count by recommendation
        counts = {}
        for r in results:
            rec = r['recommendation']
            counts[rec] = counts.get(rec, 0) + 1
        
        print("\nDecision breakdown:")
        for rec, count in counts.items():
            pct = count / len(results) * 100
            print(f"  {rec}: {count} ({pct:.1f}%)")
        
        # Save processed results
        output_file = f"batch_processed_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nProcessed results saved to: {output_file}")
        
        return results
        
    except Exception as e:
        print(f"Error downloading results: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python DOWNLOAD_BATCH_RESULTS.py <job_id>")
        sys.exit(1)
    
    job_id = sys.argv[1]
    download_batch_results(job_id)