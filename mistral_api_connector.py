#!/usr/bin/env python3
"""
Mistral API Connector for SOS Assessment
Drop-in ready with dummy model, swap to fine-tuned later
"""

import json
import os
from typing import Dict, Optional
from mistralai import Mistral
from sos_ingestion_gate_v419 import IngestionGateV419, Decision
from model_config import get_model_id, get_model_info

# Initialize Mistral client
client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY", ""))

class MistralSOSClassifier:
    """Mistral-powered classifier with dummy fallback"""
    
    def __init__(self, model_id: str = None, use_dummy: bool = False):
        """
        Initialize classifier
        model_id: Fine-tuned model ID (when ready)
        use_dummy: Use dummy prompt for now
        """
        self.model_id = model_id or get_model_id()  # Gets from config
        self.use_dummy = use_dummy
        self.regex_gate = IngestionGateV419()
        
        # Dummy prompt mimics fine-tuned behavior
        self.DUMMY_PROMPT = """You are a strict opportunity classifier for Source One Spares.
You must return a JSON object with these exact fields:
- classification: one of ["GO", "FURTHER_ANALYSIS", "CONTACT_CO", "NO-GO"]
- reasoning: short, criteria-based explanation
- confidence: number between 0 and 100

Rules:
- GO: Clear match with SOS capabilities (KC-46, Boeing platforms, surplus, refurbished)
- NO-GO: Military-only platforms (F-22, F-35), classified requirements, sole source to OEM
- FURTHER_ANALYSIS: Partial match, needs more info
- CONTACT_CO: Worth outreach but needs clarification

SOS Strengths: KC-46 ($97M contracts), Boeing/Airbus platforms, FAA certified parts, surplus/refurbished
SOS Contracts: FA860925FB031 ($39M), Naval Supply ($2M+), PSC 1680 (97% revenue)

Always respond ONLY with valid JSON."""

    def classify_opportunity(self, opportunity: Dict, temperature: float = 0.1) -> Dict:
        """
        Classify an opportunity using Mistral
        
        Args:
            opportunity: Dict with title, agency, description, etc.
            temperature: Model temperature (0.1 for consistency)
        
        Returns:
            Dict with classification, reasoning, confidence
        """
        
        # First, run through regex for initial assessment
        regex_result = self.regex_gate.assess_opportunity(opportunity)
        
        # Format opportunity for Mistral
        opp_text = self._format_opportunity(opportunity, regex_result)
        
        # Build message
        if self.use_dummy:
            content = f"{self.DUMMY_PROMPT}\n\nOpportunity:\n{opp_text}"
        else:
            # Fine-tuned model doesn't need the prompt
            content = opp_text
        
        messages = [
            {"role": "user", "content": content}
        ]
        
        try:
            # Call Mistral API
            # Check if it's an agent ID (starts with 'ag:')
            if self.model_id.startswith('ag:'):
                # Use agents.complete for fine-tuned agents
                response = client.agents.complete(
                    agent_id=self.model_id,
                    messages=messages
                )
            else:
                # Use chat.complete for regular models
                response = client.chat.complete(
                    model=self.model_id,
                    messages=messages,
                    temperature=temperature,
                    response_format={"type": "json_object"} if not self.use_dummy else None
                )
            
            # Parse response
            result_text = response.choices[0].message.content
            
            # Try to parse as JSON
            try:
                # Handle dual JSON + Markdown format
                # Look for JSON block first (could be before or after markdown)
                if "```json" in result_text:
                    # Extract JSON from code block
                    json_str = result_text.split("```json")[1].split("```")[0].strip()
                elif '{"' in result_text or "{'result'" in result_text:
                    # Find JSON object in the response
                    import re
                    # Look for JSON that starts with { and ends with }
                    json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', result_text, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(0)
                    else:
                        # Try to find from first { to last }
                        start = result_text.index("{")
                        end = result_text.rindex("}") + 1
                        json_str = result_text[start:end]
                else:
                    # Maybe the whole thing is JSON
                    json_str = result_text.strip()
                
                parsed = json.loads(json_str)
                
                # Map 'result' to 'classification' if needed
                classification = parsed.get('result', parsed.get('classification', 'FURTHER_ANALYSIS'))
                
                # Handle GO/NO-GO variations
                if classification == 'NO_GO':
                    classification = 'NO-GO'
                
                # Extract rationale
                reasoning = parsed.get('rationale', parsed.get('reasoning', ''))
                if not reasoning and 'knock_out_reasons' in parsed:
                    reasoning = '; '.join(parsed['knock_out_reasons'])
                
                # If we have markdown after JSON, we could extract additional info
                # but for now just use the JSON
                
                result = {
                    "classification": classification,
                    "reasoning": reasoning,
                    "confidence": 85  # Agent responses are high confidence
                }
            except (json.JSONDecodeError, ValueError, Exception) as e:
                # Try to extract decision from markdown if JSON fails
                if "**Assessment:** **GO**" in result_text or "Result: GO" in result_text:
                    classification = "GO"
                elif "**Assessment:** **NO-GO**" in result_text or "Result: NO-GO" in result_text:
                    classification = "NO-GO"
                elif "CONTACT" in result_text.upper():
                    classification = "CONTACT_CO"
                else:
                    classification = "FURTHER_ANALYSIS"
                
                # Try to extract reasoning from markdown
                reasoning = "Model returned mixed format - see full response"
                if "**Rationale:**" in result_text:
                    reasoning = result_text.split("**Rationale:**")[1].split("\n")[0].strip()
                
                result = {
                    "classification": classification,
                    "reasoning": reasoning,
                    "confidence": 75  # Lower confidence for parsed markdown
                }
            
            # Add metadata
            result["model_used"] = self.model_id
            result["regex_decision"] = regex_result.decision.value
            result["regex_blocker"] = regex_result.primary_blocker
            
            return result
            
        except Exception as e:
            # Fallback to regex-only decision
            return {
                "classification": self._map_decision(regex_result.decision),
                "reasoning": f"Regex: {regex_result.primary_blocker or 'Pattern match'}",
                "confidence": 75,
                "model_used": "REGEX_FALLBACK",
                "error": str(e)
            }
    
    def _format_opportunity(self, opp: Dict, regex_result) -> str:
        """Format opportunity data for model input"""
        
        # Extract key fields
        title = opp.get('title', 'N/A')
        agency = opp.get('agency', 'N/A')
        naics = opp.get('naics', 'N/A')
        psc = opp.get('psc', 'N/A')
        set_aside = opp.get('set_aside', 'None')
        value_low = opp.get('value_low', 0)
        value_high = opp.get('value_high', 0)
        # Get full document text if available, otherwise fall back to description
        full_text = opp.get('full_text', '')
        description = opp.get('description', opp.get('text', ''))
        
        # Use full text if available (up to 200k chars ~ 50 pages), otherwise use description
        content = full_text[:200000] if full_text else description[:20000]
        
        # Build formatted text
        text = f"""Title: {title}
Agency: {agency}
NAICS: {naics}
PSC: {psc}
Set Aside: {set_aside}
Value Range: ${value_low:,} - ${value_high:,}
Document Content: {content}
Regex Decision: {regex_result.decision.value}
Primary Blocker: {regex_result.primary_blocker or 'None'}
Categories Triggered: {', '.join(str(c) for c in regex_result.categories_triggered[:5])}"""
        
        # Add SOS-specific context
        if 'KC-46' in title or 'KC-46' in description:
            text += "\nNote: SOS has KC-46 IDIQ FA860922DB009 ($97.5M)"
        if psc == '1680':
            text += "\nNote: PSC 1680 is 97% of SOS revenue"
        if 'surplus' in description.lower() or 'DIBBS' in description:
            text += "\nNote: SOS specializes in surplus/DIBBS"
            
        return text
    
    def _map_decision(self, decision: Decision) -> str:
        """Map regex decision to classification"""
        if decision == Decision.GO:
            return "GO"
        elif decision == Decision.NO_GO:
            return "NO-GO"
        elif decision == Decision.FURTHER_ANALYSIS:
            return "FURTHER_ANALYSIS"
        else:
            return "CONTACT_CO"

def test_classifier():
    """Test the classifier with sample opportunities"""
    
    classifier = MistralSOSClassifier(use_dummy=True)
    
    # Test cases
    test_opportunities = [
        {
            "title": "KC-46 Initial Spare Parts",
            "agency": "Air Force",
            "naics": "336413",
            "psc": "1680",
            "description": "Spare parts for KC-46 aircraft at Tinker AFB",
            "value_low": 30000000,
            "value_high": 40000000
        },
        {
            "title": "F-22 Avionics Upgrade",
            "agency": "Air Force",
            "naics": "334511",
            "description": "Classified avionics for F-22 Raptor",
            "value_low": 5000000,
            "value_high": 10000000
        },
        {
            "title": "Surplus Aircraft Parts Sale",
            "agency": "DLA",
            "description": "DIBBS opportunity for surplus C-130 components",
            "value_low": 100000,
            "value_high": 500000
        }
    ]
    
    print("="*60)
    print("TESTING MISTRAL CLASSIFIER")
    print("="*60)
    
    for i, opp in enumerate(test_opportunities, 1):
        print(f"\nTest Case {i}: {opp['title']}")
        print("-" * 40)
        
        result = classifier.classify_opportunity(opp)
        
        print(f"Classification: {result['classification']}")
        print(f"Reasoning: {result['reasoning']}")
        print(f"Confidence: {result.get('confidence', 'N/A')}%")
        print(f"Model Used: {result['model_used']}")
        print(f"Regex Decision: {result.get('regex_decision', 'N/A')}")

if __name__ == "__main__":
    # Check for API key
    if not os.environ.get("MISTRAL_API_KEY"):
        print("WARNING: MISTRAL_API_KEY not set")
        print("Set it with: export MISTRAL_API_KEY='your-key-here'")
        print("\nRunning in demo mode with dummy responses...")
    
    test_classifier()