"""
QC Agents for Multi-Stage Pipeline
Provides quality control verification for NO-GO decisions and final GO verification
"""

import json
import logging
import requests
import time
from typing import Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum

# Import hardcoded configuration
from pipeline_config import get_api_key, get_model_id, get_endpoint, RATE_LIMITS, TIMEOUTS

logger = logging.getLogger(__name__)


class QCType(Enum):
    """Types of QC verification"""
    NO_GO_VERIFICATION = "NO_GO_VERIFICATION"
    GO_FINAL_CHECK = "GO_FINAL_CHECK"
    CONFIDENCE_BOOST = "CONFIDENCE_BOOST"


@dataclass
class QCResult:
    """Result from QC verification"""
    original_decision: str
    qc_decision: str
    qc_confidence: float
    override: bool
    rationale: str
    evidence: list


class QCAgent:
    """Quality Control Agent for pipeline decisions"""

    def __init__(self):
        """Initialize QC Agent with hardcoded configuration"""
        self.api_key = get_api_key("mistral")  # Hardcoded API key
        self.qc_model_id = get_model_id("qc_agent")  # Hardcoded QC agent ID
        self.qc_prompts = self._initialize_prompts()
        self.last_api_call = 0  # Rate limiting

    def _initialize_prompts(self) -> Dict[str, str]:
        """Initialize QC verification prompts"""
        return {
            "NO_GO_VERIFICATION": """You are a Quality Control agent verifying a NO-GO decision.

Original Stage: {stage_name}
Original Decision: {original_decision}
Original Confidence: {original_confidence}
Original Rationale: {original_rationale}

Context from previous stages:
{accumulated_context}

Your task:
1. Verify if the NO-GO decision is correct
2. Check for any exceptions that might override the knockout
3. Look for misinterpretations

Be skeptical. Common exceptions:
- FAA certifications might override military restrictions
- Commercial variants of military platforms may be acceptable
- AMSC codes Z/G/A override platform restrictions
- "Similar to" doesn't mean "is"

Output JSON:
{{"decision": "NO-GO|GO|INDETERMINATE", "confidence": 0.95, "override": boolean, "rationale": "explanation", "evidence": ["supporting quotes"]}}""",

            "GO_FINAL_CHECK": """You are the final Quality Control agent checking for any missed knockouts.

All stages passed with GO or INDETERMINATE.
Total stages processed: {stages_processed}

Full context:
{full_context}

Your task:
1. Look for ANY reason this should be NO-GO that was missed
2. Check for subtle knockouts
3. Verify no critical information was overlooked

Common missed knockouts:
- Buried set-aside statements
- Security requirements in attachments references
- Platform restrictions in part numbers
- Manufacturing requirements that imply OEM-only

Output JSON:
{{"decision": "GO|NO-GO", "confidence": 0.99, "missed_knockout": "type or null", "rationale": "explanation", "evidence": ["quotes if knockout found"]}}""",

            "CONFIDENCE_BOOST": """Review this assessment and provide confidence adjustment.

Stage: {stage_name}
Decision: {decision}
Current Confidence: {confidence}
Evidence: {evidence}

Provide refined confidence score based on evidence strength.

Output JSON:
{{"adjusted_confidence": 0.95, "rationale": "explanation of adjustment"}}"""
        }

    async def verify_no_go(self, stage_name: str, stage_result: Dict,
                           context: Dict, opportunity_text: str) -> QCResult:
        """Verify a NO-GO decision from a stage"""
        logger.info(f"QC Verification for NO-GO from {stage_name}")

        # Build prompt for verification
        prompt = self.qc_prompts["NO_GO_VERIFICATION"].format(
            stage_name=stage_name,
            original_decision=stage_result.get("decision"),
            original_confidence=stage_result.get("confidence"),
            original_rationale=stage_result.get("rationale"),
            accumulated_context=json.dumps(context, indent=2)[:2000]  # Truncate for prompt
        )

        # Make actual API call with hardcoded credentials
        qc_response = await self._call_qc_api(prompt)

        return QCResult(
            original_decision=stage_result.get("decision"),
            qc_decision=qc_response["decision"],
            qc_confidence=qc_response["confidence"],
            override=qc_response.get("override", False),
            rationale=qc_response["rationale"],
            evidence=qc_response.get("evidence", [])
        )

    async def final_go_check(self, all_results: list, context: Dict,
                            opportunity_text: str) -> Optional[QCResult]:
        """Final check for any missed knockouts before declaring GO"""
        logger.info("Running final GO verification check")

        # Build prompt for final check
        prompt = self.qc_prompts["GO_FINAL_CHECK"].format(
            stages_processed=len(all_results),
            full_context=json.dumps(context, indent=2)[:3000]  # More context for final check
        )

        # This would call actual Mistral API
        # For now, return None (no missed knockouts)
        return None

    def _mock_qc_verification(self, stage_name: str, stage_result: Dict) -> Dict:
        """Mock QC verification for testing"""
        # Simulate different QC responses based on stage
        if stage_name == "TIMING" and stage_result.get("deadline_found") is None:
            # Might override if no deadline found
            return {
                "decision": "INDETERMINATE",
                "confidence": 0.85,
                "override": True,
                "rationale": "No explicit deadline found - needs human review",
                "evidence": ["No deadline in text"]
            }

        # Default: agree with original decision
        return {
            "decision": stage_result.get("decision", "INDETERMINATE"),
            "confidence": stage_result.get("confidence", 0.90),
            "override": False,
            "rationale": "Original assessment confirmed",
            "evidence": stage_result.get("evidence", [])
        }

    def create_no_go_qc_prompt(self, stage_name: str, stage_result: Dict,
                              context: Dict) -> str:
        """Create prompt for NO-GO QC verification (for batch/agent API)"""
        return self.qc_prompts["NO_GO_VERIFICATION"].format(
            stage_name=stage_name,
            original_decision=stage_result.get("decision"),
            original_confidence=stage_result.get("confidence"),
            original_rationale=stage_result.get("rationale"),
            accumulated_context=json.dumps(context, indent=2)[:2000]
        )

    def create_final_go_prompt(self, all_results: list, context: Dict) -> str:
        """Create prompt for final GO check (for batch/agent API)"""
        return self.qc_prompts["GO_FINAL_CHECK"].format(
            stages_processed=len(all_results),
            full_context=json.dumps(context, indent=2)[:3000]
        )

    async def _call_qc_api(self, prompt: str) -> Dict:
        """Call Mistral API for QC verification with hardcoded credentials"""
        # Rate limiting
        time_since_last = time.time() - self.last_api_call
        if time_since_last < RATE_LIMITS["retry_delay_seconds"]:
            time.sleep(RATE_LIMITS["retry_delay_seconds"] - time_since_last)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "agent_id": self.qc_model_id,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.2  # Low temperature for consistency
        }

        url = get_endpoint("mistral", "agents_url")

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=TIMEOUTS["qc_api_call"]  # Use proper timeout
            )
            response.raise_for_status()
            self.last_api_call = time.time()

            # Extract JSON from response
            result = response.json()
            content = result["choices"][0]["message"]["content"]

            # Parse JSON from content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())

            # Fallback if can't parse
            return {
                "decision": "INDETERMINATE",
                "confidence": 0.5,
                "override": False,
                "rationale": "Could not parse QC response",
                "evidence": []
            }
        except Exception as e:
            logger.error(f"QC API call failed: {e}")
            # Return safe fallback on error
            return {
                "decision": "INDETERMINATE",
                "confidence": 0.0,
                "override": False,
                "rationale": f"QC API error: {str(e)}",
                "evidence": []
            }


class StageQCThresholds:
    """Confidence thresholds for QC override by stage type"""

    # Confidence needed to override NO-GO by stage type
    OVERRIDE_THRESHOLDS = {
        "BINARY": 0.98,      # Very high confidence needed to override binary stages
        "TECHNICAL": 0.95,   # High confidence for technical stages
        "BUSINESS": 0.90     # Moderate confidence for business judgment stages
    }

    # Confidence adjustment factors
    EVIDENCE_QUALITY = {
        "STRONG": 1.0,       # Clear, unambiguous evidence
        "MODERATE": 0.95,    # Good evidence but some interpretation
        "WEAK": 0.85        # Limited or indirect evidence
    }

    @classmethod
    def can_override(cls, stage_type: str, qc_confidence: float) -> bool:
        """Determine if QC confidence is sufficient to override"""
        threshold = cls.OVERRIDE_THRESHOLDS.get(stage_type, 0.95)
        return qc_confidence >= threshold


if __name__ == "__main__":
    # Test QC Agent
    import asyncio

    qc = QCAgent()

    # Test NO-GO verification
    test_stage_result = {
        "decision": "NO-GO",
        "confidence": 0.99,
        "rationale": "Found 8(a) set-aside",
        "evidence": ["This is an 8(a) set-aside"]
    }

    test_context = {
        "opportunity_id": "TEST-001",
        "summary": "Test opportunity",
        "decisions_made": []
    }

    async def test():
        result = await qc.verify_no_go(
            "SET-ASIDES",
            test_stage_result,
            test_context,
            "Test opportunity text with 8(a) set-aside"
        )
        print(f"QC Result: Override={result.override}, Decision={result.qc_decision}")

    asyncio.run(test())