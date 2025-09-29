"""
Stage 3: SECURITY Assessment
Checks for security clearance and classification requirements
"""

import re
import json
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class SecurityStage:
    """Stage 3: Check for security clearance requirements"""

    def __init__(self):
        self.stage_name = "SECURITY"
        self.stage_number = 3

        # Security clearance levels and patterns
        self.clearance_patterns = {
            "TOP SECRET/SCI": [
                r"\bTS\/SCI\b",
                r"\bTop\s+Secret\/SCI\b",
                r"\bTop\s+Secret\s+with\s+SCI\b",
                r"\bTS\s+w\/\s*SCI\b"
            ],
            "TOP SECRET": [
                r"\bTop\s+Secret\b(?!.*\/SCI)",
                r"\bTS\b(?!.*\/SCI)(?!.*SCI)",
                r"\bTS\s+clearance\b(?!.*SCI)"
            ],
            "SECRET": [
                r"\bSecret\s+clearance\b",
                r"\bSecret\s+level\b",
                r"\b(?<!Top\s)Secret\b(?!\s+Service)",
                r"\bS\s+clearance\b"
            ],
            "CONFIDENTIAL": [
                r"\bConfidential\s+clearance\b",
                r"\bConfidential\s+level\b"
            ],
            "PUBLIC TRUST": [
                r"\bPublic\s+Trust\b",
                r"\bPosition\s+of\s+Trust\b",
                r"\bMBI\b",
                r"\bModerate\s+Background\s+Investigation\b"
            ],
            "DOE Q": [
                r"\bQ\s+clearance\b",
                r"\bDOE\s+Q\b"
            ],
            "DOE L": [
                r"\bL\s+clearance\b",
                r"\bDOE\s+L\b"
            ]
        }

        # Facility clearance patterns
        self.facility_patterns = [
            r"\bFacility\s+Clearance\b",
            r"\bFacility\s+Security\s+Clearance\b",
            r"\bFCL\b",
            r"\bDD[\s\-]?254\b",
            r"\bNISPOM\b",
            r"\bNational\s+Industrial\s+Security\s+Program\b"
        ]

        # Special access programs
        self.sap_patterns = [
            r"\bSAP\b(?!\s+(?:software|system))",
            r"\bSpecial\s+Access\s+Program",
            r"\bSAR\s+code",
            r"\bSpecial\s+Access\s+Required"
        ]

        # Classification markings
        self.classification_patterns = [
            r"\bClassified\s+(?:information|data|work|contract)",
            r"\b(?:FOUO|For\s+Official\s+Use\s+Only)\b",
            r"\bCUI\b",
            r"\bControlled\s+Unclassified\s+Information\b",
            r"\bITAR[\s\-]controlled\b",
            r"\bExport[\s\-]controlled\b"
        ]

        # Negative patterns (things that look like security but aren't)
        self.false_positive_patterns = [
            r"\bSecret(?:ary|ariat)\b",
            r"\bconfidential(?:ity|ly)\b",
            r"\bpublic\s+trust\s+(?:and\s+)?confidence\b",
            r"\bSAP\s+(?:software|system|ERP)\b"
        ]

    def find_clearance_requirements(self, text: str) -> List[Tuple[str, str, str]]:
        """Find all clearance requirement mentions"""
        found_clearances = []

        # First check for special clearance patterns
        special_patterns = [
            (r"\b(?:Secret|Confidential|TS|Top\s+Secret)\s+or\s+(?:higher|above)\b", "SECRET", "Range requirement"),
            (r"\bInterim\s+(?:Secret|TS|Top\s+Secret|Confidential)\b", "SECRET", "Interim clearance"),
            (r"\b(?:must\s+have\s+)?L\s+clearance\b", "DOE L", "DOE L clearance")
        ]

        for pattern, level, desc in special_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()
                found_clearances.append((level, match.group(0), context))

        for clearance_level, patterns in self.clearance_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    # Get context
                    start = max(0, match.start() - 100)
                    end = min(len(text), match.end() + 100)
                    context = text[start:end].strip()

                    # Check for false positives
                    is_false_positive = any(
                        re.search(fp, context, re.IGNORECASE)
                        for fp in self.false_positive_patterns
                    )

                    if not is_false_positive:
                        # Check if it's a requirement or just mentioned
                        requirement_keywords = [
                            r"\brequir",
                            r"\bmust\s+(?:have|possess|maintain)",
                            r"\bmandatory\b",
                            r"\bneeded\b",
                            r"\beligib"
                        ]

                        # Check for preference vs requirement
                        preference_keywords = [
                            r"\bprefer",
                            r"\bdesir",
                            r"\bnice\s+to\s+have",
                            r"\bbut\s+not\s+requir",
                            r"\boptional"
                        ]

                        is_preference = any(
                            re.search(pref, context, re.IGNORECASE)
                            for pref in preference_keywords
                        )

                        is_requirement = any(
                            re.search(kw, context, re.IGNORECASE)
                            for kw in requirement_keywords
                        ) and not is_preference

                        if is_requirement:
                            found_clearances.append((clearance_level, match.group(0), context))

        return found_clearances

    def find_facility_requirements(self, text: str) -> List[str]:
        """Find facility clearance requirements"""
        facility_requirements = []

        for pattern in self.facility_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Get context
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()
                facility_requirements.append(context)

        return facility_requirements

    def find_sap_requirements(self, text: str) -> List[str]:
        """Find Special Access Program requirements"""
        sap_requirements = []

        for pattern in self.sap_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Get context
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()

                # Verify it's not SAP software
                if not re.search(r"\bSAP\s+(?:software|system|ERP)", context, re.IGNORECASE):
                    sap_requirements.append(context)

        return sap_requirements

    def check_security(self, opportunity_text: str, context: Dict = None) -> Dict:
        """Main security check logic"""
        # Handle empty input
        if not opportunity_text:
            return {
                "decision": "GO",
                "confidence": 0.95,
                "clearance_level": None,
                "has_facility_requirement": False,
                "has_sap_requirement": False,
                "evidence": ["No text provided"],
                "rationale": "No text to analyze for security requirements"
            }

        # Find all security requirements
        clearance_reqs = self.find_clearance_requirements(opportunity_text)
        facility_reqs = self.find_facility_requirements(opportunity_text)
        sap_reqs = self.find_sap_requirements(opportunity_text)

        # Determine highest clearance level required
        highest_clearance = None
        if clearance_reqs:
            # Order of precedence (DOE Q is equivalent to TOP SECRET)
            clearance_order = ["TOP SECRET/SCI", "TOP SECRET", "DOE Q", "SECRET", "DOE L", "CONFIDENTIAL", "PUBLIC TRUST"]
            for level in clearance_order:
                if any(req[0] == level for req in clearance_reqs):
                    highest_clearance = level
                    break

        # Build evidence
        evidence = []
        if clearance_reqs:
            evidence.extend([req[2] for req in clearance_reqs[:2]])  # First 2 clearance mentions
        if facility_reqs:
            evidence.append(f"Facility: {facility_reqs[0]}")
        if sap_reqs:
            evidence.append(f"SAP: {sap_reqs[0]}")

        # Determine decision
        if clearance_reqs or facility_reqs or sap_reqs:
            # Any security requirement is a NO-GO
            requirements = []
            if highest_clearance:
                requirements.append(f"{highest_clearance} clearance")
            if facility_reqs:
                requirements.append("Facility clearance")
            if sap_reqs:
                requirements.append("SAP access")

            return {
                "decision": "NO-GO",
                "confidence": 0.99,
                "clearance_level": highest_clearance,
                "has_facility_requirement": len(facility_reqs) > 0,
                "has_sap_requirement": len(sap_reqs) > 0,
                "evidence": evidence,
                "rationale": f"Requires: {', '.join(requirements)}"
            }

        # Check for classification markings (might be INDETERMINATE)
        classification_found = False
        for pattern in self.classification_patterns:
            if re.search(pattern, opportunity_text, re.IGNORECASE):
                classification_found = True
                break

        if classification_found:
            return {
                "decision": "INDETERMINATE",
                "confidence": 0.85,
                "clearance_level": None,
                "has_facility_requirement": False,
                "has_sap_requirement": False,
                "evidence": ["Found classification markings but no explicit clearance requirement"],
                "rationale": "Contains controlled information indicators but unclear if clearance required",
                "flag": "CLASSIFICATION_WITHOUT_CLEARANCE"
            }

        # No security requirements found
        return {
            "decision": "GO",
            "confidence": 0.95,
            "clearance_level": None,
            "has_facility_requirement": False,
            "has_sap_requirement": False,
            "evidence": ["No security clearance requirements found"],
            "rationale": "No security clearance or facility requirements detected"
        }

    def process(self, context: Dict, opportunity_text: str) -> Dict:
        """Process stage with context"""
        logger.info(f"Processing Stage {self.stage_number}: {self.stage_name}")

        # Run security check
        result = self.check_security(opportunity_text, context)

        # Add stage metadata
        result["stage_name"] = self.stage_name
        result["stage_number"] = self.stage_number

        return result


def create_batch_prompt(opportunity_text: str, context: Dict = None) -> str:
    """Create prompt for batch API"""
    context_summary = context.get("summary", "") if context else ""

    return f"""Check for security clearance requirements.
Previous findings: {context_summary}

Look for keywords indicating REQUIRED clearance:
- "Secret", "Top Secret", "TS/SCI", "Classified"
- "Security Clearance Required" or "must have clearance"
- "Facility Clearance" or "FCL"
- "DD-254" or "NISPOM"
- "SAP" or "Special Access Program"

Ignore:
- "Secretary" (the person)
- "confidentially" (adverb)
- "SAP software" or "SAP system" (enterprise software)

If clearance REQUIRED = NO-GO
If only mentions classified info but no requirement = INDETERMINATE
If NO security requirements = GO

Opportunity text:
{opportunity_text[:3000]}

Output JSON only:
{{"decision": "GO|NO-GO|INDETERMINATE", "confidence": 0.99, "clearance_level": "level or null", "has_facility_requirement": boolean, "has_sap_requirement": boolean, "evidence": ["exact quotes"], "rationale": "explanation"}}"""


if __name__ == "__main__":
    # Test the security stage
    stage = SecurityStage()

    test_cases = [
        "Contractor must possess a Secret clearance and maintain facility clearance.",
        "Work involves Top Secret/SCI information. TS/SCI clearance required.",
        "This contract involves ITAR-controlled technical data.",
        "Personnel must have Public Trust position eligibility.",
        "No special security requirements for this commercial item procurement.",
        "Secretary of Defense has approved this acquisition.",
        "Requires SAP software expertise and database management."
    ]

    for test_text in test_cases:
        result = stage.check_security(test_text)
        print(f"\nText: {test_text[:60]}...")
        print(f"Result: {json.dumps(result, indent=2)}")