#!/usr/bin/env python3
"""
Unified Output Formatter - Ensures consistent output across all assessment stages.
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any
import json
import re

class UnifiedOutputFormatter:
    """Formats assessment outputs according to unified schema."""

    def __init__(self):
        self.decision_values = ["GO", "NO-GO", "INDETERMINATE"]
        self.scope_values = ["Purchase", "Manufacture", "Managed Repair"]
        self.category_names = {
            1: "TIMING",
            2: "DOMAIN",
            3: "SECURITY",
            4: "SET-ASIDES",
            5: "SOURCE RESTRICTIONS",
            6: "TECHNICAL DATA",
            7: "EXPORT CONTROL",
            8: "AMC/AMSC",
            9: "SAR",
            10: "PLATFORM",
            11: "PROCUREMENT",
            12: "COMPETITION",
            13: "SUBCONTRACTING",
            14: "VEHICLES",
            15: "EXPERIMENTAL",
            16: "IT ACCESS",
            17: "CERTIFICATIONS",
            18: "WARRANTY/DEPOT",
            19: "CAD/CAM"
        }

    def create_output(self,
                      decision: str,
                      solicitation_number: str,
                      solicitation_title: str,
                      **kwargs) -> Dict:
        """Create a unified output structure."""

        # Validate decision
        if decision not in self.decision_values:
            raise ValueError(f"Decision must be one of: {self.decision_values}")

        output = {
            "decision": decision,
            "solicitation_number": solicitation_number,
            "solicitation_title": solicitation_title,
            "platform_info": kwargs.get("platform_info", {
                "mds": "NA",
                "commercial_designation": "NA",
                "classification": "Indeterminate"
            }),
            "dates": self._calculate_dates(kwargs.get("date_posted"), kwargs.get("date_due")),
            "scope": kwargs.get("scope", "Purchase"),
            "knockout_category": kwargs.get("knockout_category"),
            "knockout_reason": kwargs.get("knockout_reason"),
            "rationale": kwargs.get("rationale", ""),
            "pipeline_notes": self._format_pipeline_notes(kwargs.get("pipeline_data", {})),
            "contact_co": kwargs.get("contact_co", {
                "required": False,
                "questions": [],
                "reason": ""
            }),
            "potential_award": kwargs.get("potential_award", {
                "exceeds_25k": True,
                "estimated_range": "Unknown",
                "reasoning": "Unable to determine from available information"
            })
        }

        # Add pipeline stage info
        output["pipeline_stage"] = kwargs.get("pipeline_stage", "UNKNOWN")
        output["assessment_type"] = kwargs.get("assessment_type", "UNKNOWN")

        return output

    def _calculate_dates(self, date_posted: Optional[str], date_due: Optional[str]) -> Dict:
        """Calculate date-related fields."""
        dates = {
            "triage_date": datetime.now().strftime("%m-%d-%Y"),
            "date_posted": date_posted or "Unknown",
            "date_due": date_due or "Unknown",
            "days_open": 0,
            "remaining_days": 0
        }

        if date_posted and date_due:
            try:
                posted = datetime.strptime(date_posted, "%m-%d-%Y")
                due = datetime.strptime(date_due, "%m-%d-%Y")
                today = datetime.now()

                dates["days_open"] = (due - posted).days
                dates["remaining_days"] = max(0, (due - today).days)
            except ValueError:
                pass  # Keep defaults if date parsing fails

        return dates

    def _format_pipeline_notes(self, pipeline_data: Dict) -> str:
        """Format pipeline notes according to spec."""
        if not pipeline_data:
            return "PN: NA | Qty: NA | Condition: NA | MDS: NA | NA | No specific data"

        parts = pipeline_data.get("part_numbers", ["NA"])
        quantities = pipeline_data.get("quantities", ["NA"])
        condition = pipeline_data.get("condition", "NA")
        mds = pipeline_data.get("mds", "NA")
        solicitation = pipeline_data.get("solicitation_id", "NA")
        description = pipeline_data.get("description", "No description")

        # Format part numbers and quantities
        pn_str = ", ".join(str(p) for p in parts) if parts else "NA"
        qty_str = ", ".join(str(q) for q in quantities) if quantities else "NA"

        return f"PN: {pn_str} | Qty: {qty_str} | Condition: {condition} | MDS: {mds} | {solicitation} | {description}"

    def format_text_output(self, output: Dict) -> str:
        """Format output as text report."""

        header = f"{output['decision']}-{output['solicitation_number']}"

        text = f"""
{header}
{'=' * len(header)}

Solicitation Title: {output['solicitation_title']}
Solicitation Number: {output['solicitation_number']}
Mission Design Series, Platform & Commercial Designation:
{output['platform_info']['mds']} | {output['platform_info']['commercial_designation']} | {output['platform_info']['classification']}

Triage Date: {output['dates']['triage_date']}
Date Posted: {output['dates']['date_posted']}
Date Responses Due: {output['dates']['date_due']}
Days Open: {output['dates']['days_open']}
Remaining Days: {output['dates']['remaining_days']}

Potential Award:
Exceeds $25K: {'Yes' if output['potential_award']['exceeds_25k'] else 'No'}, {output['potential_award']['reasoning']}
Range: {output['potential_award']['estimated_range']}

Scope: {output['scope']}

Final Recommendation: {output['decision']}
{output['rationale']}
"""

        # Add knockout logic if NO-GO
        if output['decision'] == "NO-GO" and output.get('knockout_category'):
            cat_num = output['knockout_category']
            cat_name = self.category_names.get(cat_num, "UNKNOWN")
            text += f"\nKnockout Logic:\nCategory {cat_num}: {cat_name}\n{output.get('knockout_reason', '')}\n"

        # Add pipeline notes
        text += f"\nSOS Pipeline Notes:\n{output['pipeline_notes']}\n"

        # Add Contact CO section if required
        if output['contact_co']['required']:
            text += "\nQuestions for CO:\n"
            for i, question in enumerate(output['contact_co']['questions'], 1):
                text += f"{i}. {question}\n"

        return text

    def format_email_subject(self, output: Dict) -> str:
        """Generate email subject line."""
        mds = output['platform_info'].get('mds', '')
        scope = output.get('scope', 'Parts')

        if mds and mds != "NA":
            return f"Source One Spares: {scope} Available for {mds}"
        else:
            return f"Source One Spares: {scope} Available for Future Consideration"

    def validate_output(self, output: Dict) -> List[str]:
        """Validate output against schema requirements."""
        errors = []

        # Required fields
        required = ['decision', 'solicitation_number', 'solicitation_title']
        for field in required:
            if field not in output:
                errors.append(f"Missing required field: {field}")

        # Decision validation
        if output.get('decision') not in self.decision_values:
            errors.append(f"Invalid decision value: {output.get('decision')}")

        # NO-GO must have category
        if output.get('decision') == "NO-GO":
            if not output.get('knockout_category'):
                errors.append("NO-GO decision missing knockout_category")
            elif output['knockout_category'] not in self.category_names:
                errors.append(f"Invalid knockout_category: {output['knockout_category']}")

        # INDETERMINATE should have contact_co
        if output.get('decision') == "INDETERMINATE":
            if not output.get('contact_co', {}).get('required'):
                errors.append("INDETERMINATE decision should have contact_co.required = True")

        return errors

    def merge_stage_outputs(self, regex_output: Dict, batch_output: Dict = None, agent_output: Dict = None) -> Dict:
        """Merge outputs from multiple stages into unified format."""

        # Start with regex output as base
        merged = regex_output.copy()

        # Override with batch output if available
        if batch_output:
            merged.update({
                "decision": batch_output.get("decision", merged.get("decision")),
                "rationale": batch_output.get("rationale", merged.get("rationale")),
                "pipeline_stage": "BATCH",
                "assessment_type": "MISTRAL_BATCH_ASSESSMENT"
            })

        # Override with agent output if available (highest priority)
        if agent_output:
            merged.update({
                "decision": agent_output.get("decision", merged.get("decision")),
                "rationale": agent_output.get("rationale", merged.get("rationale")),
                "pipeline_stage": "AGENT",
                "assessment_type": "MISTRAL_ASSESSMENT",
                "contact_co": agent_output.get("contact_co", merged.get("contact_co"))
            })

        return merged


# Usage example
if __name__ == "__main__":
    formatter = UnifiedOutputFormatter()

    # Example 1: NO-GO output
    no_go_output = formatter.create_output(
        decision="NO-GO",
        solicitation_number="FA8501-24-R-0001",
        solicitation_title="F-16 Engine Components",
        knockout_category=10,
        knockout_reason="Pure military platform without AMSC override",
        rationale="F-16 is a military fighter aircraft and no AMSC Z/G/A code was found",
        platform_info={
            "mds": "F-16 Fighting Falcon",
            "commercial_designation": "NA",
            "classification": "Military"
        },
        pipeline_stage="REGEX",
        assessment_type="REGEX_KNOCKOUT"
    )

    print("=== NO-GO JSON Output ===")
    print(json.dumps(no_go_output, indent=2))

    print("\n=== NO-GO Text Output ===")
    print(formatter.format_text_output(no_go_output))

    # Example 2: INDETERMINATE output
    indeterminate_output = formatter.create_output(
        decision="INDETERMINATE",
        solicitation_number="N00019-24-R-0123",
        solicitation_title="P-8 Poseidon Landing Gear",
        rationale="Navy commercial platform with approved sources requirement and FAA 8130-3 capability",
        platform_info={
            "mds": "P-8 Poseidon",
            "commercial_designation": "Boeing 737",
            "classification": "Commercial"
        },
        contact_co={
            "required": True,
            "questions": [
                "Would FAA certified repair stations be considered as approved sources?",
                "Can commercial equivalents with 8130-3 certification satisfy the requirement?"
            ],
            "reason": "FAA 8130 exception may apply"
        }
    )

    print("\n=== INDETERMINATE Output ===")
    print(formatter.format_text_output(indeterminate_output))

    # Validate outputs
    errors = formatter.validate_output(no_go_output)
    if errors:
        print("\nValidation errors:", errors)
    else:
        print("\nValidation passed!")