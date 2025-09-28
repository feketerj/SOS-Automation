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

# HARDCODED CONFIGURATION - CLIENT APP ONLY
api_key = "2oAquITdDMiyyk0OfQuJSSqePn3SQbde"  # Hardcoded Mistral API key for client

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
        """Initialize with hardcoded model"""
        # HARDCODED MODEL ID - CLIENT APP ONLY
        self.model_id = "ag:d42144c7:20250911:untitled-agent:15489fc1"  # Hardcoded production agent
        
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

            # First try to parse as JSON (agent should return JSON)
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

                # Get result from JSON - check 'decision' field first, then 'result'
                decision_field = parsed.get("decision", parsed.get("result", "")).upper()
                if "NO-GO" in decision_field or "NO_GO" in decision_field:
                    classification = "NO-GO"
                elif "GO" in decision_field and "NO" not in decision_field:
                    classification = "GO"
                elif "INDETERMINATE" in decision_field:
                    classification = "INDETERMINATE"
                elif "CONTACT" in decision_field:
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
                    if not short_reasoning and "knockout_logic" in parsed:
                        short_reasoning = parsed.get("knockout_logic", "")
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
            
            # Extract metadata if present
            metadata = opportunity.get('metadata', {})

            # Build result with EXACT schema
            solicitation_id = opportunity.get('solicitation_id', opportunity.get('source_id', metadata.get('source_id', '')))

            result = {
                # EXACT schema fields
                "HeaderLine": f"{classification}-{solicitation_id}",
                "SolicitationTitle": opportunity.get('title', metadata.get('title', '')),
                "SolicitationNumber": solicitation_id,
                "MDSPlatformCommercialDesignation": None,  # Will be populated from parsed response
                "TriageDate": datetime.now().strftime('%m-%d-%Y'),
                "DatePosted": metadata.get('posted_date', ''),
                "DateResponsesSubmissionsDue": metadata.get('due_date', ''),
                "DaysOpen": None,  # Will be calculated from parsed response
                "RemainingDays": None,  # Will be calculated from parsed response
                "PotentialAward": {
                    "Exceeds25K": None,
                    "Range": None
                },
                "FinalRecommendation": short_reasoning,
                "Scope": None,
                "KnockoutLogic": None,
                "SOSPipelineNotes": pipeline_title,  # Already formatted correctly
                "QuestionsForCO": [],

                # Backward compatibility fields (for existing code)
                "decision": classification,
                "result": classification,
                "rationale": short_reasoning,
                "sam_url": opportunity.get('source_path', metadata.get('source_path', '')),
                "hg_url": opportunity.get('highergov_url', metadata.get('path', f"https://www.highergov.com/opportunity/{metadata.get('source_id', '')}")),
                "sos_pipeline_title": pipeline_title,
                "detailed_analysis": detailed_analysis,
                "full_model_response": full_response,
                "model_used": self.model_id,
                "regex_decision": regex_result.decision.value,
                "regex_blocker": regex_result.primary_blocker
            }

            # Try to extract EXACT schema fields from model response
            try:
                if 'parsed' in locals() and parsed:
                    # Extract HeaderLine
                    if 'HeaderLine' in parsed:
                        result['HeaderLine'] = parsed['HeaderLine']

                    # Extract MDSPlatformCommercialDesignation
                    if 'MDSPlatformCommercialDesignation' in parsed:
                        result['MDSPlatformCommercialDesignation'] = parsed['MDSPlatformCommercialDesignation']

                    # Extract dates
                    if 'DatePosted' in parsed:
                        result['DatePosted'] = parsed['DatePosted']
                    if 'DateResponsesSubmissionsDue' in parsed:
                        result['DateResponsesSubmissionsDue'] = parsed['DateResponsesSubmissionsDue']
                    if 'DaysOpen' in parsed:
                        result['DaysOpen'] = parsed['DaysOpen']
                    if 'RemainingDays' in parsed:
                        result['RemainingDays'] = parsed['RemainingDays']

                    # Extract PotentialAward
                    if 'PotentialAward' in parsed and isinstance(parsed['PotentialAward'], dict):
                        result['PotentialAward'] = parsed['PotentialAward']

                    # Extract FinalRecommendation
                    if 'FinalRecommendation' in parsed:
                        result['FinalRecommendation'] = parsed['FinalRecommendation']
                        result['rationale'] = parsed['FinalRecommendation']  # Backward compat

                    # Extract Scope
                    if 'Scope' in parsed:
                        result['Scope'] = parsed['Scope']

                    # Extract KnockoutLogic
                    if 'KnockoutLogic' in parsed:
                        result['KnockoutLogic'] = parsed['KnockoutLogic']

                    # Extract SOSPipelineNotes
                    if 'SOSPipelineNotes' in parsed:
                        result['SOSPipelineNotes'] = parsed['SOSPipelineNotes']
                        result['sos_pipeline_title'] = parsed['SOSPipelineNotes']  # Backward compat

                    # Extract QuestionsForCO
                    if 'QuestionsForCO' in parsed:
                        result['QuestionsForCO'] = parsed['QuestionsForCO']

                    # Also handle snake_case versions for compatibility
                    if 'potential_award' in parsed and isinstance(parsed['potential_award'], dict):
                        result['PotentialAward'] = parsed['potential_award']
                    if 'final_recommendation' in parsed:
                        result['FinalRecommendation'] = parsed['final_recommendation']
                        result['rationale'] = parsed['final_recommendation']
                    if 'questions_for_co' in parsed:
                        result['QuestionsForCO'] = parsed['questions_for_co']
            except:
                pass

            return result
            
        except Exception as e:
            # Extract metadata if present
            metadata = opportunity.get('metadata', {})

            # Fallback with full error context - use unified schema
            return {
                # Core identification fields
                "solicitation_id": opportunity.get('solicitation_id', opportunity.get('source_id', metadata.get('source_id', ''))),
                "solicitation_title": opportunity.get('title', metadata.get('title', '')),
                "summary": (opportunity.get('ai_summary', '') or
                           opportunity.get('description_text', '') or
                           metadata.get('description_text', ''))[:500],

                # Decision fields
                "result": self._map_decision(regex_result.decision),
                "knock_out_reasons": [regex_result.primary_blocker] if regex_result.primary_blocker else [],
                "exceptions": [],
                "special_action": "",
                "rationale": f"Regex: {regex_result.primary_blocker or 'Pattern match'}",
                "recommendation": "Model API error - using regex fallback",

                # URL fields
                "sam_url": opportunity.get('source_path', metadata.get('source_path', '')),
                "hg_url": opportunity.get('highergov_url', metadata.get('path', f"https://www.highergov.com/opportunity/{metadata.get('source_id', '')}")),

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
        """Format in training style with ALL metadata"""

        # Extract metadata if present
        metadata = opp.get('metadata', {})

        # Primary fields
        title = opp.get('title', metadata.get('title', 'N/A'))
        agency = opp.get('agency', metadata.get('agency', metadata.get('issuing_agency', 'N/A')))

        # Contract details
        source_id = opp.get('source_id', metadata.get('source_id', 'N/A'))
        notice_type = metadata.get('notice_type', 'N/A')
        contract_type = metadata.get('contract_type', 'N/A')
        set_aside = metadata.get('set_aside', 'None')

        # Codes
        naics = opp.get('naics', metadata.get('naics_code', 'N/A'))
        psc = opp.get('psc', metadata.get('psc_code', 'N/A'))

        # Dates
        posted_date = metadata.get('posted_date', 'N/A')
        due_date = metadata.get('due_date', 'N/A')

        # Location
        pop_city = metadata.get('pop_city', '')
        pop_state = metadata.get('pop_state', '')
        pop_country = metadata.get('pop_country', '')
        place_of_performance = f"{pop_city}, {pop_state}, {pop_country}".strip(', ') if any([pop_city, pop_state, pop_country]) else 'N/A'

        # Get FULL document text - check all possible fields
        document_text = (opp.get('document_text', '') or
                        opp.get('text', '') or
                        opp.get('full_text', '') or
                        opp.get('description', '') or
                        metadata.get('description_text', ''))

        # Send up to 400K chars (about 100 pages) to model
        excerpt = document_text[:400000] if document_text else "No document content"

        # Match training format with enhanced metadata and JSON output requirement
        content = f"""Context: You are an expert assessment specialist for Source One Spares (SOS), a small organic supplier specializing in surplus military and aviation parts.

You must return your assessment as a JSON object using this EXACT schema:

{{
  "AssessmentHeaderLine": "[Go/No-Go]-{source_id}",
  "SolicitationTitle": "{title}",
  "SolicitationNumber": "{source_id}",
  "MDSPlatformCommercialDesignation": "[MDS/platform type, NA/Indeterminate, e.g., P-8 Poseidon | B737 | Commercial Item: Elevator (or) KC-46/B767 | Noncommercial: Refueling Boom (or) Indeterminate MDS | Commercial Item: AMSC Z Aircraft Tire]",
  "TriageDate": "{datetime.now().strftime('%m-%d-%Y')}",
  "DatePosted": "{posted_date}",
  "DateResponsesSubmissionsDue": "{due_date}",
  "DaysOpen": [calculate exact number of days between posted and due],
  "RemainingDays": [calculate exact number of days from today to due],
  "PotentialAward": {{
    "Exceeds25K": "Yes/No, with reasoning",
    "Range": "Inferred range with logic, e.g., $100K-$500K based on component complexity"
  }},
  "FinalRecommendation": "Go or No-Go, with complete explanation citing knockout criteria, exact government quotes, page numbers, etc.",
  "Scope": "Purchase, Manufacture, or Managed Repair with inference and concise proof",
  "KnockoutLogic": "Full assessment for all 20 categories: Category 1: [timing assessment]. Category 2: [domain assessment]. Category 3: [security assessment]. Category 4: [set-aside assessment]. Category 5: [source restrictions assessment]. Category 6: [technical data assessment]. Category 7: [export control assessment]. Category 8: [AMC/AMSC assessment]. Category 9: [SAR assessment]. Category 10: [platform assessment]. Category 11: [procurement assessment]. Category 12: [competition assessment]. Category 13: [subcontracting assessment]. Category 14: [contract vehicles assessment]. Category 15: [experimental/R&D assessment]. Category 16: [IT access assessment]. Category 17: [certifications assessment]. Category 18: [warranty/depot assessment]. Category 19: [CAD/CAM assessment]. Category 20: [scope assessment].",
  "SOSPipelineNotes": "PN: [part number or NA] | Qty: [quantity or NA] | Condition: [new/surplus/overhaul/refurb/NA] | MDS: [aircraft type or NA] | {source_id} | [brief description of work]",
  "QuestionsForCO": [
    "List relevant questions if any, otherwise empty array"
  ]
}}

Remember: You must make a final Go or No-Go decision. You cannot return Indeterminate.

Title: {title}
Solicitation ID: {source_id}
Agency: {agency}
Notice Type: {notice_type}
Contract Type: {contract_type}
Set-Aside: {set_aside}
NAICS Code: {naics}
PSC Code: {psc}
Place of Performance: {place_of_performance}
Posted Date: {posted_date}
Due Date: {due_date}

Requirements excerpt: {excerpt}"""

        return content
    
    def _map_decision(self, decision: Decision) -> str:
        """Map regex decision"""
        if decision == Decision.GO:
            return "Go"
        elif decision == Decision.NO_GO:
            return "No-Go"
        elif decision == Decision.FURTHER_ANALYSIS:
            return "Further Analysis"
        else:
            return "Contact CO"

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
