"""
Multi-Stage Pipeline Orchestrator
Implements 20-stage cascade pipeline for SOS assessment
Each stage has paired Batch/Agent processors with early termination
"""

import asyncio
import json
import logging
import os
import time
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

# Import hardcoded configuration
from pipeline_config import (
    get_api_key, get_model_id, get_stage_model, get_endpoint,
    PIPELINE_CONFIG, BATCH_CONFIG, RATE_LIMITS, TIMEOUTS
)
from context_accumulator import ContextAccumulator
from qc_agents import QCAgent
from document_fetcher import DocumentFetcher

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Decision(Enum):
    """Pipeline decision types"""
    GO = "GO"
    NO_GO = "NO-GO"
    INDETERMINATE = "INDETERMINATE"


class StageType(Enum):
    """Stage complexity categories"""
    BINARY = "BINARY"  # Simple text matching, 99% confidence
    TECHNICAL = "TECHNICAL"  # Context required, 95% confidence
    BUSINESS = "BUSINESS"  # Judgment required, 85% confidence


@dataclass
class StageResult:
    """Result from a single stage assessment"""
    stage_name: str
    decision: Decision
    confidence: float
    evidence: List[str] = field(default_factory=list)
    rationale: str = ""
    processing_time: float = 0.0
    qc_verified: bool = False
    qc_override: Optional[Decision] = None


@dataclass
class Stage:
    """Base class for pipeline stages"""
    name: str
    stage_number: int
    stage_type: StageType
    batch_prompt: str
    agent_prompt: str
    confidence_threshold: float
    qc_threshold: float  # Confidence needed to override

    def get_prompt_with_context(self, context: Dict[str, Any], is_batch: bool = True) -> str:
        """Build prompt with accumulated context"""
        prompt = self.batch_prompt if is_batch else self.agent_prompt

        # Replace context placeholders
        prompt = prompt.replace("{context.summary}", context.get("summary", ""))
        prompt = prompt.replace("{current_date}", datetime.now().strftime("%Y-%m-%d"))
        prompt = prompt.replace("{opportunity_text}", context.get("opportunity_text", ""))

        return prompt

    def requires_qc(self, result: StageResult) -> bool:
        """Determine if QC verification is needed"""
        # NO-GO always gets QC'd
        if result.decision == Decision.NO_GO:
            return True

        # Low confidence gets QC'd
        if result.confidence < self.confidence_threshold:
            return True

        return False


class MultiStagePipeline:
    """Orchestrates the 20-stage cascade pipeline"""

    def __init__(self, mock_mode: bool = False):
        """Initialize pipeline with hardcoded configuration

        Args:
            mock_mode: If True, use mock responses instead of real API calls
        """
        self.mock_mode = mock_mode
        self.api_key = get_api_key("mistral") if not mock_mode else "MOCK_KEY"
        self.hg_api_key = get_api_key("highergov") if not mock_mode else "MOCK_KEY"
        self.stages: List[Stage] = []
        self.qc_agent = QCAgent()
        self.document_fetcher = DocumentFetcher() if not mock_mode else None
        self.results: List[StageResult] = []
        self.last_api_call = 0  # Rate limiting

        # Initialize all 20 stages
        self._initialize_stages()

        if mock_mode:
            logger.info("Pipeline initialized in MOCK MODE - no real API calls will be made")

    def _initialize_stages(self):
        """Set up all 20 stages in optimized order"""
        # Binary stages (1-7) - 99% confidence
        self.stages.extend([
            self._create_timing_stage(),
            self._create_set_asides_stage(),
            self._create_security_stage(),
            self._create_non_standard_stage(),
            self._create_contract_vehicle_stage(),
            self._create_export_control_stage(),
            self._create_amc_amsc_stage(),
        ])

        # Technical stages (8-14) - 95% confidence
        self.stages.extend([
            self._create_source_restrictions_stage(),
            self._create_sar_stage(),
            self._create_platform_stage(),
            self._create_domain_stage(),
            self._create_technical_data_stage(),
            self._create_it_systems_stage(),
            self._create_certifications_stage(),
        ])

        # Business stages (15-20) - 85% confidence
        self.stages.extend([
            self._create_subcontracting_stage(),
            self._create_procurement_restrictions_stage(),
            self._create_competition_stage(),
            self._create_maintenance_stage(),
            self._create_cad_cam_stage(),
            self._create_scope_stage(),
        ])

    def _create_timing_stage(self) -> Stage:
        """Stage 1: Check if opportunity has expired"""
        return Stage(
            name="TIMING",
            stage_number=1,
            stage_type=StageType.BINARY,
            batch_prompt="""Check if the opportunity deadline has passed.
Today's date: {current_date}
Look for: Response due date, submission deadline, closing date/time.
If deadline has passed = NO-GO
If deadline is future = GO
If no deadline found = GO (flag it)

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO", "confidence": 0.99, "deadline_found": "date", "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: timing_check]",
            confidence_threshold=0.99,
            qc_threshold=0.98
        )

    def _create_set_asides_stage(self) -> Stage:
        """Stage 2: Check for small business set-asides"""
        return Stage(
            name="SET-ASIDES",
            stage_number=2,
            stage_type=StageType.BINARY,
            batch_prompt="""Check for small business set-asides.
Previous findings: {context.summary}

Look for EXACT matches:
- "8(a)" or "8a set-aside"
- "SDVOSB" or "Service-Disabled Veteran-Owned"
- "WOSB" or "Women-Owned Small Business"
- "HUBZone"
- "Total Small Business Set-Aside"
- "Small Business Set-Aside"

If ANY found = NO-GO
If NONE found = GO

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO", "confidence": 0.99, "set_aside_type": "type or null", "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: set_aside_check]",
            confidence_threshold=0.99,
            qc_threshold=0.98
        )

    def _create_security_stage(self) -> Stage:
        """Stage 3: Check for security clearance requirements"""
        return Stage(
            name="SECURITY",
            stage_number=3,
            stage_type=StageType.BINARY,
            batch_prompt="""Check for security clearance requirements.
Previous findings: {context.summary}

Look for keywords:
- "Secret", "Top Secret", "TS/SCI", "Classified"
- "Security Clearance Required"
- "Facility Clearance"
- "DD-254"
- "NISPOM"
- "SAP" (Special Access Program)

If ANY found = NO-GO
If NONE found = GO

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO", "confidence": 0.99, "clearance_level": "level or null", "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: security_check]",
            confidence_threshold=0.99,
            qc_threshold=0.98
        )

    # Placeholder methods for remaining stages
    def _create_non_standard_stage(self) -> Stage:
        """Stage 4: Check for non-standard acquisition methods"""
        return Stage(
            name="NON-STANDARD",
            stage_number=4,
            stage_type=StageType.BINARY,
            batch_prompt="""Check for non-standard acquisition methods.
Previous findings: {context.summary}

Look for:
- "Other Transaction Authority" or "OTA"
- "SBIR" or "Small Business Innovation Research"
- "STTR" or "Small Business Technology Transfer"
- "BAA" or "Broad Agency Announcement"
- "Prize Competition"
- "Challenge.gov"
- "Cooperative Agreement"

If ANY found = NO-GO (special acquisition path)
If NONE found = GO

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO", "confidence": 0.99, "acquisition_type": "type or null", "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: non_standard_check]",
            confidence_threshold=0.99,
            qc_threshold=0.98
        )

    def _create_contract_vehicle_stage(self) -> Stage:
        """Stage 5: Check for restricted contract vehicles"""
        return Stage(
            name="CONTRACT-VEHICLE",
            stage_number=5,
            stage_type=StageType.BINARY,
            batch_prompt="""Check for restricted contract vehicles.
Previous findings: {context.summary}

Look for specific restricted vehicles:
- "GSA Schedule" or "Federal Supply Schedule" (if not on schedule)
- "SEWP" or "Solutions for Enterprise-Wide Procurement"
- "CIO-SP3" or "CIO-SP4"
- "GWAC" or "Government-Wide Acquisition Contract"
- Named IDIQs you're not on: "DEOS", "ENCORE", "NETCENTS"
- "BPA Call" or "Blanket Purchase Agreement" (if not a holder)

If ANY found and you're not on vehicle = NO-GO
If open competition or unrestricted = GO

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO", "confidence": 0.99, "vehicle": "vehicle name or null", "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: contract_vehicle_check]",
            confidence_threshold=0.99,
            qc_threshold=0.98
        )

    def _create_export_control_stage(self) -> Stage:
        """Stage 6: Check for export control restrictions"""
        return Stage(
            name="EXPORT-CONTROL",
            stage_number=6,
            stage_type=StageType.BINARY,
            batch_prompt="""Check for export control restrictions.
Previous findings: {context.summary}

Look for keywords:
- "ITAR" or "International Traffic in Arms Regulations"
- "EAR" or "Export Administration Regulations"
- "Export License Required"
- "Technology Transfer"
- "Foreign Person Restrictions"
- "US Persons Only"
- "No Foreign Nationals"
- "USML" or "US Munitions List"

If ANY found = NO-GO
If NONE found = GO

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO", "confidence": 0.99, "export_control": "type or null", "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: export_control_check]",
            confidence_threshold=0.99,
            qc_threshold=0.98
        )

    def _create_amc_amsc_stage(self) -> Stage:
        """Stage 7: Check for AMC/AMSC codes"""
        return Stage(
            name="AMC-AMSC",
            stage_number=7,
            stage_type=StageType.BINARY,
            batch_prompt="""Check for AMC/AMSC acquisition codes.
Previous findings: {context.summary}

Look for specific codes that indicate military-only:
- AMC codes: B, C, D, F, H, J, K, L, M, P, Q, R, T, U, V, W, X, Y
- Special attention to: X (drawings), Y (spec control), D (DoD only)
- EXCEPTION: Codes Z, G, A = GO (commercial equivalents OK)

If restricted AMC/AMSC found (not Z/G/A) = NO-GO
If Z, G, or A codes = GO
If no AMC/AMSC codes = GO

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO", "confidence": 0.99, "amc_code": "code or null", "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: amc_amsc_check]",
            confidence_threshold=0.99,
            qc_threshold=0.98
        )

    def _create_source_restrictions_stage(self) -> Stage:
        """Stage 8: Check for OEM/QPL/sole source restrictions"""
        return Stage(
            name="SOURCE-RESTRICTIONS",
            stage_number=8,
            stage_type=StageType.TECHNICAL,
            batch_prompt="""Check for source restrictions.
Previous findings: {context.summary}

Look for:
- "OEM only" or "Original Equipment Manufacturer"
- "QPL" or "Qualified Products List"
- "QML" or "Qualified Manufacturers List"
- "Sole source" or "Brand name or equal"
- "No substitutes" or "exact replacement"
- Specific part numbers without "or equivalent"
- "Proprietary" or "Patent holder only"

Consider context - some OEM requirements are acceptable for commercial items.

If hard OEM/QPL requirement = NO-GO
If "or equivalent" allowed = GO
If commercial off-the-shelf = GO

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO|INDETERMINATE", "confidence": 0.0-1.0, "restriction_type": "type or null", "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: source_restrictions_check]",
            confidence_threshold=0.95,
            qc_threshold=0.95
        )

    def _create_sar_stage(self) -> Stage:
        """Stage 9: Check for Source Approval Request requirements"""
        return Stage(
            name="SAR",
            stage_number=9,
            stage_type=StageType.TECHNICAL,
            batch_prompt="""Check for Source Approval Request (SAR) requirements.
Previous findings: {context.summary}

Look for:
- "SAR" or "Source Approval Request"
- "ESA" or "Engineering Support Activity"
- "First Article Test" or "FAT"
- "Qualification Testing Required"
- "Source qualification"
- "Must be approved source"
- "New sources must qualify"

Consider if you're already qualified or have time to qualify.

If SAR required and not qualified = NO-GO
If already approved source = GO
If qualification possible in timeline = INDETERMINATE

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO|INDETERMINATE", "confidence": 0.0-1.0, "sar_required": true/false, "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: sar_check]",
            confidence_threshold=0.95,
            qc_threshold=0.95
        )

    def _create_platform_stage(self) -> Stage:
        """Stage 10: Check for military platform restrictions"""
        return Stage(
            name="PLATFORM",
            stage_number=10,
            stage_type=StageType.TECHNICAL,
            batch_prompt="""Check what platform/system this is for.
Previous findings: {context.summary}

Classify platform:
- Pure military: F-16, F-35, Apache, Abrams, Bradley = NO-GO
- Commercial derivative: P-8 (737), KC-46 (767), C-40 (737) = GO
- Dual use: C-130, UH-60 (check context)
- Pure commercial: Boeing 737, Airbus, Cessna = GO
- Ground vehicles: HMMWV, JLTV = typically NO-GO
- Ships: DDG, LCS, CVN = NO-GO

Consider FAA 8130 exceptions for Navy commercial platforms.

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO|INDETERMINATE", "confidence": 0.0-1.0, "platform": "identified platform", "platform_type": "military/commercial/dual", "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: platform_check]",
            confidence_threshold=0.95,
            qc_threshold=0.95
        )

    def _create_domain_stage(self) -> Stage:
        """Stage 11: Check aviation/space/maritime domain"""
        return Stage(
            name="DOMAIN",
            stage_number=11,
            stage_type=StageType.TECHNICAL,
            batch_prompt="""Check the domain and assess capabilities.
Previous findings: {context.summary}

Domain classification:
- Commercial aviation: Airlines, business jets = GO
- Military aviation: Combat aircraft, weapons = NO-GO
- Space: Satellites, launch (check ITAR)
- Maritime: Naval combat systems = NO-GO
- Maritime: Commercial shipping = GO
- Ground: Tactical vehicles = typically NO-GO
- Cyber/IT: Check classification levels

Consider your domain expertise and certifications.

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO|INDETERMINATE", "confidence": 0.0-1.0, "domain": "identified domain", "capability_match": true/false, "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: domain_check]",
            confidence_threshold=0.95,
            qc_threshold=0.95
        )

    def _create_technical_data_stage(self) -> Stage:
        """Stage 12: Check for technical data rights"""
        return Stage(
            name="TECHNICAL-DATA",
            stage_number=12,
            stage_type=StageType.TECHNICAL,
            batch_prompt="""Check for technical data and IP rights issues.
Previous findings: {context.summary}

Look for:
- "Government Purpose Rights" or "GPR"
- "Limited Rights" or "Restricted Rights"
- "Unlimited Rights required"
- "Technical Data Package" or "TDP"
- "Proprietary data"
- "Background IP"
- "SBIR Data Rights"
- "Commercial license terms"

If requires surrendering IP = NO-GO
If standard commercial terms = GO
If negotiable = INDETERMINATE

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO|INDETERMINATE", "confidence": 0.0-1.0, "data_rights": "type or null", "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: technical_data_check]",
            confidence_threshold=0.95,
            qc_threshold=0.95
        )

    def _create_it_systems_stage(self) -> Stage:
        """Stage 13: Check for IT systems access requirements"""
        return Stage(
            name="IT-SYSTEMS",
            stage_number=13,
            stage_type=StageType.TECHNICAL,
            batch_prompt="""Check for IT systems access requirements.
Previous findings: {context.summary}

Look for:
- "CAC" or "Common Access Card"
- "SIPR" or "SIPRNet" or "JWICS"
- ".mil network access"
- "DISA approved"
- "JEDMICS" or "cFolders"
- "Government Furnished Equipment"
- "VPN" to classified networks
- Specific military IT systems

If classified network access required = NO-GO
If standard internet/commercial systems = GO
If CAC-only for unclassified = INDETERMINATE

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO|INDETERMINATE", "confidence": 0.0-1.0, "systems_required": ["list"], "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: it_systems_check]",
            confidence_threshold=0.95,
            qc_threshold=0.95
        )

    def _create_certifications_stage(self) -> Stage:
        """Stage 14: Check for unique certification requirements"""
        return Stage(
            name="CERTIFICATIONS",
            stage_number=14,
            stage_type=StageType.TECHNICAL,
            batch_prompt="""Check for special certification requirements.
Previous findings: {context.summary}

Look for:
- "AS9100" or "AS9110" or "AS9120" (aerospace)
- "NADCAP" (special processes)
- "ISO 9001" (general quality)
- "CMMI" level requirements
- "DCMA" or "DCAA" approved
- "Cyber Essentials" or "CMMC"
- Agency-specific certifications
- Special process certifications

If you have required certs = GO
If obtainable in timeline = INDETERMINATE
If impossible to obtain = NO-GO

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO|INDETERMINATE", "confidence": 0.0-1.0, "certifications": ["list"], "have_certs": true/false, "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: certifications_check]",
            confidence_threshold=0.95,
            qc_threshold=0.95
        )

    def _create_subcontracting_stage(self) -> Stage:
        """Stage 15: Check for subcontracting restrictions"""
        return Stage(
            name="SUBCONTRACTING",
            stage_number=15,
            stage_type=StageType.BUSINESS,
            batch_prompt="""Check for subcontracting restrictions.
Previous findings: {context.summary}

Look for:
- "No subcontracting" or "Subcontracting prohibited"
- "Prime contractor only"
- "Limitations on Subcontracting" clause
- Percentage limits (e.g., "51% self-performed")
- "Key personnel" requirements
- Teaming restrictions

Consider your self-performance capabilities.

If can self-perform requirements = GO
If need partners but allowed = GO
If prohibited and can't self-perform = NO-GO

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO|INDETERMINATE", "confidence": 0.0-1.0, "subcontracting_allowed": true/false, "self_performance_pct": "percent if specified", "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: subcontracting_check]",
            confidence_threshold=0.85,
            qc_threshold=0.90
        )

    def _create_procurement_restrictions_stage(self) -> Stage:
        """Stage 16: Check for procurement restrictions"""
        return Stage(
            name="PROCUREMENT",
            stage_number=16,
            stage_type=StageType.BUSINESS,
            batch_prompt="""Check for procurement restrictions.
Previous findings: {context.summary}

Look for:
- "Buy American Act" or "BAA"
- "Berry Amendment" (textiles)
- "DFARS specialty metals"
- Country of origin restrictions
- "Trade Agreements Act" or "TAA"
- Prohibited sources or countries
- "Domestic end product"

Consider your supply chain compliance.

If can meet requirements = GO
If restrictions manageable = INDETERMINATE
If impossible to comply = NO-GO

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO|INDETERMINATE", "confidence": 0.0-1.0, "procurement_restrictions": ["list"], "compliance_possible": true/false, "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: procurement_restrictions_check]",
            confidence_threshold=0.85,
            qc_threshold=0.90
        )

    def _create_competition_stage(self) -> Stage:
        """Stage 17: Check competition status and incumbency"""
        return Stage(
            name="COMPETITION",
            stage_number=17,
            stage_type=StageType.BUSINESS,
            batch_prompt="""Assess competition and incumbency factors.
Previous findings: {context.summary}

Look for:
- "Sole source" justification
- "Incumbent contractor" mentioned
- "Follow-on" or "Bridge contract"
- "Recompete" or "Full and open"
- Number of anticipated awards
- Past performance requirements
- Incumbent advantages mentioned

Assess competitive position.

If strong competitive position = GO
If moderate chance = INDETERMINATE
If clearly wired for incumbent = NO-GO

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO|INDETERMINATE", "confidence": 0.0-1.0, "competition_type": "full/limited/sole", "incumbent": "name if known", "competitive_position": "strong/moderate/weak", "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: competition_check]",
            confidence_threshold=0.85,
            qc_threshold=0.90
        )

    def _create_maintenance_stage(self) -> Stage:
        """Stage 18: Check maintenance and warranty requirements"""
        return Stage(
            name="MAINTENANCE",
            stage_number=18,
            stage_type=StageType.BUSINESS,
            batch_prompt="""Check maintenance and warranty requirements.
Previous findings: {context.summary}

Look for:
- Extended warranty periods (>1 year)
- On-site maintenance requirements
- 24/7 support requirements
- Geographic coverage (OCONUS)
- Response time SLAs
- Depot-level maintenance
- Field service representatives
- Spare parts provisioning

Assess capability to support.

If can fully support = GO
If need partner/development = INDETERMINATE
If cannot support = NO-GO

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO|INDETERMINATE", "confidence": 0.0-1.0, "warranty_period": "duration", "maintenance_type": "type", "geographic_scope": "scope", "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: maintenance_check]",
            confidence_threshold=0.85,
            qc_threshold=0.90
        )

    def _create_cad_cam_stage(self) -> Stage:
        """Stage 19: Check CAD/CAM and technical format requirements"""
        return Stage(
            name="CAD-CAM",
            stage_number=19,
            stage_type=StageType.BUSINESS,
            batch_prompt="""Check CAD/CAM and technical format requirements.
Previous findings: {context.summary}

Look for:
- Specific CAD software (CATIA, NX, SolidWorks)
- File format requirements (STEP, IGES, native)
- Model-based definition (MBD)
- Configuration management tools
- PDM/PLM system access
- Drawing standards (ASME Y14.5)
- 3D model requirements
- Technical data formats

Assess technical capabilities.

If have required tools/skills = GO
If can acquire/convert = INDETERMINATE
If incompatible systems = NO-GO

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO|INDETERMINATE", "confidence": 0.0-1.0, "cad_requirements": ["list"], "formats_required": ["list"], "capability_match": true/false, "evidence": ["quotes"], "rationale": "explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: cad_cam_check]",
            confidence_threshold=0.85,
            qc_threshold=0.90
        )

    def _create_scope_stage(self) -> Stage:
        """Stage 20: Final scope and capability assessment"""
        return Stage(
            name="SCOPE",
            stage_number=20,
            stage_type=StageType.BUSINESS,
            batch_prompt="""Final assessment of scope alignment and capability.
Previous findings: {context.summary}

Consider:
- Core competency alignment
- Resource availability
- Profit margin potential
- Risk/reward balance
- Strategic value
- Competition assessment
- Overall probability of win
- ROI on bid investment

Make final GO/NO-GO recommendation.

If strong fit and winnable = GO
If marginal but worth exploring = INDETERMINATE
If poor fit or unwinnable = NO-GO

Opportunity text:
{opportunity_text}

Output JSON:
{"decision": "GO|NO-GO|INDETERMINATE", "confidence": 0.0-1.0, "win_probability": "high/medium/low", "strategic_fit": "strong/moderate/weak", "key_risks": ["list"], "rationale": "comprehensive explanation"}""",
            agent_prompt="[AGENT_PLACEHOLDER: scope_check]",
            confidence_threshold=0.85,
            qc_threshold=0.90
        )

    async def process_opportunity_with_documents(self, search_id: str) -> Dict[str, Any]:
        """
        Process opportunity with FULL document fetching
        ALWAYS pulls documents if they exist, ALWAYS forwards metadata
        """
        logger.info(f"Processing opportunity with documents: {search_id}")
        start_time = time.time()

        if self.mock_mode:
            # In mock mode, create fake opportunity data
            logger.info("MOCK MODE: Creating simulated opportunity data")
            opportunity_data = self._create_mock_opportunity(search_id)
        else:
            # Step 1: ALWAYS fetch documents and metadata first
            logger.info("Fetching documents and metadata...")
            opportunity_data = self.document_fetcher.fetch_opportunity_with_documents(search_id)

            if opportunity_data["fetch_status"] == "error":
                logger.error(f"Failed to fetch opportunity data: {opportunity_data['errors']}")
                return {
                    "opportunity_id": search_id,
                    "final_decision": "INDETERMINATE",
                    "error": "Failed to fetch opportunity data",
                    "errors": opportunity_data["errors"]
                }

        # Log document stats
        logger.info(f"Fetched {len(opportunity_data['documents'])} documents, "
                   f"{len(opportunity_data['combined_text'])} total characters")

        # Step 2: Process through pipeline with full context
        return await self.process_opportunity(opportunity_data)

    async def process_opportunity(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Process opportunity through all stages with early termination"""
        opportunity_id = opportunity.get('search_id') or opportunity.get('id', 'unknown')
        logger.info(f"Processing opportunity: {opportunity_id}")

        # Initialize context accumulator with FULL data including docs
        context = ContextAccumulator(opportunity)
        self.results = []

        # Process through stages sequentially
        for stage in self.stages:
            logger.info(f"Stage {stage.stage_number}: {stage.name}")

            # Get stage result (would call actual Mistral API here)
            result = await self._process_stage(stage, context, opportunity)
            self.results.append(result)

            # Update context with stage findings
            context.add_stage_result(stage.name, result)

            # Check for knockout (NO-GO)
            if result.decision == Decision.NO_GO:
                logger.info(f"KNOCKOUT at stage {stage.stage_number}: {stage.name}")

                # QC verification for NO-GO
                if stage.requires_qc(result):
                    qc_result = await self._run_qc(stage, context, result)
                    if qc_result and qc_result.decision != Decision.NO_GO:
                        logger.info(f"QC OVERRIDE: {qc_result.decision}")
                        result.qc_override = qc_result.decision
                        # Continue if QC overrides the NO-GO
                        if qc_result.confidence >= stage.qc_threshold:
                            continue

                # Early termination on confirmed NO-GO
                break

        # Build final output
        return self._build_output(opportunity, context, self.results)

    async def _process_stage(self, stage: Stage, context: ContextAccumulator,
                            opportunity: Dict[str, Any]) -> StageResult:
        """Process single stage using hardcoded API configuration"""
        start_time = time.time()

        # Get the appropriate model for this stage
        model_id = get_stage_model(stage.stage_number)

        # Check if we should use batch or agent API
        use_batch = "batch" in model_id or stage.stage_type == StageType.BINARY

        # Build prompt with context
        prompt = stage.get_prompt_with_context(
            context.get_context_for_stage(stage.stage_number),
            is_batch=use_batch
        )

        # Rate limiting
        time_since_last = time.time() - self.last_api_call
        if time_since_last < RATE_LIMITS["retry_delay_seconds"]:
            await asyncio.sleep(RATE_LIMITS["retry_delay_seconds"] - time_since_last)

        # Make API call with hardcoded credentials
        try:
            if use_batch:
                result = await self._call_batch_api(model_id, prompt)
            else:
                result = await self._call_agent_api(model_id, prompt)

            self.last_api_call = time.time()

            # Parse response
            decision = Decision(result.get("decision", "INDETERMINATE"))
            confidence = result.get("confidence", 0.5)
            evidence = result.get("evidence", [])
            rationale = result.get("rationale", "")

            return StageResult(
                stage_name=stage.name,
                decision=decision,
                confidence=confidence,
                evidence=evidence,
                rationale=rationale,
                processing_time=time.time() - start_time
            )
        except Exception as e:
            logger.error(f"Error processing stage {stage.name}: {e}")
            # Return INDETERMINATE on error
            return StageResult(
                stage_name=stage.name,
                decision=Decision.INDETERMINATE,
                confidence=0.0,
                evidence=["Error processing stage"],
                rationale=str(e),
                processing_time=time.time() - start_time
            )

    async def _call_batch_api(self, model_id: str, prompt: str) -> Dict:
        """Call Mistral batch API with hardcoded key"""
        if self.mock_mode:
            return self._get_mock_response("batch", prompt)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model_id,
            "messages": [
                {"role": "system", "content": "You are an SOS assessment assistant."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": PIPELINE_CONFIG["max_tokens_per_request"],
            "temperature": 0.3
        }

        url = get_endpoint("mistral", "chat_url")

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=TIMEOUTS["batch_api_call"]  # Use proper timeout
            )
            response.raise_for_status()

            # Extract JSON from response
            result = response.json()
            content = result["choices"][0]["message"]["content"]

            # Parse JSON from content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {"decision": "INDETERMINATE", "confidence": 0.5, "rationale": "Could not parse response"}
        except Exception as e:
            logger.error(f"Batch API call failed: {e}")
            return {"decision": "INDETERMINATE", "confidence": 0.0, "rationale": str(e)}

    async def _call_agent_api(self, model_id: str, prompt: str) -> Dict:
        """Call Mistral agent API with hardcoded key"""
        if self.mock_mode:
            return self._get_mock_response("agent", prompt)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "agent_id": model_id,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": PIPELINE_CONFIG["max_tokens_per_request"]
        }

        url = get_endpoint("mistral", "agents_url")

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=TIMEOUTS["agent_api_call"]  # Use proper timeout
            )
            response.raise_for_status()

            # Extract JSON from response
            result = response.json()
            content = result["choices"][0]["message"]["content"]

            # Parse JSON from content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {"decision": "INDETERMINATE", "confidence": 0.5, "rationale": "Could not parse response"}
        except Exception as e:
            logger.error(f"Agent API call failed: {e}")
            return {"decision": "INDETERMINATE", "confidence": 0.0, "rationale": str(e)}

    async def _run_qc(self, stage: Stage, context: ContextAccumulator,
                     result: StageResult) -> Optional[StageResult]:
        """Run QC verification on stage result"""
        # This would call QC agent
        return None

    def _build_output(self, opportunity: Dict[str, Any],
                     context: ContextAccumulator,
                     results: List[StageResult]) -> Dict[str, Any]:
        """Build final pipeline output using unified schema"""
        from unified_pipeline_output import UnifiedPipelineOutput

        # Get the final decision
        final_decision = results[-1].decision if results else Decision.INDETERMINATE

        # Check for any QC overrides
        for result in results:
            if result.qc_override:
                final_decision = result.qc_override
                break

        # Build raw output
        raw_output = {
            "opportunity_id": opportunity.get("search_id") or opportunity.get("id"),
            "final_decision": final_decision.value,
            "stages_processed": len(results),
            "total_stages": len(self.stages),
            "knockout_stage": results[-1].stage_name if results and results[-1].decision == Decision.NO_GO else None,
            "processing_time": sum(r.processing_time for r in results),
            "timestamp": datetime.now().isoformat()
        }

        # Convert stage results to standard format
        stage_results = []
        for r in results:
            stage_dict = {
                "stage_name": r.stage_name,
                "decision": r.decision.value if hasattr(r.decision, 'value') else str(r.decision),
                "confidence": r.confidence,
                "evidence": r.evidence,
                "rationale": r.rationale,
                "processing_time": r.processing_time
            }
            if r.qc_verified:
                stage_dict["qc_verified"] = r.qc_verified
            if r.qc_override:
                stage_dict["qc_override"] = r.qc_override.value if hasattr(r.qc_override, 'value') else str(r.qc_override)
            stage_results.append(stage_dict)

        # Format using unified output
        formatted_output = UnifiedPipelineOutput.format_for_20_stage_pipeline(
            opportunity=opportunity,
            pipeline_results=raw_output,
            stage_results=stage_results
        )

        # Add the accumulated context (for debugging/analysis)
        formatted_output["accumulated_context"] = context.get_full_context()

        # Validate against schema
        if not UnifiedPipelineOutput.validate_against_schema(formatted_output, "agent"):
            logger.warning("Output does not match schema!")

        return formatted_output

    def _create_mock_opportunity(self, search_id: str) -> Dict[str, Any]:
        """Create mock opportunity data for testing"""
        return {
            "search_id": search_id,
            "metadata": {
                "title": f"Mock Opportunity {search_id}",
                "agency": "Mock Agency",
                "office": "Mock Office",
                "response_date_time": "2025-12-31 17:00:00",
                "type_of_set_aside": "None",
                "naics": "541511"
            },
            "documents": [
                {
                    "file_name": "mock_doc1.pdf",
                    "text": "This is a mock document with deadline December 31, 2025. Full and open competition."
                },
                {
                    "file_name": "mock_doc2.pdf",
                    "text": "Commercial aircraft parts for Boeing 737. No security clearance required."
                }
            ],
            "combined_text": "Mock opportunity. Deadline: December 31, 2025. Full and open competition. Commercial aircraft parts for Boeing 737. No security clearance required.",
            "fetch_status": "complete",
            "errors": []
        }

    def _get_mock_response(self, api_type: str, prompt: str) -> Dict:
        """Generate mock API responses for testing"""
        # Analyze prompt to generate appropriate mock response
        prompt_lower = prompt.lower()

        # Default response
        decision = "GO"
        confidence = 0.95
        evidence = ["Mock evidence from simulated analysis"]
        rationale = "Mock response for testing - no issues found"

        # Parse which stage this is from the prompt
        stage_specific = {
            "deadline_found": None,
            "set_aside_type": None,
            "clearance_level": None,
            "acquisition_type": None,
            "vehicle": None,
            "export_control": None,
            "amc_code": None,
            "restriction_type": None,
            "sar_required": False,
            "platform": None,
            "domain": None,
            "data_rights": None,
            "systems_required": [],
            "certifications": []
        }

        # Check the actual opportunity text in the prompt
        if "deadline december 31, 2025" in prompt_lower:
            # Future deadline - should be GO for timing
            decision = "GO"
            confidence = 0.99
            rationale = "Deadline is in the future (December 31, 2025)"
            evidence = ["Deadline: December 31, 2025"]
            stage_specific["deadline_found"] = "2025-12-31"
        elif "deadline" in prompt_lower and "2024" in prompt_lower:
            # Past deadline - should be NO-GO for timing
            decision = "NO-GO"
            confidence = 0.99
            rationale = "Deadline has passed"
            evidence = ["Response deadline was in 2024"]
            stage_specific["deadline_found"] = "2024-01-01"

        # Check for set-asides (stage 2)
        if "check for small business set-asides" in prompt_lower:
            if "8(a)" in prompt or "sdvosb" in prompt_lower:
                decision = "NO-GO"
                confidence = 0.99
                rationale = "Small business set-aside detected"
                evidence = ["8(a) set-aside requirement found"]
                stage_specific["set_aside_type"] = "8(a)"
            elif "full and open" in prompt_lower:
                decision = "GO"
                confidence = 0.99
                rationale = "Full and open competition - no set-asides"
                evidence = ["Full and open competition"]

        # Check for security clearances (stage 3)
        if "check for security clearance" in prompt_lower:
            if "top secret" in prompt_lower or "ts/sci" in prompt_lower:
                decision = "NO-GO"
                confidence = 0.99
                rationale = "Security clearance required"
                evidence = ["Top Secret clearance required"]
                stage_specific["clearance_level"] = "Top Secret"
            elif "no security clearance required" in prompt_lower:
                decision = "GO"
                confidence = 0.99
                rationale = "No security clearance required"
                evidence = ["No clearance requirements found"]

        # Check for platforms (stage 10)
        if "check what platform" in prompt_lower:
            if "f-16" in prompt_lower or "f-35" in prompt_lower:
                decision = "NO-GO"
                confidence = 0.95
                rationale = "Military platform - F-16 fighter jet"
                evidence = ["F-16 military aircraft"]
                stage_specific["platform"] = "F-16"
            elif "boeing 737" in prompt_lower:
                decision = "GO"
                confidence = 0.95
                rationale = "Commercial platform - Boeing 737"
                evidence = ["Boeing 737 commercial aircraft"]
                stage_specific["platform"] = "Boeing 737"

        # Build final response
        response = {
            "decision": decision,
            "confidence": confidence,
            "evidence": evidence,
            "rationale": rationale,
            "mock_response": True
        }

        # Add stage-specific fields
        response.update({k: v for k, v in stage_specific.items() if v is not None})

        return response

    def run_test(self):
        """Simple synchronous test method"""
        test_opportunity = {
            "id": "TEST-001",
            "title": "Test Opportunity",
            "text": "This is a test opportunity with deadline 2025-12-31"
        }

        # For testing, use synchronous mock
        import asyncio
        result = asyncio.run(self.process_opportunity(test_opportunity))

        print(f"Test Result: {json.dumps(result, indent=2)}")
        return result


if __name__ == "__main__":
    # Quick test
    pipeline = MultiStagePipeline()
    pipeline.run_test()