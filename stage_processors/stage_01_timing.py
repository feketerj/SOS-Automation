"""
Stage 1: TIMING Assessment
Checks if the opportunity deadline has passed
"""

import re
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dateutil import parser

logger = logging.getLogger(__name__)


class TimingStage:
    """Stage 1: Check opportunity deadlines"""

    def __init__(self):
        self.stage_name = "TIMING"
        self.stage_number = 1

        # Patterns for finding deadlines (including past tense)
        self.deadline_patterns = [
            r"(?:response|responses?|offers?|proposals?)\s+(?:are\s+|were\s+)?due\s+(?:by\s+)?([^\n,\.]+)",
            r"(?:submission|closing|deadline)\s+(?:date|time)[:\s]+([^\n,\.]+)",
            r"due\s+date[:\s]+([^\n,\.]+)",
            r"(?:due|were\s+due)\s+(?:by\s+|on\s+)?([^\n,\.]+)",
            r"closes?[:\s]+([^\n,\.]+)",
            r"must\s+be\s+(?:received|submitted)\s+by\s+([^\n,\.]+)",
            r"no\s+later\s+than\s+([^\n,\.]+)",
            r"NLT\s+([^\n,\.]+)",
            r"expires?\s+(?:on\s+)?([^\n,\.]+)",
            r"deadline[:\s]+([^\n,\.]+)"
        ]

    def extract_deadline(self, text: str) -> Optional[Tuple[str, datetime]]:
        """Extract deadline from text"""
        if not text:
            return None

        found_dates = []

        for pattern in self.deadline_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                date_str = match.group(1).strip()

                # Skip empty or invalid strings
                if not date_str or date_str.lower() in ['asap', 'tbd', 'tba', 'tomorrow', 'yesterday', 'soon']:
                    continue

                # Try to parse the date
                try:
                    # Clean up common additions
                    date_str = re.sub(r"\s*(?:Eastern|EST|EDT|Central|CST|CDT|Mountain|MST|MDT|Pacific|PST|PDT|HST).*", "", date_str)
                    date_str = re.sub(r"\s*(?:hours?|hrs?|ET|CT|MT|PT).*", "", date_str)

                    parsed_date = parser.parse(date_str, fuzzy=True)

                    # Only adjust year if the parsed year is way off (like 1900)
                    # Don't adjust if year is explicitly mentioned and reasonable
                    current_year = datetime.now().year
                    if parsed_date.year < 2000:  # Obviously wrong year
                        # If date would be in past this year, assume next year
                        test_date = parsed_date.replace(year=current_year)
                        if test_date < datetime.now():
                            parsed_date = parsed_date.replace(year=current_year + 1)
                        else:
                            parsed_date = test_date
                    # If explicit year is given (2024, 2025, etc), trust it

                    found_dates.append((match.group(0), parsed_date))

                except (ValueError, parser.ParserError) as e:
                    logger.debug(f"Could not parse date from: {date_str}")
                    continue

        # Return the earliest deadline found
        if found_dates:
            found_dates.sort(key=lambda x: x[1])
            return found_dates[0]

        return None

    def check_timing(self, opportunity_text: str, current_date: Optional[datetime] = None) -> Dict:
        """Main timing check logic"""
        if current_date is None:
            current_date = datetime.now()

        # Try to find deadline
        deadline_info = self.extract_deadline(opportunity_text)

        if deadline_info:
            evidence_text, deadline_date = deadline_info

            # Handle timezone-aware vs naive datetime comparison
            # Make both timezone-naive for comparison
            if deadline_date.tzinfo is not None:
                deadline_date = deadline_date.replace(tzinfo=None)
            if current_date.tzinfo is not None:
                current_date = current_date.replace(tzinfo=None)

            days_remaining = (deadline_date - current_date).days

            # Determine decision
            if days_remaining < 0:
                decision = "NO-GO"
                confidence = 0.99
                rationale = f"Opportunity expired {abs(days_remaining)} days ago"
            elif days_remaining == 0:
                decision = "NO-GO" if current_date.hour >= 14 else "INDETERMINATE"  # Assume 2PM cutoff
                confidence = 0.95 if decision == "INDETERMINATE" else 0.99
                rationale = "Deadline is today" + (" - may still be open" if decision == "INDETERMINATE" else " - likely closed")
            elif days_remaining <= 2:
                decision = "INDETERMINATE"
                confidence = 0.90
                rationale = f"Very tight deadline - only {days_remaining} days remaining"
            else:
                decision = "GO"
                confidence = 0.99
                rationale = f"Deadline in {days_remaining} days"

            return {
                "decision": decision,
                "confidence": confidence,
                "deadline_found": deadline_date.strftime("%Y-%m-%d %H:%M"),
                "days_remaining": days_remaining,
                "evidence": [evidence_text],
                "rationale": rationale
            }
        else:
            # No deadline found
            return {
                "decision": "GO",
                "confidence": 0.80,  # Lower confidence when no deadline found
                "deadline_found": None,
                "days_remaining": None,
                "evidence": ["No explicit deadline found in text"],
                "rationale": "No deadline found - opportunity may still be open",
                "flag": "NO_DEADLINE_FOUND"
            }

    def process(self, context: Dict, opportunity_text: str) -> Dict:
        """Process stage with context - PRESERVES METADATA AND DOCUMENTS"""
        logger.info(f"Processing Stage {self.stage_number}: {self.stage_name}")

        # Log document processing stats
        if context.get("document_stats"):
            logger.info(f"Processing {context['document_stats'].get('total_chars', 0)} chars "
                       f"from {context['document_stats'].get('total_documents', 0)} documents")

        # Try to get deadline from metadata first (most reliable)
        metadata = context.get("metadata", {})
        metadata_deadline = None
        if metadata.get("response_date_time"):
            try:
                metadata_deadline = parser.parse(metadata["response_date_time"])
                logger.info(f"Found deadline in metadata: {metadata_deadline}")
            except:
                pass

        # Get current date from context if provided
        current_date = datetime.now()
        if "current_date" in context:
            try:
                current_date = datetime.fromisoformat(context["current_date"])
            except:
                pass

        # Run timing check with full text (includes documents)
        result = self.check_timing(opportunity_text, current_date)

        # If no deadline found in text but metadata has one, use it
        if result.get("deadline_found") is None and metadata_deadline:
            days_remaining = (metadata_deadline - current_date).days
            result = {
                "decision": "NO-GO" if days_remaining < 0 else "GO" if days_remaining > 2 else "INDETERMINATE",
                "confidence": 0.99,
                "deadline_found": metadata_deadline.strftime("%Y-%m-%d %H:%M"),
                "days_remaining": days_remaining,
                "evidence": [f"Metadata response_date_time: {metadata['response_date_time']}"],
                "rationale": f"Deadline from metadata: {days_remaining} days {'remaining' if days_remaining >= 0 else 'ago'}"
            }

        # Add stage metadata
        result["stage_name"] = self.stage_name
        result["stage_number"] = self.stage_number

        return result


def create_batch_prompt(opportunity_text: str) -> str:
    """Create prompt for batch API"""
    current_date = datetime.now().strftime("%Y-%m-%d")

    return f"""Check if the opportunity deadline has passed.
Today's date: {current_date}

Look for: Response due date, submission deadline, closing date/time, "due by", "no later than", "expires".

If deadline has passed = NO-GO
If deadline is today = INDETERMINATE (might still be open)
If deadline is 1-2 days away = INDETERMINATE (very tight)
If deadline is future (3+ days) = GO
If no deadline found = GO (but flag it)

Opportunity text:
{opportunity_text[:3000]}

Output JSON only:
{{"decision": "GO|NO-GO|INDETERMINATE", "confidence": 0.99, "deadline_found": "YYYY-MM-DD HH:MM or null", "days_remaining": number_or_null, "evidence": ["exact quotes from text"], "rationale": "clear explanation"}}"""


def create_agent_prompt(opportunity_text: str, context: Dict) -> str:
    """Create prompt for agent API (placeholder)"""
    return f"[AGENT_PLACEHOLDER: timing_verification]"


if __name__ == "__main__":
    # Test the timing stage
    stage = TimingStage()

    test_cases = [
        "Responses are due by December 31, 2025 at 2:00 PM Eastern Time.",
        "Submission deadline: October 1, 2025",
        "This solicitation closes on September 15, 2025",
        "Proposals must be received no later than 30 days from posting",
        "No deadline specified in this opportunity"
    ]

    for test_text in test_cases:
        result = stage.check_timing(test_text)
        print(f"\nText: {test_text[:50]}...")
        print(f"Result: {json.dumps(result, indent=2)}")