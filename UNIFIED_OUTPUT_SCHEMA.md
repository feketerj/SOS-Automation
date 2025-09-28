# Unified Output Schema for SOS Assessment
## Aligned with user_added_context requirements

---

## PRIMARY OUTPUT STRUCTURE

```json
{
  "decision": "GO|NO-GO|INDETERMINATE",
  "solicitation_number": "string",
  "solicitation_title": "string",
  "platform_info": {
    "mds": "string (e.g., P-8 Poseidon)",
    "commercial_designation": "string (e.g., B737)",
    "classification": "Commercial|Military|Indeterminate"
  },
  "dates": {
    "triage_date": "MM-DD-YYYY",
    "date_posted": "MM-DD-YYYY",
    "date_due": "MM-DD-YYYY",
    "days_open": "number",
    "remaining_days": "number"
  },
  "scope": "Purchase|Manufacture|Managed Repair",
  "knockout_category": "number (1-19) or null",
  "knockout_reason": "string or null",
  "rationale": "string (concise explanation)",
  "pipeline_notes": "string (formatted as required)",
  "contact_co": {
    "required": "boolean",
    "questions": ["array of questions"],
    "reason": "string"
  },
  "potential_award": {
    "exceeds_25k": "boolean",
    "estimated_range": "string",
    "reasoning": "string"
  }
}
```

---

## FORMATTED TEXT OUTPUT

### Header Format
```
[GO/NO-GO/INDETERMINATE]-[SOLICITATION_NUMBER]
```

### Main Report Format
```
Solicitation Title: [Exact title]
Solicitation Number: [Exact number]
Mission Design Series, Platform & Commercial Designation:
[MDS/platform | Commercial designation | Classification]

Triage Date: [MM-DD-YYYY]
Date Posted: [MM-DD-YYYY]
Date Responses Due: [MM-DD-YYYY]
Days Open: [Number]
Remaining Days: [Number]

Potential Award:
Exceeds $25K: [Yes/No, reason]
Range: [Estimated range with logic]

Scope: [Purchase/Manufacture/Managed Repair]

Final Recommendation: [GO/NO-GO/INDETERMINATE]
[Detailed rationale with specific evidence]

Knockout Logic:
[Category number and name if NO-GO]
[Specific text/page that triggered knockout]
```

---

## PIPELINE NOTES FORMAT (CRITICAL)

Must follow this exact format:
```
PN: [part numbers or NA] | Qty: [quantity or NA] | Condition: [new/surplus/overhaul/etc.] | MDS: [aircraft type or NA] | [solicitation ID] | [brief description]
```

Example:
```
PN: 8675-309 | Qty: 23 | Condition: Refurb | MDS: P-8 Poseidon | N48666757PS9494-5 | Purchase refurb brackets
```

---

## CONTACT CO SECTION

### When to Include
- Approved sources + FAA 8130-3 capability
- Subcontracting prohibited + single unit
- Managed repair requirement (suggest exchange unit)

### Format
```
Questions for CO:
1. [Specific question about alternative compliance]
2. [Question about FAA certified equivalents]
3. [Request to speak with requirements owner]
```

---

## DECISION TYPES

### GO
- No knockouts found
- All overrides applied successfully
- SOS can compete

### NO-GO
- Hard knockout found (Categories 1-4)
- Conditional knockout without override (Categories 5-19)
- Include specific category and evidence

### INDETERMINATE
- Contact CO situation
- Needs human review
- Ambiguous requirements
- Missing critical information

---

## CATEGORY MAPPING FOR OUTPUT

When outputting knockout reason, use this format:
```
Category [NUMBER]: [NAME] - [Specific trigger]
```

Example:
```
Category 5: SOURCE RESTRICTIONS - Sole source to Lockheed Martin Corporation
Category 3: SECURITY - Secret clearance required
Category 10: PLATFORM - F-16 military aircraft without AMSC override
```

---

## EMAIL OUTPUT (When Requested)

### Subject Line Format
```
Source One Spares: [Type of opportunity] for [MDS if applicable]
```

Examples:
```
Source One Spares: Refurbished Spares Available for P-8 Poseidon
Source One Spares: FAA MRO Capability for Commercial Platform Support
Source One Spares: Surplus Parts Available for Future Consideration
```

### Email Content Structure
1. Introduction with SOS credentials
2. Specific value proposition for this opportunity
3. Questions for CO (if applicable)
4. Request for consideration
5. Attachment note (capabilities statement)

---

## INTEGRATION NOTES

### For Batch Processor
- Use simplified JSON structure
- Focus on decision, category, rationale
- Omit detailed pipeline notes

### For Agent
- Full detailed output
- Include all sections
- Generate email if warranted

### For Regex Stage
- Minimal output: decision + category
- No need for full formatting

---

## CONSISTENCY REQUIREMENTS

All stages must output:
1. `decision` field with exact values: GO, NO-GO, INDETERMINATE
2. `knockout_category` if NO-GO (number 1-19)
3. `rationale` explaining the decision
4. `contact_co.required` boolean for special cases

This ensures pipeline tracking and reporting work correctly across all stages.