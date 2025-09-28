# EXACT Output Schema - Triple Checked

## This is the EXACT schema all AI models should return

```json
{
  "AssessmentHeaderLine": "[Go/No-Go]-[Solicitation number]",
  "SolicitationTitle": "[Exact solicitation title]",
  "SolicitationNumber": "[Exact solicitation or announcement number]",
  "MDSPlatformCommercialDesignation": "[MDS/platform type, NA/Indeterminate, e.g., P-8 Poseidon | B737 | Commercial Item: Elevator (or) KC-46/B767 | Noncommercial: Refueling Boom (or) Indeterminate MDS | Commercial Item: AMSC Z Aircraft Tire]",
  "TriageDate": "MM-DD-YYYY",
  "DatePosted": "MM-DD-YYYY",
  "DateResponsesSubmissionsDue": "MM-DD-YYYY",
  "DaysOpen": 30,
  "RemainingDays": 15,
  "PotentialAward": {
    "Exceeds25K": "Yes/No, reason",
    "Range": "[Inferred range with logic, 1-3 sources, disclaimer]"
  },
  "FinalRecommendation": "[Go/No-Go, concise explanation based on Knockout criteria, context, exact government quote(s), page number(s), metadata, etc.]",
  "Scope": "[Type of work to be performed: Purchase, Manufacture, Managed Repair, with inference and concise proof]",
  "KnockoutLogic": "[Full rationale for each knockout item #1-19, including applicable page numbers, titles, headers, notes, inference, etc.]",
  "SOSPipelineNotes": "PN: [part numbers or NA] | Qty: [quantity per PN or NA] | Condition: [new/surplus/overhaul/etc.] | MDS: [aircraft type or NA] | [solicitation ID] | [brief description of work]",
  "QuestionsForCO": ["List relevant question(s)"]
}
```

## Stage-Specific Outputs

### Regex Stage (Limited - Many Nulls)
```json
{
  "AssessmentHeaderLine": "No-Go-FA8501-24-R-0123",
  "SolicitationTitle": "From input",
  "SolicitationNumber": "From input",
  "MDSPlatformCommercialDesignation": null,
  "TriageDate": "09-27-2025",
  "DatePosted": null,
  "DateResponsesSubmissionsDue": null,
  "DaysOpen": null,
  "RemainingDays": null,
  "PotentialAward": {
    "Exceeds25K": null,
    "Range": null
  },
  "FinalRecommendation": "No-Go - 8(a) set-aside detected",
  "Scope": null,
  "KnockoutLogic": "Category 4: Wrong set-aside type (8a)",
  "SOSPipelineNotes": "PN: NA | Qty: NA | Condition: NA | MDS: NA | FA8501-24-R-0123 | Regex knockout",
  "QuestionsForCO": []
}
```

### Batch Stage (Partial - Some Nulls)
```json
{
  "AssessmentHeaderLine": "Indeterminate-N00019-24-R-0789",
  "SolicitationTitle": "P-8A Poseidon Hydraulic Components",
  "SolicitationNumber": "N00019-24-R-0789",
  "MDSPlatformCommercialDesignation": "P-8 Poseidon | B737 | Commercial",
  "TriageDate": "09-27-2025",
  "DatePosted": "09-22-2025",
  "DateResponsesSubmissionsDue": "10-22-2025",
  "DaysOpen": 30,
  "RemainingDays": 25,
  "PotentialAward": {
    "Exceeds25K": "Yes, hydraulic components typically >$100K",
    "Range": "$250K-$750K based on quantity and complexity"
  },
  "FinalRecommendation": "Indeterminate - Navy commercial platform with source restriction needs agent review",
  "Scope": "Purchase",
  "KnockoutLogic": "Partial assessment - QPL requirement but FAA 8130 may apply",
  "SOSPipelineNotes": "PN: 65B84321-1 | Qty: 12 | Condition: New | MDS: P-8 Poseidon | N00019-24-R-0789 | Purchase hydraulic actuators",
  "QuestionsForCO": []
}
```

### Agent Stage (Complete - No Nulls)
```json
{
  "AssessmentHeaderLine": "Go-N00019-24-R-0789",
  "SolicitationTitle": "P-8A Poseidon Hydraulic Components",
  "SolicitationNumber": "N00019-24-R-0789",
  "MDSPlatformCommercialDesignation": "P-8A Poseidon | Boeing 737-800ERX | Commercial Item: Maritime Patrol Aircraft",
  "TriageDate": "09-27-2025",
  "DatePosted": "09-22-2025",
  "DateResponsesSubmissionsDue": "10-22-2025",
  "DaysOpen": 30,
  "RemainingDays": 25,
  "PotentialAward": {
    "Exceeds25K": "Yes, hydraulic components for naval aircraft typically exceed $250K",
    "Range": "$250K-$750K based on 12 units of complex hydraulic actuators"
  },
  "FinalRecommendation": "Go - Navy commercial platform (P-8 based on Boeing 737) with FAA 8130-3 certification acceptable per solicitation page 4. No security clearance or restrictive set-asides. QPL requirement can be satisfied with FAA certified sources.",
  "Scope": "Purchase: New hydraulic components with FAA 8130-3 certification",
  "KnockoutLogic": "Category 1: Not expired (due 10-22). Category 2: Aviation domain confirmed. Category 3: No clearance required. Category 4: Small business set-aside (SOS qualifies). Category 5: QPL exists but FAA 8130 exception applies for Navy commercial platform. Category 6: TDP not required for purchase. Category 7: No export restrictions. Category 8: No AMSC codes found. Category 9: No military SAR - FAA cert acceptable. Category 10: Commercial platform (Boeing 737 based). Category 11: Purchase not manufacture. Category 12: Open competition. Category 13: Subcontracting allowed. Category 14: Direct contract. Category 15: Not R&D. Category 16: No IT access required. Category 17: FAA cert acceptable. Category 18: No depot requirement. Category 19: No CAD required.",
  "SOSPipelineNotes": "PN: 65B84321-1 | Qty: 12 | Condition: New | MDS: P-8 Poseidon | N00019-24-R-0789 | Purchase hydraulic actuators with FAA 8130-3",
  "QuestionsForCO": [
    "Would FAA Part 145 certified repair stations be considered acceptable approved sources?",
    "Can commercial Boeing 737 equivalent parts with FAA 8130-3 certification satisfy the P-8 requirement?",
    "Is it possible to discuss alternative compliance paths with the requirements owner?"
  ]
}
```

## Critical Notes

1. **AssessmentHeaderLine**: Must start with decision and solicitation number
2. **MDSPlatformCommercialDesignation**: Single string with pipe separators
3. **DaysOpen/RemainingDays**: Integers (not strings)
4. **PotentialAward.Exceeds25K**: String with Yes/No and reason
5. **KnockoutLogic**: Single string covering all 19 categories (agent) or relevant ones (batch/regex)
6. **SOSPipelineNotes**: Exact format with pipes
7. **QuestionsForCO**: Array of strings (empty array if none)

## What Each Stage Can Provide

### Regex
- AssessmentHeaderLine ✓
- SolicitationTitle ✓ (from input)
- SolicitationNumber ✓ (from input)
- MDSPlatformCommercialDesignation ✗ (null)
- TriageDate ✓
- DatePosted ✗ (null)
- DateResponsesSubmissionsDue ✗ (null)
- DaysOpen ✗ (null)
- RemainingDays ✗ (null)
- PotentialAward ✗ (nulls)
- FinalRecommendation ✓ (simple)
- Scope ✗ (null)
- KnockoutLogic ✓ (category only)
- SOSPipelineNotes ✓ (mostly NA values)
- QuestionsForCO ✓ (empty array)

### Batch
- Most fields partially populated
- May not have complete knockout logic for all 19 categories
- Can infer some platform and award information

### Agent
- ALL fields fully populated
- Complete knockout logic for all 19 categories
- Detailed recommendations with evidence
- Specific CO questions when applicable