# Agent/Batch Output Schema - FINAL REQUIREMENT

## Output Format (What AI Models MUST Return)

### Header Line
```
[GO/NO-GO]-[SOLICITATION_NUMBER]
```

### Required JSON Structure
```json
{
  "decision": "GO|NO-GO",
  "solicitation_number": "exact number",
  "solicitation_title": "exact title",

  "platform": {
    "mds": "P-8 Poseidon",
    "commercial_designation": "B737",
    "classification": "Commercial|Military|Indeterminate",
    "description": "Commercial Item: Elevator"
  },

  "dates": {
    "triage_date": "MM-DD-YYYY",
    "date_posted": "MM-DD-YYYY",
    "date_due": "MM-DD-YYYY",
    "days_open": 30,
    "remaining_days": 15
  },

  "potential_award": {
    "exceeds_25k": true,
    "reasoning": "Landing gear components typically >$100K",
    "estimated_range": "$100K-$500K based on component complexity"
  },

  "scope": "Purchase|Manufacture|Managed Repair",
  "scope_description": "Purchase: Surplus pitot tubes",

  "knockout_logic": {
    "category_1_timing": "Not expired - due 10-15-2025",
    "category_2_domain": "Aviation - aircraft parts",
    "category_3_security": "No clearance required",
    "category_4_set_asides": "Small business OK",
    "category_5_source_restrictions": "No sole source",
    "category_6_technical_data": "TDP available per page 12",
    "category_7_export_control": "No restrictions",
    "category_8_amc_amsc": "No restrictive codes",
    "category_9_sar": "No SAR requirement",
    "category_10_platform": "Commercial platform",
    "category_11_procurement": "Purchase not manufacture",
    "category_12_competition": "Open competition",
    "category_13_subcontracting": "Allowed",
    "category_14_vehicles": "Direct contract",
    "category_15_experimental": "Not R&D",
    "category_16_it_access": "No special access required",
    "category_17_certifications": "FAA cert acceptable",
    "category_18_warranty_depot": "No depot requirement",
    "category_19_cad_cam": "No CAD required"
  },

  "government_quotes": [
    "FAA Form 8130-3 or equivalent certification required - page 4",
    "Small Business Set-Aside under NAICS 336413 - page 1",
    "Technical data package available in solicitation attachments - page 12"
  ],

  "pipeline_notes": {
    "part_number": "8675-309",
    "quantity": 23,
    "condition": "Refurb",
    "mds": "P-8 Poseidon",
    "solicitation_id": "N48666757PS9494-5",
    "description": "Purchase refurb brackets",
    "formatted": "PN: 8675-309 | Qty: 23 | Condition: Refurb | MDS: P-8 Poseidon | N48666757PS9494-5 | Purchase refurb brackets"
  },

  "final_recommendation": "GO - Commercial platform with FAA 8130-3 certification acceptable per solicitation page 4. No security clearance or restrictive set-asides. Technical data available.",

  "contact_co": {
    "required": false,
    "questions": [],
    "special_cases": []
  }
}
```

## Special Cases for CO Contact

### When to Include Questions:
1. **Approved sources + FAA standards** → "Would FAA Part 145 certified repair stations be considered acceptable approved sources?"
2. **Subcontracting prohibited + single unit** → "Can SOS provide this single unit directly with FAA 8130-3 certification?"
3. **Managed repair requirement** → "Would an exchange unit with FAA 8130-3 certification satisfy this requirement?"
4. **Navy + Commercial platform + Source restriction** → "Can commercial Boeing 737 equivalent parts with FAA 8130-3 certification satisfy the P-8 requirement?"

### Example CO Questions:
```json
"contact_co": {
  "required": true,
  "questions": [
    "Would the requirements owner consider refurbished spares with an FAA 8130-3?",
    "Can surplus parts with full traceability documentation be considered?",
    "Is it possible to speak directly with the requirements owner about alternative compliance paths?"
  ],
  "special_cases": ["Navy commercial platform with FAA 8130 capability"]
}
```

## Regex Stage Output (Limited Fields)

Since regex can't infer most fields, it returns:
```json
{
  "decision": "NO-GO|CONTINUE",
  "solicitation_number": "from input",
  "solicitation_title": "from input",

  "knockout_logic": {
    "triggered_category": 4,
    "category_name": "SET-ASIDES",
    "pattern_matched": "8(a) set-aside",
    "evidence": "8(a) minority-owned business set-aside"
  },

  "final_recommendation": "NO-GO - Wrong set-aside type (8a)",

  "platform": {
    "mds": null,
    "commercial_designation": null,
    "classification": "Indeterminate"
  },

  "dates": {
    "triage_date": "MM-DD-YYYY",
    "date_posted": null,
    "date_due": null,
    "days_open": null,
    "remaining_days": null
  },

  "scope": "Indeterminate",
  "potential_award": {
    "exceeds_25k": null,
    "reasoning": "Cannot determine from regex",
    "estimated_range": null
  },

  "pipeline_notes": {
    "formatted": "PN: NA | Qty: NA | Condition: NA | MDS: NA | [ID] | Regex knockout"
  }
}
```

## Critical Requirements

1. **Decision**: Must be GO or NO-GO (Agent can't return INDETERMINATE)
2. **Dates**: All dates in MM-DD-YYYY format
3. **Days**: Integer values for days_open and remaining_days
4. **Pipeline Notes**: MUST follow exact format with pipes
5. **Knockout Logic**: Must check all 19 categories
6. **Government Quotes**: Include page numbers when available
7. **Final Recommendation**: Repeat at end with full justification

## What UI Must Display

### Summary View:
- Decision with icon (✅ GO, ❌ NO-GO)
- Title and solicitation number
- Platform info (MDS | Commercial Designation | Classification)
- Days remaining
- Pipeline notes formatted string

### Detailed View:
- All 19 knockout categories with findings
- Government quotes with page references
- CO questions if applicable
- Full final recommendation
- Award estimate with reasoning

### Pipeline Journey:
- Stage decisions with reasons
- What each stage found/decided
- Progression through pipeline