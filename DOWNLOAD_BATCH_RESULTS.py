#!/usr/bin/env python3
"""
Download and process Mistral batch results
"""

import os
import sys
import json
from datetime import datetime
from mistralai import Mistral

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from API_KEYS import MISTRAL_API_KEY
from enhanced_output_manager import EnhancedOutputManager

def download_batch_results(job_id, output_file_id=None):
    """Download and process batch results"""
    client = Mistral(api_key=MISTRAL_API_KEY)
    
    print("=" * 80)
    print("DOWNLOADING BATCH RESULTS")
    print(f"Job ID: {job_id}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Get job details
    try:
        job = client.batch.jobs.get(job_id=job_id)
        if job.status != "SUCCESS":
            print(f"Job not complete. Status: {job.status}")
            return
        
        if not output_file_id:
            output_file_id = job.output_file
            
        print(f"\nDownloading output file: {output_file_id}")
        
        # Download the output file
        output_response = client.files.download(file_id=output_file_id)
        
        # Read the streaming response
        output_content = output_response.read()
        
        # Save raw output
        raw_output_file = f"batch_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        with open(raw_output_file, 'wb') as f:
            f.write(output_content)
        print(f"Saved raw output to: {raw_output_file}")
        
        # Process results
        results = []
        regex_knockouts = []  # Empty for now since these were already filtered
        
        print("\nProcessing results...")
        with open(raw_output_file, 'r') as f:
            for line in f:
                if line.strip():
                    result = json.loads(line)
                    
                    # Extract custom_id (search_id from our metadata)
                    custom_id = result.get('custom_id', '')
                    
                    # Extract response
                    response = result.get('response', {})
                    if response.get('status_code') == 200:
                        message = response.get('body', {}).get('choices', [{}])[0].get('message', {})
                        content = message.get('content', '')
                        
                        # Parse the response - model returns JSON
                        decision = "UNKNOWN"
                        reasoning = "No reasoning provided"
                        
                        # Try to extract JSON from content
                        if '```json' in content:
                            json_str = content.split('```json')[1].split('```')[0].strip()
                            try:
                                parsed = json.loads(json_str)
                                recommendation = parsed.get('recommendation', 'UNKNOWN')
                                if recommendation == 'GO':
                                    decision = "GO"
                                elif recommendation == 'NO-GO':
                                    decision = "NO-GO"
                                elif 'CONTACT' in recommendation:
                                    decision = "CONTACT CO"
                                reasoning = parsed.get('rationale', 'No reasoning provided')
                            except:
                                pass
                        elif content.strip().startswith('{'):
                            # Direct JSON response
                            try:
                                parsed = json.loads(content)
                                recommendation = parsed.get('recommendation', 'UNKNOWN')
                                if recommendation == 'GO':
                                    decision = "GO"
                                elif recommendation == 'NO-GO':
                                    decision = "NO-GO"
                                elif 'CONTACT' in recommendation:
                                    decision = "CONTACT CO"
                                reasoning = parsed.get('rationale', 'No reasoning provided')
                            except:
                                pass
                        
                        results.append({
                            'search_id': custom_id,
                            'decision': decision,
                            'reasoning': reasoning,
                            'title': custom_id  # Will be updated if we have metadata
                        })
                        
                        print(f"  {custom_id}: {decision}")
        
        # Load metadata if available
        metadata_files = [f for f in os.listdir('.') if f.startswith('batch_metadata_') and f.endswith('.json')]
        if metadata_files:
            latest_metadata = sorted(metadata_files)[-1]
            print(f"\nLoading metadata from: {latest_metadata}")
            with open(latest_metadata, 'r') as f:
                metadata = json.load(f)
                
                # Update results with opportunity titles
                for result in results:
                    for opp in metadata.get('opportunities', []):
                        if opp['search_id'] == result['search_id']:
                            result['title'] = opp.get('title', result['search_id'])
                            break
        
        # Save final results
        print("\nSaving processed results...")
        output_manager = EnhancedOutputManager()
        output_path = output_manager.save_assessment_batch(
            assessment_results=results,
            regex_knockouts=regex_knockouts,
            source="BATCH_PROCESSOR"
        )
        
        print(f"\nResults saved to: {output_path}")
        print(f"  Total assessments: {len(results)}")
        print(f"  GOs: {sum(1 for r in results if r['decision'] == 'GO')}")
        print(f"  NO-GOs: {sum(1 for r in results if r['decision'] == 'NO-GO')}")
        print(f"  CONTACT CO: {sum(1 for r in results if r['decision'] == 'CONTACT CO')}")
        
        print("\n" + "=" * 80)
        print("BATCH RESULTS PROCESSED SUCCESSFULLY")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error processing batch results: {e}")
        import traceback
        traceback.print_exc()

def main():
    if len(sys.argv) > 1:
        job_id = sys.argv[1]
    else:
        # Use our test job
        job_id = "7fae976f-0361-4e60-982e-f1799dfb0ef6"
    
    # Optional output file ID
    output_file_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Change to batch processor directory where metadata is
    os.chdir('Mistral_Batch_Processor')
    
    download_batch_results(job_id, output_file_id)

if __name__ == "__main__":
    main()