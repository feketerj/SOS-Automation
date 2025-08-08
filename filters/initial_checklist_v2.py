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

class InitialChecklistFilterV2:
    """
    Exact implementation of SOS Initial Assessment Logic v4.0 following the documented framework.
    
    CRITICAL RULES (from v4.0 documentation):
    1. Quote the government's exact language - Never paraphrase or summarize
    2. Include page/section numbers for every quote  
    3. If information not found, state "No [topic] language found in document"
    4. Follow checks in exact order - Stop at first NO-GO
    5. Hard stops OVERRIDE all positive indicators
    6. When in doubt, default to "NEEDS FURTHER ANALYSIS"
    """

    def __init__(self, platform_guide: Optional[Dict] = None):
        """Initialize filter with exact patterns from SOS Initial Checklist Logic v4.0"""
        
        # Phase 0.1: Aviation-related terms (COMPREHENSIVE for Question 1)
        self.aviation_regex = re.compile(
            '|'.join([
                # Aircraft types (primary)
                r'\b(aircraft|helicopter|rotorcraft|airplane|plane|jet|fighter|bomber|transport)\b',
                # Aircraft manufacturers (comprehensive)
                r'\b(Boeing|Airbus|Bell|Sikorsky|Lockheed|Northrop|Grumman|McDonnell|Douglas|Cessna|Beechcraft|Piper|Gulfstream|Bombardier|Embraer|Raytheon)\b',
                # Military aircraft designators (comprehensive)
                r'\b(C-130|KC-46|P-8|F-16|F-15|F-22|F-35|UH-60|CH-47|KC-135|C-17|B-1|B-2|B-52|AH-64|CH-53|MH-60|HH-60|V-22|C-40|P-3|E-3|E-6|E-8|A-10|T-6|T-34|T-38|T-45)\b',
                # Aircraft components and systems
                r'\b(engine|avionics|landing\s+gear|hydraulic|propeller|rotor|turbine|compressor|nacelle|cowling|fuselage|wing|aileron|rudder|elevator|flap|slat|spoiler)\b',
                r'\b(flight\s+control|autopilot|navigation|radar|transponder|altimeter|airspeed|pitot|static|pneumatic)\b',
                r'\b(cockpit|cabin|cargo\s+bay|wheel\s+well|fuel\s+system|electrical\s+system|environmental\s+control)\b',
                # Aircraft maintenance and support
                r'\b(ground\s+support\s+equipment|GSE|AGE|aerospace|maintenance|overhaul|repair|modification|MRO)\b',
                r'\b(airworthiness|flight\s+worthy|air\s+worthy|faa\s+approved|mil\s+spec|aviation)\b',
                r'\b(hangar|ramp|tarmac|runway|taxiway|apron|airport|airfield|air\s+base|flight\s+line)\b',
                # Aviation codes and classifications
                r'\bPSC\s*1[567]\d{2}\b',  # PSC codes 1500-1799 (aircraft/aerospace)
                r'\bNAICS\s*3364\d{2}\b',  # NAICS 336400s (aerospace)
                # Aviation terms and operations
                r'\b(flight|aviation|aeronautical|aerospace|air\s+force|navy|marine\s+corps|coast\s+guard)\b',
                r'\b(pilot|aircrew|crew\s+chief|maintenance\s+technician|avionics\s+technician)\b',
                r'\b(de-icing|anti-icing|ice\s+protection|weather\s+radar|terrain\s+avoidance)\b',
                # Common aviation part types
                r'\b(actuator|sensor|valve|pump|filter|bearing|seal|gasket|harness|cable|antenna)\b.*\b(aircraft|aviation|flight)\b',
                r'\b(aircraft|aviation|flight)\b.*\b(actuator|sensor|valve|pump|filter|bearing|seal|gasket|harness|cable|antenna)\b'
            ]), re.IGNORECASE
        )

        # Platform Guide (EXACT from SOS Platform Identification Guide v4.0)
        self.platform_guide = platform_guide or {
            'pure_military_no_go': [
                # Pure Military - NO-GO
                'C-17 Globemaster III', 'AH-64 Apache', 'CH-47 Chinook', 'CH-53',
                'C-130 Hercules', 'C-27J Spartan', 'HC-27J', 'OA-10 Thunderbolt II', 'AC-130'
            ],
            'conditional_analysis': [
                # CONDITIONAL - Needs Analysis
                'P-3 Orion', 'A-29 Super Tucano'
            ],
            'always_go': [
                # Boeing Military Aircraft with Civilian Equivalents - ALWAYS GO
                'KC-46 Pegasus', 'P-8 Poseidon', 'C-40 Clipper', 'C-32', 'VC-25', 
                'E-3 Sentry', 'E-6 Mercury', 'E-8 JSTARS', 'KC-135 Stratotanker', 
                'E-4B', 'E-7 Wedgetail', 'KC-10 Extender',
                # Other Transport Aircraft - GO
                'C-12 Huron', 'UC-12', 'C-26 Metroliner', 'C-20', 'C-21', 'C-37', 
                'UC-35', 'C-47 Skytrain', 'UV-18 Twin Otter', 'C-23 Sherpa', 
                'CN-235', 'C-144 Ocean Sentry', 'CL-415',
                # Military Helicopters with Civilian Equivalents - GO
                'UH-60 Black Hawk', 'MH-60', 'HH-60 Pave Hawk', 'VH-60', 
                'MH-65 Dolphin', 'UH-72 Lakota', 'TH-57 Sea Ranger', 'UH-1', 
                'TH-67 Creek', 'OH-58 Kiowa',
                # Trainer Aircraft - GO
                'T-34 Mentor', 'T-6 Texan II', 'T-44 Pegasus', 'T-1 Jayhawk',
                # Special Mission Aircraft - GO
                'AT-802U',
                # Civilian Aircraft Names (always GO)
                'Boeing 737', 'Boeing 767', 'Boeing 747', 'Boeing 757', 'Boeing 707',
                'King Air', 'Beechcraft', 'Cessna', 'Bell 206', 'Bell 407',
                'Gulfstream', 'Learjet', 'Sikorsky S-70', 'Eurocopter'
            ]
        }

        # Phase 1: EXACT Hard Stop Patterns from v4.0 documentation
        
        # CHECK 1: Source Approval Required (SAR) - EXACT phrases and AMC/AMSC codes from v4.0 + Bid Matrix
        self.sar_regex = re.compile(
            '|'.join([
                r'source\s+approval\s+required',
                r'approved\s+source\s+list', 
                r'qualified\s+suppliers?\s+list',
                r'\bQPL\b',  # Qualified Products List
                r'\bQML\b',  # Qualified Manufacturers List
                r'requires\s+engineering\s+source\s+approval',
                r'Government\s+source\s+approval\s+required',
                r'military\s+specification',
                # AMC/AMSC codes that indicate NO-GO per bid matrix
                r'\bAMC\s*[345]\b',      # AMC 3,4,5 = NOT until SAR approved / No unless teaming / No
                r'\bAMSC\s*[CDPR]\b',    # AMSC C,D,P,R = No until SAR / No / No / No unless OEM deal  
                r'\bAMSC\s*B\b',         # AMSC B = Only if OEM lists SOS
                r'\bAMSC\s*H\b',         # AMSC H = Unlikely
                r'\b3B\b',               # 3B = Only via OEM listing
                r'\b3P\b'                # 3P = No
            ]), re.IGNORECASE
        )
        
        # AMC/AMSC codes that SOS CAN bid (per bid matrix)
        self.acceptable_amc_amsc_regex = re.compile(
            '|'.join([
                r'\bAMC\s*[12]\b',       # AMC 1,2 = Yes
                r'\bAMSC\s*[AGZ]\b',     # AMSC A,G,Z = Possibly/Yes/Yes
                r'\b1[GR]\b',            # 1G,1R = Yes
                r'\b2G\b'                # 2G = Yes
            ]), re.IGNORECASE
        )
        
        # CHECK 2: Sole Source Detection - Question 2 Methodical Approach
        # Enhanced patterns to distinguish ACTUAL sole source vs intent language
        self.sole_source_regex = re.compile(
            '|'.join([
                # HARD BLOCKERS - Actual sole source announcements
                r'sole\s+source\s+to\s+[A-Za-z\s&,\.]+(?:Company|Corp|Corporation|LLC|Inc)',
                r'single\s+source\s+to\s+[A-Za-z\s&,\.]+(?:Company|Corp|Corporation|LLC|Inc)',
                r'awarded\s+on\s+a\s+sole\s+source\s+basis\s+to',
                r'sole\s+source\s+award\s+to',
                r'sole\s+source\s+procurement\s+from',
                r'this\s+is\s+a\s+sole\s+source\s+procurement',
                r'this\s+procurement\s+is\s+sole\s+source',
                
                # ANALYSIS NEEDED - Intent language (challengeable)
                r'intent\s+to\s+sole\s+source',
                r'intent\s+to\s+award.*sole\s+source',
                r'intends\s+to\s+sole\s+source',
                r'plans\s+to\s+sole\s+source',
                r'considering\s+sole\s+source',
                
                # ANALYSIS NEEDED - Brand name or equal opportunities  
                r'brand\s+name.*equal',
                r'or\s+equal\s+to',
                r'brand\s+name\s+or\s+approved\s+equal',
                
                # HARD BLOCKERS - Manufacturer-specific requirements (effective sole source)
                r'in\s+accordance\s+with\s+[A-Za-z\s&,\.]+\s+(?:Company|Corp|Corporation|LLC|Inc).*drawing\s+number',
                r'manufactured.*tested.*inspected.*in\s+accordance\s+with\s+[A-Za-z\s&,\.]+.*drawing\s+number',
                r'[A-Za-z\s&,\.]+\s+(?:Company|Corp|Corporation|LLC|Inc).*drawing\s+number',
                r'[A-Za-z\s&,\.]+\s+(?:Company|Corp|Corporation|LLC|Inc).*Company\s+Name',
                r'facility\s+identified\s+within\s+this\s+SOW.*(?:Company|Corp|Corporation|LLC|Inc)',
                
                # HARD BLOCKERS - Proprietary/OEM only requirements
                r'proprietary\s+design\s+of',
                r'OEM\s+proprietary',
                r'only\s+available\s+from\s+[A-Za-z\s&,\.]+(?:Company|Corp|Corporation|LLC|Inc)',
                
                # General sole source terms for catching any sole source language
                r'sole\s+source',
                r'only\s+one\s+responsible\s+source',
                r'single\s+source',
                r'brand\s+name\s+justification'
            ]), re.IGNORECASE
        )
        
        # CHECK 3: Technical Data Availability - Binary Decision (EXACT from v4.0)
        # BLOCKER: Not available or OEM proprietary
        # GO: Government owns or commonly available
        self.tech_data_regex = re.compile(
            '|'.join([
                # BLOCKERS - Drawings/data not available (flexible patterns)
                r'drawings?\s+(?:are\s+)?not\s+available',
                r'technical\s+data\s+(?:is\s+)?not\s+available',
                r'no\s+technical\s+data\s+available',
                r'data\s+(?:is\s+)?not\s+available',
                r'drawings?\s+will\s+not\s+be\s+provided',
                r'no\s+drawings?\s+provided',
                
                # BLOCKERS - OEM proprietary ownership
                r'OEM\s+owns\s+technical\s+data',
                r'proprietary\s+to\s+(?:the\s+)?manufacturer',
                r'manufacturer\s+proprietary\s+data',
                r'proprietary\s+technical\s+data',
                r'contractor\s+owns\s+data\s+rights',
                
                # BLOCKERS - Government doesn't have rights
                r'government\s+does\s+not\s+have\s+(?:the\s+)?(?:technical\s+)?(?:data\s+rights?|drawings?)',
                r'government\s+does\s+not\s+own\s+(?:the\s+)?(?:technical\s+)?data',
                r'no\s+government\s+furnished\s+information',
                r'no\s+GFI',
                r'contractor\s+will\s+not\s+receive\s+technical\s+data',
                
                # POSITIVE INDICATORS - Government owns or available
                r'government\s+owns\s+(?:the\s+)?technical\s+data',
                r'government\s+has\s+data\s+rights',
                r'technical\s+data\s+available\s+upon\s+award',
                r'drawings?\s+available\s+upon\s+award',
                r'government\s+furnished\s+information',
                r'GFI\s+provided',
                r'technical\s+data\s+package\s+available',
                r'drawings?\s+will\s+be\s+provided',
                r'commercially\s+available\s+drawings?',
                r'standard\s+commercial\s+drawings?'
            ]), re.IGNORECASE
        )
        
        # CHECK 4: Security Clearance Requirements - EXACT phrases
        self.security_regex = re.compile(
            '|'.join([
                r'security\s+clearance',
                r'\bsecret\b',
                r'top\s+secret',
                r'\bclassified\b',
                r'facility\s+clearance',
                r'personnel\s+clearance'
            ]), re.IGNORECASE
        )
        
        # CHECK 5: New Parts Only Restriction - EXACT phrases  
        self.new_parts_regex = re.compile(
            '|'.join([
                r'factory\s+new\s+only',
                r'new\s+manufacture\s+only',
                r'no\s+refurbished',
                r'no\s+rebuilt', 
                r'no\s+overhauled',
                r'no\s+used',
                r'new\s+condition\s+only'
            ]), re.IGNORECASE
        )
        
        # CHECK 6: Prohibited Certifications - EXACT phrases
        self.prohibited_certs_regex = re.compile(
            '|'.join([
                r'AS9100',  # SOS does NOT have AS9100
                r'NADCAP'   # SOS does NOT have NADCAP
            ]), re.IGNORECASE
        )
        
        # CHECK 7: ITAR/Export Control - EXACT phrases (REQUIRES ANALYSIS not NO-GO per docs)
        self.itar_regex = re.compile(
            '|'.join([
                r'\bITAR\b',
                r'export\s+control',
                r'export\s+license\s+required',
                r'\bEAR\b',
                r'international\s+traffic\s+in\s+arms'
            ]), re.IGNORECASE
        )
        
        # CHECK 8: OEM Distribution Restrictions - EXACT phrases
        self.oem_regex = re.compile(
            '|'.join([
                r'OEM\s+only',
                r'authorized\s+distributor',
                r'OEM\s+distributor',
                r'factory\s+authorized\s+dealer',
                r'Source-Control\s+drawing.*OEM\s+list\s+governs',
                r'\bAMSC\s*B\b'  # Item on Source-Control drawing – OEM list governs
            ]), re.IGNORECASE
        )


    def _find_match_with_quote(self, regex, text: str, context_window: int = 50) -> Optional[str]:
        """Finds a regex match and returns the matched text with surrounding context."""
        match = regex.search(text)
        if match:
            start = max(0, match.start() - context_window)
            end = min(len(text), match.end() + context_window)
            context = text[start:end].strip()
            return context
        return None

    def extract_text_from_opportunity(self, opp) -> str:
        """Extracts and concatenates all searchable text fields from an opportunity object."""
        # Include the full analysis text if available from RAG processing
        if 'full_analysis_text' in opp:
            return opp['full_analysis_text']
            
        # Otherwise, combine available fields
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

    # PHASE 0 CHECKS (EXACT sequence from v4.0 documentation)

    def check_0_1_aviation_related(self, text: str) -> CheckResult:
        """
        CHECK 0.1: IS THIS AVIATION-RELATED? (EXACT from v4.0)
        Decision Logic:
        - IF aviation-related terms are found → CONTINUE
        - IF NOT aviation-related terms are found → NO-GO (Not aviation-related)
        """
        quote = self._find_match_with_quote(self.aviation_regex, text)
        if quote:
            return CheckResult("0.1 Aviation Check", Decision.PASS, "Aviation-related terms found", quote)
        return CheckResult("0.1 Aviation Check", Decision.NO_GO, "Not aviation-related", "No aviation-related terms found in document")

    def check_0_2_opportunity_current(self, opp) -> CheckResult:
        """
        CHECK 0.2: IS THIS OPPORTUNITY CURRENT? (EXACT from v4.0)
        Decision Logic:
        - IF a future or current date is specified → CONTINUE
        - IF the date is in the past (expired) → NO-GO (Expired)
        """
        # Check multiple possible date fields
        response_date = opp.get('response_date') or opp.get('due_date') or opp.get('closing_date')
        
        if not response_date:
            return CheckResult("0.2 Currency Check", Decision.NEEDS_ANALYSIS, "Response due date not specified", "No response due date found in document")
        
        try:
            # Handle different date formats
            if isinstance(response_date, str):
                # Try common date formats
                for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%m-%d-%Y', '%Y/%m/%d']:
                    try:
                        due_date = datetime.strptime(response_date, fmt).date()
                        break
                    except ValueError:
                        continue
                else:
                    return CheckResult("0.2 Currency Check", Decision.NEEDS_ANALYSIS, f"Cannot parse due date: {response_date}", f"Unclear due date format: {response_date}")
            else:
                due_date = response_date if isinstance(response_date, date) else date.today()
            
            today = date.today()
            if due_date < today:
                return CheckResult("0.2 Currency Check", Decision.NO_GO, f"Expired on {due_date}", f"Response Due: {response_date} (Expired)")
            
            return CheckResult("0.2 Currency Check", Decision.PASS, "Opportunity is current", f"Response Due: {response_date}")
            
        except Exception as e:
            return CheckResult("0.2 Currency Check", Decision.NEEDS_ANALYSIS, f"Error parsing date: {e}", f"Date parsing issue: {response_date}")

    def check_0_3_platform_viability(self, text: str) -> CheckResult:
        """
        CHECK 0.3: PLATFORM VIABILITY CHECK (EXACT from v4.0)
        Decision Logic (Referencing Platform Identification Guide):
        - IF primary platform is "PURE MILITARY - TYPICALLY NO-GO" → NO-GO (Pure Military Platform)
        - IF primary platform is "CONDITIONAL" → REQUIRES ANALYSIS  
        - IF primary platform is "ALWAYS GO" → PASS
        """
        # Check for P-8 first (common abbreviation without hyphen)
        p8_pattern = r'\bP-?8\b'
        if re.search(p8_pattern, text, re.IGNORECASE):
            quote = self._find_match_with_quote(re.compile(p8_pattern, re.IGNORECASE), text)
            return CheckResult("0.3 Platform Check", Decision.PASS, "P-8 Poseidon (Boeing 737 derivative) - Commercial/viable platform", quote or "P-8 aircraft identified")
        
        # Check for KC-46 (common abbreviation)
        kc46_pattern = r'\bKC-?46\b'
        if re.search(kc46_pattern, text, re.IGNORECASE):
            quote = self._find_match_with_quote(re.compile(kc46_pattern, re.IGNORECASE), text)
            return CheckResult("0.3 Platform Check", Decision.PASS, "KC-46 Pegasus (Boeing 767 derivative) - Commercial/viable platform", quote or "KC-46 aircraft identified")
        
        # Check for C-130 first (special case - less likely but not blocker due to AMSC Z possibility)
        c130_pattern = r'\bC-130\b'
        if re.search(c130_pattern, text, re.IGNORECASE):
            # Check if it's specifically L-100 civilian variant
            if re.search(r'\bL-100\b', text, re.IGNORECASE):
                quote = self._find_match_with_quote(re.compile(r'\bL-100\b', re.IGNORECASE), text)
                return CheckResult("0.3 Platform Check", Decision.PASS, "L-100 civilian variant found", quote or "L-100 civilian variant")
            else:
                quote = self._find_match_with_quote(re.compile(c130_pattern, re.IGNORECASE), text)
                return CheckResult("0.3 Platform Check", Decision.NEEDS_ANALYSIS, "C-130 Hercules - Pure Military Platform (less likely commercial parts but AMSC Z possible)", quote or "C-130 platform identified")
        
        # Check for other pure military platforms (less likely but not blockers due to AMSC Z)
        for platform in self.platform_guide['pure_military_no_go']:
            if platform == 'C-130 Hercules':  # Skip C-130 since we handled it above
                continue
            pattern = r'\b' + re.escape(platform) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                quote = self._find_match_with_quote(re.compile(pattern, re.IGNORECASE), text)
                return CheckResult("0.3 Platform Check", Decision.NEEDS_ANALYSIS, f"Pure Military Platform: {platform} (less likely commercial parts but AMSC Z possible)", quote or f"Platform identified: {platform}")
        
        # Check for conditional platforms (needs analysis)
        for platform in self.platform_guide['conditional_analysis']:
            pattern = r'\b' + re.escape(platform) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                quote = self._find_match_with_quote(re.compile(pattern, re.IGNORECASE), text)
                return CheckResult("0.3 Platform Check", Decision.NEEDS_ANALYSIS, f"Conditional platform found: {platform}", quote or f"Platform identified: {platform}")
        
        # Check for always-go platforms (positive indicator)
        for platform in self.platform_guide['always_go']:
            pattern = r'\b' + re.escape(platform) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                quote = self._find_match_with_quote(re.compile(pattern, re.IGNORECASE), text)
                return CheckResult("0.3 Platform Check", Decision.PASS, f"Commercial/viable platform: {platform}", quote or f"Platform identified: {platform}")
        
        # No specific platform identified - continue but note
        return CheckResult("0.3 Platform Check", Decision.PASS, "No restricted platforms detected", "No specific aircraft platform identified")

    # PHASE 1 HARD STOP CHECKS (EXACT sequence from v4.0, stop at first NO-GO)

    def check_1_sar_required(self, text: str) -> CheckResult:
        """
        CHECK 1: SOURCE APPROVAL REQUIRED (SAR) (EXACT from v4.0 + AMC/AMSC Bid Matrix)
        Decision Logic:
        - IF "source approval required" AND military specification, OR NO-GO AMC/AMSC codes → NO-GO (Military SAR Present)
        - IF "FAA source approval" → PASS (SOS can meet FAA standards)
        - IF "QPL" or "QML" found AND path to apply → REQUIRES ANALYSIS
        - IF Acceptable AMC/AMSC codes found → PASS
        - IF NOT found → PASS
        """
        # First check for acceptable AMC/AMSC codes (these are GO signals)
        acceptable_quote = self._find_match_with_quote(self.acceptable_amc_amsc_regex, text)
        if acceptable_quote:
            return CheckResult("1 SAR Check", Decision.PASS, "Acceptable AMC/AMSC code found (SOS can bid)", acceptable_quote)
        
        # Check for problematic SAR requirements
        quote = self._find_match_with_quote(self.sar_regex, text)
        if quote:
            # Check if it's FAA-related (acceptable)
            if re.search(r'FAA\s+source\s+approval', quote, re.IGNORECASE):
                return CheckResult("1 SAR Check", Decision.PASS, "FAA source approval found (SOS can meet)", quote)
            
            # Check if it's QPL/QML with application path (needs analysis)
            if re.search(r'\b(QPL|QML)\b', quote, re.IGNORECASE):
                if re.search(r'apply|application|become|register', text, re.IGNORECASE):
                    return CheckResult("1 SAR Check", Decision.NEEDS_ANALYSIS, "QPL/QML with application path identified", quote)
                else:
                    return CheckResult("1 SAR Check", Decision.NO_GO, "QPL/QML restriction without clear application path", quote)
            
            # Check for specific problematic AMC/AMSC codes
            if re.search(r'\b(AMC\s*[345]|AMSC\s*[BCDPHR]|3[BP])\b', quote, re.IGNORECASE):
                return CheckResult("1 SAR Check", Decision.NO_GO, "Problematic AMC/AMSC code found (SAR required or OEM restriction)", quote)
            
            # General military SAR language - NO-GO
            return CheckResult("1 SAR Check", Decision.NO_GO, "Military SAR Present", quote)
        
        return CheckResult("1 SAR Check", Decision.PASS, "No source approval requirements found", "No source approval language found in document")

    def check_2_sole_source(self, text: str) -> CheckResult:
        """
        CHECK 2: SOLE SOURCE DETECTION - Question 2 Methodical Approach
        
        CRITICAL LOGIC: Actual sole source announcements are HARD BLOCKERS
        Decision Logic:
        - IF "Sole source to [specific company]" (and NOT Source One Spares) → NO-GO
        - IF "awarded on a sole source basis to [company]" (and NOT Source One Spares) → NO-GO
        - IF manufacturer-specific drawings/facility required → NO-GO (effective sole source)
        - IF "intent to sole source" → REQUIRES ANALYSIS (can be challenged by SOS)
        - IF "brand name or equal" → REQUIRES ANALYSIS (opportunity exists)
        - IF NOT found → PASS
        """
        quote = self._find_match_with_quote(self.sole_source_regex, text)
        if quote:
            quote_lower = quote.lower()
            
            # HARD BLOCKERS - Actual sole source awards to other companies
            hard_sole_source_patterns = [
                r'sole\s+source\s+to\s+([A-Za-z\s&,\.]+(?:Company|Corp|Corporation|LLC|Inc))',
                r'single\s+source\s+to\s+([A-Za-z\s&,\.]+(?:Company|Corp|Corporation|LLC|Inc))',
                r'awarded\s+on\s+a\s+sole\s+source\s+basis\s+to\s+([A-Za-z\s&,\.]+(?:Company|Corp|Corporation|LLC|Inc))',
                r'sole\s+source\s+award\s+to\s+([A-Za-z\s&,\.]+(?:Company|Corp|Corporation|LLC|Inc))',
                r'sole\s+source\s+procurement\s+from\s+([A-Za-z\s&,\.]+(?:Company|Corp|Corporation|LLC|Inc))',
                r'only\s+available\s+from\s+([A-Za-z\s&,\.]+(?:Company|Corp|Corporation|LLC|Inc))'
            ]
            
            for pattern in hard_sole_source_patterns:
                match = re.search(pattern, quote, re.IGNORECASE)
                if match:
                    company_name = match.group(1).strip()
                    # Allow if sole source to Source One Spares
                    if 'source one spares' not in company_name.lower():
                        return CheckResult("2 Sole Source Check", Decision.NO_GO, 
                                         f"Sole source to {company_name} (not Source One Spares)", quote)
            
            # HARD BLOCKERS - General sole source announcements without company name
            absolute_sole_source_patterns = [
                r'this\s+is\s+a\s+sole\s+source\s+procurement',
                r'this\s+procurement\s+is\s+sole\s+source',
                r'procurement\s+will\s+be\s+awarded.*sole\s+source\s+basis'
            ]
            
            for pattern in absolute_sole_source_patterns:
                if re.search(pattern, quote, re.IGNORECASE):
                    return CheckResult("2 Sole Source Check", Decision.NO_GO, 
                                     "Absolute sole source procurement announcement", quote)
            
            # HARD BLOCKERS - Manufacturer-specific requirements (effective sole source)
            manufacturer_specific_patterns = [
                r'in\s+accordance\s+with\s+([A-Za-z\s&,\.]+(?:Company|Corp|Corporation|LLC|Inc)).*drawing\s+number',
                r'manufactured.*tested.*inspected.*in\s+accordance\s+with\s+([A-Za-z\s&,\.]+).*drawing\s+number',
                r'([A-Za-z\s&,\.]+(?:Company|Corp|Corporation|LLC|Inc)).*drawing\s+number',
                r'facility\s+identified\s+within\s+this\s+SOW.*([A-Za-z\s&,\.]+(?:Company|Corp|Corporation|LLC|Inc))'
            ]
            
            for pattern in manufacturer_specific_patterns:
                match = re.search(pattern, quote, re.IGNORECASE)
                if match:
                    company_name = match.group(1).strip()
                    return CheckResult("2 Sole Source Check", Decision.NO_GO, 
                                     f"Manufacturer-specific requirement: {company_name} (effective sole source)", quote)
            
            # HARD BLOCKERS - Proprietary restrictions
            if re.search(r'proprietary\s+design\s+of\s+([A-Za-z\s&,\.]+(?:Company|Corp|Corporation|LLC|Inc))', quote, re.IGNORECASE):
                match = re.search(r'proprietary\s+design\s+of\s+([A-Za-z\s&,\.]+(?:Company|Corp|Corporation|LLC|Inc))', quote, re.IGNORECASE)
                company_name = match.group(1).strip()
                return CheckResult("2 Sole Source Check", Decision.NO_GO, 
                                 f"Proprietary design restriction: {company_name}", quote)
            
            # NORMAL BUSINESS - Intent/award language (NOT blockers - standard government practice)
            normal_business_patterns = [
                r'intent\s+to\s+sole\s+source',
                r'intent\s+to\s+award.*sole\s+source',
                r'intends\s+to\s+sole\s+source',
                r'plans\s+to\s+sole\s+source',
                r'considering\s+sole\s+source',
                r'awarded\s+on\s+a\s+sole\s+source\s+basis',  # Standard government practice
                r'will\s+be\s+awarded.*sole\s+source\s+basis'
            ]
            
            for pattern in normal_business_patterns:
                if re.search(pattern, quote, re.IGNORECASE):
                    # Check if it has ACTUAL restrictive language that makes it a real blocker
                    actual_restriction_patterns = [
                        r'only\s+source',
                        r'sole\s+known\s+source',
                        r'only\s+known\s+source',
                        r'only\s+company.*data',
                        r'proprietary.*only\s+available',
                        r'exclusive\s+rights',
                        r'only\s+authorized',
                        r'no\s+other\s+source'
                    ]
                    
                    has_actual_restriction = any(re.search(rest_pattern, quote, re.IGNORECASE) for rest_pattern in actual_restriction_patterns)
                    
                    if has_actual_restriction:
                        return CheckResult("2 Sole Source Check", Decision.NO_GO, 
                                         "Actual restriction - only source/no other source available", quote)
                    else:
                        return CheckResult("2 Sole Source Check", Decision.PASS, 
                                         "Normal government award practice - not a restriction", quote)
            
            # ANALYSIS NEEDED - Brand name or equal opportunities (competitive)
            brand_name_patterns = [
                r'brand\s+name.*equal',
                r'or\s+equal\s+to',
                r'brand\s+name\s+or\s+approved\s+equal'
            ]
            
            for pattern in brand_name_patterns:
                if re.search(pattern, quote, re.IGNORECASE):
                    return CheckResult("2 Sole Source Check", Decision.PASS, 
                                     "Brand name or equal opportunity (competitive opportunity exists)", quote)
            
            # ALL OTHER sole source language - treat as normal business practice
            general_sole_source_patterns = [
                r'sole\s+source',
                r'only\s+one\s+responsible\s+source',
                r'single\s+source',
                r'brand\s+name\s+justification'
            ]
            
            for pattern in general_sole_source_patterns:
                if re.search(pattern, quote, re.IGNORECASE):
                    return CheckResult("2 Sole Source Check", Decision.PASS, 
                                     "Standard sole source language - normal government business practice", quote)
        
        return CheckResult("2 Sole Source Check", Decision.PASS, "No sole source restrictions found", "No sole source language found in document")

    def check_3_tech_data_availability(self, text: str) -> CheckResult:
        """
        CHECK 3: TECHNICAL DATA AVAILABILITY - Binary Decision (EXACT from v4.0)
        Key User Logic: "This is binary if the drawings are not available either for purchase 
        commercially or owned by the government with the latter being the more likely scenario it's out. 
        Either they're commonly available or the government owns them because if their proprietary 
        to the original equipment manufacturer we're not in we're not in that game"
        
        Decision Logic:
        - IF "Drawings not available" OR "OEM owns technical data" OR "Proprietary to manufacturer" → NO-GO (BLOCKER)
        - IF "Government owns technical data" OR "Drawings available upon award" OR "Commercially available" → PASS
        - IF NOT found → PASS (assume standard government practice)
        """
        quote = self._find_match_with_quote(self.tech_data_regex, text)
        if quote:
            quote_lower = quote.lower()
            
            # BLOCKERS - Technical data not available or OEM proprietary
            blocking_patterns = [
                'drawings not available',
                'drawings are not available',
                'technical data not available',
                'technical data is not available',
                'no technical data available',
                'data not available',
                'data is not available',
                'drawings will not be provided',
                'no drawings provided',
                'oem owns technical data',
                'proprietary to manufacturer',
                'proprietary to the manufacturer',
                'manufacturer proprietary data',
                'proprietary technical data',
                'contractor owns data rights',
                'government does not have data rights',
                'government does not have the technical',
                'government does not have technical',
                'government does not have drawings',
                'government does not own the technical data',
                'government does not own technical data',
                'no government furnished information',
                'no gfi',
                'contractor will not receive technical data'
            ]
            
            for pattern in blocking_patterns:
                if pattern in quote_lower:
                    return CheckResult("3 Tech Data Check", Decision.NO_GO, 
                                     f"Technical data not available - {pattern.title()}", quote)
            
            # POSITIVE INDICATORS - Government owns or commonly available (pass these)
            positive_patterns = [
                'government owns technical data',
                'government has data rights', 
                'technical data available upon award',
                'drawings available upon award',
                'government furnished information',
                'gfi provided',
                'technical data package available',
                'drawings will be provided',
                'commercially available drawings',
                'standard commercial drawings'
            ]
            
            for pattern in positive_patterns:
                if pattern in quote_lower:
                    return CheckResult("3 Tech Data Check", Decision.PASS, 
                                     f"Technical data available - {pattern.title()}", quote)
            
            # Found tech data language but unclear - treat as potential blocker for analysis
            return CheckResult("3 Tech Data Check", Decision.NEEDS_ANALYSIS, 
                             "Technical data restrictions found - needs review", quote)
        
        # No tech data language found - assume standard government practice (PASS)
        return CheckResult("3 Tech Data Check", Decision.PASS, 
                         "No technical data restrictions found", 
                         "No technical data restrictions found in document")

    def check_4_security_clearance(self, text: str) -> CheckResult:
        """
        CHECK 4: SECURITY CLEARANCE REQUIREMENTS (EXACT from v4.0)
        Decision Logic:
        - IF "Secret clearance required" or similar (any security clearance) → NO-GO
        - IF "May require clearance" → REQUIRES ANALYSIS
        - IF "unclassified" explicitly stated OR NOT found → PASS
        """
        quote = self._find_match_with_quote(self.security_regex, text)
        if quote:
            # Check for explicit clearance requirements
            if re.search(r'clearance\s+required|classified\s+required', quote, re.IGNORECASE):
                return CheckResult("4 Security Check", Decision.NO_GO, "Security clearance required", quote)
            
            # Check for potential clearance needs
            if re.search(r'may\s+require\s+clearance|potential.*clearance', quote, re.IGNORECASE):
                return CheckResult("4 Security Check", Decision.NEEDS_ANALYSIS, "May require security clearance", quote)
            
            # Other security language - generally a blocker
            return CheckResult("4 Security Check", Decision.NO_GO, "Security requirements identified", quote)
        
        return CheckResult("4 Security Check", Decision.PASS, "No security clearance requirements found", "No security clearance requirements found in document")

    def check_5_new_parts_only(self, text: str) -> CheckResult:
        """
        CHECK 5: NEW PARTS ONLY RESTRICTION (EXACT from v4.0)
        Decision Logic:
        - IF any phrases indicating only new parts are found → NO-GO
        - IF "Prefer new" or "new for critical items" → REQUIRES ANALYSIS
        - IF "Refurbished acceptable" OR "new or refurbished" → PASS (positive indicator)
        - IF NOT found (no restriction on condition) → PASS
        """
        quote = self._find_match_with_quote(self.new_parts_regex, text)
        if quote:
            return CheckResult("5 New Parts Check", Decision.NO_GO, "New parts only restriction found", quote)
        
        # Check for positive indicators (refurb acceptable)
        refurb_pattern = re.compile(r'refurbished\s+acceptable|new\s+or\s+refurbished|serviceable.*acceptable', re.IGNORECASE)
        refurb_quote = self._find_match_with_quote(refurb_pattern, text)
        if refurb_quote:
            return CheckResult("5 New Parts Check", Decision.PASS, "Refurbished parts acceptable", refurb_quote)
        
        # Check for preference language (needs analysis)
        prefer_pattern = re.compile(r'prefer\s+new|new\s+for\s+critical', re.IGNORECASE)
        prefer_quote = self._find_match_with_quote(prefer_pattern, text)
        if prefer_quote:
            return CheckResult("5 New Parts Check", Decision.NEEDS_ANALYSIS, "Preference for new parts noted", prefer_quote)
        
        return CheckResult("5 New Parts Check", Decision.PASS, "No parts condition restrictions found", "No parts condition restrictions found in document")

    def check_6_prohibited_certifications(self, text: str) -> CheckResult:
        """
        CHECK 6: PROHIBITED CERTIFICATIONS (EXACT from v4.0)
        Decision Logic:
        - IF "AS9100 required" → NO-GO (SOS does NOT have AS9100 manufacturing certification)
        - IF "NADCAP required" → NO-GO (SOS does NOT have NADCAP)
        - IF "ISO 9001 required" OR "AS9120 required" OR "FAA certification required" → PASS (SOS has these)
        - IF NOT found (no special certifications required) → PASS
        
        Note: SOS has ISO 9001:2015, AS9120B (distributor cert), and FAA certifications
              SOS does NOT have AS9100 (manufacturing cert) or NADCAP
        """
        
        # Check for explicit AS9100 ONLY requirements (hard blocker)
        as9100_only_pattern = re.compile(r'AS9100\s+(?:only|required|must|shall)(?!\s*(?:/|or)\s*(?:ISO|9001))', re.IGNORECASE)
        as9100_only_quote = self._find_match_with_quote(as9100_only_pattern, text)
        if as9100_only_quote:
            return CheckResult("6 Certifications Check", Decision.NO_GO, "AS9100 manufacturing certification required (SOS lacks this)", as9100_only_quote)
        
        # Check for explicit NADCAP requirements (hard blocker)
        nadcap_pattern = re.compile(r'NADCAP\s+(?:required|must|shall)', re.IGNORECASE)
        nadcap_quote = self._find_match_with_quote(nadcap_pattern, text)
        if nadcap_quote:
            return CheckResult("6 Certifications Check", Decision.NO_GO, "NADCAP certification required (SOS lacks this)", nadcap_quote)
        
        # Check for acceptable certifications that SOS has (positive indicators)
        acceptable_certs = re.compile(r'ISO\s*9001|AS9120|FAA\s+certification|FAA\s+certified', re.IGNORECASE)
        cert_quote = self._find_match_with_quote(acceptable_certs, text)
        if cert_quote:
            return CheckResult("6 Certifications Check", Decision.PASS, "Acceptable certifications required (SOS has these)", cert_quote)
        
        # Check for ISO 9001/AS9100 alternatives (where either is acceptable - SOS has ISO 9001)
        iso_or_as9100_pattern = re.compile(r'ISO\s*9001\s*[/|]\s*(?:SAE\s+)?AS9100|(?:SAE\s+)?AS9100\s*[/|]\s*ISO\s*9001', re.IGNORECASE)
        iso_or_quote = self._find_match_with_quote(iso_or_as9100_pattern, text)
        if iso_or_quote:
            return CheckResult("6 Certifications Check", Decision.PASS, "ISO 9001 or AS9100 required (SOS has ISO 9001:2015)", iso_or_quote)
        
        return CheckResult("6 Certifications Check", Decision.PASS, "No special certifications required", "No special certifications required in document")

    def check_7_itar_export_control(self, text: str) -> CheckResult:
        """
        CHECK 7: ITAR/EXPORT CONTROL (EXACT from v4.0)
        Decision Logic:
        - IF "ITAR registration required" or "export license required" → REQUIRES ANALYSIS
        - IF NOT found → PASS
        (Note: SOS can handle ITAR compliance with planning, not immediate NO-GO)
        """
        quote = self._find_match_with_quote(self.itar_regex, text)
        if quote:
            return CheckResult("7 ITAR Check", Decision.NEEDS_ANALYSIS, "ITAR/export control requirements found", quote)
        
        return CheckResult("7 ITAR Check", Decision.PASS, "No ITAR/export requirements found", "No ITAR/export requirements found in document")

    def check_8_oem_distribution_restrictions(self, text: str) -> CheckResult:
        """
        CHECK 8: OEM DISTRIBUTION RESTRICTIONS (EXACT from v4.0)
        Decision Logic:
        - IF "OEM only", "authorized distributor required", "OEM distributor only", "factory authorized dealer", OR AMSC B → NO-GO
        - IF NOT found → PASS
        """
        quote = self._find_match_with_quote(self.oem_regex, text)
        if quote:
            return CheckResult("8 OEM Restriction Check", Decision.NO_GO, "OEM distribution restriction found", quote)
        
        return CheckResult("8 OEM Restriction Check", Decision.PASS, "No OEM distribution restrictions found", "No OEM distribution restrictions found in document")

    def assess_opportunity(self, opp) -> Tuple[Decision, List[CheckResult]]:
        """
        EXACT implementation of SOS Initial Assessment Logic v4.0 with proper sequence and stop logic.
        
        CRITICAL RULES:
        1. Follow checks in exact order
        2. Stop at first NO-GO  
        3. Hard stops OVERRIDE all positive indicators
        4. When in doubt, default to "NEEDS FURTHER ANALYSIS"
        """
        text = self.extract_text_from_opportunity(opp)
        all_results = []

        # PHASE 0: PRELIMINARY GATES (must pass all to continue)
        logging.info("Starting Phase 0 checks...")
        
        # CHECK 0.1: Aviation-related?
        result_0_1 = self.check_0_1_aviation_related(text)
        all_results.append(result_0_1)
        if result_0_1.decision == Decision.NO_GO:
            logging.info("Phase 0.1 FAILED: Not aviation-related")
            return Decision.NO_GO, all_results

        # CHECK 0.2: Current opportunity?
        result_0_2 = self.check_0_2_opportunity_current(opp)
        all_results.append(result_0_2)
        if result_0_2.decision == Decision.NO_GO:
            logging.info("Phase 0.2 FAILED: Opportunity expired")
            return Decision.NO_GO, all_results

        # CHECK 0.3: Platform viability?
        result_0_3 = self.check_0_3_platform_viability(text)
        all_results.append(result_0_3)
        if result_0_3.decision == Decision.NO_GO:
            logging.info("Phase 0.3 FAILED: Pure military platform")
            return Decision.NO_GO, all_results

        logging.info("Phase 0 PASSED - Proceeding to Phase 1 hard stops...")

        # PHASE 1: HARD STOP ANALYSIS (stop at first NO-GO)
        phase1_checks = [
            self.check_1_sar_required,
            self.check_2_sole_source,
            self.check_3_tech_data_availability,
            self.check_4_security_clearance,
            self.check_5_new_parts_only,
            self.check_6_prohibited_certifications,
            self.check_7_itar_export_control,
            self.check_8_oem_distribution_restrictions
        ]

        needs_analysis = False
        
        for check_func in phase1_checks:
            result = check_func(text)
            all_results.append(result)
            
            if result.decision == Decision.NO_GO:
                logging.info(f"Phase 1 FAILED: {result.check_name} - {result.reason}")
                return Decision.NO_GO, all_results
            
            if result.decision == Decision.NEEDS_ANALYSIS:
                needs_analysis = True
                logging.info(f"Phase 1 ANALYSIS NEEDED: {result.check_name} - {result.reason}")

        # FINAL DECISION MATRIX (EXACT from v4.0)
        if needs_analysis:
            logging.info("FINAL DECISION: NEEDS ANALYSIS - Some items require manual review")
            return Decision.NEEDS_ANALYSIS, all_results
        else:
            logging.info("FINAL DECISION: GO - All checks passed")
            return Decision.GO, all_results
