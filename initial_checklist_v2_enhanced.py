import re
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime, date
from enum import Enum

logger = logging.getLogger(__name__)

class Decision(Enum):
    """Enumeration for assessment decisions."""
    GO = "GO"
    NO_GO = "NO-GO"
    NEEDS_ANALYSIS = "NEEDS ANALYSIS"
    PASS = "PASS" # Used for individual checks that don't terminate the process

class CheckResult:
    """Stores the result of a single checklist item."""
    def __init__(self, check_name: str, decision: Decision, reason: str, quote: str = ""):
        self.check_name = check_name
        self.decision = decision
        self.reason = reason
        self.quote = quote

    def __repr__(self):
        return f"CheckResult(check='{self.check_name}', decision={self.decision.value}, reason='{self.reason}')"

class InitialChecklistFilterV2Enhanced:
    """
    Enhanced implementation of SOS Initial Assessment Logic v4.0 with improved patterns
    based on comprehensive documentation analysis and real SAR language patterns.
    """

    def __init__(self, platform_guide: Optional[Dict] = None):
        """
        Initializes the filter with compiled regular expressions for efficiency.

        Args:
            platform_guide (Optional[Dict]): A dictionary defining platform viability.
                                              Keys: 'pure_military', 'conditional', 'always_go'.
                                              Values: List of platform names/patterns.
        """
        # --- V2: Enhanced Regular Expressions ---

        # Phase 0.1: Aviation Patterns - Expanded based on comprehensive checklist
        self.aviation_regex = re.compile(
            '|'.join([
                r'\b(aircraft|helicopter|rotorcraft|airplane|aerospace|avionics)\b',
                r'\b(Boeing|Airbus|Bell|Sikorsky|Lockheed|Northrop|McDonnell)\b',
                r'\b(engine|landing gear|hydraulic|propeller|flight control)\b',
                r'\b(ground support equipment|GSE|AGE|test equipment)\b',
                r'\bPSC\s*(15\d{2}|16\d{2}|17\d{2})\b',
                r'\bNAICS\s*3364\d{2}\b',
                r'\b(MRO|maintenance|repair|overhaul)\b',
                r'\b(spare parts|rotable|consumable)\b'
            ]), re.IGNORECASE
        )

        # Phase 0.3: Platform Viability - Enhanced with comprehensive platform list
        # Use negative lookbehind to avoid matching part numbers (P/N, NSN, etc.)
        self.PLATFORM_CONTEXT_PATTERN = r"(?<!(P/N|Part Number|Drawing|Number|No|Item|NSN)[:;\s-]{1,5})"

        # Enhanced platform guide based on SOS Platform Identification Guide
        self.platform_guide = platform_guide or {
            'pure_military': [
                r'F-15', r'F-16', r'F-18', r'F-22', r'F-35', r'A-10', r'AV-8B', 
                r'B-1B', r'B-2', r'B-52', r'B-21', r'C-5', r'C-17', r'V-22', 
                r'MQ-9', r'MQ-1', r'E-2', r'AH-64', r'CH-53', r'OA-10', r'AC-130'
            ],
            'conditional': [
                r'P-3', r'A-29', r'KC-135', r'C-130', r'C-27J', r'CH-47'
            ],
            'always_go': [
                r'KC-46', r'P-8', r'C-40', r'C-32', r'VC-25', r'E-3', r'E-6', r'E-8',
                r'E-4B', r'E-7', r'KC-10', r'C-12', r'UC-12', r'C-26', r'C-20', r'C-21',
                r'C-37', r'UC-35', r'C-47', r'UV-18', r'C-23', r'CN-235', r'C-144',
                r'UH-60', r'MH-60', r'HH-60', r'VH-60', r'MH-65', r'UH-72', r'TH-57',
                r'UH-1', r'TH-67', r'OH-58', r'T-34', r'T-6', r'T-44', r'T-1', r'AT-802U',
                r'Boeing\s*7\d{2}', r'Bell\s*\d{3}', r'King\s*Air', r'Citation',
                r'Gulfstream', r'Learjet', r'Beechcraft', r'Cessna', r'Sikorsky\s*S-70'
            ]
        }

        # Phase 1: Enhanced Hard Stop Patterns based on SAR Language Patterns analysis
        self.sar_regex = re.compile(r'source approval required|approved source list|qualified suppliers list|\bQPL\b|\bQML\b|requires engineering source approval|Government source approval required|military specification|requires engineering source approval by the design control activity|Source Approval Request|SAR package|SAMSAR|must submit.{0,20}Source Approval|approved source only|\bAMC\s*[345]\b|\bAMSC\s*[CDPR]\b', re.IGNORECASE)
        
        self.sole_source_regex = re.compile(r'sole source to (?!(Source One Spares))|only one responsible source|single source to (?!(Source One Spares))', re.IGNORECASE)
        
        self.intent_to_sole_source_regex = re.compile(r'intent to sole source|brand name justification', re.IGNORECASE)
        
        self.tech_data_regex = re.compile(r'drawings not available|technical data not available|OEM owns technical data|proprietary technical data|no GFI|government does not have|contractor will not receive|data rights|proprietary data', re.IGNORECASE)
        
        self.security_regex = re.compile(r'security clearance|secret|top secret|classified|facility clearance|personnel clearance|security requirements', re.IGNORECASE)
        
        self.new_parts_regex = re.compile(r'factory new only|new manufacture only|no refurbished|no rebuilt|no overhauled|no used|new condition only', re.IGNORECASE)
        
        self.prohibited_certs_regex = re.compile(r'AS9100.{0,10}required|NADCAP.{0,10}required', re.IGNORECASE)
        
        self.oem_regex = re.compile(r'OEM only|authorized distributor|OEM distributor|factory authorized dealer|OEM direct traceability only|authorized distributor required|factory authorized|OEM approved only|\bAMSC\s*B\b', re.IGNORECASE)
        
        self.itar_regex = re.compile(r'ITAR|export control|international traffic in arms|ITAR registration required|export license required|EAR', re.IGNORECASE)

        # Additional patterns for enhanced detection
        self.commercial_indicators_regex = re.compile(r'FAR Part 12|commercial item|commercial off.{0,10}shelf|COTS|14 CFR|FAA certified', re.IGNORECASE)
        
        self.sled_regex = re.compile(r'\b(state|county|city|municipal|school district|university|state agency)\b', re.IGNORECASE)


    def _find_match_with_quote(self, regex: re.Pattern, text: str, context_window: int = 50) -> Optional[str]:
        """Finds a regex match and returns the matched text with surrounding context."""
        match = regex.search(text)
        if match:
            start = max(0, match.start() - context_window)
            end = min(len(text), match.end() + context_window)
            context = text[start:end].strip()
            return context
        return None

    def extract_text_from_opportunity(self, opp: Dict) -> str:
        """Extracts and concatenates all searchable text fields from an opportunity object."""
        text_fields = [
            opp.get('title', ''),
            opp.get('description_text', ''),
            opp.get('ai_summary', ''),
            opp.get('source_id', ''),
            opp.get('set_aside', '')
        ]
        # Include document text if it has been extracted by a previous process
        for doc in opp.get('documents', []):
            text_fields.append(doc.get('text_extract', ''))
        return ' '.join(filter(None, text_fields))

    # --- PHASE 0 CHECKS ---

    def check_aviation_related(self, text: str) -> CheckResult:
        """Phase 0.1: Is this aviation-related?"""
        quote = self._find_match_with_quote(self.aviation_regex, text)
        if quote:
            return CheckResult("Aviation Check", Decision.PASS, "Aviation-related terms found.", quote)
        return CheckResult("Aviation Check", Decision.NO_GO, "Not aviation-related.", "No aviation-related terms found.")

    def check_current(self, opp: Dict) -> CheckResult:
        """Phase 0.2: Is this opportunity current?"""
        due_date_str = opp.get('due_date')
        if not due_date_str:
            return CheckResult("Currency Check", Decision.NEEDS_ANALYSIS, "Due date not specified.", "No response due date found.")
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            if due_date < date.today():
                return CheckResult("Currency Check", Decision.NO_GO, f"Expired on {due_date_str}.", f"Response Due: {due_date_str}")
            return CheckResult("Currency Check", Decision.PASS, "Opportunity is current.", f"Response Due: {due_date_str}")
        except ValueError:
            return CheckResult("Currency Check", Decision.NEEDS_ANALYSIS, "Cannot parse due date.", f"Unclear due date format: {due_date_str}")

    def check_platform_viability(self, text: str) -> CheckResult:
        """
        Phase 0.3: Enhanced Platform Viability Check with comprehensive platform guide.
        """
        # Enhanced context words for platform validation
        positive_context = ['for', 'aircraft', 'platform', 'system', 'helicopter', 'overhaul of', 'maintenance on', 'spare parts for', 'components for']
        negative_context = ['p/n', 'part number', 'drawing', 'nsn', 'item number', 'model number']

        for category, platforms in self.platform_guide.items():
            for platform in platforms:
                # V2 Enhancement: Use the context-aware pattern
                full_pattern = self.PLATFORM_CONTEXT_PATTERN + r'\b' + platform + r'\b'
                try:
                    # Find all potential matches
                    for match in re.finditer(full_pattern, text, re.IGNORECASE):
                        confidence_score = 0
                        # Analyze a window of text around the match
                        start = max(0, match.start() - 40)
                        end = min(len(text), match.end() + 40)
                        context_snippet = text[start:end].lower()

                        for word in positive_context:
                            if word in context_snippet:
                                confidence_score += 1
                        for word in negative_context:
                            if word in context_snippet:
                                confidence_score -= 1

                        # If confidence is high enough, make a decision based on the category
                        if confidence_score >= 1:
                            quote = match.group(0)
                            if category == 'pure_military':
                                return CheckResult("Platform Check", Decision.NO_GO, f"High confidence match for pure military platform: {quote}", quote)
                            elif category == 'conditional':
                                return CheckResult("Platform Check", Decision.NEEDS_ANALYSIS, f"Conditional platform found: {quote}", quote)
                            # 'always_go' platforms don't need a hard PASS here, just absence of NO_GO

                except re.error as e:
                    logger.error(f"Regex error for platform '{platform}': {e}")
                    continue

        return CheckResult("Platform Check", Decision.PASS, "No restricted platforms detected with high confidence.", "")

    def check_sled_opportunity(self, text: str) -> CheckResult:
        """Check for State/Local/Education opportunities which are always viable."""
        quote = self._find_match_with_quote(self.sled_regex, text)
        if quote:
            return CheckResult("SLED Check", Decision.PASS, "State/Local/Education opportunity - enhanced viability", quote)
        return CheckResult("SLED Check", Decision.PASS, "Not identified as SLED opportunity", "")

    def check_commercial_indicators(self, text: str) -> CheckResult:
        """Check for positive commercial indicators."""
        quote = self._find_match_with_quote(self.commercial_indicators_regex, text)
        if quote:
            return CheckResult("Commercial Indicators", Decision.PASS, "Positive commercial indicators found", quote)
        return CheckResult("Commercial Indicators", Decision.PASS, "No specific commercial indicators", "")

    # --- PHASE 1 CHECKS ---

    def run_phase1_checks(self, text: str) -> List[CheckResult]:
        """Runs all Phase 1 hard stop checks with enhanced patterns."""
        checks_to_run = [
            ("SAR Check", self.sar_regex, Decision.NO_GO, "Military SAR Present."),
            ("OEM Restriction Check", self.oem_regex, Decision.NO_GO, "OEM distribution restriction found."),
            ("Sole Source Check", self.sole_source_regex, Decision.NO_GO, "Sole source to another company."),
            ("Tech Data Check", self.tech_data_regex, Decision.NO_GO, "Technical data is not available."),
            ("Security Check", self.security_regex, Decision.NO_GO, "Security clearance required."),
            ("New Parts Only Check", self.new_parts_regex, Decision.NO_GO, "'New parts only' restriction found."),
            ("Prohibited Certs Check", self.prohibited_certs_regex, Decision.NO_GO, "Prohibited certification (AS9100/NADCAP) required."),
            ("Intent to Sole Source Check", self.intent_to_sole_source_regex, Decision.NEEDS_ANALYSIS, "Intent to sole source or brand name justification found."),
            ("ITAR Check", self.itar_regex, Decision.NEEDS_ANALYSIS, "ITAR/Export control language found.")
        ]

        results = []
        for name, regex, decision, reason in checks_to_run:
            quote = self._find_match_with_quote(regex, text)
            if quote:
                # This check has been triggered, so we record the result and stop if it's a NO-GO.
                result = CheckResult(name, decision, reason, quote)
                results.append(result)
                if decision == Decision.NO_GO:
                    return results # Stop at the first hard NO-GO
            else:
                # This check was not triggered, record as a PASS for this specific check.
                results.append(CheckResult(name, Decision.PASS, "No matching restrictions found.", ""))

        return results

    def generate_pipeline_title(self, opp: Dict, decision: Decision) -> str:
        """Generates standardized pipeline title format for GO decisions."""
        if decision != Decision.GO:
            return ""
        
        # Extract key information
        part_numbers = self._extract_part_numbers(opp)
        quantity = self._extract_quantity(opp)
        announcement = opp.get('source_id', 'Unknown')
        aircraft = self._extract_aircraft(opp)
        description = self._extract_description(opp)
        
        return f"PN: {part_numbers} | Qty: {quantity} | {announcement} | {aircraft} | {description}"

    def _extract_part_numbers(self, opp: Dict) -> str:
        """Extract part numbers from opportunity, max 3."""
        text = self.extract_text_from_opportunity(opp)
        # Simple regex to find part numbers - could be enhanced
        pn_pattern = r'P/?N:?\s*([A-Z0-9-]{5,20})'
        matches = re.findall(pn_pattern, text, re.IGNORECASE)
        if len(matches) > 3:
            return "Various"
        elif matches:
            return ", ".join(matches[:3])
        return "Various"

    def _extract_quantity(self, opp: Dict) -> str:
        """Extract quantity from opportunity."""
        text = self.extract_text_from_opportunity(opp)
        qty_pattern = r'(?:quantity|qty|each):?\s*(\d+)'
        match = re.search(qty_pattern, text, re.IGNORECASE)
        return match.group(1) if match else "Unk"

    def _extract_aircraft(self, opp: Dict) -> str:
        """Extract aircraft type from opportunity."""
        text = self.extract_text_from_opportunity(opp)
        # Check for known aircraft patterns
        for category, platforms in self.platform_guide.items():
            for platform in platforms:
                if re.search(r'\b' + platform + r'\b', text, re.IGNORECASE):
                    return platform
        return "Support Equipment"

    def _extract_description(self, opp: Dict) -> str:
        """Extract brief description (2-4 words max)."""
        text = self.extract_text_from_opportunity(opp).lower()
        if 'overhaul' in text:
            return "overhaul parts"
        elif 'repair' in text:
            return "repair services"
        elif 'spare' in text:
            return "spare parts"
        elif 'purchase' in text:
            return "purchase items"
        return "aviation support"

    def assess_opportunity(self, opp: Dict) -> Tuple[Decision, List[CheckResult]]:
        """
        Runs the enhanced full Phase 0 and Phase 1 assessment on an opportunity.

        Returns:
            A tuple containing the final decision and a list of all check results.
        """
        text = self.extract_text_from_opportunity(opp)
        all_results = []

        # --- Run Phase 0 ---
        phase0_checks = [
            self.check_aviation_related(text),
            self.check_current(opp),
            self.check_sled_opportunity(text),
            self.check_commercial_indicators(text),
            self.check_platform_viability(text)
        ]
        all_results.extend(phase0_checks)
        
        # Check for immediate disqualifiers in Phase 0
        for result in phase0_checks:
            if result.decision == Decision.NO_GO:
                return Decision.NO_GO, all_results

        # --- Run Phase 1 ---
        phase1_results = self.run_phase1_checks(text)
        all_results.extend(phase1_results)

        # --- Determine Final Decision ---
        final_decision = Decision.GO # Assume GO unless a blocker is found
        for result in all_results:
            if result.decision == Decision.NO_GO:
                return Decision.NO_GO, all_results # A single NO_GO fails the entire assessment
            if result.decision == Decision.NEEDS_ANALYSIS:
                final_decision = Decision.NEEDS_ANALYSIS # Mark for review but continue checking for hard NO_GOs

        return final_decision, all_results

    def generate_assessment_report(self, opp: Dict) -> Dict:
        """Generate a comprehensive assessment report."""
        decision, results = self.assess_opportunity(opp)
        
        report = {
            'opportunity_id': opp.get('source_id', 'Unknown'),
            'final_decision': decision.value,
            'pipeline_title': self.generate_pipeline_title(opp, decision) if decision == Decision.GO else "",
            'assessment_summary': self._generate_summary(results),
            'detailed_results': [
                {
                    'check': result.check_name,
                    'decision': result.decision.value,
                    'reason': result.reason,
                    'quote': result.quote
                } for result in results
            ],
            'next_actions': self._generate_next_actions(decision, results)
        }
        
        return report

    def _generate_summary(self, results: List[CheckResult]) -> str:
        """Generate a brief summary of the assessment."""
        no_gos = [r for r in results if r.decision == Decision.NO_GO]
        needs_analysis = [r for r in results if r.decision == Decision.NEEDS_ANALYSIS]
        
        if no_gos:
            return f"NO-GO due to: {', '.join([r.check_name for r in no_gos])}"
        elif needs_analysis:
            return f"NEEDS ANALYSIS due to: {', '.join([r.check_name for r in needs_analysis])}"
        else:
            return "All checks passed - opportunity viable for pursuit"

    def _generate_next_actions(self, decision: Decision, results: List[CheckResult]) -> List[str]:
        """Generate specific next action recommendations."""
        actions = []
        
        if decision == Decision.NO_GO:
            # Check if CO contact is warranted
            sar_failures = [r for r in results if r.check_name == "SAR Check" and r.decision == Decision.NO_GO]
            oem_failures = [r for r in results if r.check_name == "OEM Restriction Check" and r.decision == Decision.NO_GO]
            
            if sar_failures or oem_failures:
                actions.append("Contact Contracting Officer about future acceptability of refurbished/surplus parts")
                
        elif decision == Decision.NEEDS_ANALYSIS:
            intent_sole_source = [r for r in results if r.check_name == "Intent to Sole Source Check" and r.decision == Decision.NEEDS_ANALYSIS]
            if intent_sole_source:
                actions.append("Consider challenging sole source justification")
                
        elif decision == Decision.GO:
            actions.append("Proceed with bid preparation")
            actions.append("Conduct detailed technical review")
            
        return actions
