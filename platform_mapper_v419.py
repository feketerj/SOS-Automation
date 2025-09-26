#!/usr/bin/env python3
"""
Platform Mapper V4.19 - Comprehensive military/civilian platform discrimination.
Based on SOS Platform Identification Guide - Full Implementation.
Covers 100+ platforms with civilian equivalency mappings.
"""

import re
from typing import Tuple, List, Dict, Optional, Set
from enum import Enum

class PlatformDecision(Enum):
    GO = "GO"
    NO_GO = "NO-GO"
    CONDITIONAL = "CONDITIONAL"
    UNKNOWN = "UNKNOWN"

class PlatformMapper:
    """Comprehensive platform mapper with 100+ military/civilian mappings."""
    
    def __init__(self):
        self.platform_mappings = self._initialize_mappings()
        self.engine_mappings = self._initialize_engine_mappings()
        self.civilian_manufacturers = self._initialize_civilian_manufacturers()
        self.civilian_variants = self._initialize_civilian_variants()
        self.compiled_patterns = self._compile_patterns()
    
    def _initialize_mappings(self) -> Dict:
        """Initialize comprehensive platform mappings from guide."""
        return {
            # ============ BOEING MILITARY AIRCRAFT ============
            'KC-46': {'civilian': 'Boeing 767', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'P-8': {'civilian': 'Boeing 737', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'C-40': {'civilian': 'Boeing 737 BBJ', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'C-32': {'civilian': 'Boeing 757', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'VC-25': {'civilian': 'Boeing 747', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'E-3': {'civilian': 'Boeing 707', 'decision': PlatformDecision.GO, 'commonality': 'Medium'},
            'E-6': {'civilian': 'Boeing 707', 'decision': PlatformDecision.GO, 'commonality': 'Medium'},
            'E-8': {'civilian': 'Boeing 707', 'decision': PlatformDecision.GO, 'commonality': 'Medium'},
            'KC-135': {'civilian': 'Boeing 707 variant', 'decision': PlatformDecision.GO, 'commonality': 'Medium'},
            'E-4B': {'civilian': 'Boeing 747', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'E-7': {'civilian': 'Boeing 737', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'KC-10': {'civilian': 'McDonnell Douglas DC-10', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'C-17': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            
            # ============ TRANSPORT AIRCRAFT ============
            'C-130': {'civilian': 'L-100', 'decision': PlatformDecision.CONDITIONAL, 'note': 'Check for L-100 variant'},
            'L-100': {'civilian': 'L-100', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'L-382': {'civilian': 'L-100', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'C-27J': {'civilian': 'G.222 (minimal)', 'decision': PlatformDecision.NO_GO, 'commonality': 'Very Low'},
            'C-12': {'civilian': 'Beechcraft King Air 200/350', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'UC-12': {'civilian': 'Beechcraft King Air', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'RC-12': {'civilian': 'Beechcraft King Air', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'MC-12': {'civilian': 'Beechcraft King Air 350', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'C-26': {'civilian': 'Fairchild Metro/Merlin', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'C-20': {'civilian': 'Gulfstream III/IV/V', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'C-21': {'civilian': 'Learjet 35', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'C-37': {'civilian': 'Gulfstream V/550', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'UC-35': {'civilian': 'Cessna Citation', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'C-47': {'civilian': 'DC-3', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'P-3': {'civilian': 'L-188 Electra', 'decision': PlatformDecision.CONDITIONAL, 'note': 'Check for L-188 variant'},
            'UV-18': {'civilian': 'De Havilland DHC-6', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'C-23': {'civilian': 'Shorts 330/360', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'CN-235': {'civilian': 'CASA CN-235', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'C-144': {'civilian': 'CASA CN-235', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'HC-27J': {'civilian': 'C-27J', 'decision': PlatformDecision.NO_GO, 'note': 'NO-GO unless FAA'},
            'C-5': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'U-28': {'civilian': 'Pilatus PC-12', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'U-21': {'civilian': 'Beechcraft King Air', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'EO-5': {'civilian': 'DHC-7 Dash 7', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'RC-7': {'civilian': 'DHC-7 Dash 7', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            
            # ============ HELICOPTERS ============
            'UH-60': {'civilian': 'Sikorsky S-70', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'MH-60': {'civilian': 'Sikorsky S-70', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'HH-60': {'civilian': 'Sikorsky S-70', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'VH-60': {'civilian': 'Sikorsky S-70', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'MH-65': {'civilian': 'Eurocopter AS365', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'HH-65': {'civilian': 'AS365 Dauphin', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'UH-72': {'civilian': 'Eurocopter EC145', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'TH-57': {'civilian': 'Bell 206', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'TH-67': {'civilian': 'Bell 206', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'UH-1': {'civilian': 'Bell 204/205/212', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'OH-58': {'civilian': 'Bell 206/407', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'AH-64': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'AH-1': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'CH-47': {'civilian': 'Model 234', 'decision': PlatformDecision.CONDITIONAL, 'note': 'Check for Model 234 variant'},
            'CH-53': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'Very Low'},
            'MH-53': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'Very Low'},
            'V-22': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            
            # ============ TRAINER AIRCRAFT ============
            'T-34': {'civilian': 'Beechcraft Bonanza-based', 'decision': PlatformDecision.GO, 'commonality': 'Medium'},
            'T-6': {'civilian': 'Pilatus PC-9', 'decision': PlatformDecision.GO, 'commonality': 'Medium'},
            'T-44': {'civilian': 'Beechcraft King Air 90', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'T-1': {'civilian': 'Beechcraft 400', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'T-38': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'Very Low'},
            'T-45': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'Low'},
            'T-41': {'civilian': 'Cessna 172', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'T-51': {'civilian': 'Cessna 162', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'T-53': {'civilian': 'Cirrus SR20', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            
            # ============ FIGHTERS/ATTACK (ALL NO-GO) ============
            'F-15': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'F-16': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'F-18': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'F/A-18': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'F-22': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'F-35': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'A-10': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'OA-10': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'AV-8': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'F-5': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'F-4': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'F-14': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'F-111': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            
            # ============ BOMBERS (ALL NO-GO) ============
            'B-1': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'B-2': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'B-52': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'B-21': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            
            # ============ SPECIAL MISSION ============
            'A-29': {'civilian': 'EMB-314', 'decision': PlatformDecision.CONDITIONAL, 'commonality': 'Medium'},
            'AT-802': {'civilian': 'Air Tractor AT-802', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'AC-130': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'Very Low'},
            'EC-130': {'civilian': 'C-130 base', 'decision': PlatformDecision.NO_GO, 'commonality': 'Low'},
            'HC-130': {'civilian': 'C-130 base', 'decision': PlatformDecision.NO_GO, 'note': 'NO-GO unless FAA'},
            'MC-130': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'E-2': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'C-2': {'civilian': None, 'decision': PlatformDecision.CONDITIONAL, 'commonality': 'Low'},
            'S-3': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'Very Low'},
            'OV-10': {'civilian': None, 'decision': PlatformDecision.CONDITIONAL, 'commonality': 'Medium'},
            'S-2': {'civilian': 'S-2T Turbo Tracker', 'decision': PlatformDecision.CONDITIONAL, 'note': 'Check for S-2T variant'},
            
            # ============ COAST GUARD/DHS ============
            'HC-144': {'civilian': 'CASA CN-235', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'MH-60T': {'civilian': 'Sikorsky S-70', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'MH-65D': {'civilian': 'Eurocopter AS365', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'MH-65E': {'civilian': 'Eurocopter AS365', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'HU-25': {'civilian': 'Dassault Falcon 20', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            'HC-131': {'civilian': 'Convair C-131', 'decision': PlatformDecision.GO, 'commonality': 'High'},
            'C-143': {'civilian': 'Dornier 328', 'decision': PlatformDecision.GO, 'commonality': 'Very High'},
            
            # ============ UAVs (ALL NO-GO) ============
            'MQ-1': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'MQ-9': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'RQ-4': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
            'RQ-7': {'civilian': None, 'decision': PlatformDecision.NO_GO, 'commonality': 'None'},
        }
    
    def _initialize_engine_mappings(self) -> Dict:
        """Initialize engine to platform mappings."""
        return {
            # Commercial/Dual-Use Engines (GO)
            'CFM56': {'platforms': ['Boeing 737', 'KC-135R', 'E-3/E-6'], 'decision': PlatformDecision.GO},
            'CF6': {'platforms': ['Boeing 767', 'KC-10', 'C-5M'], 'decision': PlatformDecision.GO},
            'F103': {'platforms': ['KC-10'], 'decision': PlatformDecision.GO},
            'F117': {'platforms': ['Boeing 757', 'C-32'], 'decision': PlatformDecision.GO},
            'PW2000': {'platforms': ['Boeing 757', 'C-32'], 'decision': PlatformDecision.GO},
            'PW4000': {'platforms': ['Boeing 777', 'KC-46', 'C-17'], 'decision': PlatformDecision.GO},
            'GE90': {'platforms': ['Boeing 777'], 'decision': PlatformDecision.GO},
            'V2500': {'platforms': ['Airbus A320'], 'decision': PlatformDecision.GO},
            'PT6': {'platforms': ['King Air', 'Caravan', 'PC-12'], 'decision': PlatformDecision.GO},
            'TFE731': {'platforms': ['Business jets'], 'decision': PlatformDecision.GO},
            'BR700': {'platforms': ['Gulfstream', 'Global Express'], 'decision': PlatformDecision.GO},
            
            # Military Turboprops (CONDITIONAL)
            'T56': {'platforms': ['C-130', 'P-3', 'L-100'], 'decision': PlatformDecision.CONDITIONAL},
            '501D': {'platforms': ['C-130', 'P-3', 'L-100'], 'decision': PlatformDecision.CONDITIONAL},
            'T700': {'platforms': ['UH-60', 'Apache'], 'decision': PlatformDecision.CONDITIONAL},
            'T701': {'platforms': ['UH-60', 'Apache'], 'decision': PlatformDecision.CONDITIONAL},
            
            # Fighter/Military Only Engines (NO-GO)
            'F100': {'platforms': ['F-15', 'F-16'], 'decision': PlatformDecision.NO_GO},
            'F110': {'platforms': ['F-15', 'F-16'], 'decision': PlatformDecision.NO_GO},
            'F119': {'platforms': ['F-22'], 'decision': PlatformDecision.NO_GO},
            'F135': {'platforms': ['F-35'], 'decision': PlatformDecision.NO_GO},
            'F404': {'platforms': ['F/A-18'], 'decision': PlatformDecision.NO_GO},
            'F414': {'platforms': ['F/A-18'], 'decision': PlatformDecision.NO_GO},
            'T400': {'platforms': ['V-22'], 'decision': PlatformDecision.NO_GO},
        }
    
    def _initialize_civilian_manufacturers(self) -> Set[str]:
        """Initialize set of civilian aircraft manufacturers."""
        return {
            'cessna', 'piper', 'beechcraft', 'cirrus', 'diamond', 'mooney',
            'pilatus', 'tbm', 'socata', 'gulfstream', 'learjet', 'challenger',
            'bombardier', 'embraer', 'atr', 'saab', 'fokker', 'dassault',
            'hawker', 'citation', 'bell', 'airbus', 'eurocopter', 'sikorsky',
            'agustawestland', 'robinson', 'maule', 'quest', 'viking',
            'de havilland', 'dornier', 'fairchild', 'shorts', 'casa'
        }
    
    def _initialize_civilian_variants(self) -> Dict[str, List[str]]:
        """Initialize civilian variant mappings for military platforms."""
        return {
            # Military -> [Civilian variants to check for]
            'C-130': ['L-100', 'L-382', 'civilian hercules', 'commercial hercules'],
            'P-3': ['L-188', 'Electra', 'L188', 'civilian electra'],
            'CH-47': ['Model 234', '234', 'commercial chinook', 'civilian chinook'],
            'S-2': ['S-2T', 'S2T', 'Turbo Tracker', 'firefighting'],
            'C-47': ['DC-3', 'DC3', 'Dakota'],
        }
    
    def civilian_variant_check(self, military_platform: str, text: str) -> Tuple[bool, Optional[str]]:
        """
        Check if a military platform's civilian variant is mentioned.
        Returns (is_civilian_variant, variant_name)
        """
        if military_platform not in self.civilian_variants:
            return (False, None)
        
        text_lower = text.lower()
        
        for variant in self.civilian_variants[military_platform]:
            # Create flexible pattern for variant
            variant_pattern = variant.lower().replace('-', r'[\-\s]?')
            if re.search(r'\b' + variant_pattern + r'\b', text_lower):
                return (True, variant)
        
        return (False, None)
    
    def _compile_patterns(self) -> List[Tuple[re.Pattern, str]]:
        """Compile comprehensive regex patterns for platform detection."""
        patterns = []
        
        # Add patterns for each mapped platform
        for platform in self.platform_mappings.keys():
            # Handle various designation formats
            if '-' in platform:
                # Military designations like F-16, KC-46
                base = platform.split('-')[0]
                number = platform.split('-')[1]
                
                # Create flexible pattern
                if base in ['F', 'A', 'B', 'C', 'E', 'H', 'K', 'M', 'O', 'P', 'R', 'S', 'T', 'U', 'V']:
                    # Allow variants like F-16A, F-16C, etc.
                    pattern = rf'\b{re.escape(base)}[\-\s]?{re.escape(number)}[A-Z0-9]*\b'
                else:
                    pattern = rf'\b{re.escape(platform)}[A-Z0-9]*\b'
            else:
                pattern = rf'\b{re.escape(platform)}\b'
            
            patterns.append((re.compile(pattern, re.IGNORECASE), platform))
        
        # Add special patterns for L-100/L-382
        patterns.append((re.compile(r'\bL[\-\s]?100\b', re.IGNORECASE), 'L-100'))
        patterns.append((re.compile(r'\bL[\-\s]?382\b', re.IGNORECASE), 'L-382'))
        
        # Add patterns for pure civilian aircraft
        patterns.extend([
            (re.compile(r'\bBoeing\s+7[0-9]{2}\b', re.IGNORECASE), 'BOEING_CIVILIAN'),
            (re.compile(r'\bBoeing\s+7[0-9]{2}[\-\s]?[0-9]{3}\b', re.IGNORECASE), 'BOEING_CIVILIAN'),
            (re.compile(r'\bAirbus\s+A[0-9]{3}\b', re.IGNORECASE), 'AIRBUS_CIVILIAN'),
            (re.compile(r'\bCessna\s+[0-9]{3}\b', re.IGNORECASE), 'CESSNA_CIVILIAN'),
            (re.compile(r'\bPiper\s+[A-Z]+\b', re.IGNORECASE), 'PIPER_CIVILIAN'),
            (re.compile(r'\bBeechcraft\s+[A-Z0-9]+\b', re.IGNORECASE), 'BEECHCRAFT_CIVILIAN'),
            (re.compile(r'\bGulfstream\s+[IVX]+\b', re.IGNORECASE), 'GULFSTREAM_CIVILIAN'),
            (re.compile(r'\bLearjet\s+[0-9]+\b', re.IGNORECASE), 'LEARJET_CIVILIAN'),
            (re.compile(r'\bCitation\s+[A-Z0-9]+\b', re.IGNORECASE), 'CITATION_CIVILIAN'),
            (re.compile(r'\bBell\s+[0-9]{3}\b', re.IGNORECASE), 'BELL_CIVILIAN'),
            (re.compile(r'\bSikorsky\s+S[\-\s]?[0-9]{2}\b', re.IGNORECASE), 'SIKORSKY_CIVILIAN'),
            (re.compile(r'\bRobinson\s+R[0-9]{2}\b', re.IGNORECASE), 'ROBINSON_CIVILIAN'),
            (re.compile(r'\bDash[\-\s]?8\b', re.IGNORECASE), 'DASH8_CIVILIAN'),
            (re.compile(r'\bDHC[\-\s]?8\b', re.IGNORECASE), 'DASH8_CIVILIAN'),
            (re.compile(r'\bQ400\b', re.IGNORECASE), 'DASH8_CIVILIAN'),
            (re.compile(r'\bKing\s+Air\b', re.IGNORECASE), 'KINGAIR_CIVILIAN'),
            (re.compile(r'\bCaravan\b', re.IGNORECASE), 'CARAVAN_CIVILIAN'),
            (re.compile(r'\bPC[\-\s]?12\b', re.IGNORECASE), 'PC12_CIVILIAN'),
        ])
        
        # Add engine patterns
        for engine in self.engine_mappings.keys():
            pattern = rf'\b{re.escape(engine)}\b'
            patterns.append((re.compile(pattern, re.IGNORECASE), f'ENGINE_{engine}'))
        
        return patterns
    
    def check_amsc_override(self, text: str) -> bool:
        """Check if AMSC Z/G/A codes are present for override."""
        amsc_override_pattern = re.compile(
            r'\bAMSC\s+(?:Code\s+)?[ZGA]\b|\bAMC\s+[12]\b',
            re.IGNORECASE
        )
        return bool(amsc_override_pattern.search(text))
    
    def check_commercial_override(self, text: str) -> bool:
        """Check for commercial item or FAA standard mentions."""
        commercial_patterns = [
            r'\bcommercial\s+(?:item|equivalent|standard)\b',
            r'\bFAA\s+(?:certified|standard|approved)\b',
            r'\bFAA\s+Form\s+8130',
            r'\bcommercial\s+off[\s\-]the[\s\-]shelf\b',
            r'\bCOTS\b',
            r'\bcommercial\s+parts?\s+acceptable\b'
        ]
        
        for pattern in commercial_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def identify_platform(self, text: str) -> Tuple[Optional[str], PlatformDecision, Optional[str]]:
        """
        Identify platform in text and return decision with override checks.
        
        Returns:
            Tuple of (platform_identified, decision, civilian_equivalent)
        """
        identified_platforms = []
        identified_engines = []
        
        # Check for platform and engine mentions
        for pattern, identifier in self.compiled_patterns:
            if pattern.search(text):
                if identifier.startswith('ENGINE_'):
                    identified_engines.append(identifier.replace('ENGINE_', ''))
                else:
                    identified_platforms.append(identifier)
        
        # Check for override conditions
        has_amsc_override = self.check_amsc_override(text)
        has_commercial_override = self.check_commercial_override(text)
        
        # Special handling for L-100/L-382 (always GO)
        if 'L-100' in identified_platforms or 'L-382' in identified_platforms:
            return ('L-100', PlatformDecision.GO, 'L-100 Civilian Hercules')
        
        # Check for military platforms with civilian variants
        for platform in identified_platforms:
            if platform in self.civilian_variants:
                has_variant, variant_name = self.civilian_variant_check(platform, text)
                if has_variant:
                    civilian_equiv = self.platform_mappings[platform].get('civilian', '')
                    return (platform, PlatformDecision.GO, f'{platform} with {variant_name} civilian variant')
        
        # Check for pure civilian aircraft
        civilian_indicators = [
            'BOEING_CIVILIAN', 'AIRBUS_CIVILIAN', 'CESSNA_CIVILIAN',
            'PIPER_CIVILIAN', 'BEECHCRAFT_CIVILIAN', 'GULFSTREAM_CIVILIAN',
            'LEARJET_CIVILIAN', 'CITATION_CIVILIAN', 'BELL_CIVILIAN',
            'SIKORSKY_CIVILIAN', 'ROBINSON_CIVILIAN', 'DASH8_CIVILIAN',
            'KINGAIR_CIVILIAN', 'CARAVAN_CIVILIAN', 'PC12_CIVILIAN'
        ]
        
        # Check if pure civilian without military platform
        has_civilian = any(civ in identified_platforms for civ in civilian_indicators)
        military_platforms = [p for p in identified_platforms 
                             if p in self.platform_mappings and p not in civilian_indicators]
        
        if has_civilian and not military_platforms:
            return ('Civilian Aircraft', PlatformDecision.GO, 'Pure Civilian Platform')
        
        # Process military platforms
        for platform in identified_platforms:
            if platform in self.platform_mappings:
                mapping = self.platform_mappings[platform]
                decision = mapping['decision']
                
                # Apply overrides
                if decision == PlatformDecision.NO_GO:
                    if has_amsc_override:
                        return (platform, PlatformDecision.GO, 
                               f"{mapping.get('civilian', platform)} with AMSC Z/commercial override")
                    elif has_commercial_override:
                        return (platform, PlatformDecision.GO,
                               f"{mapping.get('civilian', platform)} with commercial/FAA override")
                
                return (platform, decision, mapping.get('civilian'))
        
        # Check engines if no platform found
        for engine in identified_engines:
            if engine in self.engine_mappings:
                engine_info = self.engine_mappings[engine]
                decision = engine_info['decision']
                
                # Apply overrides for engines too
                if decision == PlatformDecision.NO_GO and (has_amsc_override or has_commercial_override):
                    return (f'{engine} Engine', PlatformDecision.GO, 
                           f"Commercial override for {engine} engine")
                
                return (f'{engine} Engine', decision, 
                       f"Engine for {', '.join(engine_info['platforms'])}")
        
        # Check for civilian manufacturer mentions (with word boundaries)
        text_lower = text.lower()
        for manufacturer in self.civilian_manufacturers:
            # Use word boundaries to avoid false matches like "atr" in "Patriot"
            if re.search(r'\b' + re.escape(manufacturer) + r'\b', text_lower):
                return (f'{manufacturer.title()} Aircraft', PlatformDecision.GO, 'Civilian Manufacturer')
        
        # No platform identified
        return (None, PlatformDecision.UNKNOWN, None)
    
    def assess_platform_impact(self, text: str) -> Dict:
        """
        Assess platform impact on opportunity with comprehensive override logic.
        
        Returns dict with:
            - platform: Identified platform
            - decision: GO/NO-GO/CONDITIONAL/UNKNOWN  
            - civilian_equivalent: Civilian platform if applicable
            - has_override: Whether override conditions apply
            - reasoning: Explanation
        """
        platform, decision, civilian = self.identify_platform(text)
        has_amsc = self.check_amsc_override(text)
        has_commercial = self.check_commercial_override(text)
        
        result = {
            'platform': platform,
            'decision': decision.value,
            'civilian_equivalent': civilian,
            'has_override': has_amsc or has_commercial,
            'reasoning': ''
        }
        
        if decision == PlatformDecision.GO:
            if has_amsc or has_commercial:
                result['reasoning'] = f'{platform} with override (AMSC Z or commercial standard)'
            elif civilian:
                result['reasoning'] = f'{platform} has civilian equivalent ({civilian})'
            else:
                result['reasoning'] = 'Pure civilian platform identified'
        elif decision == PlatformDecision.NO_GO:
            result['reasoning'] = f'{platform} is pure military with no civilian equivalent'
            if has_amsc or has_commercial:
                result['reasoning'] += ' (override conditions present but not applied)'
        elif decision == PlatformDecision.CONDITIONAL:
            result['reasoning'] = f'{platform} requires further analysis (limited civilian use)'
        else:
            result['reasoning'] = 'No specific platform identified'
        
        return result


def test_platform_mapper():
    """Test the comprehensive platform mapper."""
    mapper = PlatformMapper()
    
    test_cases = [
        # Pure military - should be NO-GO
        'F-16 Fighting Falcon engine parts',
        'F-22 Raptor avionics systems',
        'C-17 Globemaster III components',
        
        # Boeing variants with civilian equivalents - should be GO
        'KC-46 Pegasus tanker parts',
        'P-8 Poseidon maritime patrol aircraft',
        'E-3 Sentry AWACS systems',
        
        # C-130 variants
        'C-130 Hercules cargo aircraft parts',
        'L-100 civilian Hercules components',
        'C-130 with AMSC Code Z',
        
        # Pure civilian - should be GO
        'Boeing 737-800 commercial parts',
        'Cessna 172 general aviation',
        'Gulfstream V business jet',
        'Bell 407 helicopter parts',
        
        # Engines
        'CFM56 engine components',
        'F119 engine for F-22',
        'PT6 turboprop engine',
        
        # Override cases
        'F-16 parts with commercial equivalent acceptable',
        'C-130 FAA certified components'
    ]
    
    print('COMPREHENSIVE PLATFORM MAPPER TEST')
    print('='*60)
    
    for text in test_cases:
        result = mapper.assess_platform_impact(text)
        print(f'\nText: {text[:50]}...')
        print(f'  Platform: {result["platform"]}')
        print(f'  Decision: {result["decision"]}')
        if result['civilian_equivalent']:
            print(f'  Civilian: {result["civilian_equivalent"]}')
        if result['has_override']:
            print(f'  Override: YES')
        print(f'  Reason: {result["reasoning"][:70]}...')


if __name__ == '__main__':
    test_platform_mapper()