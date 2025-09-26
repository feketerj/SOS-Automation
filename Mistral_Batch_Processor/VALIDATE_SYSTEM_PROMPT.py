"""
VALIDATE_SYSTEM_PROMPT.py
Test script to validate system prompt injection in batch processing
Creates a small test batch with known opportunities to verify behavior
"""

import json
import os
from datetime import datetime

def create_validation_batch():
    """Create a test batch with 3 known opportunities using system prompt injection"""
    
    # Load the system prompt
    system_prompt_path = os.path.join(
        os.path.dirname(__file__),
        "Mistral-Batch-Prompts-Training-Data",
        "SOS-Triage-Agent-Sys-Prompt.md"
    )
    
    try:
        with open(system_prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = f.read().strip()
        print(f"[OK] Loaded system prompt ({len(system_prompt)} characters)")
    except Exception as e:
        print(f"ERROR: Could not load system prompt: {e}")
        return None
    
    # Test opportunities from the training examples
    test_opportunities = [
        {
            "id": "test-001-bolt",
            "title": "BOLT, MACHINE",
            "agency": "DLA Aviation",
            "naics": "336413",
            "psc": "5306",
            "text": "Proposed procurement for NSN 5306-01-123-4567, BOLT, MACHINE. Quantity 500 EA. Small business set-aside. No special requirements. Standard commercial item."
        },
        {
            "id": "test-002-f16",
            "title": "F-16 FIGHTER JET PARTS",
            "agency": "Air Force",
            "naics": "336413",
            "psc": "1680",
            "text": "Requirement for F-16 Block 50 specific components. OEM only. Must have Lockheed Martin approval. Sole source to original manufacturer."
        },
        {
            "id": "test-003-uh60",
            "title": "UH-60 BLACK HAWK OVERHAUL",
            "agency": "Army Aviation",
            "naics": "336413",
            "psc": "1520",
            "text": "Depot level maintenance for UH-60 Black Hawk helicopters. Contractor must be approved depot. Military-specific platform. No commercial equivalent."
        }
    ]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    validation_file = f"validation_batch_{timestamp}.jsonl"
    
    print(f"\nCreating validation batch: {validation_file}")
    print("=" * 60)
    
    with open(validation_file, 'w') as f:
        for i, opp in enumerate(test_opportunities):
            print(f"\n{i+1}. {opp['id']}: {opp['title']}")
            print(f"   Expected: {'GO' if 'BOLT' in opp['title'] else 'NO-GO'}")
            
            # User message (opportunity data only)
            user_prompt = f"""Analyze this government contracting opportunity for Source One Spares:

Title: {opp['title']}
Agency: {opp['agency']}
NAICS: {opp['naics']}
PSC: {opp['psc']}

Requirements excerpt: {opp['text']}"""
            
            # Create batch request WITH system prompt
            batch_request = {
                "custom_id": opp['id'],
                "body": {
                    "model": "ft:mistral-medium-latest:d42144c7:20250902:908db254",
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": user_prompt
                        }
                    ],
                    "temperature": 0.1,
                    "max_tokens": 2000
                }
            }
            
            f.write(json.dumps(batch_request) + '\n')
    
    print("\n" + "=" * 60)
    print(f"[OK] Validation batch created: {validation_file}")
    print("\nBatch structure:")
    print("  - System message: Full SOS agent prompt with KO rules")
    print("  - User message: Opportunity data only")
    print("\nExpected results:")
    print("  1. BOLT, MACHINE -> GO (simple commercial item)")
    print("  2. F-16 FIGHTER -> NO-GO (military platform, OEM only)")
    print("  3. UH-60 BLACK HAWK -> NO-GO (military platform)")
    
    return validation_file

def inspect_batch_file(filename):
    """Inspect the created batch file to verify structure"""
    print("\n" + "=" * 60)
    print("INSPECTING BATCH FILE STRUCTURE")
    print("=" * 60)
    
    with open(filename, 'r') as f:
        first_line = f.readline()
        request = json.loads(first_line)
        
        print(f"\nFirst request structure:")
        print(f"  Custom ID: {request['custom_id']}")
        print(f"  Model: {request['body']['model']}")
        print(f"  Messages: {len(request['body']['messages'])} messages")
        
        for i, msg in enumerate(request['body']['messages']):
            print(f"\n  Message {i+1}:")
            print(f"    Role: {msg['role']}")
            print(f"    Content length: {len(msg['content'])} characters")
            if msg['role'] == 'system':
                print(f"    Content preview: {msg['content'][:200]}...")
            else:
                print(f"    Content preview: {msg['content'][:150]}...")

if __name__ == "__main__":
    print("SYSTEM PROMPT VALIDATION SCRIPT")
    print("================================")
    print("This script creates a test batch with system prompt injection")
    print("to validate that the fine-tuned model behaves like the agent.\n")
    
    batch_file = create_validation_batch()
    if batch_file:
        inspect_batch_file(batch_file)
        
        print("\n" + "=" * 60)
        print("NEXT STEPS:")
        print("=" * 60)
        print("1. Submit this batch to Mistral:")
        print(f"   python BATCH_SUBMITTER_V2.py {batch_file}")
        print("\n2. Compare results with expected outcomes")
        print("\n3. If results match expectations, the system prompt")
        print("   injection is working correctly!")