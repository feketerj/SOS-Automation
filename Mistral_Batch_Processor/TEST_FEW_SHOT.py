"""
Test script to verify few-shot implementation
Creates a small test batch with few-shot examples
"""

import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from datetime import datetime

# Import the few-shot examples
sys.path.insert(0, "Mistral-Batch-Prompts-Training-Data")
from few_shot_examples import get_few_shot_messages

def test_few_shot_batch():
    """Create a test batch file to verify few-shot structure"""
    
    print("TESTING FEW-SHOT IMPLEMENTATION")
    print("=" * 60)
    
    # Load system prompt
    system_prompt_path = "Mistral-Batch-Prompts-Training-Data/SOS-Triage-Agent-Sys-Prompt.md"
    with open(system_prompt_path, 'r', encoding='utf-8') as f:
        system_prompt = f.read().strip()
    print(f"[OK] Loaded system prompt ({len(system_prompt)} chars)")
    
    # Get few-shot examples
    few_shot_messages = get_few_shot_messages()
    print(f"[OK] Loaded {len(few_shot_messages)//2} few-shot examples")
    
    # Create a test opportunity
    test_opp = {
        "search_id": "test-few-shot",
        "opportunity_id": "001",
        "title": "WASHER, FLAT",
        "agency": "DLA Aviation",
        "naics": "336413",
        "psc": "5310",
        "text": "Procurement for NSN 5310-01-234-5678, WASHER, FLAT. Quantity 1000 EA. Commercial item. No special requirements."
    }
    
    # Build the message chain
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    messages.extend(few_shot_messages)
    messages.append({
        "role": "user",
        "content": f"""Analyze this government contracting opportunity for Source One Spares:

Title: {test_opp['title']}
Agency: {test_opp['agency']}
NAICS: {test_opp['naics']}
PSC: {test_opp['psc']}

Requirements excerpt: {test_opp['text']}"""
    })
    
    # Create batch request
    batch_request = {
        "custom_id": f"test-few-shot-001",
        "body": {
            "model": "ft:mistral-medium-latest:d42144c7:20250902:908db254",
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 2000
        }
    }
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"test_few_shot_{timestamp}.jsonl"
    
    with open(output_file, 'w') as f:
        f.write(json.dumps(batch_request) + '\n')
    
    print(f"\n[OK] Created test batch: {output_file}")
    
    # Show structure
    print("\nMessage Structure:")
    print(f"  1. System prompt: {len(system_prompt)} chars")
    for i in range(0, len(few_shot_messages), 2):
        if i < len(few_shot_messages):
            print(f"  {i//2 + 2}. Example {i//2 + 1} User: {few_shot_messages[i]['content'][:50]}...")
            print(f"  {i//2 + 3}. Example {i//2 + 1} Assistant: {few_shot_messages[i+1]['content'][:50]}...")
    print(f"  {len(few_shot_messages) + 2}. Actual query: WASHER, FLAT opportunity")
    
    print("\nExpected behavior:")
    print("  - Model sees system prompt establishing SOS rules")
    print("  - Model sees 3 examples: GO (commercial), NO-GO (military), NO-GO (set-aside)")
    print("  - Model evaluates actual opportunity")
    print("  - Should return GO (simple commercial item, no restrictions)")
    
    return output_file

if __name__ == "__main__":
    test_file = test_few_shot_batch()
    print("\n" + "=" * 60)
    print("Test complete! You can now submit this batch to verify")
    print("few-shot examples are working correctly.")
    print(f"\nTo submit: python BATCH_SUBMITTER_V2.py {test_file}")