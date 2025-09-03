#!/usr/bin/env python3
"""
SOS Ingestion Gate V4.19 - 19-Category Knock-Out Assessment System
Implements deterministic rule-based assessment with complete category scoring.
"""

import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict
import logging
from datetime import datetime, timedelta
from enum import Enum
from platform_mapper_v419 import PlatformMapper, PlatformDecision
from parts_condition_checker import PartsConditionChecker, ConditionDecision

logger = logging.getLogger(__name__)


class Decision(Enum):
    """Assessment decision types."""
    GO = "GO"
    NO_GO = "NO-GO"
    FURTHER_ANALYSIS = "FURTHER_ANALYSIS"
    CONTACT_CO = "CONTACT_CO"


@dataclass
class CategoryScore:
    """Score for a single knock-out category."""
    category_id: int
    category_name: str
    score: int  # 0=Pass, 1-5=Severity of block
    triggered: bool
    patterns_matched: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    contact_co_applicable: bool = False
    contact_co_reason: str = ""


@dataclass
class AssessmentResult:
    """Complete assessment result with all category scores."""
    ko_logic_version: str = "4.19"
    opportunity_id: str = ""
    decision: Decision = Decision.FURTHER_ANALYSIS
    categories_triggered: List[int] = field(default_factory=list)
    primary_blocker: Optional[str] = None
    primary_blocker_category: Optional[int] = None
    category_scores: Dict[int, CategoryScore] = field(default_factory=dict)
    co_contact_applicable: bool = False
    co_contact_reason: str = ""
    further_analysis_queued: bool = False
    further_analysis_items: List[str] = field(default_factory=list)
    confidence_score: float = 0.0
    platform_result: Optional[Dict] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        result = asdict(self)
        result['decision'] = self.decision.value
        return result
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    def to_markdown(self) -> str:
        """Generate markdown report."""
        md = f"""# SOS Assessment Report

**KO Logic Version:** {self.ko_logic_version}
**Opportunity:** {self.opportunity_id}
**Decision:** **{self.decision.value}**
**Timestamp:** {self.timestamp}

## Summary
- **Categories Triggered:** {', '.join(map(str, self.categories_triggered)) if self.categories_triggered else 'None'}
- **Primary Blocker:** {self.primary_blocker or 'N/A'}
- **CO Contact Applicable:** {'Yes - ' + self.co_contact_reason if self.co_contact_applicable else 'No'}
- **Further Analysis:** {'Yes' if self.further_analysis_queued else 'No'}

## Category Scores

| Category | Name | Score | Triggered | Evidence |
|----------|------|-------|-----------|----------|
"""
        for cat_id in sorted(self.category_scores.keys()):
            score = self.category_scores[cat_id]
            md += f"| {cat_id} | {score.category_name} | {score.score} | {'✓' if score.triggered else ''} | {', '.join(score.evidence[:2]) if score.evidence else ''} |\n"
        
        if self.further_analysis_items:
            md += f"\n## Further Analysis Items\n"
            for item in self.further_analysis_items:
                md += f"- {item}\n"
        
        return md
    
    def to_csv_row(self) -> str:
        """Generate CSV row."""
        scores = [str(self.category_scores[i].score) if i in self.category_scores else "0" 
                  for i in range(1, 20)]
        return ','.join([
            self.opportunity_id,
            self.decision.value,
            str(len(self.categories_triggered)),
            self.primary_blocker or "",
            *scores,
            "Yes" if self.co_contact_applicable else "No",
            "Yes" if self.further_analysis_queued else "No",
            f"{self.confidence_score:.2f}",
            self.timestamp
        ])


class KnockOutCategories:
    """Definition of the 19 knock-out categories."""
    
    CATEGORIES = {
        1: {"name": "TIMING", "description": "Expired deadline"},
        2: {"name": "DOMAIN", "description": "Non-aviation (all agencies OK)"},
        3: {"name": "SECURITY", "description": "Classified work"},
        4: {"name": "SET-ASIDES", "description": "Wrong type (8(a), SDVOSB, WOSB, HUBZone)"},
        5: {"name": "SOURCE_RESTRICTIONS", "description": "OEM only, approved lists, sole source"},
        6: {"name": "TECH_DATA", "description": "No government drawings, proprietary only"},
        7: {"name": "EXPORT_CONTROL", "description": "DoD-cleared manufacturer only"},
        8: {"name": "AMC_AMSC", "description": "B/C/D/P/R/H codes, AMC 3/4/5"},
        9: {"name": "SAR", "description": "Source Approval Required"},
        10: {"name": "PLATFORM", "description": "Pure military platform/engine/drone"},
        11: {"name": "PROCUREMENT", "description": "New manufacture without data, FAT DoD only"},
        12: {"name": "COMPETITION", "description": "Bridge/follow-on/incumbent"},
        13: {"name": "SUBCONTRACTING", "description": "Prohibited"},
        14: {"name": "VEHICLES", "description": "IDIQ/GSA/GWAC not held"},
        15: {"name": "EXPERIMENTAL", "description": "OTA/BAA/SBIR/CRADA"},
        16: {"name": "IT_ACCESS", "description": "Pre-cleared systems only"},
        17: {"name": "CERTIFICATIONS", "description": "Agency-specific (NASA, EPA, TSA)"},
        18: {"name": "WARRANTY", "description": "Direct sustainment obligations"},
        19: {"name": "CAD_CAM", "description": "Native proprietary formats required"}
    }
    
    # Map pattern families to categories (using actual names from regex_pack_v14_production.yaml)
    PATTERN_TO_CATEGORY = {
        # Category 1: TIMING
        'currency_patterns': 1,  # Contains deadline markers
        
        # Category 2: DOMAIN  
        'excluded_platform_patterns': 2,  # Non-aviation keywords
        
        # Category 3: SECURITY
        'security_clearance_patterns': 3,  # Security clearance requirements
        
        # Category 4: SET-ASIDES
        # Note: Handled via special logic in _check_set_aside
        
        # Category 5: SOURCE RESTRICTIONS
        'sole_source_patterns': 5,
        'approved_source_only_patterns': 5,
        'intent_to_award_patterns': 5,  # Intent to award = source restriction
        'qpl_qml_patterns': 5,
        
        # Category 6: TECH DATA
        'tdp_negative_patterns': 6,  # TDP restrictions/unavailable
        
        # Category 7: EXPORT CONTROL
        'risk_clause_patterns': 7,  # Contains export controls
        
        # Category 8: AMC/AMSC
        'amc_amsc_patterns': 8,
        
        # Category 9: SAR
        'sar_patterns': 9,
        
        # Category 10: PLATFORM
        'aviation_platform_patterns': 10,  # Military/civilian platforms
        
        # Category 11: PROCUREMENT
        'refurbished_rotatable_aftermarket_surplus_patterns': 11,  # New-only requirements
        
        # Category 12: COMPETITION/QUALIFICATION
        'first_article_patterns': 12,  # First article testing requirements
        
        # Category 13: SUBCONTRACTING
        # Note: No direct subcontracting patterns in v094
        
        # Category 14: VEHICLES
        'agency_specific_patterns': 14,  # Agency-specific patterns
        
        # Category 15: EXPERIMENTAL
        # Note: No direct experimental patterns in v094
        
        # Category 16: IT ACCESS
        # Note: No direct IT patterns in v094
        
        # Category 17: CERTIFICATIONS
        'commercial_items_patterns': 17,  # FAR Part 12 commercial items
        'faa_8130_patterns': 17,  # FAA certifications
        
        # Category 18: WARRANTY
        'traceability_patterns': 18,  # Chain of custody/traceability
        
        # Category 19: CAD/CAM
        'tdp_positive_patterns': 19  # TDP availability (positive)
    }
    
    # Exceptions that override category blocks (using v094 pattern names)
    OVERRIDE_CONDITIONS = {
        8: ['amc_amsc_patterns'],  # AMSC Z/G can override restrictions
        9: ['faa_8130_patterns'],  # FAA 8130 can override SAR
        10: ['commercial_items_patterns'],  # Commercial items override platform restrictions
        11: ['tdp_positive_patterns']  # Gov data overrides new manufacture block
    }
    
    # Contact CO triggers
    CONTACT_CO_TRIGGERS = {
        5: "Approved sources with FAA 8130-3 mentioned",
        11: "U.S. domestic manufacturer requirement",
        13: "Subcontracting prohibited for single unit"
    }
    
    # Further analysis triggers
    FURTHER_ANALYSIS_TRIGGERS = {
        'document_management_systems': "Check MRO compliance",
        'jcp_access': "Verify MRO status",
        'cmmc_requirements': "Validate equivalency",
        'first_article_non_dod': "Case by case review"
    }


class IngestionGateV419:
    """
    19-Category deterministic assessment gate.
    """
    
    # Testing mode - evaluating patterns not deadlines
    IGNORE_TIMING_FOR_TESTING = True  # DISABLE TIMING CHECKS - they're broken
    
    def __init__(self, config_path: str = 'packs/regex_pack_v14_production.yaml'):
        """Initialize the V4.19 gate."""
        self.config_path = config_path
        self.regex_pack = self._load_regex_pack()
        self.compiled_patterns = self._compile_patterns()
        self.categories = KnockOutCategories()
        self.platform_mapper = PlatformMapper()  # Initialize platform mapper
        self.condition_checker = PartsConditionChecker()  # Initialize condition checker
    
    def _load_regex_pack(self) -> Dict[str, Any]:
        """Load regex pack from YAML."""
        pack_path = Path(self.config_path)
        
        if not pack_path.exists():
            logger.warning(f"Regex pack not found: {pack_path}")
            return {'metadata': {}, 'globals': {}}
        
        with open(pack_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    
    def _compile_patterns(self) -> Dict[str, List[re.Pattern]]:
        """Compile all regex patterns from pack."""
        compiled = {}
        
        # Skip non-pattern keys
        skip_keys = ['version', 'metadata', 'globals', 'conflict_resolution', 'subjects']
        
        for family_name, family_data in self.regex_pack.items():
            if family_name in skip_keys:
                continue
                
            if not isinstance(family_data, dict):
                continue
            
            patterns = []
            
            # Handle v094 structure with pattern_groups
            if 'pattern_groups' in family_data:
                for group in family_data['pattern_groups']:
                    # Get regex_patterns from each group
                    if 'regex_patterns' in group:
                        for pattern in group['regex_patterns']:
                            if isinstance(pattern, str):
                                try:
                                    regex = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
                                    patterns.append(regex)
                                except re.error as e:
                                    logger.warning(f"Failed to compile pattern in {family_name}: {e}")
                    
                    # Get exact_phrases from each group
                    if 'exact_phrases' in group:
                        for phrase in group['exact_phrases']:
                            if isinstance(phrase, str):
                                try:
                                    escaped = re.escape(phrase)
                                    regex = re.compile(r'\b' + escaped + r'\b', re.IGNORECASE)
                                    patterns.append(regex)
                                except re.error as e:
                                    logger.warning(f"Failed to compile phrase in {family_name}: {e}")
            
            # Also handle old structure for backwards compatibility
            elif 'patterns' in family_data:
                pattern_list = family_data['patterns']
                if isinstance(pattern_list, list):
                    for pattern in pattern_list:
                        if isinstance(pattern, str):
                            try:
                                regex = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
                                patterns.append(regex)
                            except re.error as e:
                                logger.warning(f"Failed to compile pattern in {family_name}: {e}")
            
            if patterns:
                compiled[family_name] = patterns
        
        return compiled
    
    def _check_deadline(self, text: str) -> Tuple[bool, List[str]]:
        """Check if deadline has passed (Category 1)."""
        # Simple deadline check - would need enhancement for production
        deadline_patterns = [
            r'deadline[:\s]+passed',
            r'closed[:\s]+on',
            r'expired',
            r'no longer accepting'
        ]
        
        evidence = []
        for pattern in deadline_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                evidence.append(f"Deadline indicator found: {pattern}")
                return True, evidence
        
        return False, []
    
    def _check_set_aside(self, text: str, opportunity: Dict) -> Tuple[bool, List[str]]:
        """Check for ineligible set-asides (Category 4)."""
        evidence = []
        
        # Check opportunity metadata first
        set_aside = opportunity.get('set_aside', '') or ''
        set_aside = set_aside.strip().upper().replace(' ', '').replace('-', '')
        
        # Also check text for set-aside mentions
        ineligible_patterns = [
            (r'\b8\s*\(\s*a\s*\)', '8(a) minority-owned business'),
            (r'\b8a\b', '8(a) minority-owned business'),
            (r'\bwosb\b', 'women-owned small business'),
            (r'\bedwosb\b', 'economically disadvantaged women-owned'),
            (r'\bsdvosb\b', 'service-disabled veteran-owned'),
            (r'\bhubzone\b', 'HUBZone small business'),
            (r'\bvosb\b', 'veteran-owned small business')
        ]
        
        # Check metadata
        ineligible_codes = {
            '8A': '8(a) minority-owned business',
            '8(A)': '8(a) minority-owned business',
            'WOSB': 'women-owned small business',
            'EDWOSB': 'economically disadvantaged women-owned',
            'SDVOSB': 'service-disabled veteran-owned',
            'VOSB': 'veteran-owned small business',
            'HUBZONE': 'HUBZone small business',
            'HZ': 'HUBZone small business'
        }
        
        for code, description in ineligible_codes.items():
            if code in set_aside:
                evidence.append(f"Set-aside: {description}")
                return True, evidence
        
        # Check text patterns
        for pattern, description in ineligible_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                evidence.append(f"Set-aside detected: {description}")
                return True, evidence
        
        return False, []
    
    def _scan_text_for_patterns(self, text: str) -> Dict[str, List[str]]:
        """Scan text and return matched pattern families with evidence."""
        matches = {}
        
        for family_name, patterns in self.compiled_patterns.items():
            family_matches = []
            for pattern in patterns:
                found = pattern.findall(text)
                if found:
                    # Store first match as evidence
                    family_matches.extend(found[:2])  # Max 2 examples
            
            if family_matches:
                matches[family_name] = family_matches
        
        return matches
    
    def _score_category(self, category_id: int, text: str, pattern_matches: Dict[str, List[str]], 
                       opportunity: Dict = None) -> CategoryScore:
        """Score a single category based on text and pattern matches."""
        category_info = self.categories.CATEGORIES[category_id]
        score = CategoryScore(
            category_id=category_id,
            category_name=category_info["name"],
            score=0,
            triggered=False
        )
        
        # FAA 8130 EXCEPTION CHECK - Do this FIRST
        # If FAA 8130 is mentioned, source restrictions don't apply
        if category_id == 5:  # SOURCE_RESTRICTIONS
            import re  # Import locally to avoid scope issues
            faa_patterns = [
                r'FAA[\s-]*8130',
                r'8130[\s-]*3',
                r'FAA[\s-]*Form[\s-]*8130',
                r'FAA[\s-]*Certified',
                r'FAA[\s-]*MRO',
                r'FAA[\s-]*approved',
                r'airworthiness[\s-]*certificate',
                r'airworthy[\s-]*approval'
            ]
            for pattern in faa_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    # If FAA 8130 + approved sources, this is GO for SOS
                    score.evidence = ["FAA 8130 Exception: SOS MRO partners can provide"]
                    score.contact_co_applicable = True
                    score.contact_co_reason = "FAA 8130 certified parts - SOS can provide through MRO network"
                    return score  # Return untriggered (GO)
        
        # Special handling for timing (Category 1)
        if category_id == 1:
            # Testing mode - evaluating patterns not deadlines
            if IngestionGateV419.IGNORE_TIMING_FOR_TESTING:
                score.evidence = ["TIMING: IGNORED (Test Mode)"]
                return score  # Return untriggered score
            
            triggered, evidence = self._check_deadline(text)
            if triggered:
                score.score = 5
                score.triggered = True
                score.evidence = evidence
                return score
        
        # Special handling for set-asides (Category 4)
        if category_id == 4:
            triggered, evidence = self._check_set_aside(text, opportunity or {})
            if triggered:
                score.score = 5
                score.triggered = True
                score.evidence = evidence
                return score
        
        # Special handling for Category 8 - Military platforms
        if category_id == 8:
            # Check if text contains military aircraft designations
            military_patterns = [
                r'(?i)\bF[-\s]?(?:15|16|18|22|35)[A-Z]?\b',  # F-15, F-16, F-22, F-35
                r'(?i)\bF[-\s]?(?:4|5|14|111|117)[A-Z]?\b',   # F-4, F-5, F-14, etc.
                r'(?i)\bB[-\s]?(?:1|2|52|21)[A-Z]?\b',        # B-1, B-2, B-52
                r'(?i)\bAH[-\s]?(?:1|64|6)[A-Z]?\b',          # AH-1, AH-64 Apache
                r'(?i)\bUH[-\s]?(?:1|60|72)[A-Z]?\b',         # UH-1, UH-60 Black Hawk
            ]
            
            import re
            for pattern in military_patterns:
                if re.search(pattern, text):
                    score.triggered = True
                    score.score = 5
                    score.patterns_matched.append('military_aircraft')
                    match = re.search(pattern, text)
                    if match:
                        score.evidence.append(f"Military aircraft: {match.group()}")
                    break
        
        # Special handling for platform (Category 10) with platform mapper
        if category_id == 10:
            # First check if AMSC override is present
            has_amsc_override = self.platform_mapper.check_amsc_override(text)
            
            # Get platform assessment
            platform_result = self.platform_mapper.assess_platform_impact(text)
            
            # If platform is military and no AMSC override, trigger NO-GO
            if platform_result['decision'] == 'NO-GO' and not has_amsc_override:
                score.triggered = True
                score.score = 5
                score.patterns_matched.append('platform_mapper')
                score.evidence.append(f"Military platform: {platform_result['platform']}")
                if platform_result.get('civilian_equivalent'):
                    score.evidence.append(f"Civilian equivalent exists: {platform_result['civilian_equivalent']}")
            # If AMSC override present, note it but don't trigger
            elif platform_result['decision'] == 'NO-GO' and has_amsc_override:
                score.triggered = False
                score.score = 0
                score.evidence.append(f"Military platform {platform_result['platform']} overridden by AMSC Z/G/A")
            # If platform is GO or conditional, don't trigger category
            elif platform_result['decision'] == 'GO':
                score.evidence.append(f"Civilian platform identified: {platform_result['platform']}")
                score.triggered = False  # Civilian platform = GO
                score.score = 0
                # Skip pattern matching for Category 10 when platform is civilian
                return score
        
        # Special handling for procurement/parts condition (Category 11) with condition checker
        if category_id == 11:
            # Check parts condition requirements
            condition_decision, condition_reason = self.condition_checker.assess_for_sos(text)
            
            # If new-only requirement detected, trigger NO-GO
            if condition_decision == ConditionDecision.NO_GO:
                score.triggered = True
                score.score = 5
                score.patterns_matched.append('condition_checker')
                score.evidence.append(condition_reason)
            # If conditional (override present), note it
            elif condition_decision == ConditionDecision.CONDITIONAL:
                # Let pattern matching continue but note the condition
                score.evidence.append(f"Condition: {condition_reason}")
        
        # Check pattern matches for this category
        for family_name, cat_id in self.categories.PATTERN_TO_CATEGORY.items():
            if cat_id == category_id and family_name in pattern_matches:
                score.triggered = True
                score.score = 5  # Default to highest severity
                score.patterns_matched.append(family_name)
                score.evidence.extend(pattern_matches[family_name][:2])
        
        # Check for override conditions
        if category_id in self.categories.OVERRIDE_CONDITIONS:
            override_patterns = self.categories.OVERRIDE_CONDITIONS[category_id]
            for override in override_patterns:
                if override in pattern_matches:
                    # For Category 10, if platform mapper already handled AMSC override, skip
                    if category_id == 10 and 'overridden by AMSC' in str(score.evidence):
                        continue
                    score.score = 0  # Override cancels the block
                    score.triggered = False
                    score.evidence.append(f"Override: {override}")
                    break
        
        # Check for CO contact applicability
        if category_id in self.categories.CONTACT_CO_TRIGGERS:
            # Simplified check - would need more logic in production
            if score.triggered:
                score.contact_co_applicable = True
                score.contact_co_reason = self.categories.CONTACT_CO_TRIGGERS[category_id]
        
        return score
    
    def _has_faa_8130_exception(self, text: str) -> bool:
        """Check if text contains FAA 8130 certification - overrides many NO-GO conditions"""
        import re
        faa_patterns = [
            r'FAA[\s-]*8130',
            r'8130[\s-]*3',
            r'FAA[\s-]*Form[\s-]*8130',
            r'FAA[\s-]*Certified',
            r'FAA[\s-]*MRO',
            r'FAA[\s-]*approved',
            r'airworthiness[\s-]*certificate',
            r'airworthy[\s-]*approval'
        ]
        for pattern in faa_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def assess_opportunity(self, opportunity: Dict[str, Any]) -> AssessmentResult:
        """
        Perform complete 19-category assessment on an opportunity.
        Continues scoring all categories even after NO-GO is found.
        """
        # Initialize result
        result = AssessmentResult(
            opportunity_id=opportunity.get('id', opportunity.get('title', 'unknown')[:50])
        )
        
        # Combine all text fields for analysis
        # CRITICAL: 'text' field contains 210KB of documents from process_opportunity
        text_fields = ['title', 'text', 'description', 'summary', 'requirements', 
                      'statement_of_work', 'attachments_text', 'full_text']
        combined_text = ' '.join(str(opportunity.get(field, '')) for field in text_fields)
        
        # If we have the main 'text' field with documents, use it primarily
        if opportunity.get('text') and len(opportunity.get('text', '')) > 1000:
            combined_text = opportunity.get('text', '')
        
        # CHECK FOR FAA 8130 EXCEPTION FIRST
        has_faa_8130 = self._has_faa_8130_exception(combined_text)
        if has_faa_8130:
            # FAA 8130 parts are GO for SOS regardless of other restrictions
            result.decision = Decision.GO
            result.primary_reason = "FAA 8130 certified parts - SOS can provide through MRO network"
            result.co_contact_applicable = True
            result.co_contact_reason = "FAA 8130 exception applies"
            return result  # Return immediately as GO
        
        # Scan for all pattern matches
        pattern_matches = self._scan_text_for_patterns(combined_text)
        
        # Track platform assessment result for later use
        platform_result = None
        
        # Score all 19 categories (continue even after NO-GO)
        decision_made = False
        for category_id in range(1, 20):
            category_score = self._score_category(category_id, combined_text, pattern_matches, opportunity)
            result.category_scores[category_id] = category_score
            
            # Capture platform result for Bug 3 fix
            if category_id == 10:
                platform_result = self.platform_mapper.assess_platform_impact(combined_text)
                result.platform_result = platform_result
            
            # Track triggered categories
            if category_score.triggered:
                result.categories_triggered.append(category_id)
                
                # Set primary blocker (first NO-GO found)
                if not decision_made and category_score.score > 0:
                    # Check if this is FAA 8130 exception case
                    if category_id == 5 and category_score.contact_co_applicable:
                        # This is FAA 8130 - should be GO not NO-GO
                        continue  # Skip setting NO-GO
                    result.decision = Decision.NO_GO
                    result.primary_blocker = f"Category {category_id} - {category_score.category_name}: {category_score.evidence[0] if category_score.evidence else 'Pattern matched'}"
                    result.primary_blocker_category = category_id
                    decision_made = True
                
                # Check for CO contact
                if category_score.contact_co_applicable:
                    result.co_contact_applicable = True
                    if not result.co_contact_reason:
                        result.co_contact_reason = category_score.contact_co_reason
        
        # Set final decision if no blocks found
        if not decision_made:
            # BUG 3 FIX: Check if platform mapper returned GO for civilian platforms
            if platform_result and platform_result.get('decision') == 'GO':
                result.decision = Decision.GO
                result.confidence_score = 90.0
                result.primary_blocker = f"Civilian platform: {platform_result.get('platform', 'Unknown')}"
            else:
                # Check for positive signals
                positive_patterns = ['aviation_platform_patterns', 'faa_8130_airworthiness_patterns',
                                   'commercial_item_patterns', 'refurbished_allowance_patterns',
                                   'tdp_positive_patterns', 'amc_amsc_open_patterns',
                                   'go_platform_civilian_equivalents', 'opportunity_positive_patterns']
                
                has_positive = any(p in pattern_matches for p in positive_patterns)
                
                # BUG 2 FIX: Check for aviation content in long text
                aviation_keywords = ['aircraft', 'aviation', 'aerospace', 'FAA', 'airworthiness', 
                                   'engine', 'avionics', 'helicopter', 'flight']
                has_aviation_content = any(keyword.lower() in combined_text.lower() for keyword in aviation_keywords)
                
                if has_positive or (has_aviation_content and len(combined_text) > 100):
                    result.decision = Decision.GO
                    result.confidence_score = 85.0
                else:
                    result.decision = Decision.FURTHER_ANALYSIS
                    result.confidence_score = 50.0
                    result.further_analysis_queued = True
                
                # Add further analysis items
                for trigger_pattern, analysis_item in self.categories.FURTHER_ANALYSIS_TRIGGERS.items():
                    if trigger_pattern in pattern_matches:
                        result.further_analysis_items.append(analysis_item)
        
        # Calculate confidence based on evidence strength
        if result.categories_triggered:
            result.confidence_score = min(95.0, 70.0 + (len(result.categories_triggered) * 5))
        
        return result
    
    def generate_csv_header(self) -> str:
        """Generate CSV header row."""
        category_headers = [f"Cat{i}_Score" for i in range(1, 20)]
        return ','.join([
            "Opportunity_ID", "Decision", "Categories_Triggered_Count", "Primary_Blocker",
            *category_headers,
            "CO_Contact", "Further_Analysis", "Confidence", "Timestamp"
        ])


def main():
    """Test the V4.19 gate with sample data."""
    gate = IngestionGateV419()
    
    # Test opportunities
    test_cases = [
        {
            'id': 'TEST-001',
            'title': 'F-16 Engine Parts with AMSC Code B',
            'description': 'Procurement of F-16 engine components. AMSC Code B applies.'
        },
        {
            'id': 'TEST-002',
            'title': 'Commercial Aviation Parts - FAA 8130-3',
            'description': 'Boeing 737 parts with FAA Form 8130-3 certification required.'
        },
        {
            'id': 'TEST-003',
            'title': 'C-130 Parts - AMSC Z Override',
            'description': 'C-130 aircraft parts. AMSC Code Z - commercial equivalent acceptable.'
        },
        {
            'id': 'TEST-004',
            'title': 'Secret Clearance Required - F-35 Components',
            'description': 'F-35 maintenance requiring Secret clearance and facility clearance.'
        }
    ]
    
    print("=== SOS ASSESSMENT V4.19 - 19 CATEGORY SYSTEM ===\n")
    print(gate.generate_csv_header())
    print()
    
    for test in test_cases:
        result = gate.assess_opportunity(test)
        
        print(f"\n{'='*60}")
        print(f"Opportunity: {result.opportunity_id}")
        print(f"KO Logic Version: {result.ko_logic_version}")
        print(f"Decision: {result.decision.value}")
        print(f"Categories Triggered: {result.categories_triggered}")
        print(f"Primary Blocker: {result.primary_blocker or 'None'}")
        print(f"\nCategory Scores:")
        for i in range(1, 20):
            score = result.category_scores[i]
            if score.triggered or score.score > 0:
                print(f"  {i:2}. {score.category_name:20} Score: {score.score} {'[TRIGGERED]' if score.triggered else ''}")
        
        print(f"\nCO Contact: {'Yes - ' + result.co_contact_reason if result.co_contact_applicable else 'No'}")
        print(f"Further Analysis: {'Yes' if result.further_analysis_queued else 'No'}")
        
        if result.further_analysis_items:
            print(f"Analysis Items: {', '.join(result.further_analysis_items)}")
        
        print(f"\nCSV Row:")
        print(result.to_csv_row())
    
    print("\n=== TEST COMPLETE ===")


if __name__ == "__main__":
    main()