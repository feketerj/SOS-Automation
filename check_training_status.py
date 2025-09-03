#!/usr/bin/env python3
"""
Check status of Mistral fine-tuning job
Updates model_config.py when training completes
"""

import os
import time
from datetime import datetime
from mistralai import Mistral

def check_training_status(job_id: str = None):
    """
    Check the status of a fine-tuning job
    
    Args:
        job_id: The job ID from Mistral (e.g., 'job_abc123')
    """
    
    # Get API key
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("ERROR: MISTRAL_API_KEY not set!")
        return
    
    client = Mistral(api_key=api_key)
    
    if not job_id:
        print("="*60)
        print("MISTRAL TRAINING STATUS CHECKER")
        print("="*60)
        job_id = input("Enter your fine-tuning job ID: ").strip()
    
    print(f"\nChecking job: {job_id}")
    print("-"*40)
    
    try:
        # Get job status
        job = client.fine_tuning.jobs.get(job_id=job_id)
        
        print(f"Status: {job.status}")
        print(f"Model: {job.model}")
        print(f"Created: {job.created_at}")
        
        if job.status == "succeeded":
            print(f"\n✅ TRAINING COMPLETE!")
            print(f"Fine-tuned Model ID: {job.fine_tuned_model}")
            
            # Ask if user wants to update config
            update = input("\nUpdate model_config.py with this model? (y/n): ")
            if update.lower() == 'y':
                update_model_config(job.fine_tuned_model)
        
        elif job.status == "running":
            print(f"\n⏳ Training in progress...")
            if hasattr(job, 'trained_tokens'):
                print(f"Tokens processed: {job.trained_tokens:,}")
            
        elif job.status == "failed":
            print(f"\n❌ Training failed!")
            if hasattr(job, 'error'):
                print(f"Error: {job.error}")
        
        else:
            print(f"\nStatus: {job.status}")
            
    except Exception as e:
        print(f"Error checking job: {e}")

def update_model_config(model_id: str):
    """Update model_config.py with the new model ID"""
    
    config_file = "model_config.py"
    
    # Read current config
    with open(config_file, 'r') as f:
        lines = f.readlines()
    
    # Update the production model line
    for i, line in enumerate(lines):
        if '"production_model": None,' in line:
            lines[i] = f'    "production_model": "{model_id}",  # Updated {datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
            break
    
    # Update active model
    for i, line in enumerate(lines):
        if 'ACTIVE_MODEL = "holding_agent"' in line:
            lines[i] = 'ACTIVE_MODEL = "production_model"  # Using trained model\n'
            break
    
    # Write back
    with open(config_file, 'w') as f:
        f.writelines(lines)
    
    print(f"\n✅ Updated {config_file}")
    print(f"   Production model: {model_id}")
    print(f"   Active model: production_model")

def monitor_training(job_id: str, check_interval: int = 60):
    """
    Monitor training progress
    
    Args:
        job_id: The job ID to monitor
        check_interval: Seconds between checks (default 60)
    """
    
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("ERROR: MISTRAL_API_KEY not set!")
        return
    
    client = Mistral(api_key=api_key)
    
    print(f"Monitoring job: {job_id}")
    print(f"Checking every {check_interval} seconds...")
    print("Press Ctrl+C to stop monitoring\n")
    
    start_time = time.time()
    
    try:
        while True:
            job = client.fine_tuning.jobs.get(job_id=job_id)
            
            elapsed = (time.time() - start_time) / 3600
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            print(f"[{timestamp}] Status: {job.status} | Elapsed: {elapsed:.1f}h")
            
            if job.status == "succeeded":
                print(f"\n✅ TRAINING COMPLETE!")
                print(f"Model ID: {job.fine_tuned_model}")
                update_model_config(job.fine_tuned_model)
                break
            
            elif job.status == "failed":
                print(f"\n❌ Training failed!")
                break
            
            time.sleep(check_interval)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "monitor" and len(sys.argv) > 2:
            monitor_training(sys.argv[2])
        else:
            check_training_status(sys.argv[1])
    else:
        print("Usage:")
        print("  python check_training_status.py <job_id>")
        print("  python check_training_status.py monitor <job_id>")
        print("\nOr run without arguments to enter job ID interactively")