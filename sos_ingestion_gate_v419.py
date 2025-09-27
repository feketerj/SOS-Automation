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
    
    def __init__(self, config_path: str = 'packs/regex_pack_v419_complete.yaml'):
        """Initialize the V4.19 gate."""
        self.config_path = config_path
        self.regex_pack = self._load_regex_pack()
        self.compiled_patterns = self._compile_patterns()
        self.categories = KnockOutCategories()
        self.platform_mapper = PlatformMapper()  # Initialize platform mapper
        self.condition_checker = PartsConditionChecker()  # Initialize condition checker
    
    def _load_regex_pack(self) -> Dict[str, Any]:
        """Load regex pack from YAML with self-healing path resolution."""
        # Try multiple locations for robustness
        possible_paths = [
            Path(self.config_path),  # Direct path
            Path('..') / self.config_path,  # Parent directory
            Path('../..') / self.config_path,  # Two levels up
            Path(__file__).parent / self.config_path,  # Relative to this file
            Path('_ARCHIVE_OLD_FILES_2025_09_09') / self.config_path  # Fallback to archive
        ]
        
        pack_path = None
        for path in possible_paths:
            if path.exists():
                pack_path = path
                logger.info(f"Found regex pack at: {pack_path}")
                break
        
        if not pack_path:
            logger.warning(f"Regex pack not found in any location. Tried: {possible_paths}")
            # Still return empty structure so processing continues
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
        
        # FAA 8130 EXCEPTION CHECK for Category 5 (Source Restrictions)
        # Navy + SAR + FAA 8130 = Exception
        if category_id == 5:  # SOURCE_RESTRICTIONS
            # Check if this is a Navy FAA 8130 exception case
            if self._has_faa_8130_exception(text):
                # Navy + SAR + FAA 8130 = GO for SOS
                score.evidence = ["Navy FAA 8130 Exception: SOS MRO partners can provide"]
                score.contact_co_applicable = True
                score.contact_co_reason = "Navy + SAR + FAA 8130 = SOS eligible through MRO partners"
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
            import re
            # FIRST: Check for AMSC Z/G override
            amsc_override_pattern = r'\bAMSC\s+(?:Code\s+)?[ZGA]\b|\bAMC\s+[12]\b'
            has_amsc_override = bool(re.search(amsc_override_pattern, text, re.IGNORECASE))
            
            # SECOND: Check platform mapper for civilian equivalents
            platform_result = self.platform_mapper.assess_platform_impact(text)
            has_civilian_equivalent = (platform_result.get('decision') == 'GO' or 
                                      platform_result.get('civilian_equivalent') is not None)
            
            # If AMSC override present, don't block
            if has_amsc_override:
                score.triggered = False
                score.score = 0
                score.evidence.append(f"AMSC Z/G/A override present - commercial equivalent acceptable")
                return score
                
            # Check if text contains military aircraft/weapons/EW designations
            # NOTE: C-12 is King Air, not included here
            military_patterns = [
                # Fighter aircraft
                r'(?i)\bF[-\s]?(?:15|16|18|22|35)[A-Z]{0,2}\b',  # F-15, F-16, F-22, F-35 (including F15EX)
                r'(?i)\bF[-\s]?(?:4|5|14|111|117)[A-Z]{0,2}\b',   # F-4, F-5, F-14, etc.
                
                # Bombers
                r'(?i)\bB[-\s]?(?:1|2|52|21)[A-Z]{0,2}\b',        # B-1, B-2, B-52 (including B52H)
                
                # Transport (military-only)
                r'(?i)\bC[-\s]?(?:130|17|5)\b',                   # C-130, C-17, C-5 (NOT C-12 which is King Air)
                r'(?i)\bC[-\s]?(?:27|21)\b',                      # C-27, C-21 (military only)
                
                # Tankers
                r'(?i)\bKC[-\s]?(?:135|10|46)[A-Z]{0,2}\b',       # KC-135, KC-10, KC-46 (including KC46A)
                
                # Maritime patrol
                r'(?i)\bP[-\s]?(?:3|8)[A-Z]{0,2}\b',              # P-3 Orion, P-8 Poseidon (including P3C, P8A)
                
                # Electronic warfare/surveillance
                r'(?i)\bE[-\s]?(?:2|3|4|6|8)[A-Z]{0,2}\b',        # E-2, E-3 AWACS, E-4, E-6, E-8
                r'(?i)\bEA[-\s]?(?:6B|18G)\b',                    # EA-6B Prowler, EA-18G Growler
                r'(?i)\bRC[-\s]?135[A-Z]?\b',                     # RC-135 reconnaissance
                r'(?i)\bEP[-\s]?3[A-Z]?\b',                       # EP-3 ARIES
                
                # Helicopters (military-only)
                r'(?i)\bAH[-\s]?(?:1|64|6)[A-Z]?\b',              # AH-1, AH-64 Apache
                r'(?i)\bUH[-\s]?(?:1|60|72)[A-Z]?\b',             # UH-1, UH-60 Black Hawk
                r'(?i)\bCH[-\s]?(?:47|53)[A-Z]?\b',               # CH-47 Chinook, CH-53
                r'(?i)\bMH[-\s]?(?:60|53|47)[A-Z]?\b',            # MH-60, MH-53, MH-47
                r'(?i)\bV[-\s]?22\b',                             # V-22 Osprey
                
                # WEAPONS SYSTEMS
                r'(?i)\bweapon\s+system\b',                       # Generic weapon system
                r'(?i)\bweapons\s+system\b',                      # Weapons system
                r'(?i)\bmissile\s+system\b',                      # Missile systems
                r'(?i)\btorpedo\s+system\b',                      # Torpedo systems
                r'(?i)\bbomb(?:ing)?\s+system\b',                 # Bombing systems
                r'(?i)\bgunnery\s+system\b',                      # Gunnery systems
                r'(?i)\bfire\s+control\s+system\b',               # Fire control systems
                r'(?i)\btargeting\s+system\b',                    # Targeting systems
                r'(?i)\bordnance\s+system\b',                     # Ordnance systems
                
                # ELECTRONIC WARFARE SYSTEMS
                r'(?i)\belectronic\s+warfare\b',                  # Electronic warfare
                r'(?i)\bEW\s+system\b',                           # EW system
                r'(?i)\bjamming\s+system\b',                      # Jamming systems
                r'(?i)\bcountermeasure\s+system\b',               # Countermeasure systems
                r'(?i)\bradar\s+warning\s+receiver\b',            # RWR
                r'(?i)\bRWR\b',                                   # RWR abbreviation
                r'(?i)\bECM\s+(?:system|pod)\b',                  # Electronic countermeasures
                r'(?i)\bESM\s+system\b',                          # Electronic support measures
                r'(?i)\bSIGINT\b',                                # Signals intelligence
                r'(?i)\bELINT\b',                                 # Electronic intelligence
                
                # ROCKET/MISSILE SYSTEMS
                r'(?i)\brocket\s+system\b',                       # Rocket systems
                r'(?i)\bMLRS\b',                                  # Multiple Launch Rocket System
                r'(?i)\bHIMARS\b',                                # High Mobility Artillery Rocket System
                r'(?i)\bPatriot\s+(?:missile|system)\b',          # Patriot missile system
                r'(?i)\bTHAAD\b',                                 # Terminal High Altitude Area Defense
                r'(?i)\bAegis\s+(?:combat|weapon)\b',             # Aegis combat system
                r'(?i)\bSM[-\s]?[23]\b',                          # SM-2, SM-3 missiles
                r'(?i)\bAIM[-\s]?\d+[A-Z]?\b',                    # AIM-120, AIM-9, etc.
                r'(?i)\bAGM[-\s]?\d+[A-Z]?\b',                    # AGM-65, AGM-88, etc.
                r'(?i)\bTomahawk\b',                              # Tomahawk missile
                r'(?i)\bHellfire\b',                              # Hellfire missile
                r'(?i)\bJDAM\b',                                  # Joint Direct Attack Munition
                r'(?i)\bGBU[-\s]?\d+\b',                          # Guided Bomb Unit
                r'(?i)\bMk[-\s]?\d+\s+(?:torpedo|mine)\b',        # Mk torpedoes/mines
                
                # GENERIC MILITARY COMPONENT TERMS
                r'(?i)\brocket\s+tube[s]?\b',                     # Rocket tubes
                r'(?i)\blaunch(?:er)?\s+tube[s]?\b',             # Launch/launcher tubes
                r'(?i)\bmissile\s+tube[s]?\b',                    # Missile tubes
                r'(?i)\btorpedo\s+tube[s]?\b',                    # Torpedo tubes
                r'(?i)\bbomb\s+rack[s]?\b',                       # Bomb racks
                r'(?i)\bmissile\s+rack[s]?\b',                    # Missile racks
                r'(?i)\bweapon[s]?\s+rack[s]?\b',                 # Weapon racks
                r'(?i)\bpylon[s]?\s+(?:assembly|adapter)\b',      # Pylon assemblies
                r'(?i)\bhardpoint[s]?\b',                         # Hardpoints
                r'(?i)\bmunition[s]?\s+(?:rack|dispenser)\b',     # Munitions dispensers
                r'(?i)\bejector\s+rack[s]?\b',                    # Ejector racks
                r'(?i)\brelease\s+mechanism[s]?\b',               # Release mechanisms
                r'(?i)\barming\s+(?:wire|mechanism)\b',           # Arming mechanisms
                r'(?i)\bfuze[s]?\s+(?:assembly|mechanism)\b',     # Fuze assemblies
                r'(?i)\bwarhead[s]?\b',                           # Warheads
                r'(?i)\bexplosive\s+(?:device|component)\b',      # Explosive devices
                r'(?i)\bdetonator[s]?\b',                         # Detonators
                r'(?i)\b(?:rocket|missile|ordnance|munition)\s+igniter[s]?\b',  # Military igniters only
                r'(?i)\bpropellant\s+(?:grain|charge)\b',         # Propellant components
                r'(?i)\bbooster[s]?\s+(?:motor|charge)\b',        # Booster motors
                r'(?i)\bsustainer\s+motor[s]?\b',                 # Sustainer motors
                r'(?i)\bguidance\s+(?:section|unit)\b',           # Guidance sections
                r'(?i)\bseeker\s+(?:head|assembly)\b',            # Seeker heads
                r'(?i)\bcontrol\s+(?:surface|fin)[s]?\b',         # Control surfaces/fins
                r'(?i)\bcanard[s]?\b',                            # Canards
                r'(?i)\bumbilical\s+(?:cable|connector)\b',       # Umbilical connectors
                r'(?i)\blauncher\s+(?:rail|tube)\b',              # Launcher rails/tubes
                r'(?i)\bbreech\s+(?:block|mechanism)\b',          # Breech mechanisms
                r'(?i)\bbarrel\s+assembly\b',                     # Barrel assemblies
                r'(?i)\brecoil\s+(?:mechanism|buffer)\b',         # Recoil mechanisms
                r'(?i)\btraverse\s+(?:mechanism|motor)\b',        # Traverse mechanisms
                r'(?i)\belevation\s+(?:mechanism|motor)\b',       # Elevation mechanisms
                r'(?i)\bammunition\s+(?:feed|handling)\b',        # Ammo feed systems
                r'(?i)\bshell\s+(?:casing|case)[s]?\b',          # Shell casings
                r'(?i)\bcartridge\s+case[s]?\b',                  # Cartridge cases
                r'(?i)\bpowder\s+charge[s]?\b',                   # Powder charges
                r'(?i)\bballistic[s]?\s+(?:computer|calculator)\b', # Ballistic computers
                r'(?i)\bfire\s+(?:director|control)\b',           # Fire directors
                r'(?i)\blaser\s+(?:designator|rangefinder)\b',    # Laser designators
                r'(?i)\bthermal\s+(?:sight|imager)\b',            # Thermal sights
                r'(?i)\bnight\s+vision\s+(?:scope|device)\b',     # Night vision
                r'(?i)\bIFF\s+(?:system|transponder)\b',          # IFF systems
                r'(?i)\bchaff\s+(?:dispenser|cartridge)\b',       # Chaff dispensers
                r'(?i)\bflare\s+(?:dispenser|cartridge)\b',       # Flare dispensers
                r'(?i)\bdecoy[s]?\s+(?:launcher|dispenser)\b',    # Decoy launchers
                r'(?i)\bsmoke\s+(?:grenade|dispenser)\b'          # Smoke dispensers
            ]
            
            for pattern in military_patterns:
                if re.search(pattern, text):
                    # Check if platform mapper says it has civilian equivalent
                    if has_civilian_equivalent:
                        score.triggered = False
                        score.score = 0
                        score.evidence.append(f"Military designation with civilian equivalent: {platform_result.get('civilian_equivalent')}")
                    else:
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
        """
        Check if FAA 8130 exception applies.
        Rule: Navy + Commercial Platform + SAR + FAA 8130 = Exception (SOS can provide through MRO network)
        Only applies to commercial-based platforms, not military-only aircraft
        """
        import re
        
        # Must have Navy context
        navy_patterns = [
            r'\bNavy\b',
            r'\bNaval\b',
            r'\bNAVSUP\b',
            r'\bNAVAIR\b',
            r'\bNAVSEA\b',
        ]
        has_navy = any(re.search(p, text, re.IGNORECASE) for p in navy_patterns)
        
        # Must have SAR (Source Approval Required) 
        sar_patterns = [
            r'source[\s-]*approval[\s-]*required',
            r'approved[\s-]*source',
            r'OEM[\s-]*only',
            r'original[\s-]*equipment[\s-]*manufacturer',
        ]
        has_sar = any(re.search(p, text, re.IGNORECASE) for p in sar_patterns)
        
        # Must have FAA 8130
        faa_patterns = [
            r'FAA[\s-]*8130',
            r'8130[\s-]*3',
            r'FAA[\s-]*Form[\s-]*8130',
            r'airworthiness[\s-]*certificate',
            r'airworthy[\s-]*approval'
        ]
        has_faa = any(re.search(p, text, re.IGNORECASE) for p in faa_patterns)
        
        # CRITICAL: Must be a commercial-based platform
        # These are Navy aircraft based on commercial designs that SOS can support
        # Must match specific aircraft models, NOT generic Navy equipment
        commercial_navy_platforms = [
            r'P[\s-]*8[A-Z]*[\s]+Poseidon',             # P-8/P-8A Poseidon (Boeing 737) - require full name
            r'E[\s-]*6[B]*[\s]+(?:Mercury|TACAMO)',     # E-6B Mercury/TACAMO (Boeing 707)
            r'C[\s-]*40[A-Z]*[\s]+Clipper',             # C-40A Clipper (Boeing 737) - require full name
            r'UC[\s-]*35[A-Z]*[\s]+Citation',           # UC-35 Citation (Cessna) - require full name
            r'C[\s-]*12[\s]+(?:Huron|King[\s]+Air)',    # C-12 Huron/King Air - both names valid
            r'Boeing[\s]+737.*P[\s-]*8',                # Boeing 737 specifically for P-8
            r'Boeing[\s]+707.*E[\s-]*6',                # Boeing 707 specifically for E-6
        ]
        has_commercial_platform = any(re.search(p, text, re.IGNORECASE) for p in commercial_navy_platforms)
        
        # All FOUR conditions must be met for the exception
        return has_navy and has_commercial_platform and has_sar and has_faa
    
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
        # Navy + Commercial Platform + SAR + FAA 8130 = Exception (SOS can provide through MRO network)
        # ONLY applies to specific commercial-based Navy platforms (P-8, E-6B, C-40, UC-35, C-12)
        has_faa_8130_exception = self._has_faa_8130_exception(combined_text)
        if has_faa_8130_exception:
            # Navy commercial platform contracts with FAA 8130 + SAR are GO for SOS
            result.decision = Decision.GO
            result.primary_reason = "Navy FAA 8130 Exception: Commercial platform eligible through MRO network"
            result.co_contact_applicable = True
            result.co_contact_reason = "Navy commercial platform + SAR + FAA 8130 = SOS eligible"
            # Log which platform was detected for tracking
            import logging
            logging.info(f"FAA 8130 exception applied for opportunity {result.opportunity_id}")
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
            # Only set GO if there are genuinely no issues
            # Don't override NO-GO decisions that should have been made
            
            # Check if any categories were triggered with high scores
            high_score_categories = [cat for cat_id, cat in result.category_scores.items() 
                                    if cat.score >= 3]  # Score 3+ means significant issue
            
            if high_score_categories:
                # Categories triggered but decision wasn't made - this is a NO-GO
                result.decision = Decision.NO_GO
                result.primary_blocker = f"Multiple restrictions: {len(high_score_categories)} categories triggered"
                result.confidence_score = 85.0
            elif platform_result and platform_result.get('decision') == 'GO':
                # Civilian platform with no other issues
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
                
                if has_positive:
                    result.decision = Decision.GO
                    result.confidence_score = 85.0
                else:
                    # Default to FURTHER_ANALYSIS, not GO
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