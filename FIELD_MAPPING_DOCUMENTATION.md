# Field Mapping Documentation

## Overview
This document describes all field mappings and transformations applied in the SOS Assessment Pipeline.

Last Updated: September 13, 2025

## Assessment Type Mappings

### Canonical Assessment Types
1. **APP_KNOCKOUT** - Regex/App-based filtering
2. **MISTRAL_BATCH_ASSESSMENT** - Batch API processing
3. **MISTRAL_ASSESSMENT** - Agent verification

### Legacy Type Translations
| Legacy Type | Canonical Type | Source |
|------------|---------------|---------|
| AGENT_VERIFIED | MISTRAL_ASSESSMENT | FULL_BATCH_PROCESSOR.py |
| REGEX_KNOCKOUT | APP_KNOCKOUT | Legacy pipeline |
| REGEX_ONLY | APP_KNOCKOUT | sos_ingestion_gate.py |
| APP_ONLY | APP_KNOCKOUT | Early versions |
| AGENT_AI | MISTRAL_ASSESSMENT | Alternative naming |
| BATCH_AI | MISTRAL_BATCH_ASSESSMENT | Batch processor |

## Decision Field Mappings

### Decision Value Normalization
The pipeline accepts various decision field names and normalizes to 'result':

| Input Field | Output Field | Valid Values |
|------------|--------------|--------------|
| decision | result | GO, NO-GO, INDETERMINATE |
| final_decision | result | GO, NO-GO, INDETERMINATE |
| recommendation | result | GO, NO-GO, INDETERMINATE |
| assessment.decision | result | GO, NO-GO, INDETERMINATE |

### Decision Value Variants
| Input Value | Normalized Value |
|------------|-----------------|
| GO | GO |
| go | GO |
| NO-GO | NO-GO |
| NO_GO | NO-GO |
| NOGO | NO-GO |
| no-go | NO-GO |
| no go | NO-GO |
| INDETERMINATE | INDETERMINATE |
| indeterminate | INDETERMINATE |
| (empty/null) | INDETERMINATE |

## URL Field Mappings

### URL Field Sources (Priority Order)
| Field Name | Maps To | Priority | Description |
|-----------|---------|----------|-------------|
| sam_url | sam_url | 1 | Direct field (if already present) |
| sam_gov_url | sam_url | 2 | Alternative naming |
| source_path | sam_url | 3 | Government source URL (SAM.gov/DIBBS) |
| hg_url | hg_url | 1 | Direct field (if already present) |
| highergov_url | hg_url | 2 | Alternative naming |
| path | hg_url | 3 | HigherGov platform URL |
| url | hg_url | 4 | Legacy field fallback |

## Rationale Field Mappings

### Reasoning Text Sources (Priority Order)
1. `rationale` - Direct field
2. `reasoning` - Common alternative
3. `assessment.reasoning` - Nested legacy format
4. `primary_blocker` - Fallback field

## Metadata Field Mappings

### Opportunity Identification
| Input Fields | Output Field | Priority |
|-------------|--------------|----------|
| solicitation_id | solicitation_id | 1 |
| source_id | solicitation_id | 2 |
| announcement_number | solicitation_id | 3 |

### Title Fields
| Input Fields | Output Field | Priority |
|-------------|--------------|----------|
| solicitation_title | solicitation_title | 1 |
| title | solicitation_title | 2 |
| announcement_title | solicitation_title | 3 |

### Summary/Description
| Input Fields | Output Field | Priority |
|-------------|--------------|----------|
| summary | summary | 1 |
| ai_summary | summary | 2 |
| description_text | summary | 3 |

## Processing Method Mappings

### Processing Method to Pipeline Stage
| Processing Method | Pipeline Stage | Assessment Type |
|------------------|---------------|-----------------|
| APP_ONLY | APP | APP_KNOCKOUT |
| REGEX_ONLY | APP | APP_KNOCKOUT |
| BATCH_AI | BATCH | MISTRAL_BATCH_ASSESSMENT |
| AGENT_AI | AGENT | MISTRAL_ASSESSMENT |
| AGENT_VERIFIED | AGENT | MISTRAL_ASSESSMENT |

## Preserved Fields

The following fields are preserved without transformation:
- agency
- due_date
- posted_date
- naics
- psc
- set_aside
- value_low
- value_high
- place_of_performance
- doc_length

## Special Handling

### Nested Assessment Structure
Legacy format with nested assessment dictionary:
```json
{
  "assessment": {
    "decision": "GO",
    "reasoning": "Explanation"
  }
}
```
Is transformed to:
```json
{
  "result": "GO",
  "rationale": "Explanation"
}
```

### Knock-out Reasons
- Single `knock_pattern` string converted to array
- Empty patterns result in empty array
- Multiple reasons preserved as-is

## Monitoring and Debugging

### Enable Translation Logging
To monitor field translations in real-time:
```python
DecisionSanitizer._log_translation = True
```

### Validation Points
1. Schema compliance check in quality_control_validator.py
2. Backward compatibility tests in test_backward_compat.py
3. Assessment type normalization tests in test_assessment_type_fix.py
4. URL preservation tests in test_url_preservation.py

## Rollback Procedures

### To Disable Assessment Type Normalization
Comment out the normalization call in decision_sanitizer.py:
```python
# Line 154: assessment_type = DecisionSanitizer._normalize_assessment_type(assessment_type)
```

### To Disable URL Field Addition
Remove sam_url and hg_url from line 230-231 in highergov_batch_fetcher.py

### To Revert All Changes
1. Restore decision_sanitizer.py from backup
2. Restore enhanced_output_manager.py from backup
3. Restore highergov_batch_fetcher.py from backup

## Field Consolidation (Bug #5 Fix)

### Decision Field Strategy
As of Session 27 Part 2:
- **Primary Field**: `result` - Used in CSV output and unified schema
- **Internal Field**: `final_decision` - Kept for backward compatibility and internal counting
- **Migration Path**: Phase 1 (current) - Both fields exist, Phase 2 (future) - Remove `final_decision`

### Output Formats
| Format | Fields Present | Notes |
|--------|---------------|-------|
| CSV | `result` only | No duplication, follows unified schema |
| JSON | Both `result` and `final_decision` | Backward compatibility |
| Internal Processing | Both fields | `final_decision` used for counting/filtering |

## Version History

### Session 27 Part 2 (Sept 13, 2025)
- Fixed field duplication (Bug #5)
- Consolidated to use `result` as primary field
- Maintained backward compatibility with `final_decision`
- Updated CSV headers to eliminate duplication

### Session 27 Part 1 (Sept 13, 2025)
- Added sam_url and hg_url field preservation
- Implemented assessment type normalization
- Fixed nested assessment.reasoning extraction
- Added monitoring capability

### Previous Sessions
- See CLAUDE.md for full history