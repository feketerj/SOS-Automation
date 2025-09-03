#!/usr/bin/env python3
"""
SOS Pipeline Title Generator
Generates standardized pipeline titles from opportunity data
"""

import re
from typing import Dict, Optional

class PipelineTitleGenerator:
    """Generate SOS Pipeline Titles in standard format"""
    
    def __init__(self):
        """Initialize with common patterns"""
        self.aircraft_patterns = {
            'KC-46': 'KC-46 Pegasus',
            'P-8': 'P-8 Poseidon',
            'C-130': 'C-130 Hercules',
            'F-15': 'F-15 Eagle',
            'F-16': 'F-16 Falcon',
            'F-18': 'F/A-18 Hornet',
            'C-17': 'C-17 Globemaster',
            'B-52': 'B-52 Stratofortress',
            'A-10': 'A-10 Thunderbolt',
            'E-3': 'E-3 Sentry',
            'KC-135': 'KC-135 Stratotanker'
        }
        
        self.condition_keywords = {
            'new': ['new', 'unused', 'factory'],
            'refurb': ['refurb', 'refurbish', 'recondition', 'overhaul'],
            'surplus': ['surplus', 'excess', 'DIBBS', 'DRMO'],
            'repair': ['repair', 'fix', 'maintenance'],
            'used': ['used', 'serviceable', 'as-is']
        }
    
    def generate_title(self, opportunity: Dict) -> str:
        """
        Generate pipeline title from opportunity data
        
        EXACT FORMAT: 
        PN: [part numbers or NA] | Qty: [quantity per PN or NA] | Condition: [new/surplus/overhaul/etc.] | MDS: [aircraft type or NA] | [solicitation_id] | [brief description of work]
        
        Example: PN: 8675-309 | Qty: 23 | Condition: refurb | MDS: P-8 Poseidon | N48666757PS9494-5 | Purchase refurb brackets
        """
        
        title = opportunity.get('title', '')
        description = opportunity.get('description', opportunity.get('full_text', ''))[:1000]
        solicitation_number = opportunity.get('solicitation_number', opportunity.get('announcement_number', ''))
        
        # Extract components
        part_numbers = self._extract_part_numbers(title + ' ' + description)
        quantities = self._extract_quantities(title + ' ' + description)
        condition = self._determine_condition(title + ' ' + description)
        aircraft = self._identify_aircraft(title + ' ' + description)
        work_description = self._create_brief_description(title)
        
        # Build pipeline title EXACTLY as specified
        # PN: [part numbers or NA]
        pn_str = part_numbers[0] if part_numbers else 'NA'
        
        # Qty: [quantity per PN or NA]
        qty_str = str(quantities[0]) if quantities else 'NA'
        
        # Condition: [new/surplus/overhaul/etc.]
        condition_str = condition.lower()
        
        # MDS: [aircraft type or NA]
        mds_str = aircraft if aircraft else 'NA'
        
        # [solicitation_id]
        solicitation_id = solicitation_number if solicitation_number else 'NO-SOLICITATION'
        
        # [brief description of work]
        work_desc = work_description if work_description else 'General procurement'
        
        # Assemble EXACTLY as specified
        pipeline_title = f"PN: {pn_str} | Qty: {qty_str} | Condition: {condition_str} | MDS: {mds_str} | {solicitation_id} | {work_desc}"
        
        return pipeline_title
    
    def _extract_part_numbers(self, text: str) -> list:
        """Extract part numbers from text"""
        part_numbers = []
        
        # Common part number patterns
        patterns = [
            r'\b\d{4,6}-\d{3,6}\b',  # 1234-5678
            r'\b\d{4,6}-\d{3,6}-\d{1,4}\b',  # 1234-5678-90
            r'\bP/N[\s:]*([A-Z0-9-]+)',  # P/N ABC-123
            r'\bPN[\s:]*([A-Z0-9-]+)',  # PN ABC-123
            r'\bNSN[\s:]*\d{4}-\d{2}-\d{3}-\d{4}',  # NSN format
            r'\b[A-Z]{2,4}\d{4,8}[A-Z]?\b'  # AB12345C
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            part_numbers.extend(matches)
        
        return part_numbers[:5]  # Return up to 5 part numbers
    
    def _extract_quantities(self, text: str) -> list:
        """Extract quantities from text"""
        quantities = []
        
        # Patterns for quantities
        patterns = [
            r'qty[\s:]*(\d+)',
            r'quantity[\s:]*(\d+)',
            r'\b(\d+)\s*(?:ea|each|units?|pieces?)\b',
            r'deliver\s+(\d+)',
            r'procure\s+(\d+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            quantities.extend([int(m) for m in matches if m.isdigit()])
        
        return quantities[:3]  # Return up to 3 quantities
    
    def _determine_condition(self, text: str) -> str:
        """Determine the condition of items"""
        text_lower = text.lower()
        
        for condition, keywords in self.condition_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return condition.capitalize()
        
        # Default to 'unknown' instead of 'TBD'
        return 'unknown'
    
    def _identify_aircraft(self, text: str) -> str:
        """Identify aircraft type mentioned"""
        text_upper = text.upper()
        
        for pattern, full_name in self.aircraft_patterns.items():
            if pattern in text_upper:
                return full_name
        
        # Check for generic aircraft mentions
        if 'AIRCRAFT' in text_upper:
            return 'Aircraft'
        elif 'HELICOPTER' in text_upper:
            return 'Helicopter'
        elif 'UAV' in text_upper or 'DRONE' in text_upper:
            return 'UAV'
        
        return ''
    
    def _create_brief_description(self, title: str) -> str:
        """Create brief description from title"""
        # Clean and truncate title
        title = re.sub(r'[^\w\s-]', '', title)
        title = ' '.join(title.split())
        
        # Remove common prefixes
        for prefix in ['RFQ', 'RFP', 'RFI', 'Sources Sought']:
            if title.upper().startswith(prefix.upper()):
                title = title[len(prefix):].strip()
        
        # Truncate to reasonable length
        if len(title) > 50:
            title = title[:47] + '...'
        
        return title if title else 'Procurement'


def test_generator():
    """Test the pipeline title generator"""
    
    generator = PipelineTitleGenerator()
    
    print("EXACT FORMAT REQUIRED:")
    print("PN: [part# or NA] | Qty: [qty or NA] | Condition: [new/surplus/etc.] | MDS: [aircraft or NA] | [solicitation_id] | [description]")
    print("="*80)
    print()
    
    test_cases = [
        {
            'title': 'KC-46 Spare Parts RFQ',
            'solicitation_number': 'FA8606-25-Q-0123',
            'description': 'Procure 23 refurbished brackets P/N 8675-309 for KC-46 aircraft'
        },
        {
            'title': 'P-8 Poseidon Maintenance',
            'solicitation_number': 'N00019-25-R-0456',
            'description': 'Repair and overhaul of P-8 aircraft components'
        },
        {
            'title': 'Aircraft Parts',
            'solicitation_number': 'SPE4A5-25-R-0789',
            'description': 'Various surplus parts from DIBBS'
        }
    ]
    
    print("Test Results:")
    for case in test_cases:
        title = generator.generate_title(case)
        print(f"Input: {case['title']}")
        print(f"Output: {title}")
        print()


if __name__ == "__main__":
    test_generator()