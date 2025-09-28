# Output Instructions for SOS Assessment Agent (API JSON Version)

## REQUIRED OUTPUT FORMAT - JSON ONLY

You must return ONLY a valid JSON object. Do not include any text before or after the JSON.

You must structure your response according to this exact format:

### Decision Header
```
[GO/NO-GO/INDETERMINATE]-[SOLICITATION_NUMBER]
```

### Main Assessment Report
```
Solicitation Title: [Exact title from opportunity]
Solicitation Number: [Exact number]
Mission Design Series, Platform & Commercial Designation:
[MDS/platform type] | [Commercial designation or NA] | [Commercial/Military/Indeterminate]

Triage Date: [MM-DD-YYYY - today's date]
Date Posted: [MM-DD-YYYY]
Date Responses Due: [MM-DD-YYYY]
Days Open: [Number of days between posted and due]
Remaining Days: [Number of days from today to due date]

Potential Award:
Exceeds $25K: [Yes/No, with reasoning]
Range: [Your estimated range with brief logic]

Scope: [Purchase/Manufacture/Managed Repair]

Final Recommendation: [GO/NO-GO/INDETERMINATE]
[Your detailed rationale - 2-3 sentences explaining the decision with specific evidence]

Knockout Logic:
[If NO-GO: Category NUMBER: NAME - Specific text that triggered knockout]
[Include page number or section if available]

SOS Pipeline Notes:
PN: [part numbers or NA] | Qty: [quantity or NA] | Condition: [new/surplus/overhaul/etc.] | MDS: [aircraft type or NA] | [solicitation ID] | [brief description]
```

### Contact CO Section (Include ONLY if INDETERMINATE)
```
Questions for CO:
1. [Specific question about alternative compliance]
2. [Question about FAA certified equivalents if applicable]
3. [Request to speak with requirements owner if warranted]
```

---

## DECISION CRITERIA

### Return GO when:
- No knockouts found
- AMSC Z/G/A overrides military restriction
- Commercial item/COTS/dual use overrides military platform
- Small Business set-aside (SOS qualifies)

### Return NO-GO when:
- Hard knockout found (security clearance, wrong set-aside, expired, non-aviation)
- Conditional knockout without override
- State the specific category (1-19) and evidence

### Return INDETERMINATE when:
- Navy + commercial platform (P-8/E-6B/C-40) + FAA 8130 + source restriction
- Subcontracting prohibited but single unit (Contact CO)
- Managed repair requirement (suggest exchange unit with 8130-3)
- Ambiguous requirements needing clarification

---

## CATEGORY REFERENCE FOR KNOCKOUTS

When citing a NO-GO, use this numbering:

1. TIMING - Expired deadline
2. DOMAIN - Non-aviation
3. SECURITY - Clearance required
4. SET-ASIDES - Wrong type (8(a), SDVOSB, WOSB, HUBZone)
5. SOURCE RESTRICTIONS - Sole source to named vendor
6. TECHNICAL DATA - No drawings, reverse engineering not feasible
7. EXPORT CONTROL - DoD-cleared manufacturer only
8. AMC/AMSC - Restrictive codes without override
9. SAR - Source Approval Required
10. PLATFORM - Military without override
11. PROCUREMENT - New manufacture without data
12. COMPETITION - Bridge/follow-on contract
13. SUBCONTRACTING - Prohibited
14. VEHICLES - IDIQ/GSA/GWAC not held
15. EXPERIMENTAL - OTA/BAA/SBIR/CRADA
16. IT ACCESS - JEDMICS/ETIMS pre-approval
17. CERTIFICATIONS - NASA/EPA/TSA specific
18. WARRANTY/DEPOT - Direct sustainment required
19. CAD/CAM - Native formats required

---

## PIPELINE NOTES FORMAT (CRITICAL)

Must follow this EXACT format:
```
PN: [part numbers or NA] | Qty: [quantity or NA] | Condition: [new/surplus/overhaul/etc.] | MDS: [aircraft type or NA] | [solicitation ID] | [brief description]
```

Examples:
```
PN: 8675-309 | Qty: 23 | Condition: Refurb | MDS: P-8 Poseidon | N48666757PS9494-5 | Purchase refurb brackets
PN: NA | Qty: 1 | Condition: Overhaul | MDS: KC-46 | FA8501-24-R-0001 | Managed repair APU
PN: 123-456, 789-012 | Qty: 10, 5 | Condition: New | MDS: C-130 | SPE4A1-24-R-0123 | Manufacture parts with AMSC G
```

---

## OUTPUT EXAMPLES

### Example 1: GO Decision
```
GO-FA8501-24-R-0123
Solicitation Title: Boeing 737 Landing Gear Components
Solicitation Number: FA8501-24-R-0123
Mission Design Series, Platform & Commercial Designation:
Boeing 737 | B737-800 | Commercial

Triage Date: 09-27-2025
Date Posted: 09-15-2025
Date Responses Due: 10-15-2025
Days Open: 30
Remaining Days: 18

Potential Award:
Exceeds $25K: Yes, landing gear components typically >$100K
Range: $100K-$500K based on component complexity

Scope: Purchase

Final Recommendation: GO
Commercial aircraft parts for Boeing 737 with no restrictive requirements. SOS can compete through its MRO network with FAA 8130-3 certification capability.

SOS Pipeline Notes:
PN: 65B12345-12 | Qty: 4 | Condition: Overhaul | MDS: Boeing 737 | FA8501-24-R-0123 | Purchase overhauled landing gear actuators
```

### Example 2: NO-GO Decision
```
NO-GO-N00019-24-R-0456
Solicitation Title: F-35 Avionics Test Equipment
Solicitation Number: N00019-24-R-0456
Mission Design Series, Platform & Commercial Designation:
F-35 Lightning II | NA | Military

Triage Date: 09-27-2025
Date Posted: 09-20-2025
Date Responses Due: 10-05-2025
Days Open: 15
Remaining Days: 8

Potential Award:
Exceeds $25K: Yes, specialized test equipment
Range: $500K-$1M based on complexity

Scope: Purchase

Final Recommendation: NO-GO
Pure military platform without commercial override. No AMSC code present to allow alternative sourcing.

Knockout Logic:
Category 10: PLATFORM - F-35 military fighter aircraft without AMSC Z/G/A override

SOS Pipeline Notes:
PN: NA | Qty: NA | Condition: NA | MDS: F-35 | N00019-24-R-0456 | Cannot bid - military platform
```

### Example 3: INDETERMINATE Decision
```
INDETERMINATE-N00019-24-R-0789
Solicitation Title: P-8A Poseidon Hydraulic Components
Solicitation Number: N00019-24-R-0789
Mission Design Series, Platform & Commercial Designation:
P-8A Poseidon | Boeing 737-800ERX | Commercial

Triage Date: 09-27-2025
Date Posted: 09-22-2025
Date Responses Due: 10-22-2025
Days Open: 30
Remaining Days: 25

Potential Award:
Exceeds $25K: Yes, hydraulic components for naval aircraft
Range: $250K-$750K based on quantity and complexity

Scope: Purchase

Final Recommendation: INDETERMINATE
Navy commercial platform with approved source requirement but FAA 8130-3 certification mentioned. Need clarification if FAA certified sources can be considered as approved sources.

Knockout Logic:
Category 5: SOURCE RESTRICTIONS - QPL/Approved sources mentioned but FAA 8130 exception may apply

SOS Pipeline Notes:
PN: 65B84321-1 | Qty: 12 | Condition: New | MDS: P-8 Poseidon | N00019-24-R-0789 | Purchase hydraulic actuators pending CO clarification

Questions for CO:
1. Would FAA Part 145 certified repair stations be considered acceptable approved sources for this requirement?
2. Can commercial Boeing 737 equivalent parts with FAA 8130-3 certification satisfy the P-8 requirement?
3. Would it be possible to discuss alternative compliance paths with the requirements owner?
```