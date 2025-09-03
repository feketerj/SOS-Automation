#!/usr/bin/env python3
"""
Test script for SOS Triage Holding Agent
Agent ID: ag:d42144c7:20250902:sos-triage-holding-agent:80b28a97
"""

import os
import json
from mistralai import Mistral

# Your agent ID (PRODUCTION MODEL - Trained on 8,482 examples)
SOS_AGENT_ID = "ag:d42144c7:20250902:sos-triage-agent:73e9cddd"

def test_sos_agent():
    """Test the SOS agent with various opportunities"""
    
    # Initialize client
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("ERROR: MISTRAL_API_KEY not set!")
        print("Set it with: export MISTRAL_API_KEY='your-key-here'")
        return
    
    client = Mistral(api_key=api_key)
    
    print("="*60)
    print("TESTING SOS PRODUCTION AGENT")
    print(f"Agent ID: {SOS_AGENT_ID}")
    print("Trained on 8,482 real SOS examples")
    print("="*60)
    
    # Test cases matching your training data
    test_cases = [
        {
            "name": "KC-46 Spare Parts (Should be GO)",
            "prompt": "KC-46 initial spare parts for Tinker AFB. Value $35M. Can SOS compete?"
        },
        {
            "name": "F-22 Components (Should be NO-GO)",
            "prompt": "F-22 Raptor avionics upgrade. Classified components. Should we bid?"
        },
        {
            "name": "DIBBS Surplus (Should be GO)",
            "prompt": "DIBBS opportunity for surplus C-130 parts. Is this good for SOS?"
        },
        {
            "name": "Navy Contract (Should be GO/FURTHER)",
            "prompt": "Naval Supply needs P-8 Poseidon parts. Commercial acquisition. PSC 1680."
        },
        {
            "name": "8(a) Set-aside (Should be FURTHER)",
            "prompt": "8(a) set-aside for aircraft parts. Can we team with an 8(a) firm?"
        },
        {
            "name": "L-100 Parts (Should be GO)",
            "prompt": "L-100 (civilian C-130) components required. FAA certified only."
        },
        {
            "name": "Complex Assessment",
            "prompt": """Assess this opportunity:
Title: Aircraft Ground Support Equipment
Agency: Air Force
PSC: 1680 (our primary)
NAICS: 336413
Value: $15M
Description: Refurbished equipment acceptable. FAA 8130 required.
Set-aside: None
Should SOS pursue?"""
        }
    ]
    
    # Run tests
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST {i}: {test['name']}")
        print(f"{'='*60}")
        print(f"Prompt: {test['prompt'][:100]}...")
        
        try:
            # Call the agent
            response = client.agents.complete(
                agent_id=SOS_AGENT_ID,
                messages=[
                    {"role": "user", "content": test['prompt']}
                ]
            )
            
            # Get response
            answer = response.choices[0].message.content
            
            print(f"\nAgent Response:")
            print("-" * 40)
            print(answer[:500] if len(answer) > 500 else answer)
            
            # Try to extract decision if present
            if "GO" in answer and "NO-GO" not in answer and "NO_GO" not in answer:
                print(f"\n✓ Decision: GO")
            elif "NO-GO" in answer or "NO_GO" in answer:
                print(f"\n✓ Decision: NO-GO")
            elif "FURTHER" in answer:
                print(f"\n✓ Decision: FURTHER ANALYSIS")
            else:
                print(f"\n? Decision: UNCLEAR")
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    print(f"\n{'='*60}")
    print("TESTING COMPLETE")
    print("="*60)
    print("\nNOTE: The agent should respond based on your training data:")
    print("- KC-46 → GO (SOS has contracts)")
    print("- F-22 → NO-GO (military only)")
    print("- DIBBS → GO (surplus marketplace)")
    print("- PSC 1680 → Favorable (97% of SOS revenue)")
    print("- L-100 → GO (civilian C-130)")

def quick_test():
    """Quick single test"""
    
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("ERROR: Set MISTRAL_API_KEY first!")
        return
    
    client = Mistral(api_key=api_key)
    
    # Simple test
    response = client.agents.complete(
        agent_id=SOS_AGENT_ID,
        messages=[
            {"role": "user", "content": "KC-46 spare parts opportunity. Should SOS bid?"}
        ]
    )
    
    print("Quick Test Response:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_test()
    else:
        test_sos_agent()