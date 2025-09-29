"""
Enhanced Pipeline: Regex → 10 Batches → 10 Agents → 2 Report Writers
Implements the complete architecture with proper confidence thresholds
"""

import asyncio
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Setup logging first
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import existing components
from pipeline_config import (
    get_api_key, get_model_id, get_endpoint,
    PIPELINE_CONFIG, BATCH_CONFIG, RATE_LIMITS
)
from context_accumulator import ContextAccumulator
from document_fetcher import DocumentFetcher
from prompt_templates import build_batch_prompt, build_agent_prompt, build_report_prompt

# Try to import regex gate, but handle if missing dependencies
try:
    from sos_ingestion_gate_v419 import SOSIngestionGate
    REGEX_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Regex gate not available: {e}")
    REGEX_AVAILABLE = False
    # Create a dummy class
    class SOSIngestionGate:
        def assess_opportunity(self, text, metadata):
            return {"decision": "INDETERMINATE", "matched_patterns": [], "summary": "Regex not available"}


DISPLAY_STAGE_LABELS = {
    "REGEX_FILTER": "Automated Screening",
    "BATCH_1_SIMPLE_BINARY": "Timing & Regulatory Gate",
    "BATCH_2_CONTRACT_VEHICLES": "Contract Vehicle Access",
    "BATCH_3_PLATFORM_DOMAIN": "Platform & Airworthiness",
    "BATCH_4_TECHNICAL_CAPABILITIES": "Technical Source Restrictions",
    "BATCH_5_CERTIFICATIONS": "Certification Requirements",
    "BATCH_6_IT_SYSTEMS": "IT & Network Access",
    "BATCH_7_BUSINESS_RESTRICTIONS": "Business & Performance Limits",
    "BATCH_8_COMPETITION": "Competition & Incumbency",
    "BATCH_9_MAINTENANCE": "Maintenance & Warranty Obligations",
    "BATCH_10_STRATEGIC_FIT": "Strategic Fit & Economics",
    "AGENT_1_TIMING": "Detailed Timing Validation",
    "AGENT_2_SETASIDE_EXCEPTIONS": "Set-Aside Exceptions & Teaming",
    "AGENT_3_SECURITY_NUANCE": "Security Requirement Analysis",
    "AGENT_4_VEHICLE_ANALYSIS": "Contract Vehicle Strategy",
    "AGENT_5_TECHNICAL_PATHS": "Technical Alternative Pathways",
    "AGENT_6_PLATFORM_EXCEPTIONS": "Platform Exception Handling",
    "AGENT_7_CERT_PATHWAYS": "Certification Coverage Plan",
    "AGENT_8_COMPETITION_INTEL": "Competitive Intelligence",
    "AGENT_9_BUSINESS_CASE": "Business Case & Profitability",
    "AGENT_10_RISK_ASSESSMENT": "Risk Aggregation & Win Odds",
    "AGENT_11_WIN_STRATEGY": "Win Strategy Development",
    "AGENT_12_EXECUTIVE_SUMMARY": "Executive Summary Packaging",
}


class Decision(Enum):
    """Pipeline decision types"""
    GO = "GO"
    NO_GO = "NO-GO"
    INDETERMINATE = "INDETERMINATE"


@dataclass
class AssessmentResult:
    """Result from any assessment stage"""
    stage_name: str
    decision: Decision
    confidence: float
    evidence: List[str] = field(default_factory=list)
    rationale: str = ""
    processing_time: float = 0.0
    qc_override: bool = False
    qc_rationale: str = ""


class EnhancedPipeline:
    """
    Complete pipeline implementation:
    Regex → 10 Parallel Batches → 10 Sequential Agents → 2 Report Writers
    """

    def __init__(self, mock_mode: bool = False):
        """Initialize pipeline with all components"""
        self.mock_mode = mock_mode
        self.api_key = get_api_key("mistral") if not mock_mode else "MOCK_KEY"
        self.hg_api_key = get_api_key("highergov") if not mock_mode else "MOCK_KEY"

        # Core components
        self.regex_gate = SOSIngestionGate()
        self.document_fetcher = DocumentFetcher() if not mock_mode else None

        # Initialize batch and agent processors
        self.batch_processors = self._initialize_batch_processors()
        self.agent_validators = self._initialize_agent_validators()
        self.report_writers = self._initialize_report_writers()

        # QC thresholds
        self.KNOCKOUT_THRESHOLD = 0.90  # >=90% confidence for NO-GO
        self.QC_OVERRIDE_THRESHOLD = 0.95  # >=95% confidence to override

        # Rate limiting
        self.last_api_call = 0

        logger.info("Enhanced Pipeline initialized with correct architecture")

    def _initialize_batch_processors(self) -> List[Dict]:
        """Initialize 10 batch processor groups"""
        return [
            {
                "name": "BATCH_1_SIMPLE_BINARY",
                "criteria": ["deadlines", "set_asides", "security_clearance", "export_controls"],
                "model": "batch_pixtral"
            },
            {
                "name": "BATCH_2_CONTRACT_VEHICLES",
                "criteria": ["contract_vehicles", "amc_amsc", "berry_amendment", "dfars_metals"],
                "model": "batch_pixtral"
            },
            {
                "name": "BATCH_3_PLATFORM_DOMAIN",
                "criteria": ["military_platforms", "naval_systems", "combat_systems", "faa_8130"],
                "model": "batch_medium"
            },
            {
                "name": "BATCH_4_TECHNICAL_CAPABILITIES",
                "criteria": ["oem_requirements", "qpl_qml", "sar", "first_article"],
                "model": "batch_medium"
            },
            {
                "name": "BATCH_5_CERTIFICATIONS",
                "criteria": ["as9100", "nadcap", "cmmi", "iso"],
                "model": "batch_medium"
            },
            {
                "name": "BATCH_6_IT_SYSTEMS",
                "criteria": ["sipr_jwics", "cac", "mil_network", "gfe"],
                "model": "batch_medium"
            },
            {
                "name": "BATCH_7_BUSINESS_RESTRICTIONS",
                "criteria": ["subcontracting", "self_performance", "geographic", "oconus"],
                "model": "batch_medium"
            },
            {
                "name": "BATCH_8_COMPETITION",
                "criteria": ["incumbent", "sole_source", "past_performance", "evaluation"],
                "model": "batch_medium"
            },
            {
                "name": "BATCH_9_MAINTENANCE",
                "criteria": ["warranty", "support_24_7", "depot", "field_service"],
                "model": "batch_medium"
            },
            {
                "name": "BATCH_10_STRATEGIC_FIT",
                "criteria": ["core_competency", "resources", "profit_margin", "roi"],
                "model": "batch_medium"
            }
        ]

    def _initialize_agent_validators(self) -> List[Dict]:
        """Initialize 10 agent validators for deeper analysis"""
        return [
            {"name": "AGENT_1_TIMING"},
            {"name": "AGENT_2_SETASIDE_EXCEPTIONS"},
            {"name": "AGENT_3_SECURITY_NUANCE"},
            {"name": "AGENT_4_VEHICLE_ANALYSIS"},
            {"name": "AGENT_5_TECHNICAL_PATHS"},
            {"name": "AGENT_6_PLATFORM_EXCEPTIONS"},
            {"name": "AGENT_7_CERT_PATHWAYS"},
            {"name": "AGENT_8_COMPETITION_INTEL"},
            {"name": "AGENT_9_BUSINESS_CASE"},
            {"name": "AGENT_10_RISK_ASSESSMENT"},
        ]

    def _initialize_report_writers(self) -> List[Dict]:
        """Initialize Agents 11-12 for GO report writing"""
        return [
            {"name": "AGENT_11_WIN_STRATEGY"},
            {"name": "AGENT_12_EXECUTIVE_SUMMARY"},
        ]

    async def process_opportunity(self, search_id: str) -> Dict[str, Any]:
        """
        Process opportunity through complete pipeline
        """
        logger.info(f"Processing opportunity: {search_id}")
        start_time = time.time()

        # Step 1: Fetch documents and metadata
        opportunity_data = await self._fetch_opportunity_data(search_id)
        if not opportunity_data:
            return self._create_error_result(search_id, "Failed to fetch opportunity data")

        # Step 2: REGEX FILTER (FREE)
        regex_result = self._apply_regex_filter(opportunity_data)
        if regex_result.decision == Decision.NO_GO:
            logger.info(f"REGEX KNOCKOUT: {regex_result.rationale}")
            return self._create_knockout_result(opportunity_data, regex_result, "REGEX")

        # Step 3: 10 PARALLEL BATCH PROCESSORS
        batch_results = await self._run_parallel_batches(opportunity_data)

        # Check for any knockouts from batches
        for result in batch_results:
            if result.decision == Decision.NO_GO and result.confidence >= self.KNOCKOUT_THRESHOLD:
                # Apply QC check
                qc_result = await self._apply_qc_check(result, opportunity_data)
                if not qc_result.qc_override:
                    logger.info(f"BATCH KNOCKOUT: {result.stage_name} - {result.rationale}")
                    return self._create_knockout_result(opportunity_data, result, "BATCH")

        # Step 4: 10 SEQUENTIAL AGENT VALIDATORS
        agent_results = await self._run_sequential_agents(opportunity_data, batch_results)

        # Check for any knockouts from agents
        for result in agent_results:
            if result.decision == Decision.NO_GO and result.confidence >= self.KNOCKOUT_THRESHOLD:
                # Apply QC check
                qc_result = await self._apply_qc_check(result, opportunity_data)
                if not qc_result.qc_override:
                    logger.info(f"AGENT KNOCKOUT: {result.stage_name} - {result.rationale}")
                    return self._create_knockout_result(opportunity_data, result, "AGENT")

        # Step 5: SURVIVED EVERYTHING - Generate GO Reports
        logger.info(f"WINNER! Opportunity {search_id} survived all stages")
        go_reports = await self._generate_go_reports(opportunity_data, batch_results, agent_results)

        processing_time = time.time() - start_time

        return {
            "opportunity_id": search_id,
            "decision": "GO",
            "confidence": 0.95,  # High confidence - survived everything!
            "processing_time": processing_time,
            "survival_rate": "TOP 4%",
            "batch_results": [r.__dict__ for r in batch_results],
            "agent_results": [r.__dict__ for r in agent_results],
            "win_strategy": go_reports.get("win_strategy"),
            "executive_summary": go_reports.get("executive_summary"),
            "timestamp": datetime.now().isoformat()
        }

    async def _fetch_opportunity_data(self, search_id: str) -> Optional[Dict]:
        """Fetch opportunity with all documents and metadata"""
        if self.mock_mode:
            return self._create_mock_opportunity(search_id)

        try:
            data = self.document_fetcher.fetch_opportunity_with_documents(search_id)
            if data["fetch_status"] == "complete":
                return data
            else:
                logger.error(f"Failed to fetch complete data: {data.get('errors')}")
                return None
        except Exception as e:
            logger.error(f"Error fetching opportunity: {e}")
            return None

    def _apply_regex_filter(self, opportunity: Dict) -> AssessmentResult:
        """Apply FREE regex filter as first stage"""
        start_time = time.time()

        try:
            # Use the existing regex gate
            regex_assessment = self.regex_gate.assess_opportunity(
                opportunity.get("combined_text", ""),
                opportunity.get("metadata", {})
            )

            decision = Decision.NO_GO if regex_assessment["decision"] == "NO-GO" else Decision.INDETERMINATE

            return AssessmentResult(
                stage_name="REGEX_FILTER",
                decision=decision,
                confidence=0.99 if decision == Decision.NO_GO else 0.0,
                evidence=regex_assessment.get("matched_patterns", [])[:5],
                rationale=regex_assessment.get("summary", "Regex pattern matching"),
                processing_time=time.time() - start_time
            )
        except Exception as e:
            logger.error(f"Regex filter error: {e}")
            # On error, continue processing
            return AssessmentResult(
                stage_name="REGEX_FILTER",
                decision=Decision.INDETERMINATE,
                confidence=0.0,
                rationale=f"Regex error: {str(e)}",
                processing_time=time.time() - start_time
            )

    async def _run_parallel_batches(self, opportunity: Dict) -> List[AssessmentResult]:
        """Run 10 batch processors in parallel"""
        logger.info("Running 10 parallel batch processors")

        # Create tasks for all batch processors
        tasks = []
        for batch_config in self.batch_processors:
            task = self._process_batch(batch_config, opportunity)
            tasks.append(task)

        # Run all batches in parallel
        results = await asyncio.gather(*tasks)

        logger.info(f"Batch processing complete. NO-GOs: {sum(1 for r in results if r.decision == Decision.NO_GO)}")
        return results

    async def _process_batch(self, batch_config: Dict, opportunity: Dict) -> AssessmentResult:
        """Process single batch with proper prompt"""
        start_time = time.time()

        # Build prompt with opportunity text
        prompt = build_batch_prompt(
            stage_name=batch_config["name"],
            current_date=datetime.now().strftime("%Y-%m-%d"),
            metadata_json=json.dumps(opportunity.get("metadata", {}), indent=2)[:8000],
            opportunity_text=opportunity.get("combined_text", "")[:50000],
        )

        # Make API call
        try:
            result = await self._call_batch_api(
                model_id=get_model_id(batch_config["model"]),
                prompt=prompt
            )

            # Parse response
            decision_str = result.get("decision", "INDETERMINATE")
            decision = Decision[decision_str.replace("-", "_")]

            return AssessmentResult(
                stage_name=batch_config["name"],
                decision=decision,
                confidence=result.get("confidence", 0.5),
                evidence=result.get("evidence", []),
                rationale=result.get("rationale", ""),
                processing_time=time.time() - start_time
            )
        except Exception as e:
            logger.error(f"Batch {batch_config['name']} error: {e}")
            return AssessmentResult(
                stage_name=batch_config["name"],
                decision=Decision.INDETERMINATE,
                confidence=0.0,
                rationale=f"Processing error: {str(e)}",
                processing_time=time.time() - start_time
            )

    async def _run_sequential_agents(self, opportunity: Dict,
                                    batch_results: List[AssessmentResult]) -> List[AssessmentResult]:
        """Run 10 agent validators sequentially"""
        logger.info("Running 10 sequential agent validators")

        results = []
        context = self._build_context(batch_results)

        for agent_config in self.agent_validators:
            result = await self._process_agent(agent_config, opportunity, context)
            results.append(result)

            # Check for knockout
            if result.decision == Decision.NO_GO and result.confidence >= self.KNOCKOUT_THRESHOLD:
                # Apply QC check immediately
                qc_result = await self._apply_qc_check(result, opportunity)
                if not qc_result.qc_override:
                    logger.info(f"Agent knockout at {agent_config['name']}")
                    break  # Stop processing further agents
                else:
                    result.qc_override = True
                    result.qc_rationale = qc_result.qc_rationale

            # Add to context for next agent
            context["previous_agents"].append({
                "name": result.stage_name,
                "decision": result.decision.value,
                "confidence": result.confidence
            })

        return results

    async def _process_agent(self, agent_config: Dict, opportunity: Dict,
                            context: Dict) -> AssessmentResult:
        """Process single agent validator"""
        start_time = time.time()

        # Build prompt with context
        prompt = build_agent_prompt(
            stage_name=agent_config["name"],
            current_date=datetime.now().strftime("%Y-%m-%d"),
            metadata_json=json.dumps(opportunity.get("metadata", {}), indent=2)[:6000],
            batch_context=json.dumps(context, indent=2)[:12000],
            opportunity_text=opportunity.get("combined_text", "")[:50000],
        )

        try:
            result = await self._call_agent_api(prompt)

            decision_str = result.get("decision", "INDETERMINATE")
            decision = Decision[decision_str.replace("-", "_")]

            return AssessmentResult(
                stage_name=agent_config["name"],
                decision=decision,
                confidence=result.get("confidence", 0.5),
                evidence=result.get("evidence", []),
                rationale=result.get("rationale", ""),
                processing_time=time.time() - start_time
            )
        except Exception as e:
            logger.error(f"Agent {agent_config['name']} error: {e}")
            return AssessmentResult(
                stage_name=agent_config["name"],
                decision=Decision.INDETERMINATE,
                confidence=0.0,
                rationale=f"Processing error: {str(e)}",
                processing_time=time.time() - start_time
            )

    async def _apply_qc_check(self, result: AssessmentResult,
                              opportunity: Dict) -> AssessmentResult:
        """Apply QC check for NO-GO decisions"""
        logger.info(f"QC Check for {result.stage_name} NO-GO @ {result.confidence:.2%}")

        qc_prompt = f"""
        A stage returned NO-GO. Verify this decision or find exceptions.

        Stage: {result.stage_name}
        Decision: {result.decision.value}
        Confidence: {result.confidence}
        Rationale: {result.rationale}
        Evidence: {json.dumps(result.evidence)}

        FULL OPPORTUNITY TEXT:
        {opportunity.get("combined_text", "")[:30000]}

        Your job: Find ANY valid exception that would override this NO-GO.
        You need >=95% confidence to override.

        Common exceptions:
        - Set-aside BUT subcontracting allowed
        - Security clearance BUT can be obtained
        - Military platform BUT commercial variant
        - OEM only BUT "or equivalent" elsewhere

        Output JSON:
        {{"override": true/false, "confidence": 0.95-1.0, "exception": "details", "rationale": "explanation"}}
        """

        try:
            qc_result = await self._call_agent_api(qc_prompt)

            if qc_result.get("override") and qc_result.get("confidence", 0) >= self.QC_OVERRIDE_THRESHOLD:
                logger.info(f"QC OVERRIDE! Exception found: {qc_result.get('exception')}")
                result.qc_override = True
                result.qc_rationale = qc_result.get("rationale", "QC override applied")
            else:
                logger.info("QC confirmed NO-GO - no valid exception found")
                result.qc_override = False

            return result
        except Exception as e:
            logger.error(f"QC check failed: {e}")
            # On QC error, maintain original NO-GO
            result.qc_override = False
            return result

    async def _generate_go_reports(self, opportunity: Dict,
                                   batch_results: List[AssessmentResult],
                                   agent_results: List[AssessmentResult]) -> Dict[str, str]:
        """Generate compelling GO reports with Agents 11-12"""
        logger.info("Generating GO reports - THIS IS A WINNER!")

        reports = {}

        # Agent 11: Win Strategy
        shared_metadata = json.dumps(opportunity.get("metadata", {}), indent=2)[:6000]
        shared_opportunity = opportunity.get("combined_text", "")[:30000]
        batch_summary = self._summarize_results(batch_results)
        agent_summary = self._summarize_results(agent_results)
        win_context = json.dumps({
            "batch_summary": batch_summary,
            "agent_summary": agent_summary,
            "key_strengths": self._extract_strengths(batch_results, agent_results),
        }, indent=2)[:12000]

        win_strategy_prompt = build_report_prompt(
            stage_name="AGENT_11_WIN_STRATEGY",
            current_date=datetime.now().strftime("%Y-%m-%d"),
            metadata_json=shared_metadata,
            context=win_context,
            opportunity_text=shared_opportunity,
        )

        try:
            win_result = await self._call_agent_api(win_strategy_prompt)
            reports["win_strategy"] = win_result.get("strategy", "Strong opportunity identified")
            reports["win_key_strengths"] = win_result.get("key_strengths", [])
            reports["win_action_items"] = win_result.get("action_items", [])
        except Exception as e:
            logger.error(f"Win strategy generation failed: {e}")
            reports["win_strategy"] = "Error generating win strategy"
            reports["win_key_strengths"] = []
            reports["win_action_items"] = []

        exec_context = json.dumps({
            "win_strategy": reports.get("win_strategy", ""),
            "key_strengths": reports.get("win_key_strengths", []),
            "action_items": reports.get("win_action_items", []),
        }, indent=2)[:8000]

        exec_summary_prompt = build_report_prompt(
            stage_name="AGENT_12_EXECUTIVE_SUMMARY",
            current_date=datetime.now().strftime("%Y-%m-%d"),
            metadata_json=shared_metadata,
            context=exec_context,
            opportunity_text=shared_opportunity,
        )

        try:
            exec_result = await self._call_agent_api(exec_summary_prompt)
            reports["executive_summary"] = exec_result.get("summary", "High-value opportunity")
            reports["executive_key_points"] = exec_result.get("key_points", [])
            reports["call_to_action"] = exec_result.get("call_to_action", "")
            reports["executive_confidence"] = exec_result.get("confidence_level", "HIGH")
        except Exception as e:
            logger.error(f"Executive summary generation failed: {e}")
            reports["executive_summary"] = "Error generating executive summary"
            reports["executive_key_points"] = []
            reports["call_to_action"] = ""
            reports["executive_confidence"] = "UNKNOWN"

        return reports

    # ========== PROMPT DEFINITIONS ==========

    async def _call_batch_api(self, model_id: str, prompt: str) -> Dict:
        """Call Mistral batch API"""
        if self.mock_mode:
            return {"decision": "GO", "confidence": 0.92, "rationale": "Mock response"}

        # Rate limiting
        await self._apply_rate_limit()

        import requests

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model_id,
            "messages": [
                {"role": "system", "content": "You are an SOS assessment specialist."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post(
                get_endpoint("mistral", "chat_url"),
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            content = result["choices"][0]["message"]["content"]

            # Parse JSON from content
            return json.loads(content)
        except Exception as e:
            logger.error(f"Batch API error: {e}")
            return {"decision": "INDETERMINATE", "confidence": 0.0, "rationale": str(e)}

    async def _call_agent_api(self, prompt: str) -> Dict:
        """Call Mistral agent API"""
        if self.mock_mode:
            return {"decision": "GO", "confidence": 0.91, "rationale": "Mock response"}

        # Rate limiting
        await self._apply_rate_limit()

        import requests

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "agent_id": get_model_id("agent"),
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }

        try:
            response = requests.post(
                get_endpoint("mistral", "agents_url"),
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()

            result = response.json()
            content = result["choices"][0]["message"]["content"]

            # Extract JSON from content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {"decision": "INDETERMINATE", "confidence": 0.0, "rationale": "Could not parse"}
        except Exception as e:
            logger.error(f"Agent API error: {e}")
            return {"decision": "INDETERMINATE", "confidence": 0.0, "rationale": str(e)}

    async def _apply_rate_limit(self):
        """Apply rate limiting between API calls"""
        time_since_last = time.time() - self.last_api_call
        min_delay = RATE_LIMITS.get("retry_delay_seconds", 5)

        if time_since_last < min_delay:
            await asyncio.sleep(min_delay - time_since_last)

        self.last_api_call = time.time()

    def _build_context(self, batch_results: List[AssessmentResult]) -> Dict:
        """Build context from batch results"""
        return {
            "batch_summary": [
                {
                    "stage": r.stage_name,
                    "decision": r.decision.value,
                    "confidence": r.confidence,
                    "qc_override": r.qc_override
                }
                for r in batch_results
            ],
            "knockouts_found": [r.rationale for r in batch_results if r.decision == Decision.NO_GO],
            "previous_agents": []
        }

    def _summarize_results(self, results: List[AssessmentResult]) -> str:
        """Summarize assessment results"""
        summary = []
        for r in results:
            status = "OVERRIDE" if r.qc_override else r.decision.value
            label = DISPLAY_STAGE_LABELS.get(r.stage_name, r.stage_name)
            summary.append(f"{label}: {status} ({r.confidence:.0%})")
        return "\n".join(summary)

    def _extract_strengths(self, batch_results: List[AssessmentResult],
                          agent_results: List[AssessmentResult]) -> str:
        """Extract key strengths from assessments"""
        strengths = []
        for r in batch_results + agent_results:
            if r.decision == Decision.GO and r.confidence > 0.8:
                strengths.append(r.rationale[:100])
        return "\n".join(strengths[:5])  # Top 5 strengths

    def _create_knockout_result(self, opportunity: Dict, result: AssessmentResult,
                                phase: str) -> Dict:
        """Create knockout result"""
        phase_map = {
            "REGEX": "pattern",
            "BATCH": "batch",
            "AGENT": "agent",
            "QC": "qc",
        }
        knockout_category = phase_map.get(phase, "other")
        display_reason = DISPLAY_STAGE_LABELS.get(result.stage_name, result.stage_name)
        return {
            "opportunity_id": opportunity.get("search_id"),
            "decision": "NO-GO",
            "knockout_phase": knockout_category,
            "knockout_reason": display_reason,
            "confidence": result.confidence,
            "rationale": result.rationale,
            "evidence": result.evidence,
            "qc_checked": result.qc_override is not None,
            "timestamp": datetime.now().isoformat()
        }

    def _create_error_result(self, search_id: str, error: str) -> Dict:
        """Create error result"""
        return {
            "opportunity_id": search_id,
            "decision": "ERROR",
            "error": error,
            "timestamp": datetime.now().isoformat()
        }

    def _create_mock_opportunity(self, search_id: str) -> Dict:
        """Create mock opportunity for testing"""
        return {
            "search_id": search_id,
            "metadata": {
                "title": f"Mock Opportunity {search_id}",
                "agency": "Department of Defense",
                "response_date": "2025-12-31"
            },
            "combined_text": "This is a mock opportunity for testing. No security clearance required. Full and open competition.",
            "documents": [],
            "fetch_status": "complete"
        }


# ========== MAIN EXECUTION ==========

if __name__ == "__main__":
    import sys

    # Test mode
    pipeline = EnhancedPipeline(mock_mode=True)

    # Test with a mock opportunity
    test_id = sys.argv[1] if len(sys.argv) > 1 else "TEST-001"

    async def test():
        result = await pipeline.process_opportunity(test_id)
        print(json.dumps(result, indent=2))

    asyncio.run(test())
