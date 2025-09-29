"""
Stage 2: SET-ASIDES Assessment
Checks for small business set-aside requirements
"""

import re
import json
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class SetAsidesStage:
    """Stage 2: Check for small business set-asides"""

    def __init__(self):
        self.stage_name = "SET-ASIDES"
        self.stage_number = 2

        # Define set-aside types and their patterns
        self.set_aside_patterns = {
            "8(a)": [
                r"\b8\s*\(\s*a\s*\)",
                r"\b8a\b(?:\s+(?:set[\s\-]?aside|business))?",  # Match "8a" standalone too
                r"\bsection\s+8\s*\(\s*a\s*\)",
                r"\b8\s*\(\s*a\s*\)\s+(?:competitive|sole[\s\-]?source)"
            ],
            "SDVOSB": [
                r"\bSDVOSB\b",
                r"\bService[\s\-]?Disabled[\s\-]?Veteran[\s\-]?Owned[\s\-]?Small[\s\-]?Business",
                r"\bSD[\s\-]?VOSB\b"
            ],
            "VOSB": [
                r"\bVOSB\b(?!\s*Service[\s\-]?Disabled)",
                r"\bVeteran[\s\-]?Owned[\s\-]?Small[\s\-]?Business\b(?!\s*Service[\s\-]?Disabled)"
            ],
            "WOSB": [
                r"\bWOSB\b",
                r"\bWomen[\s\-]?Owned[\s\-]?Small[\s\-]?Business",
                r"\bWO[\s\-]?SB\b",
                r"\bEDWOSB\b",
                r"\bEconomically[\s\-]?Disadvantaged[\s\-]?Women"
            ],
            "HUBZone": [
                r"\bHUBZone\b",
                r"\bHUB[\s\-]?Zone\b",
                r"\bHistorically[\s\-]?Underutilized[\s\-]?Business[\s\-]?Zone"
            ],
            "Small Business Set-Aside": [
                r"\bTotal[\s\-]?Small[\s\-]?Business[\s\-]?Set[\s\-]?Aside\b",
                r"\bSmall[\s\-]?Business[\s\-]?Set[\s\-]?Aside\b",
                r"\b(?:Set[\s\-]?Aside|Reserved)\s+for\s+Small[\s\-]?Business",
                r"\bSB[\s\-]?Set[\s\-]?Aside\b"
            ]
        }

        # Negative patterns that might override set-asides
        self.exception_patterns = [
            r"\bnot\s+(?:a\s+)?set[\s\-]?aside",
            r"\bun[\s\-]?restricted",
            r"\bfull\s+and\s+open",
            r"\bopen\s+competition",
            r"\bother\s+than\s+small",
            r"\blarge\s+business"
        ]

    def find_set_asides(self, text: str) -> List[Tuple[str, str, str]]:
        """Find all set-aside mentions in text"""
        found_set_asides = []

        for set_aside_type, patterns in self.set_aside_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    # Get context around match (50 chars before and after)
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end].strip()

                    # Check if this is negated - look before AND around the match
                    negation_check = text[max(0, match.start() - 100):match.end() + 50]
                    is_negated = any(re.search(neg_pattern, negation_check, re.IGNORECASE)
                                    for neg_pattern in self.exception_patterns)

                    # Also check for specific negation phrases
                    specific_negations = [
                        r"not\s+an?\s+" + re.escape(match.group(0)),
                        r"was\s+previously\s+" + re.escape(match.group(0)),
                        r"no\s+longer\s+" + re.escape(match.group(0)),
                        re.escape(match.group(0)) + r"\s*\(\s*not",  # "SDVO (not SDVOSB)"
                        r"\bnot\s+" + re.escape(match.group(0))  # "not SDVOSB"
                    ]
                    for neg in specific_negations:
                        if re.search(neg, negation_check, re.IGNORECASE):
                            is_negated = True
                            break

                    if not is_negated:
                        found_set_asides.append((set_aside_type, match.group(0), context))

        return found_set_asides

    def check_naics_size_standard(self, text: str) -> Optional[str]:
        """Check for NAICS code and size standard indicators"""
        # Look for NAICS codes
        naics_pattern = r"NAICS\s*(?:Code)?\s*[:\s]*(\d{6})"
        naics_match = re.search(naics_pattern, text, re.IGNORECASE)

        if naics_match:
            # Check for size standard mentions
            size_patterns = [
                r"Size\s+Standard[:\s]*\$?(\d+(?:\.\d+)?)\s*(?:million|M)",
                r"Size\s+Standard[:\s]*(\d+)\s+employees",
                r"small\s+business\s+size\s+standard"
            ]

            for pattern in size_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return f"NAICS {naics_match.group(1)} with size standard"

        return None

    def check_set_asides(self, opportunity_text: str, context: Dict = None) -> Dict:
        """Main set-aside check logic"""
        # Handle empty input
        if not opportunity_text:
            return {
                "decision": "GO",
                "confidence": 0.95,
                "set_aside_types": [],
                "set_aside_count": 0,
                "evidence": ["No text provided"],
                "rationale": "No text to analyze for set-asides",
                "naics_info": None
            }

        # Find all set-aside mentions
        set_asides_found = self.find_set_asides(opportunity_text)

        # Check for NAICS/size indicators
        naics_info = self.check_naics_size_standard(opportunity_text)

        if set_asides_found:
            # Group by type
            unique_types = list(set(sa[0] for sa in set_asides_found))

            # Get evidence
            evidence = [f"{sa[0]}: {sa[2]}" for sa in set_asides_found[:3]]  # First 3 examples

            return {
                "decision": "NO-GO",
                "confidence": 0.99,
                "set_aside_types": unique_types,
                "set_aside_count": len(set_asides_found),
                "evidence": evidence,
                "rationale": f"Found {len(unique_types)} set-aside type(s): {', '.join(unique_types)}",
                "naics_info": naics_info
            }

        elif naics_info:
            # Found NAICS but no explicit set-aside
            return {
                "decision": "INDETERMINATE",
                "confidence": 0.85,
                "set_aside_types": [],
                "set_aside_count": 0,
                "evidence": [f"Found {naics_info} but no explicit set-aside statement"],
                "rationale": "Has NAICS code with size standard but no clear set-aside designation",
                "naics_info": naics_info,
                "flag": "NAICS_WITHOUT_SET_ASIDE"
            }

        else:
            # Check for explicit non-set-aside statements
            for pattern in self.exception_patterns:
                match = re.search(pattern, opportunity_text, re.IGNORECASE)
                if match:
                    return {
                        "decision": "GO",
                        "confidence": 0.99,
                        "set_aside_types": [],
                        "set_aside_count": 0,
                        "evidence": [match.group(0)],
                        "rationale": "Explicitly stated as unrestricted/full and open competition",
                        "naics_info": None
                    }

            # No set-aside found
            return {
                "decision": "GO",
                "confidence": 0.95,
                "set_aside_types": [],
                "set_aside_count": 0,
                "evidence": ["No set-aside designations found"],
                "rationale": "No small business set-aside requirements detected",
                "naics_info": None
            }

    def process(self, context: Dict, opportunity_text: str) -> Dict:
        """Process stage with context"""
        logger.info(f"Processing Stage {self.stage_number}: {self.stage_name}")

        # Check previous findings for relevant info
        if context and "key_findings" in context:
            # Look for agency info that might affect set-aside interpretation
            pass

        # Run set-aside check
        result = self.check_set_asides(opportunity_text, context)

        # Add stage metadata
        result["stage_name"] = self.stage_name
        result["stage_number"] = self.stage_number

        return result


def create_batch_prompt(opportunity_text: str, context: Dict = None) -> str:
    """Create prompt for batch API"""
    context_summary = context.get("summary", "") if context else ""

    return f"""Check for small business set-asides.
Previous findings: {context_summary}

Look for EXACT matches:
- "8(a)" or "8a set-aside" or "Section 8(a)"
- "SDVOSB" or "Service-Disabled Veteran-Owned"
- "VOSB" or "Veteran-Owned Small Business" (not SDVOSB)
- "WOSB" or "Women-Owned Small Business" or "EDWOSB"
- "HUBZone" or "Historically Underutilized Business Zone"
- "Total Small Business Set-Aside" or "Small Business Set-Aside"

Also check for:
- "unrestricted" or "full and open" = likely NOT set-aside
- NAICS code with size standard = possible set-aside

If ANY set-aside found = NO-GO
If explicitly unrestricted = GO
If NAICS but no set-aside = INDETERMINATE
If NONE found = GO

Opportunity text:
{opportunity_text[:3000]}

Output JSON only:
{{"decision": "GO|NO-GO|INDETERMINATE", "confidence": 0.99, "set_aside_types": ["list of types found"], "evidence": ["exact quotes"], "rationale": "explanation"}}"""


if __name__ == "__main__":
    # Test the set-aside stage
    stage = SetAsidesStage()

    test_cases = [
        "This procurement is set aside for 8(a) certified small businesses.",
        "NAICS Code: 541330, Size Standard: $16.5 million. This is a Total Small Business Set-Aside.",
        "This is an unrestricted, full and open competition.",
        "Service-Disabled Veteran-Owned Small Business (SDVOSB) set-aside procurement.",
        "NAICS 541611 with size standard but no mention of set-aside.",
        "No special requirements for this opportunity."
    ]

    for test_text in test_cases:
        result = stage.check_set_asides(test_text)
        print(f"\nText: {test_text[:60]}...")
        print(f"Result: {json.dumps(result, indent=2)}")