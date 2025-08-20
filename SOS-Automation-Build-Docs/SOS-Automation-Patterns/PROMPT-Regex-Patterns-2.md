**OBJECTIVE:**
Build a comprehensive pattern-based data set that will inform a Python script ingesting thousands of government opportunities via the HigherGov (commercial platorm) API. The API endpoints allow for ingestion (GET) of the announcement ID and documents.

**CONTEXT:**
Building a production-grade regex/pattern matching system to process 10,000+ federal contract opportunities monthly. System must identify and classify opportunities based on Source Onse Spares (SOS) GO/NO-GO criteria and related restrictions. Nuance matters in opportunities assessment, so patterns must be rock-solid. 

**COMPLETED PATTERNS:**
* Source Approval Required (SAR)
* Sole Source
* TDPs
* Refurb, et. al.
* OEM Approved
* Traceability

**AVAILABLE DATA SOURCES:**
1. Raw SAM.gov contract announcements (text)
2. HTML scrapes from SAM.gov searches
3. Analysis documents on military procurement language
4. Federal Contract Pattern Mining document
5. Military Source Approval Requirements document
1. SOS Checklists and Logic previously used

**REQUIRED PATTERN CATEGORIES:**
- `sar_patterns`: Source approval requirements (military SAR only, ignore FAA/ISO)
- `sole_source_patterns`: Actual sole source language
- `intent_to_award_patterns`: Notice of intent language
- `only_known_source_patterns`: Named sole vendor language
- `oem_patterns`: Original Equipment Manufacturer references
- `oem_approved_patterns`: Authorized distributor or vendor required
- `traceability_patterns`: Chain of custody/anti-counterfeit language
- `aviation_platform_patterns`: Aircraft/engine/avionics identifiers
- `excluded_platform_patterns`: Non-aviation (ships, trucks, ground vehicles)
- `risk_clause_patterns`: CSI, DFARS, ITAR, export controls
- `currency_patterns`: Deadline/expiration language
- `tech_data_package_drawings_patterns`: Does the government own or is able to furnish the tech data or drawings
- `refurbished_rotatable_aftermarket_surplus_patterns`: Condition requirements
- `common_commercial_commercial-off-the-shelf_patterns`: Is the item(s) commercial and therefore only subject to commercial or industry requirements
- `far_part_12_usage_patterns`: Government is or intends on using FAR Part 12 and explicitly is not
- `aviation_indicator_patterns`: Language present indication relevance absent platform
- `security_clearance_patterns`: Security clearance and level required
- `original_manufacturer_patterns`: Must be procured from the manufacturer regardless of OEM relationship
- `selection_criteria_patterns`: Language used to select the awardee, e.g. LPTA, Prior Performance, etc.
- `civilan_aircraft_patterns`: Language used to communicate a platform or MDS is commercial, commercial-based, general, or civilian

**PRODUCTION REQUIREMENTS:**
Each category needs:
- 20-50 distinct pattern groups
- 50-200 variations per group
- Regex patterns with typo tolerance
- Exact phrase matching
- Partial/fuzzy matching
- Context patterns (before/after triggers)
- Agency-specific variations (Navy/Army/AF/DLA)
- Negative patterns (exclusions)
- Compound patterns (multi-part matches)
- Scoring weights for confidence levels
- AMC/AMSC code combinations
- CAGE code patterns

**OUTPUT FORMAT:**
```json
{
  "category": "",
  "pattern_groups": [
    {
      "group_name": "",
      "regex_patterns": [],
      "exact_phrases": [],
      "partial_triggers": [],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {}
    }
  ]
}
```

**CRITICAL NOTES:**
- This is for PRODUCTION use on 10K+ opportunities/month
- Must catch ALL variations (abbreviations, typos, formatting)
- False positive rate must be <2%
- Each pattern must be tested against real solicitation language
- System processes military aviation parts primarily
- Distributor perspective (not manufacturer)
- Must distinguish between tactical GO/NO-GO and strategic opportunities

**YOUR TASK:**
Use only actual government language to inform your Regex patterns from the project knowledge. Generate comprehensive, production-ready pattern sets for each category. Start with - `aviation_platform_patterns`: Aircraft/engine/avionics identifiers` and build complete pattern groups with hundreds of variations. Use the actual solicitation language from the provided documents as source material. 

**Think:** "What would catch this in 10,000 messy, inconsistent government documents?"