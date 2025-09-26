"""
Quick test to verify few-shot injection is working
Creates batch file without API fetching
"""

import json
import os
import sys
from datetime import datetime

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Test opportunities (no API fetch needed)
test_opportunities = [
    {
        "search_id": "test",
        "opportunity_id": "001",
        "title": "BOLT, MACHINE",
        "agency": "DLA Aviation",
        "naics": "336413",
        "psc": "5306",
        "text": "Procurement for NSN 5306-01-123-4567, BOLT, MACHINE. Quantity 500 EA. Small business set-aside. Commercial item, surplus acceptable."
    },
    {
        "search_id": "test",
        "opportunity_id": "002",
        "title": "F-16 FIGHTER JET PARTS",
        "agency": "Air Force",
        "naics": "336413",
        "psc": "1680",
        "text": "F-16 Block 50 specific components. OEM only. Secret clearance required. Military fighter platform."
    }
]

def test_phase2():
    """Test Phase 2 with few-shot injection"""
    print("\n" + "=" * 70)
    print("TESTING PHASE 2: CREATING BATCH WITH SYSTEM PROMPT + FEW-SHOT")
    print("=" * 70)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    jsonl_file = f"quick_test_{timestamp}.jsonl"
    
    # Load system prompt
    system_prompt_path = os.path.join(
        os.path.dirname(__file__),
        "Mistral-Batch-Prompts-Training-Data",
        "SOS-Triage-Agent-Sys-Prompt.md"
    )
    
    try:
        with open(system_prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = f.read().strip()
        print(f"[OK] Loaded system prompt ({len(system_prompt)} chars)")
    except Exception as e:
        print(f"ERROR loading system prompt: {e}")
        return
    
    # Load few-shot examples
    try:
        sys.path.insert(0, "Mistral-Batch-Prompts-Training-Data")
        from few_shot_examples import get_few_shot_messages
        few_shot_messages = get_few_shot_messages()
        print(f"[OK] Loaded {len(few_shot_messages)//2} few-shot examples")
    except Exception as e:
        print(f"ERROR loading few-shot: {e}")
        few_shot_messages = []
    
    # Create batch file
    with open(jsonl_file, 'w') as f:
        for i, opp in enumerate(test_opportunities):
            user_prompt = f"""Analyze this government contracting opportunity for Source One Spares:

Title: {opp['title']}
Agency: {opp.get('agency', 'N/A')}
NAICS: {opp.get('naics', 'N/A')}
PSC: {opp.get('psc', 'N/A')}

Requirements excerpt: {opp['text']}"""

            # Build message chain
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(few_shot_messages)
            messages.append({"role": "user", "content": user_prompt})
            
            batch_request = {
                "custom_id": f"test-{i:04d}",
                "body": {
                    "model": "ft:mistral-medium-latest:d42144c7:20250902:908db254",
                    "messages": messages,
                    "temperature": 0.1,
                    "max_tokens": 2000
                }
            }
            
            f.write(json.dumps(batch_request) + '\n')
    
    print(f"\n[OK] Created batch file: {jsonl_file}")
    print(f"  - Contains {len(test_opportunities)} test opportunities")
    print(f"  - Each has: system prompt + {len(few_shot_messages)//2} examples + query")
    
    # Verify structure
    print("\nVerifying first entry structure...")
    with open(jsonl_file, 'r') as f:
        first = json.loads(f.readline())
        msg_count = len(first['body']['messages'])
        print(f"  Total messages: {msg_count}")
        print(f"  Expected: 1 system + {len(few_shot_messages)} few-shot + 1 user = {1 + len(few_shot_messages) + 1}")
        
        if msg_count == 1 + len(few_shot_messages) + 1:
            print("  [OK] Structure verified!")
        else:
            print("  [ERROR] Message count mismatch!")
    
    print("\nExpected results:")
    print("  1. BOLT, MACHINE -> Should be GO (commercial item)")
    print("  2. F-16 FIGHTER -> Should be NO-GO (military platform)")

if __name__ == "__main__":
    test_phase2()