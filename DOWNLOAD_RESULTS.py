#!/usr/bin/env python3
"""Download and process batch results"""

import json
import sys
from mistralai import Mistral
from API_KEYS import MISTRAL_API_KEY
from datetime import datetime

def download_results(job_id):
    """Download and process batch results"""
    client = Mistral(api_key=MISTRAL_API_KEY)
    
    try:
        # Get job details
        job = client.batch.jobs.get(job_id=job_id)
        
        if job.status != "SUCCESS":
            print(f"Job not complete. Status: {job.status}")
            return
            
        # Download output file
        print(f"Downloading results from file: {job.output_file}")
        output = client.files.download(file_id=job.output_file)
        
        # Save raw output
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"batch_output_{timestamp}.jsonl"
        
        # Read the streaming response properly
        content = output.read()
        with open(output_file, 'wb') as f:
            f.write(content)
        print(f"Raw output saved to: {output_file}")
        
        # Parse and summarize
        results = []
        with open(output_file, 'r') as f:
            for line in f:
                if line.strip():
                    result = json.loads(line)
                    results.append(result)
        
        print(f"\nProcessed {len(results)} results")
        
        # Count decisions
        decisions = {}
        for r in results:
            try:
                response = r.get('response', {})
                if response.get('choices'):
                    content = response['choices'][0]['message']['content']
                    # Try to extract decision from JSON
                    if '```json' in content:
                        json_str = content.split('```json')[1].split('```')[0]
                        data = json.loads(json_str)
                        decision = data.get('recommendation', 'UNKNOWN')
                    else:
                        decision = 'PARSE_ERROR'
                    decisions[decision] = decisions.get(decision, 0) + 1
            except:
                decisions['ERROR'] = decisions.get('ERROR', 0) + 1
        
        print("\nDecision Summary:")
        for decision, count in sorted(decisions.items()):
            print(f"  {decision}: {count}")
            
        return output_file
        
    except Exception as e:
        print(f"Error downloading results: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        download_results(sys.argv[1])
    else:
        # Default to the job we just ran
        download_results("9d1d5895-d144-45af-a3a9-11d070b52222")