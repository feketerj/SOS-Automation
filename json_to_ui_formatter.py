#!/usr/bin/env python3
"""
JSON to UI Formatter - Converts API JSON responses to human-readable format.
"""

import json
from typing import Dict, Any, Optional

class JSONToUIFormatter:
    """Formats JSON API responses for UI display."""

    def __init__(self):
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

    def format_for_display(self, json_data: Dict[str, Any]) -> str:
        """Convert JSON to formatted text display."""

        # Header
        header = f"{json_data['decision']}-{json_data['solicitation_number']}"
        output = f"{header}\n{'=' * len(header)}\n\n"

        # Basic Info
        output += f"Solicitation Title: {json_data['solicitation_title']}\n"
        output += f"Solicitation Number: {json_data['solicitation_number']}\n"

        # Platform Info
        platform = json_data.get('platform', {})
        output += "Mission Design Series, Platform & Commercial Designation:\n"
        output += f"{platform.get('mds', 'NA')} | "
        output += f"{platform.get('commercial_designation', 'NA')} | "
        output += f"{platform.get('classification', 'Indeterminate')}\n\n"

        # Dates
        output += f"Triage Date: {json_data.get('triage_date', 'Unknown')}\n"
        output += f"Date Posted: {json_data.get('date_posted', 'Unknown')}\n"
        output += f"Date Responses Due: {json_data.get('date_due', 'Unknown')}\n"
        output += f"Days Open: {json_data.get('days_open', 0)}\n"
        output += f"Remaining Days: {json_data.get('remaining_days', 0)}\n\n"

        # Potential Award
        award = json_data.get('potential_award', {})
        output += "Potential Award:\n"
        exceeds = "Yes" if award.get('exceeds_25k', False) else "No"
        output += f"Exceeds $25K: {exceeds}, {award.get('reasoning', 'No reasoning provided')}\n"
        output += f"Range: {award.get('estimated_range', 'Unknown')}\n\n"

        # Scope
        output += f"Scope: {json_data.get('scope', 'Purchase')}\n\n"

        # Final Recommendation
        output += f"Final Recommendation: {json_data['decision']}\n"
        output += f"{json_data.get('rationale', 'No rationale provided')}\n"

        # Knockout Logic (if NO-GO)
        knockout = json_data.get('knockout', {})
        if knockout.get('triggered', False) and knockout.get('category'):
            output += "\nKnockout Logic:\n"
            cat_num = knockout['category']
            cat_name = knockout.get('category_name', self.category_names.get(cat_num, 'UNKNOWN'))
            output += f"Category {cat_num}: {cat_name}\n"
            output += f"{knockout.get('evidence', 'No specific evidence provided')}\n"

        # Pipeline Notes
        output += "\nSOS Pipeline Notes:\n"
        output += self._format_pipeline_notes(json_data.get('pipeline_notes', {}))
        output += "\n"

        # Contact CO (if required)
        contact = json_data.get('contact_co', {})
        if contact.get('required', False) and contact.get('questions'):
            output += "\nQuestions for CO:\n"
            for i, question in enumerate(contact['questions'], 1):
                output += f"{i}. {question}\n"
            if contact.get('reason'):
                output += f"\nReason: {contact['reason']}\n"

        return output

    def _format_pipeline_notes(self, notes: Dict[str, Any]) -> str:
        """Format pipeline notes according to specification."""
        if not notes:
            return "PN: NA | Qty: NA | Condition: NA | MDS: NA | NA | No specific data"

        # Extract fields
        part_numbers = notes.get('part_numbers', ['NA'])
        quantities = notes.get('quantities', ['NA'])
        condition = notes.get('condition', 'NA')
        mds = notes.get('mds', 'NA')
        solicitation_id = notes.get('solicitation_id', 'NA')
        description = notes.get('description', 'No description')

        # Format part numbers and quantities
        if part_numbers and part_numbers != ['NA']:
            pn_str = ", ".join(str(p) for p in part_numbers)
        else:
            pn_str = "NA"

        if quantities and quantities != ['NA']:
            qty_str = ", ".join(str(q) for q in quantities)
        else:
            qty_str = "NA"

        return f"PN: {pn_str} | Qty: {qty_str} | Condition: {condition} | MDS: {mds} | {solicitation_id} | {description}"

    def format_email_subject(self, json_data: Dict[str, Any]) -> str:
        """Generate email subject line from JSON data."""
        platform = json_data.get('platform', {})
        mds = platform.get('mds', '')
        scope = json_data.get('scope', 'Parts')

        if mds and mds != "NA":
            return f"Source One Spares: {scope} Available for {mds}"
        else:
            return f"Source One Spares: {scope} Available for Future Consideration"

    def format_summary_line(self, json_data: Dict[str, Any]) -> str:
        """Generate single-line summary for logs/reports."""
        decision = json_data.get('decision', 'UNKNOWN')
        sol_num = json_data.get('solicitation_number', 'UNKNOWN')

        if decision == "NO-GO":
            knockout = json_data.get('knockout', {})
            cat = knockout.get('category', 'UNK')
            return f"[{decision}] {sol_num} - Category {cat} knockout"
        elif decision == "INDETERMINATE":
            return f"[{decision}] {sol_num} - Requires CO contact"
        else:
            return f"[{decision}] {sol_num} - Eligible for competition"

    def validate_json_response(self, json_data: Dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate JSON response against schema requirements."""
        errors = []

        # Required fields
        required_fields = ['decision', 'solicitation_number', 'solicitation_title', 'rationale']
        for field in required_fields:
            if field not in json_data:
                errors.append(f"Missing required field: {field}")

        # Decision validation
        valid_decisions = ['GO', 'NO-GO', 'INDETERMINATE']
        if json_data.get('decision') not in valid_decisions:
            errors.append(f"Invalid decision: {json_data.get('decision')}")

        # NO-GO must have knockout info
        if json_data.get('decision') == 'NO-GO':
            knockout = json_data.get('knockout', {})
            if not knockout.get('triggered'):
                errors.append("NO-GO decision but knockout.triggered is not true")
            if not knockout.get('category'):
                errors.append("NO-GO decision but no knockout category specified")

        # INDETERMINATE should have CO contact info
        if json_data.get('decision') == 'INDETERMINATE':
            contact = json_data.get('contact_co', {})
            if not contact.get('required'):
                errors.append("INDETERMINATE but contact_co.required is not true")

        return (len(errors) == 0), errors


# Example usage
if __name__ == "__main__":
    formatter = JSONToUIFormatter()

    # Example JSON from API
    api_response = {
        "decision": "INDETERMINATE",
        "solicitation_number": "N00019-24-R-0789",
        "solicitation_title": "P-8A Poseidon Hydraulic Components",
        "triage_date": "09-27-2025",
        "date_posted": "09-22-2025",
        "date_due": "10-22-2025",
        "days_open": 30,
        "remaining_days": 25,
        "platform": {
            "mds": "P-8A Poseidon",
            "commercial_designation": "Boeing 737-800ERX",
            "classification": "Commercial"
        },
        "scope": "Purchase",
        "potential_award": {
            "exceeds_25k": True,
            "estimated_range": "$250K-$750K",
            "reasoning": "Hydraulic components for naval aircraft"
        },
        "knockout": {
            "triggered": False,
            "category": 5,
            "category_name": "SOURCE_RESTRICTIONS",
            "evidence": "QPL requirement but FAA 8130 exception may apply"
        },
        "rationale": "Navy commercial platform with approved sources but FAA 8130 mentioned.",
        "pipeline_notes": {
            "part_numbers": ["65B84321-1"],
            "quantities": [12],
            "condition": "new",
            "mds": "P-8 Poseidon",
            "solicitation_id": "N00019-24-R-0789",
            "description": "Hydraulic actuators pending CO clarification"
        },
        "contact_co": {
            "required": True,
            "questions": [
                "Would FAA Part 145 certified repair stations be acceptable?",
                "Can commercial Boeing 737 parts with 8130-3 satisfy requirements?"
            ],
            "reason": "FAA 8130 exception may apply"
        },
        "pipeline_metadata": {
            "stage": "AGENT",
            "assessment_type": "MISTRAL_ASSESSMENT",
            "processing_time_ms": 3500,
            "model_used": "ag:d42144c7:20250911:untitled-agent:15489fc1"
        }
    }

    # Validate JSON
    valid, errors = formatter.validate_json_response(api_response)
    if not valid:
        print("Validation Errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("JSON validation passed!")

    # Format for display
    print("\n" + "="*60)
    print("FORMATTED OUTPUT:")
    print("="*60)
    print(formatter.format_for_display(api_response))

    # Generate summary line
    print("\nSUMMARY LINE:")
    print(formatter.format_summary_line(api_response))

    # Generate email subject
    print("\nEMAIL SUBJECT:")
    print(formatter.format_email_subject(api_response))