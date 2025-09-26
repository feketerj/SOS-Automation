#!/usr/bin/env python3
"""
ULTIMATE Mistral Connector - Full model responses + smart pipeline titles
Gets EVERYTHING from the model for comprehensive reports
NOW WITH STANDALONE FALLBACK - Works without mistralai package!
"""

import json
import os
import re
from typing import Dict, Optional
from sos_ingestion_gate_v419 import IngestionGateV419, Decision

# HARDWIRED CONFIGURATION - PRIVATE CLIENT APP
api_key = "2oAquITdDMiyyk0OfQuJSSqePn3SQbde"  # Mistral API key

# Try to import mistralai, fall back to HTTP if not available
try:
    from mistralai import Mistral
    client = Mistral(api_key=api_key)
    USING_SDK = True
    print('[INFO] Using mistralai SDK')
except ImportError:
    # Fallback to direct HTTP
    import requests
    client = None
    USING_SDK = False
    print("[INFO] mistralai not found, using HTTP fallback")
    # Use the same hardwired key
    API_KEY = api_key
    API_URL = 'https://api.mistral.ai/v1/chat/completions'

class MistralSOSClassifier:
    """Ultimate classifier with full reasoning capture"""
    
    def __init__(self, model_id: str = None):
        """Initialize with hardwired model"""
        # HARDWIRED MODEL ID - PRIVATE CLIENT APP
        self.model_id = "ag:d42144c7:20250911:untitled-agent:15489fc1"  # Production agent
        
        self.regex_gate = IngestionGateV419()

    def extract_pipeline_title(self, text: str, title: str = "") -> str:
        """Extract smart pipeline title from document"""
        
        text_upper = text.upper() if text else ""
        title_upper = title.upper() if title else ""
        
        # Extract part number
        part_number = "NA"
        pn_patterns = [
            r'P/N[\s:]+([A-Z0-9]{2,}[\-][A-Z0-9\-]+)',
            r'PN[\s:]+([A-Z0-9]{2,}[\-][A-Z0-9\-]+)',
            r'PART NUMBER[\s:]+([A-Z0-9]{2,}[\-][A-Z0-9\-]+)',
            r'PART NO[\s:]+([A-Z0-9]{2,}[\-][A-Z0-9\-]+)'
        ]
        
        for pattern in pn_patterns:
            match = re.search(pattern, text_upper)
            if match:
                part_number = match.group(1)
                break
        
        # If no P/N in document, try NSN
        if part_number == "NA":
            nsn_match = re.search(r'NSN[\s:]*(\d{4}[\-\s]\d{2}[\-\s]\d{3}[\-\s]\d{4})', text_upper)
            if nsn_match:
                part_number = f"NSN-{nsn_match.group(1).replace(' ', '-')}"
        
        # Extract quantity
        quantity = "NA"
        qty_patterns = [
            r'QUANTITY[\s:]+(\d+)',
            r'QTY[\s:]+(\d+)',
            r'(\d+)\s+EACH',
            r'(\d+)\s+EA\b'
        ]
        
        for pattern in qty_patterns:
            match = re.search(pattern, text_upper)
            if match:
                quantity = match.group(1)
                break
        
        # Extract condition
        condition = "unknown"
        if any(word in text_upper for word in ['REPAIR', 'OVERHAUL', 'OH ', 'O/H']):
            condition = "repair"
        elif any(word in text_upper for word in ['REFURBISH', 'REFURB', 'RECONDITION']):
            condition = "refurbished"
        elif any(word in text_upper for word in ['SURPLUS', 'EXCESS', 'DIBBS']):
            condition = "surplus"
        elif any(word in text_upper for word in ['NEW', 'UNUSED', 'FACTORY NEW']):
            condition = "new"
        elif 'AS IS' in text_upper or 'AS-IS' in text_upper:
            condition = "as-is"
        
        # Extract MDS/Aircraft
        mds = "NA"
        aircraft_patterns = [
            r'MDS[\s:]+([A-Z0-9\-]+)',
            r'AIRCRAFT[\s:]+([A-Z0-9\-]+)',
            r'PLATFORM[\s:]+([A-Z0-9\-]+)',
            r'APPLICATION[\s:]+([A-Z0-9\-]+)'
        ]
        
        for pattern in aircraft_patterns:
            match = re.search(pattern, text_upper)
            if match:
                mds = match.group(1)
                break
        
        # Look for specific aircraft mentions
        if mds == "NA":
            aircraft_list = ['KC-46', 'C-130', 'F-16', 'F-15', 'F-22', 'F-35', 'C-17', 
                           'P-8', 'E-3', 'B-52', 'UH-60', 'CH-47', 'AH-64']
            for aircraft in aircraft_list:
                if aircraft in text_upper:
                    mds = aircraft
                    break
        
        # Get solicitation number
        solicitation = "NO-SOLICITATION"
        sol_patterns = [
            r'RFP[\s#:]+([A-Z0-9\-]+)',
            r'SOLICITATION[\s:]+([A-Z0-9\-]+)',
            r'CONTRACT[\s:]+([A-Z0-9\-]+)'
        ]
        
        for pattern in sol_patterns:
            match = re.search(pattern, text_upper)
            if match:
                solicitation = match.group(1)
                break
        
        # Clean title for description
        clean_title = title.replace(",", "").strip()[:50] if title else "UNKNOWN"
        
        # Build pipeline title
        pipeline_title = f"PN: {part_number} | Qty: {quantity} | Condition: {condition} | MDS: {mds} | {solicitation} | {clean_title}"
        
        return pipeline_title

    def classify_opportunity(self, opportunity: Dict, temperature: float = 0.1, bypass_regex: bool = False) -> Dict:
        """
        Classify opportunity and capture FULL model response
        
        Args:
            opportunity: Dict with opportunity data
            temperature: Model temperature
            bypass_regex: If True, skip regex and go straight to model
        """
        
        # Run regex assessment FIRST (unless bypassed)
        regex_result = self.regex_gate.assess_opportunity(opportunity)
        
        # Get document text
        document_text = opportunity.get('text', '') or opportunity.get('full_text', '') or opportunity.get('description', '')
        title = opportunity.get('title', '')
        
        # Generate pipeline title from document
        pipeline_title = self.extract_pipeline_title(document_text, title)
        
        # CRITICAL: If regex says NO-GO, don't waste model's time (unless bypassed)
        if regex_result.decision == Decision.NO_GO and not bypass_regex:
            return {
                "classification": "NO-GO",
                "reasoning": f"Regex knockout: {regex_result.primary_blocker}",
                "detailed_analysis": f"Hard knockout by regex pattern: {regex_result.primary_blocker}. Categories triggered: {', '.join(str(c) for c in regex_result.categories_triggered[:3])}",
                "full_model_response": "[Model not called - regex hard knockout]",
                "confidence": None,  # Regex doesn't calculate confidence
                "sos_pipeline_title": pipeline_title,
                "model_used": "REGEX_ONLY",
                "regex_decision": regex_result.decision.value,
                "regex_blocker": regex_result.primary_blocker
            }
        
        # Only send GO and FURTHER_ANALYSIS to the model
        # Format for model (matching training format)
        content = self._format_for_model(opportunity, regex_result)
        
        messages = [{"role": "user", "content": content}]
        
        try:
            # Call model - use SDK if available, otherwise HTTP
            if USING_SDK:
                # Use mistralai SDK
                if self.model_id.startswith('ag:'):
                    response = client.agents.complete(
                        agent_id=self.model_id,
                        messages=messages
                    )
                else:
                    response = client.chat.complete(
                        model=self.model_id,
                        messages=messages,
                        temperature=temperature
                    )
                
                # Capture FULL model response
                full_response = response.choices[0].message.content
            else:
                # Use direct HTTP fallback
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                
                # Build payload - agents use different endpoint
                if self.model_id.startswith('ag:'):
                    url = "https://api.mistral.ai/v1/agents/completions"
                    payload = {
                        "agent_id": self.model_id,
                        "messages": messages
                    }
                else:
                    url = API_URL
                    payload = {
                        "model": self.model_id,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": 2000
                    }
                
                # Make HTTP request
                http_response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if http_response.status_code != 200:
                    print(f"[ERROR] API returned status {http_response.status_code}")
                    raise Exception(f"API error: {http_response.status_code}")
                
                data = http_response.json()
                
                # Extract response content
                full_response = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            # Parse classification - handle JSON format
            classification = "FURTHER_ANALYSIS"
            
            # First try to parse as JSON (model often returns JSON)
            try:
                import json
                # Extract JSON from response
                json_str = full_response
                if "```json" in full_response:
                    json_str = full_response.split("```json")[1].split("```")[0].strip()
                elif "{" in full_response:
                    # Find JSON object
                    start = full_response.index("{")
                    end = full_response.rindex("}") + 1
                    json_str = full_response[start:end]
                
                parsed = json.loads(json_str)
                
                # Get result from JSON
                result_field = parsed.get("result", "").upper()
                if "NO-GO" in result_field or "NO_GO" in result_field:
                    classification = "NO-GO"
                elif "GO" in result_field and "NO" not in result_field:
                    classification = "GO"
                elif "INDETERMINATE" in result_field:
                    classification = "INDETERMINATE"
                elif "CONTACT" in result_field:
                    classification = "CONTACT_CO"
                    
            except:
                # Fallback to text parsing if JSON fails
                if "NO-GO" in full_response or "NO_GO" in full_response:
                    classification = "NO-GO"
                elif "INDETERMINATE" in full_response.upper():
                    classification = "INDETERMINATE"
                elif "GO" in full_response and "NO-GO" not in full_response:
                    classification = "GO"
                elif "CONTACT" in full_response.upper():
                    classification = "CONTACT_CO"
            
            # Extract short reasoning for CSV
            short_reasoning = ""
            
            # Try to get reasoning from parsed JSON first
            try:
                if 'parsed' in locals():
                    short_reasoning = parsed.get("rationale", "") or parsed.get("reasoning", "")
                    if not short_reasoning and "knock_out_reasons" in parsed:
                        reasons = parsed.get("knock_out_reasons", [])
                        if reasons:
                            short_reasoning = "; ".join(reasons)
            except:
                pass
            
            # Fallback to text extraction
            if not short_reasoning:
                if "Reason:" in full_response:
                    short_reasoning = full_response.split("Reason:")[1].split("\n")[0].strip()
                elif "PRIMARY BLOCKER:" in full_response:
                    short_reasoning = full_response.split("PRIMARY BLOCKER:")[1].split("\n")[0].strip()
                elif "This opportunity" in full_response:
                    for line in full_response.split('\n'):
                        if "This opportunity" in line:
                            short_reasoning = line.strip()
                            break
            
            if not short_reasoning:
                short_reasoning = f"Model decision: {classification}"
            
            # Extract detailed analysis (full reasoning)
            detailed_analysis = ""
            
            # Try to extract structured sections
            if "ANALYSIS:" in full_response:
                detailed_analysis = full_response.split("ANALYSIS:")[1].split("RECOMMENDATION:")[0].strip()
            elif "REASONING:" in full_response:
                detailed_analysis = full_response.split("REASONING:")[1].split("RECOMMENDATION:")[0].strip()
            elif "Decision:" in full_response and len(full_response) > 100:
                # Get everything after the decision line
                lines = full_response.split('\n')
                for i, line in enumerate(lines):
                    if "Decision:" in line and i < len(lines) - 1:
                        detailed_analysis = '\n'.join(lines[i+1:]).strip()
                        break
            
            # If no structured extraction worked, use the full response
            if not detailed_analysis:
                detailed_analysis = full_response
            
            # Clean up the detailed analysis
            detailed_analysis = detailed_analysis.replace('\n\n', '\n').strip()
            
            # Extract confidence ONLY if explicitly stated by model
            confidence = None
            if "Confidence:" in full_response:
                conf_match = re.search(r'Confidence[:\s]+(\d+)', full_response)
                if conf_match:
                    confidence = int(conf_match.group(1))
            
            # REMOVED: Don't override model decision
            # The model is already trained on military platforms
            # Let it make the decision based on full context
            
            # Build unified Agent schema output IN ORDER
            result = {
                # Core identification fields
                "solicitation_id": opp.get('solicitation_id', opp.get('source_id', '')),
                "solicitation_title": opp.get('title', ''),
                "summary": opp.get('ai_summary', opp.get('description_text', ''))[:500] if opp.get('ai_summary') or opp.get('description_text') else '',

                # Decision fields
                "result": classification,  # Changed from 'classification' to 'result'
                "knock_out_reasons": [],  # Extract from model response if available
                "exceptions": [],  # Extract from model response if available
                "special_action": "",  # Extract from model response if available
                "rationale": short_reasoning,  # Changed from 'reasoning' to 'rationale'
                "recommendation": "",  # Extract from model response if available

                # URL fields
                "sam_url": opp.get('source_path', ''),
                "hg_url": f"https://www.highergov.com/opportunity/{opp.get('opp_key', '')}" if opp.get('opp_key') else '',

                # Pipeline title
                "sos_pipeline_title": pipeline_title,

                # Additional fields for backward compatibility
                "detailed_analysis": detailed_analysis,  # Full model response
                "full_model_response": full_response,  # Complete raw response
                "confidence": confidence,
                "model_used": self.model_id,
                "regex_decision": regex_result.decision.value,
                "regex_blocker": regex_result.primary_blocker
            }

            # Try to extract structured fields from model response
            try:
                if 'parsed' in locals() and parsed:
                    # Extract knock_out_reasons if present
                    if 'knock_out_reasons' in parsed:
                        result['knock_out_reasons'] = parsed['knock_out_reasons']
                    # Extract exceptions if present
                    if 'exceptions' in parsed:
                        result['exceptions'] = parsed['exceptions']
                    # Extract special_action if present
                    if 'special_action' in parsed:
                        result['special_action'] = parsed['special_action']
                    # Extract recommendation if present
                    if 'recommendation' in parsed:
                        result['recommendation'] = parsed['recommendation']
            except:
                pass

            return result
            
        except Exception as e:
            # Fallback with full error context - use unified schema
            return {
                # Core identification fields
                "solicitation_id": opp.get('solicitation_id', opp.get('source_id', '')),
                "solicitation_title": opp.get('title', ''),
                "summary": opp.get('ai_summary', opp.get('description_text', ''))[:500] if opp.get('ai_summary') or opp.get('description_text') else '',

                # Decision fields
                "result": self._map_decision(regex_result.decision),
                "knock_out_reasons": [regex_result.primary_blocker] if regex_result.primary_blocker else [],
                "exceptions": [],
                "special_action": "",
                "rationale": f"Regex: {regex_result.primary_blocker or 'Pattern match'}",
                "recommendation": "Model API error - using regex fallback",

                # URL fields
                "sam_url": opp.get('source_path', ''),
                "hg_url": f"https://www.highergov.com/opportunity/{opp.get('opp_key', '')}" if opp.get('opp_key') else '',

                # Pipeline title
                "sos_pipeline_title": pipeline_title,

                # Additional fields for backward compatibility
                "detailed_analysis": f"Model API error: {str(e)}. Falling back to regex-based assessment.",
                "full_model_response": "",
                "confidence": 75,
                "model_used": "REGEX_FALLBACK",
                "error": str(e)
            }
    
    def _format_for_model(self, opp: Dict, regex_result) -> str:
        """Format in training style"""
        
        title = opp.get('title', 'N/A')
        agency = opp.get('agency', 'N/A')
        naics = opp.get('naics', 'N/A')
        psc = opp.get('psc', 'N/A')
        
        # Get FULL document text - model needs to see everything!
        document_text = opp.get('text', '') or opp.get('description', '')
        # Send up to 400K chars (about 100 pages) to model
        excerpt = document_text[:400000] if document_text else "No document content"
        
        # Match training format
        content = f"""Context: You are an expert assessment specialist for Source One Spares (SOS), a small organic supplier specializing in surplus military and aviation parts.

Question: Analyze this government contracting opportunity for Source One Spares:

Title: {title}
Agency: {agency}
NAICS: {naics}
PSC: {psc}

Requirements excerpt: {excerpt}"""
        
        return content
    
    def _map_decision(self, decision: Decision) -> str:
        """Map regex decision"""
        if decision == Decision.GO:
            return "GO"
        elif decision == Decision.NO_GO:
            return "NO-GO"
        elif decision == Decision.FURTHER_ANALYSIS:
            return "FURTHER_ANALYSIS"
        else:
            return "CONTACT_CO"

if __name__ == "__main__":
    print("Testing ULTIMATE Mistral Connector...")
    
    classifier = MistralSOSClassifier()
    
    # Test with sample opportunity
    test_opp = {
        'title': 'KC-46 Aircraft Component Repair',
        'agency': 'Air Force',
        'naics': '336413',
        'psc': '1680',
        'text': """
        SOLICITATION: SPRPA125QET76
        PART NUMBER: 2342154-2-1
        QUANTITY: 25 EACH
        REPAIR/OVERHAUL
        APPLICATION: KC-46 AIRCRAFT
        
        This is a requirement for repair services on KC-46 components.
        SOS has extensive experience with KC-46 platform.
        """
    }
    
    result = classifier.classify_opportunity(test_opp)
    
    print("\n" + "="*60)
    print("Classification:", result.get('classification'))
    print("Pipeline Title:", result.get('sos_pipeline_title'))
    print("\nShort Reasoning:", result.get('reasoning'))
    print("\nDetailed Analysis:")
    print(result.get('detailed_analysis', '')[:500])
    print("="*60)
