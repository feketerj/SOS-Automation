#!/usr/bin/env python3
"""
BATCH API HANDLER - Optional batch processing via Mistral API

This module provides batch API functionality when needed.
It's NOT the main way to run assessments - use RUN_ASSESSMENT.py instead.

This is only for when you specifically need to:
1. Submit opportunities to Mistral batch API for cost savings
2. Check batch job status
3. Download batch results
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Add paths for imports
sys.path.insert(0, 'Mistral_Batch_Processor')
sys.path.insert(0, '.')

class BatchAPIHandler:
    """Handles Mistral batch API operations"""

    def __init__(self):
        """Initialize with API configuration"""
        # Try to get from environment first
        self.api_key = os.getenv('MISTRAL_API_KEY', '2oAquITdDMiyyk0OfQuJSSqePn3SQbde')
        self.model = 'ft:pixtral-12b-latest:d42144c7:20250912:f7d61150'

    def prepare_batch_input(self, opportunities):
        """
        Prepare opportunities for batch processing

        Args:
            opportunities: List of opportunity dicts with assessments

        Returns:
            Path to JSONL file ready for batch submission
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'Mistral_Batch_Processor/batch_input_{timestamp}.jsonl'

        with open(output_file, 'w') as f:
            for i, opp in enumerate(opportunities):
                # Create batch request format
                request = {
                    "custom_id": f"opp_{i}_{opp.get('announcement_number', 'unknown')}",
                    "body": {
                        "model": self.model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are an SOS assessment expert. Evaluate if this opportunity is GO, NO-GO, or INDETERMINATE."
                            },
                            {
                                "role": "user",
                                "content": f"Opportunity: {opp.get('announcement_title', '')}\n"
                                         f"Agency: {opp.get('agency', '')}\n"
                                         f"Description: {opp.get('description', '')[:5000]}"
                            }
                        ]
                    }
                }
                f.write(json.dumps(request) + '\n')

        print(f"Batch input prepared: {output_file}")
        return output_file

    def submit_batch(self, input_file):
        """
        Submit batch to Mistral API

        Args:
            input_file: Path to JSONL file

        Returns:
            Job ID or None if submission fails
        """
        try:
            from mistralai import Mistral

            client = Mistral(api_key=self.api_key)

            # Read the file
            with open(input_file, 'rb') as f:
                batch_data = client.files.upload(
                    file=(input_file, f.read()),
                    purpose="batch"
                )

            # Create batch job
            batch_job = client.batch.jobs.create(
                input_files=[batch_data.id],
                model=self.model,
                endpoint="/v1/chat/completions",
                metadata={"description": f"SOS Assessment Batch - {datetime.now().isoformat()}"}
            )

            print(f"Batch submitted successfully!")
            print(f"Job ID: {batch_job.id}")
            print(f"Status: {batch_job.status}")

            return batch_job.id

        except Exception as e:
            print(f"ERROR submitting batch: {e}")
            return None

    def check_status(self, job_id):
        """
        Check status of a batch job

        Args:
            job_id: Batch job ID

        Returns:
            Status dict or None
        """
        try:
            from mistralai import Mistral

            client = Mistral(api_key=self.api_key)
            job = client.batch.jobs.get(job_id=job_id)

            status = {
                'id': job.id,
                'status': job.status,
                'created_at': job.created_at,
                'total_requests': job.total_requests,
                'succeeded_requests': job.succeeded_requests,
                'failed_requests': job.failed_requests
            }

            print(f"Job {job_id}:")
            print(f"  Status: {job.status}")
            print(f"  Progress: {job.succeeded_requests}/{job.total_requests}")

            return status

        except Exception as e:
            print(f"ERROR checking status: {e}")
            return None

    def download_results(self, job_id, output_dir='Mistral_Batch_Processor'):
        """
        Download results from completed batch job

        Args:
            job_id: Batch job ID
            output_dir: Directory to save results

        Returns:
            Path to results file or None
        """
        try:
            from mistralai import Mistral

            client = Mistral(api_key=self.api_key)
            job = client.batch.jobs.get(job_id=job_id)

            if job.status != 'SUCCEEDED':
                print(f"Job not complete. Status: {job.status}")
                return None

            # Download results file
            if job.output_file:
                result_content = client.files.download(file_id=job.output_file)

                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = f'{output_dir}/batch_results_{job_id[:8]}_{timestamp}.jsonl'

                with open(output_file, 'wb') as f:
                    f.write(result_content)

                print(f"Results downloaded: {output_file}")

                # Parse and show summary
                self._summarize_results(output_file)

                return output_file
            else:
                print("No output file available")
                return None

        except Exception as e:
            print(f"ERROR downloading results: {e}")
            return None

    def _summarize_results(self, results_file):
        """Summarize batch results"""
        stats = {'GO': 0, 'NO-GO': 0, 'INDETERMINATE': 0}

        with open(results_file, 'r') as f:
            for line in f:
                try:
                    result = json.loads(line)
                    content = result.get('response', {}).get('body', {}).get('choices', [{}])[0].get('message', {}).get('content', '')

                    # Extract decision from response
                    if 'GO' in content and 'NO-GO' not in content:
                        stats['GO'] += 1
                    elif 'NO-GO' in content:
                        stats['NO-GO'] += 1
                    else:
                        stats['INDETERMINATE'] += 1
                except:
                    continue

        print(f"\nBatch Results Summary:")
        print(f"  GO: {stats['GO']}")
        print(f"  NO-GO: {stats['NO-GO']}")
        print(f"  INDETERMINATE: {stats['INDETERMINATE']}")
        print(f"  TOTAL: {sum(stats.values())}")


# Command-line interface
if __name__ == "__main__":
    handler = BatchAPIHandler()

    if len(sys.argv) < 2:
        print("BATCH API HANDLER - For batch processing via Mistral API")
        print("")
        print("This is NOT the main way to run assessments!")
        print("Use RUN_ASSESSMENT.py for normal operations.")
        print("")
        print("Usage:")
        print("  python BATCH_API_HANDLER.py submit <input.jsonl>")
        print("  python BATCH_API_HANDLER.py status <job_id>")
        print("  python BATCH_API_HANDLER.py download <job_id>")
        print("")
        print("To run a full assessment, use:")
        print("  python RUN_ASSESSMENT.py")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'submit' and len(sys.argv) > 2:
        handler.submit_batch(sys.argv[2])
    elif command == 'status' and len(sys.argv) > 2:
        handler.check_status(sys.argv[2])
    elif command == 'download' and len(sys.argv) > 2:
        handler.download_results(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        print("Use 'submit', 'status', or 'download'")