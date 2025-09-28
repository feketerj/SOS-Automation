# API JSON Output Schema
## For Regex, Batch Processor, and Agent Models

All three stages (regex, batch, agent) should return JSON in this exact format. The UI/display layer will handle formatting for human consumption.

---

## REQUIRED JSON STRUCTURE

```json
{
  "decision": "GO|NO-GO|INDETERMINATE",
  "solicitation_number": "string",
  "solicitation_title": "string",
  "triage_date": "MM-DD-YYYY",
  "date_posted": "MM-DD-YYYY",
  "date_due": "MM-DD-YYYY",
  "days_open": integer,
  "remaining_days": integer,
  "platform": {
    "mds": "string",
    "commercial_designation": "string",
    "classification": "Commercial|Military|Indeterminate"
  },
  "scope": "Purchase|Manufacture|Managed Repair",
  "potential_award": {
    "exceeds_25k": boolean,
    "estimated_range": "string",
    "reasoning": "string"
  },
  "knockout": {
    "triggered": boolean,
    "category": integer | null,
    "category_name": "string | null",
    "evidence": "string | null"
  },
  "rationale": "string",
  "pipeline_notes": {
    "part_numbers": ["array of strings"] | null,
    "quantities": [array of integers] | null,
    "condition": "new|surplus|overhaul|refurb|NA",
    "mds": "string",
    "solicitation_id": "string",
    "description": "string"
  },
  "contact_co": {
    "required": boolean,
    "questions": ["array of questions"],
    "reason": "string"
  },
  "pipeline_metadata": {
    "stage": "REGEX|BATCH|AGENT",
    "assessment_type": "REGEX_KNOCKOUT|MISTRAL_BATCH_ASSESSMENT|MISTRAL_ASSESSMENT",
    "processing_time_ms": integer,
    "model_used": "string | null"
  }
}
```

---

## FIELD SPECIFICATIONS

### Core Fields (REQUIRED)
- `decision`: Must be exactly "GO", "NO-GO", or "INDETERMINATE"
- `solicitation_number`: The exact solicitation/announcement number
- `solicitation_title`: The exact title from the opportunity
- `rationale`: Brief explanation (1-3 sentences)

### Date Fields (REQUIRED when available)
- All dates in "MM-DD-YYYY" format
- `days_open`: Integer calculation between posted and due
- `remaining_days`: Integer calculation from today to due date

### Platform Fields
- `mds`: Mission Design Series (e.g., "P-8 Poseidon", "F-16", "Boeing 737")
- `commercial_designation`: Commercial equivalent if applicable (e.g., "B737-800ERX")
- `classification`: One of "Commercial", "Military", or "Indeterminate"

### Knockout Fields (Required for NO-GO)
- `triggered`: true for NO-GO, false otherwise
- `category`: Number 1-19 (see category mapping)
- `category_name`: Human-readable name
- `evidence`: Specific text that triggered the knockout

### Contact CO Fields (Required for INDETERMINATE)
- `required`: true for INDETERMINATE cases needing CO contact
- `questions`: Array of specific questions for the CO
- `reason`: Why CO contact is needed

---

## CATEGORY NUMBER MAPPING

```json
{
  "1": "TIMING",
  "2": "DOMAIN",
  "3": "SECURITY",
  "4": "SET-ASIDES",
  "5": "SOURCE_RESTRICTIONS",
  "6": "TECHNICAL_DATA",
  "7": "EXPORT_CONTROL",
  "8": "AMC_AMSC",
  "9": "SAR",
  "10": "PLATFORM",
  "11": "PROCUREMENT",
  "12": "COMPETITION",
  "13": "SUBCONTRACTING",
  "14": "VEHICLES",
  "15": "EXPERIMENTAL",
  "16": "IT_ACCESS",
  "17": "CERTIFICATIONS",
  "18": "WARRANTY_DEPOT",
  "19": "CAD_CAM"
}
```

---

## EXAMPLES BY STAGE

### REGEX Stage Output
```json
{
  "decision": "NO-GO",
  "solicitation_number": "FA8501-24-R-0001",
  "solicitation_title": "F-16 Engine Components",
  "triage_date": "09-27-2025",
  "date_posted": "09-15-2025",
  "date_due": "10-15-2025",
  "days_open": 30,
  "remaining_days": 18,
  "platform": {
    "mds": "F-16 Fighting Falcon",
    "commercial_designation": null,
    "classification": "Military"
  },
  "scope": "Purchase",
  "potential_award": {
    "exceeds_25k": true,
    "estimated_range": "Unknown",
    "reasoning": "Unable to determine from text"
  },
  "knockout": {
    "triggered": true,
    "category": 10,
    "category_name": "PLATFORM",
    "evidence": "F-16 military fighter without AMSC override"
  },
  "rationale": "Pure military platform F-16 without AMSC Z/G/A code",
  "pipeline_notes": {
    "part_numbers": null,
    "quantities": null,
    "condition": "NA",
    "mds": "F-16",
    "solicitation_id": "FA8501-24-R-0001",
    "description": "Cannot bid - military platform"
  },
  "contact_co": {
    "required": false,
    "questions": [],
    "reason": ""
  },
  "pipeline_metadata": {
    "stage": "REGEX",
    "assessment_type": "REGEX_KNOCKOUT",
    "processing_time_ms": 45,
    "model_used": null
  }
}
```

### BATCH Processor Output
```json
{
  "decision": "GO",
  "solicitation_number": "SPE4A1-24-R-0123",
  "solicitation_title": "Boeing 737 APU Components",
  "triage_date": "09-27-2025",
  "date_posted": "09-20-2025",
  "date_due": "10-20-2025",
  "days_open": 30,
  "remaining_days": 23,
  "platform": {
    "mds": "Boeing 737",
    "commercial_designation": "B737-800",
    "classification": "Commercial"
  },
  "scope": "Purchase",
  "potential_award": {
    "exceeds_25k": true,
    "estimated_range": "$100K-$500K",
    "reasoning": "APU components typically high value"
  },
  "knockout": {
    "triggered": false,
    "category": null,
    "category_name": null,
    "evidence": null
  },
  "rationale": "Commercial aircraft parts, no restrictive requirements found",
  "pipeline_notes": {
    "part_numbers": ["3307541-3", "3307542-1"],
    "quantities": [2, 4],
    "condition": "overhaul",
    "mds": "Boeing 737",
    "solicitation_id": "SPE4A1-24-R-0123",
    "description": "APU control units for overhaul"
  },
  "contact_co": {
    "required": false,
    "questions": [],
    "reason": ""
  },
  "pipeline_metadata": {
    "stage": "BATCH",
    "assessment_type": "MISTRAL_BATCH_ASSESSMENT",
    "processing_time_ms": 1250,
    "model_used": "ft:pixtral-12b-latest:d42144c7:20250912:f7d61150"
  }
}
```

### AGENT Output (INDETERMINATE)
```json
{
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
    "exceeds_25k": true,
    "estimated_range": "$250K-$750K",
    "reasoning": "Hydraulic components for naval aircraft typically high value"
  },
  "knockout": {
    "triggered": false,
    "category": 5,
    "category_name": "SOURCE_RESTRICTIONS",
    "evidence": "QPL requirement but FAA 8130 exception may apply"
  },
  "rationale": "Navy commercial platform with approved sources requirement but FAA 8130-3 mentioned. Need CO clarification.",
  "pipeline_notes": {
    "part_numbers": ["65B84321-1"],
    "quantities": [12],
    "condition": "new",
    "mds": "P-8 Poseidon",
    "solicitation_id": "N00019-24-R-0789",
    "description": "Hydraulic actuators pending CO clarification"
  },
  "contact_co": {
    "required": true,
    "questions": [
      "Would FAA Part 145 certified repair stations be considered acceptable approved sources?",
      "Can commercial Boeing 737 equivalent parts with FAA 8130-3 certification satisfy the P-8 requirement?",
      "Is it possible to discuss alternative compliance paths with the requirements owner?"
    ],
    "reason": "FAA 8130 exception may apply to Navy commercial platform"
  },
  "pipeline_metadata": {
    "stage": "AGENT",
    "assessment_type": "MISTRAL_ASSESSMENT",
    "processing_time_ms": 3500,
    "model_used": "ag:d42144c7:20250911:untitled-agent:15489fc1"
  }
}
```

---

## INSTRUCTIONS FOR MODELS

### For Batch Processor and Agent
Add this to your system prompt:

```
Return your assessment as a valid JSON object following this exact structure:
{
  "decision": "GO|NO-GO|INDETERMINATE",
  "solicitation_number": "...",
  "solicitation_title": "...",
  [... rest of schema]
}

Ensure all fields are present. Use null for missing optional fields.
Do not include any text outside the JSON structure.
```

### For UI Layer
The UI code will:
1. Parse the JSON response
2. Format it for human display using the template from AGENT_OUTPUT_INSTRUCTIONS.md
3. Generate the formatted text blocks, pipeline notes, and CO questions as needed

This separation ensures:
- Clean API responses that can be programmatically processed
- Consistent data structure across all stages
- UI flexibility to format display as needed
- Easy integration with databases and reporting tools