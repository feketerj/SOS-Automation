#!/usr/bin/env python3
"""Save and analyze batch error file"""

from mistralai import Mistral
import json

client = Mistral(api_key='2oAquITdDMiyyk0OfQuJSSqePn3SQbde')
job_id = '791d8c44-5fa1-4cd6-b7f7-900521255bec'

job = client.batch.jobs.get(job_id=job_id)

# Download error file
error_content = client.files.download(file_id=job.error_file)
content = error_content.read()

# Save error file
with open('batch_errors.jsonl', 'wb') as f:
    f.write(content)
print('Error file saved as batch_errors.jsonl')

# Analyze errors
lines = content.decode('utf-8').strip().split('\n')
print(f'\nTotal errors: {len(lines)}')

# Check first error in detail
if lines:
    first_error = json.loads(lines[0])
    print('\nFirst error details:')
    print(f"Custom ID: {first_error.get('custom_id', 'N/A')}")
    if 'error' in first_error:
        print(f"Error type: {first_error['error'].get('type', 'N/A')}")
        print(f"Error message: {first_error['error'].get('message', 'N/A')}")
    
    # Count error types
    error_types = {}
    for line in lines:
        try:
            record = json.loads(line)
            if 'error' in record:
                error_type = record['error'].get('type', 'unknown')
                if error_type not in error_types:
                    error_types[error_type] = 0
                error_types[error_type] += 1
        except:
            pass
    
    print('\nError type breakdown:')
    for error_type, count in error_types.items():
        print(f'  {error_type}: {count}')