"""
SOS Official Filter Implementation
Based on SOS Initial Assessment Logic v4.0 and official documentation
"""

import re
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, date
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class AssessmentResult:
    """Complete assessment result with all details"""
    decision: str  # 'GO', 'NO-GO', 'NEEDS ANALYSIS'
    phase_0: Dict[str, str]
    phase_1: Dict[str, str]
    reasoning: List[str]
    
class SOSFilter:
    """
    Official SOS Filter Implementation based on:
    - SOS Initial Assessment Logic v4.0
    - SAR Language Patterns
    - Platform Identification Guide
    - AMC/AMSC Bid Matrix
    """
    
    def __init__(self):
        self._init_aviation_patterns()
        self._init_platform_guide()
        self._init_sar_patterns()
        self._init_assessment_patterns()
    
    def _init_aviation_patterns(self):
        """Enhanced aviation patterns with exclusions for non-aviation equipment"""
        
        # Core aviation patterns
        self.aviation_regex = re.compile(
            '|'.join([
                # Aircraft types
                r'\b(aircraft|helicopter|rotorcraft|airplane|aviation|aerospace)\b',
                # Military designators from platform guide
                r'\b(C-130|KC-46|P-8|F-16|UH-60|CH-47|F-15|F-18|F-22|F-35|A-10|B-1B|B-2|B-52)\b',
                r'\b(C-17|C-40|C-32|VC-25|E-3|E-6|E-8|KC-135|E-4B|E-7|KC-10)\b',
                r'\b(C-12|UC-12|C-26|C-20|C-21|C-37|UC-35|C-47|P-3|UV-18|C-23|CN-235|C-144)\b',
                r'\b(MH-60|HH-60|VH-60|MH-65|UH-72|TH-57|UH-1|TH-67|OH-58|AH-64|CH-53)\b',
                r'\b(T-34|T-6|T-44|T-1|A-29|AT-802U|OA-10|AC-130|V-22|E-2|MQ-9|MQ-1)\b',
                # Aviation manufacturers (be more specific)
                r'\b(Boeing\s+(aircraft|aerospace|helicopter))\b',
                r'\b(Airbus\s+(aircraft|helicopter))\b',
                r'\b(Bell\s+(helicopter|aircraft))\b',
                r'\b(Sikorsky|Grumman\s+aircraft|McDonnell\s+Douglas)\b',
                # Aircraft-specific components
                r'\b(aircraft\s+engine|jet\s+engine|turbine\s+engine)\b',
                r'\b(avionics|flight\s+control|autopilot)\b',
                r'\b(landing\s+gear|aircraft\s+hydraulic)\b',
                r'\b(propeller|rotor\s+blade|wing\s+assembly|fuselage)\b',
                r'\b(flight\s+deck|cockpit|aircraft\s+seat)\b',
                # Ground support equipment (aviation-specific)
                r'\b(aircraft\s+ground\s+support|AGE|aircraft\s+maintenance)\b',
                # PSC codes for aviation
                r'\bPSC\s*1[567]\d{2}\b',
                # NAICS aviation codes
                r'\bNAICS\s*3364\d{2}\b'
            ]), re.IGNORECASE
        )
        
        # Non-aviation exclusion patterns (things that might match but aren't aviation)
        self.non_aviation_exclusions = re.compile(
            '|'.join([
                # Commercial/Industrial equipment
                r'\b(commercial\s+off\s+the\s+shelf|COTS)\b',
                r'\b(office\s+equipment|office\s+supplies)\b',
                r'\b(desktop\s+computer|laptop|printer|scanner)\b',
                r'\b(facility\s+maintenance|building\s+maintenance)\b',
                r'\b(janitorial|cleaning\s+supplies|custodial)\b',
                
                # Ground vehicles/equipment
                r'\b(truck|vehicle|automobile|automotive)\b',
                r'\b(forklift|crane|bulldozer|excavator)\b',
                r'\b(generator\s+set|diesel\s+generator)\b',
                r'\b(ground\s+vehicle|military\s+vehicle)\b',
                
                # Marine/Naval (non-aviation)
                r'\b(ship|vessel|submarine|naval\s+vessel)\b',
                r'\b(sonar|torpedo|naval\s+gun|radar\s+system)\b',
                r'\b(marine\s+engine|ship\s+engine)\b',
                
                # General industrial
                r'\b(industrial\s+equipment|manufacturing\s+equipment)\b',
                r'\b(machine\s+tool|lathe|drill\s+press)\b',
                r'\b(pump|valve|motor|gear\s+box)(?!\s+(aircraft|aviation|helicopter))\b',
                r'\b(electrical\s+component|electronic\s+component)\b',
                
                # IT/Communications
                r'\b(computer\s+software|IT\s+services|information\s+technology)\b',
                r'\b(telecommunications|radio\s+equipment|communication\s+system)\b',
                r'\b(server|network\s+equipment|cyber\s+security)\b',
                
                # Medical/Laboratory
                r'\b(medical\s+equipment|laboratory\s+equipment)\b',
                r'\b(pharmaceutical|medical\s+supplies)\b',
                
                # Construction/Civil
                r'\b(construction\s+services|civil\s+engineering)\b',
                r'\b(architectural\s+services|engineering\s+services)\b',
                r'\b(road\s+construction|building\s+construction)\b',
                
                # Specific non-aviation PSC codes
                r'\bPSC\s*(23\d{2}|24\d{2}|25\d{2}|29\d{2}|30\d{2}|31\d{2}|32\d{2}|33\d{2}|34\d{2}|35\d{2}|36\d{2}|37\d{2}|38\d{2}|39\d{2}|40\d{2}|41\d{2}|42\d{2}|43\d{2}|44\d{2}|45\d{2}|46\d{2}|47\d{2}|48\d{2}|49\d{2}|50\d{2}|51\d{2}|52\d{2}|53\d{2}|54\d{2}|55\d{2}|58\d{2}|59\d{2}|60\d{2}|61\d{2}|62\d{2}|63\d{2}|66\d{2}|67\d{2}|68\d{2}|69\d{2}|70\d{2}|71\d{2}|72\d{2}|73\d{2}|74\d{2}|75\d{2}|76\d{2}|77\d{2}|78\d{2}|79\d{2}|80\d{2}|81\d{2}|83\d{2}|84\d{2}|85\d{2}|87\d{2}|88\d{2}|89\d{2}|91\d{2}|92\d{2}|93\d{2}|94\d{2}|95\d{2}|96\d{2}|99\d{2})\b'
            ]), re.IGNORECASE
        )
    
    def _init_platform_guide(self):
        """Platform viability from SOS Platform Identification Guide"""
        self.platform_guide = {
            'pure_military': [
                # Combat Aircraft - Always worth pursuing
                'A-10', 'A-29', 'AC-130', 'AT-802U', 'OA-10',
                # Bombers
                'B-1B', 'B-2', 'B-52',
                # Transport
                'C-130', 'C-17',
                # Fighters
                'F-15', 'F-16', 'F-18', 'F-22', 'F-35',
                # Tankers
                'KC-135', 'KC-46', 'KC-10',
                # ISR/Special Mission
                'E-3', 'E-8', 'P-8', 'P-3', 'E-4B', 'E-6', 'E-7',
                # Rotorcraft - Pure Military
                'UH-60', 'CH-47', 'UH-1', 'AH-64', 'CH-53', 'MH-60', 'HH-60',
                # Tiltrotor
                'V-22',
                # Unmanned
                'MQ-9', 'MQ-1'
            ],
            'civilian_equivalent': [
                # VIP/Transport with civilian variants - Still viable
                'C-40', 'C-32', 'VC-25', 'C-12', 'UC-12', 'C-26', 'C-20', 'C-21', 'C-37', 'UC-35',
                'C-47', 'UV-18', 'C-23', 'CN-235', 'C-144',
                # Training/Light Aircraft
                'UH-72', 'TH-57', 'TH-67', 'T-34', 'T-6', 'T-44', 'T-1',
                # Carrier-based
                'E-2'
            ]
        }
        
        # Create regex patterns for platform detection
        all_platforms = self.platform_guide['pure_military'] + self.platform_guide['civilian_equivalent']
        self.platform_regex = re.compile(
            r'\b(' + '|'.join(re.escape(p) for p in all_platforms) + r')\b',
            re.IGNORECASE
        )
    
    def _init_sar_patterns(self):
        """Enhanced SAR patterns from SAR-Language-Patterns.md and real-world examples"""
        self.sar_regex = re.compile(
            '|'.join([
                # Core SAR phrases
                r'source\s+approval\s+required',
                r'engineering\s+source\s+approval',
                r'government\s+source\s+approval',
                r'approved\s+source\s+list',
                r'qualified\s+suppliers?\s+list',
                r'requires\s+engineering\s+source\s+approval\s+by\s+the\s+design\s+control\s+activity',
                
                # Certification lists
                r'\bQPL\b',  # Qualified Products List
                r'\bQML\b',  # Qualified Manufacturers List
                
                # Military specs (often indicate SAR)
                r'military\s+specification',
                r'mil-spec',
                r'mil\s+std',
                
                # DLA-specific SAR indicators
                r'sources\s+sought',
                r'market\s+research',
                r'capability\s+statement',
                r'manufacturing\s+capability',
                r'production\s+capability',
                r'recent\s+manufacturing\s+history',
                r'similar\s+part\s+production',
                r'manufacturing\s+experience',
                
                # Technical data gaps (common SAR trigger)
                r'no\s+technical\s+data\s+package',
                r'technical\s+data\s+not\s+available',
                r'limited\s+technical\s+data',
                r'incomplete\s+technical\s+data',
                
                # Flight critical/safety requirements
                r'flight\s+critical',
                r'safety\s+critical',
                r'critical\s+application',
                
                # Special notice patterns that often indicate SAR
                r'special\s+notice.*capability',
                r'special\s+notice.*manufacturing',
                r'sources\s+sought.*capability',
                # AMC/AMSC codes indicating SAR
                r'\bAMC\s*[345]\b',
                r'\bAMSC\s*[CDPR]\b',
                # SAR package requirements
                r'Source\s+Approval\s+Request\s+package',
                r'\bSAR\s+package\b',
                r'NAVSUP.*Source\s+Approval.*Brochure',
                r'submit.*Source\s+Approval\s+Request',
                # DLA SAR indicators
                r'DLA.*source\s+approval',
                r'design\s+control\s+activity\s+approval'
            ]), re.IGNORECASE
        )
    
    def _init_assessment_patterns(self):
        """All other assessment patterns"""
        # Sole source indicators
        self.sole_source_regex = re.compile(
            '|'.join([
                r'sole\s+source',
                r'only\s+source',
                r'single\s+source',
                r'brand\s+name\s+or\s+equal',
                r'no\s+substitute',
                r'proprietary',
                r'OEM\s+only',
                r'original\s+equipment\s+manufacturer\s+only'
            ]), re.IGNORECASE
        )
        
        # Technical data requirements
        self.tech_data_regex = re.compile(
            '|'.join([
                r'technical\s+data\s+package',
                r'engineering\s+drawings?',
                r'design\s+data',
                r'manufacturing\s+data',
                r'test\s+data',
                r'certification\s+data',
                r'data\s+rights',
                r'intellectual\s+property\s+rights?',
                r'proprietary\s+information'
            ]), re.IGNORECASE
        )
        
        # Security clearance requirements
        self.clearance_regex = re.compile(
            '|'.join([
                r'security\s+clearance',
                r'secret\s+clearance',
                r'top\s+secret',
                r'confidential\s+clearance',
                r'facility\s+security\s+clearance',
                r'personnel\s+security\s+clearance',
                r'DoD\s+clearance',
                r'background\s+investigation'
            ]), re.IGNORECASE
        )
        
        # New parts only indicators
        self.new_parts_regex = re.compile(
            '|'.join([
                r'new\s+parts?\s+only',
                r'no\s+used\s+parts?',
                r'no\s+refurbished\s+parts?',
                r'no\s+repaired\s+parts?',
                r'factory\s+new\s+only',
                r'original\s+manufacture\s+only',
                r'\bAMC\s*4\b',
                r'\bAMSC\s*N\b'
            ]), re.IGNORECASE
        )
        
        # Prohibited certifications
        self.prohibited_cert_regex = re.compile(
            '|'.join([
                r'ISO\s*9001',
                r'AS\s*9100',
                r'NADCAP',
                r'quality\s+management\s+system',
                r'quality\s+assurance\s+program',
                r'contractor\s+quality\s+control',
                r'inspection\s+system'
            ]), re.IGNORECASE
        )
        
        # OEM restrictions
        self.oem_regex = re.compile(
            '|'.join([
                r'OEM\s+authorization',
                r'manufacturer\s+authorization',
                r'authorized\s+dealer',
                r'authorized\s+distributor',
                r'factory\s+authorized',
                r'direct\s+from\s+manufacturer',
                r'\bAMC\s*1\b',
                r'\bAMSC\s*A\b'
            ]), re.IGNORECASE
        )
        
        # Currency check - posted within last 12 months
        self.current_date = datetime.now()
    
    def extract_text(self, opp: Dict) -> str:
        """Extract all text content from opportunity"""
        # Check if we have enhanced text with documents first
        if 'full_analysis_text' in opp:
            return opp['full_analysis_text']
        
        # Otherwise, build from available fields
        text_fields = [
            opp.get('title', ''),
            opp.get('description_text', ''),
            opp.get('ai_summary', ''),
            opp.get('source_id', ''),
            opp.get('set_aside', '')
        ]
        
        # Add document text if available in documents array
        for doc in opp.get('documents', []):
            text_fields.append(doc.get('text_extract', ''))
        
        return ' '.join(filter(None, text_fields))
    
    def check_aviation(self, text: str) -> Tuple[bool, str]:
        """Phase 0.1: Enhanced aviation check with exclusions"""
        
        # First check for aviation matches
        aviation_match = self.aviation_regex.search(text)
        if not aviation_match:
            return False, "FAIL - Not aviation-related"
        
        # If we found aviation keywords, check for exclusions
        exclusion_match = self.non_aviation_exclusions.search(text)
        if exclusion_match:
            context_start = max(0, exclusion_match.start() - 50)
            context_end = min(len(text), exclusion_match.end() + 50)
            exclusion_quote = text[context_start:context_end].strip()
            return False, f"FAIL - Non-aviation equipment detected: '{exclusion_match.group()}' in context: '{exclusion_quote}'"
        
        # Passed both tests - it's aviation related and not excluded
        context_start = max(0, aviation_match.start() - 50)
        context_end = min(len(text), aviation_match.end() + 50)
        quote = text[context_start:context_end].strip()
        return True, f"PASS - Aviation-related: '{aviation_match.group()}' in context: '{quote}'"
    
    def check_currency(self, opp: Dict) -> Tuple[bool, str]:
        """Phase 0.2: Currency check - within last 12 months"""
        posted_date_str = opp.get('posted_date', '')
        if not posted_date_str:
            return False, "FAIL - No posted date available"
        
        try:
            # Handle different date formats
            for fmt in ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%SZ']:
                try:
                    posted_date = datetime.strptime(posted_date_str.split('T')[0], '%Y-%m-%d')
                    break
                except ValueError:
                    continue
            else:
                return False, f"FAIL - Unable to parse date: {posted_date_str}"
            
            days_old = (self.current_date - posted_date).days
            if days_old > 365:
                return False, f"FAIL - Too old ({days_old} days)"
            
            return True, f"PASS - Current ({days_old} days old)"
            
        except Exception as e:
            return False, f"FAIL - Date parsing error: {str(e)}"
    
    def check_platform_viability(self, text: str) -> Tuple[bool, str]:
        """Phase 0.3: Platform viability check"""
        platform_match = self.platform_regex.search(text)
        if not platform_match:
            return True, "PASS - General aviation, no specific platform restrictions"
        
        platform = platform_match.group()
        if platform.upper() in [p.upper() for p in self.platform_guide['pure_military']]:
            return True, f"PASS - Pure military platform: {platform}"
        elif platform.upper() in [p.upper() for p in self.platform_guide['civilian_equivalent']]:
            return True, f"PASS - Platform with civilian equivalent: {platform}"
        
        return True, f"PASS - Platform identified: {platform}"
    
    def check_sar(self, text: str, opp: Dict = None) -> Tuple[bool, str]:
        """Phase 1.1: Enhanced SAR check with contextual analysis"""
        
        # First check explicit SAR patterns
        match = self.sar_regex.search(text)
        if match:
            context_start = max(0, match.start() - 30)
            context_end = min(len(text), match.end() + 30)
            quote = text[context_start:context_end].strip()
            return False, f"FAIL - SAR required: '{match.group()}' in '{quote}'"
        
        # Enhanced contextual SAR detection
        if opp:
            # DLA Special Notice for aircraft parts often means sources sought = SAR
            agency_name = opp.get('agency', {}).get('agency_abbreviation', '') if isinstance(opp.get('agency'), dict) else ''
            opp_type = opp.get('opp_type', {}).get('description', '') if isinstance(opp.get('opp_type'), dict) else ''
            
            if (agency_name == 'DLA' and 
                'Special Notice' in opp_type and 
                any(indicator in text.lower() for indicator in [
                    'aircraft', 'aviation', 'flight', 'helicopter', 'engine', 
                    'rotor', 'wing', 'fuselage', 'landing gear', 'hydraulic'
                ])):
                return False, "FAIL - DLA Special Notice for aircraft parts typically requires SAR approval and manufacturing capability demonstration"
            
            # PSC codes that typically require SAR for aircraft
            psc_code = opp.get('psc_code', {}).get('psc_code', '') if isinstance(opp.get('psc_code'), dict) else ''
            if psc_code and psc_code.startswith(('1560', '1650', '1660', '1680', '2840')):  # Aircraft structural, hydraulic, airframe, landing gear, engines
                return False, f"FAIL - PSC code {psc_code} typically requires SAR for aircraft components"
        
        return True, "PASS - No SAR requirements detected"
    
    def check_sole_source(self, text: str) -> Tuple[bool, str]:
        """Phase 1.2: Sole source check"""
        match = self.sole_source_regex.search(text)
        if match:
            context_start = max(0, match.start() - 30)
            context_end = min(len(text), match.end() + 30)
            quote = text[context_start:context_end].strip()
            return False, f"FAIL - Sole source: '{match.group()}' in '{quote}'"
        return True, "PASS - No sole source restrictions"
    
    def check_technical_data(self, text: str) -> Tuple[bool, str]:
        """Phase 1.3: Technical data check"""
        match = self.tech_data_regex.search(text)
        if match:
            context_start = max(0, match.start() - 30)
            context_end = min(len(text), match.end() + 30)
            quote = text[context_start:context_end].strip()
            return False, f"FAIL - Technical data required: '{match.group()}' in '{quote}'"
        return True, "PASS - No technical data requirements"
    
    def check_security_clearance(self, text: str) -> Tuple[bool, str]:
        """Phase 1.4: Security clearance check"""
        match = self.clearance_regex.search(text)
        if match:
            context_start = max(0, match.start() - 30)
            context_end = min(len(text), match.end() + 30)
            quote = text[context_start:context_end].strip()
            return False, f"FAIL - Security clearance required: '{match.group()}' in '{quote}'"
        return True, "PASS - No security clearance requirements"
    
    def check_new_parts_only(self, text: str) -> Tuple[bool, str]:
        """Phase 1.5: New parts only check"""
        match = self.new_parts_regex.search(text)
        if match:
            context_start = max(0, match.start() - 30)
            context_end = min(len(text), match.end() + 30)
            quote = text[context_start:context_end].strip()
            return False, f"FAIL - New parts only: '{match.group()}' in '{quote}'"
        return True, "PASS - No new parts only requirements"
    
    def check_prohibited_certifications(self, text: str) -> Tuple[bool, str]:
        """Phase 1.6: Prohibited certifications check"""
        match = self.prohibited_cert_regex.search(text)
        if match:
            context_start = max(0, match.start() - 30)
            context_end = min(len(text), match.end() + 30)
            quote = text[context_start:context_end].strip()
            return False, f"FAIL - Prohibited certification: '{match.group()}' in '{quote}'"
        return True, "PASS - No prohibited certifications"
    
    def check_oem_restrictions(self, text: str) -> Tuple[bool, str]:
        """Phase 1.8: OEM restrictions check"""
        match = self.oem_regex.search(text)
        if match:
            context_start = max(0, match.start() - 30)
            context_end = min(len(text), match.end() + 30)
            quote = text[context_start:context_end].strip()
            return False, f"FAIL - OEM restrictions: '{match.group()}' in '{quote}'"
        return True, "PASS - No OEM restrictions"
    
    def assess_opportunity(self, opp: Dict) -> AssessmentResult:
        """
        Complete SOS Initial Assessment Logic v4.0
        
        Phase 0: Preliminary Gates
        1. Aviation check
        2. Currency check  
        3. Platform viability

        Phase 1: Hard Stops (8 criteria)
        1. SAR check
        2. Sole source check
        3. Technical data check
        4. Security clearance check
        5. New parts only check
        6. Prohibited certifications check
        7. ITAR/export control check (disabled per user requirements)
        8. OEM restrictions check
        """
        text = self.extract_text(opp)
        
        phase_0 = {}
        phase_1 = {}
        reasoning = []
        
        # Phase 0.1: Aviation Check
        aviation_pass, aviation_reason = self.check_aviation(text)
        phase_0['aviation'] = aviation_reason
        if not aviation_pass:
            reasoning.append('Failed aviation check')
            return AssessmentResult('NO-GO', phase_0, phase_1, reasoning)
        
        # Phase 0.2: Currency Check
        currency_pass, currency_reason = self.check_currency(opp)
        phase_0['currency'] = currency_reason
        if not currency_pass:
            reasoning.append('Failed currency check')
            return AssessmentResult('NO-GO', phase_0, phase_1, reasoning)
        
        # Phase 0.3: Platform Viability
        platform_pass, platform_reason = self.check_platform_viability(text)
        phase_0['platform_viability'] = platform_reason
        if not platform_pass:
            reasoning.append('Failed platform viability')
            return AssessmentResult('NO-GO', phase_0, phase_1, reasoning)
        
        # Phase 1: Hard Stop Analysis
        hard_stops = []
        
        # 1. SAR Check
        sar_pass, sar_reason = self.check_sar(text, opp)
        phase_1['sar'] = sar_reason
        if not sar_pass:
            hard_stops.append('SAR required')
        
        # 2. Sole Source Check
        sole_pass, sole_reason = self.check_sole_source(text)
        phase_1['sole_source'] = sole_reason
        if not sole_pass:
            hard_stops.append('Sole source')
        
        # 3. Technical Data Check
        tech_pass, tech_reason = self.check_technical_data(text)
        phase_1['technical_data'] = tech_reason
        if not tech_pass:
            hard_stops.append('Technical data required')
        
        # 4. Security Clearance Check
        clear_pass, clear_reason = self.check_security_clearance(text)
        phase_1['security_clearance'] = clear_reason
        if not clear_pass:
            hard_stops.append('Security clearance required')
        
        # 5. New Parts Only Check
        new_pass, new_reason = self.check_new_parts_only(text)
        phase_1['new_parts_only'] = new_reason
        if not new_pass:
            hard_stops.append('New parts only')
        
        # 6. Prohibited Certifications Check
        cert_pass, cert_reason = self.check_prohibited_certifications(text)
        phase_1['prohibited_certifications'] = cert_reason
        if not cert_pass:
            hard_stops.append('Prohibited certifications')
        
        # 7. ITAR/Export Control Check (disabled)
        phase_1['itar_export'] = 'PASS - Check disabled per user requirements'
        
        # 8. OEM Restrictions Check
        oem_pass, oem_reason = self.check_oem_restrictions(text)
        phase_1['oem_restrictions'] = oem_reason
        if not oem_pass:
            hard_stops.append('OEM restrictions')
        
        # Final Decision
        if hard_stops:
            reasoning = hard_stops
            return AssessmentResult('NO-GO', phase_0, phase_1, reasoning)
        
        reasoning = ['All assessment criteria met - viable opportunity']
        return AssessmentResult('GO', phase_0, phase_1, reasoning)
