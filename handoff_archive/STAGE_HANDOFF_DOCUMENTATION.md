# Stage Handoff Documentation - 20-Stage Pipeline

## Overview
The 20-stage pipeline implements a cascade architecture where each stage receives accumulated context from all previous stages. Early termination occurs when any stage returns a high-confidence NO-GO decision.

## Data Flow Architecture

### Initial Input
Each opportunity starts with:
```json
{
  "solicitation_id": "string",
  "solicitation_title": "string",
  "agency": "string",
  "notice_type": "string",
  "naics_code": "string",
  "set_aside": "string",
  "solicitation_url": "string",
  "documents": [
    {
      "text": "document content (up to 2M chars total)",
      "metadata": {...}
    }
  ],
  "metadata": {
    "source": "HigherGov",
    "fetch_timestamp": "ISO-8601",
    "document_count": "number"
  }
}
```

### Context Accumulation Structure
The context passed between stages builds incrementally:
```json
{
  "current_stage": 1-20,
  "accumulated_findings": {
    "stage_1": {
      "decision": "GO|NO-GO",
      "confidence": 0.99,
      "evidence": ["quoted text"],
      "rationale": "explanation"
    },
    "stage_2": {...},
    // ... continues for each processed stage
  },
  "summary": "Natural language summary of findings so far",
  "documents": "Full document text (preserved throughout)",
  "metadata": "Original metadata (preserved throughout)"
}
```

## Stage-by-Stage Handoff

### Stage 1: TIMING → Stage 2
**Receives:** Original opportunity + documents
**Adds to context:**
- `deadline_found`: Specific date/time or null
- `evidence`: Quoted deadline text
- `rationale`: Why deadline passed/not passed

**Handoff format:**
```json
{
  "context": {
    "summary": "Deadline is [date], which is [past/future]. [Additional notes about missing deadline].",
    "stage_1_findings": {
      "deadline_found": "2025-10-15",
      "decision": "GO",
      "confidence": 0.99
    }
  }
}
```

### Stage 2: SET-ASIDES → Stage 3
**Receives:** Context from Stage 1 + original data
**Adds to context:**
- `set_aside_type`: Specific set-aside found or null
- `evidence`: Quoted set-aside text
- `rationale`: Why this is/isn't applicable

**Handoff format:**
```json
{
  "context": {
    "summary": "Previous findings: [Stage 1 summary]. No small business set-asides found.",
    "stage_2_findings": {
      "set_aside_type": null,
      "decision": "GO",
      "confidence": 0.99
    }
  }
}
```

### Stage 3: SECURITY → Stage 4
**Receives:** Context from Stages 1-2 + original data
**Adds to context:**
- `clearance_level`: Required clearance or null
- `evidence`: Security requirement quotes
- `rationale`: Security assessment

**Handoff format:**
```json
{
  "context": {
    "summary": "Previous findings: [Stages 1-2 summary]. No security clearance requirements identified.",
    "stage_3_findings": {
      "clearance_level": null,
      "decision": "GO",
      "confidence": 0.99
    }
  }
}
```

### Stages 4-7: Binary Filters
Each stage adds its specific finding to the accumulated context:
- **Stage 4 (NON-STANDARD):** `acquisition_type`
- **Stage 5 (CONTRACT-VEHICLE):** `vehicle`
- **Stage 6 (EXPORT-CONTROL):** `export_control`
- **Stage 7 (AMC-AMSC):** `amc_code`

### Stages 8-14: Technical Assessments
These stages can return INDETERMINATE and add more nuanced findings:
- **Stage 8 (SOURCE-RESTRICTIONS):** `restriction_type`, allows INDETERMINATE
- **Stage 9 (SAR):** `sar_required` boolean, qualification timeline considerations
- **Stage 10 (PLATFORM):** `platform`, `platform_type` (military/commercial/dual)
- **Stage 11 (DOMAIN):** `domain`, `capability_match`
- **Stage 12 (TECHNICAL-DATA):** `data_rights` type
- **Stage 13 (IT-SYSTEMS):** `systems_required` list
- **Stage 14 (CERTIFICATIONS):** `certifications` list, `have_certs` boolean

### Stages 15-20: Business Assessments
These stages receive the full accumulated context and make business judgments:
- **Stage 15 (SUBCONTRACTING):** `subcontracting_allowed`, `self_performance_pct`
- **Stage 16 (PROCUREMENT):** `procurement_restrictions`, `compliance_possible`
- **Stage 17 (COMPETITION):** `competition_type`, `incumbent`, `competitive_position`
- **Stage 18 (MAINTENANCE):** `warranty_period`, `maintenance_type`, `geographic_scope`
- **Stage 19 (CAD-CAM):** `cad_requirements`, `formats_required`, `capability_match`
- **Stage 20 (SCOPE):** `win_probability`, `strategic_fit`, `key_risks`

## Early Termination Logic

### Binary Stages (1-7)
- **NO-GO with 99% confidence:** Pipeline terminates immediately
- **GO with 99% confidence:** Continues to next stage
- No INDETERMINATE option for binary stages

### Technical Stages (8-14)
- **NO-GO with >95% confidence:** Pipeline terminates
- **GO with >95% confidence:** Continues to next stage
- **INDETERMINATE or <95% confidence:** Continues to next stage with note

### Business Stages (15-20)
- **NO-GO with >85% confidence:** Pipeline terminates
- **GO with >85% confidence:** Continues to next stage
- **INDETERMINATE or <85% confidence:** Continues to next stage with analysis

## Context Summary Building

The summary field builds progressively:
1. **After Stage 1:** "Deadline check passed. Due date is [date]."
2. **After Stage 2:** "Deadline check passed. No set-asides found."
3. **After Stage 3:** "Deadline check passed. No set-asides found. No security clearance required."
4. **And so on...**

By Stage 20, the summary provides a complete narrative of the assessment.

## Special Handling

### Document Preservation
- Full document text (up to 2M chars) is preserved throughout all stages
- Each stage sees the complete documents, not summaries
- Documents are passed in the prompt but not duplicated in findings

### Metadata Tracking
- Original metadata preserved throughout
- Each stage adds its processing timestamp
- Decision confidence tracked at each stage
- Evidence quotes maintained for audit trail

### NO-GO Quality Control
When any stage returns NO-GO:
1. Pipeline terminates at that stage
2. Special QC agent is invoked with:
   - The NO-GO decision and rationale
   - Full document text
   - Accumulated context from all stages
3. QC agent verifies the NO-GO is justified
4. If QC disagrees, marks for human review

## Output Format
Final output includes:
```json
{
  "solicitation_id": "original_id",
  "result": "GO|NO-GO|INDETERMINATE",
  "pipeline_stage_completed": 1-20,
  "knock_out_reasons": ["list of NO-GO reasons"],
  "accumulated_findings": {
    // All stage findings preserved
  },
  "summary": "Complete assessment narrative",
  "rationale": "Final reasoning",
  "recommendation": "Actionable next steps"
}
```

## Implementation Notes

### Prompt Construction
Each stage prompt includes:
1. **Current stage instructions:** Specific to that stage's criteria
2. **Previous findings:** `{context.summary}` placeholder
3. **Full opportunity text:** `{opportunity_text}` placeholder
4. **Output format:** JSON structure expected

### Context Size Management
- Summary kept concise (under 500 chars per stage)
- Only essential findings in accumulated_findings
- Full documents passed separately, not in context
- Evidence quotes limited to relevant excerpts

### Model Selection
- **Stages 1-7:** batch_pixtral (fine-tuned for binary decisions)
- **Stages 8-14:** batch_medium (fine-tuned for technical analysis)
- **Stages 15-20:** agent (production agent for business judgment)

## Error Handling

### Missing Documents
- If no documents found, pipeline continues with metadata only
- Each stage notes "No documents available" in evidence
- Decisions based on title/description only marked lower confidence

### API Failures
- Retry logic with exponential backoff
- If stage fails after retries, mark INDETERMINATE
- Continue to next stage with failure noted

### Parsing Errors
- If JSON parsing fails, extract decision via regex
- Log parsing errors for debugging
- Continue pipeline with partial data if possible

## Testing and Validation

### Mock Mode
- Returns predetermined responses for each stage
- Allows full pipeline testing without API calls
- Validates context accumulation logic

### Debug Output
- Each stage logs its input context
- Each stage logs its output findings
- Full trace available for debugging

### Validation Points
1. Context properly accumulates
2. Early termination works correctly
3. Documents preserved throughout
4. Output schema matches requirements
5. All 20 stages reachable in GO path