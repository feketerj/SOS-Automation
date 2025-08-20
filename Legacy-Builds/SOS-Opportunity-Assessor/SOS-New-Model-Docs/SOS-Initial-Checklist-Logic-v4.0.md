---

### SOURCE ONE SPARES - INITIAL ASSESSMENT LOGIC
#### Universal Go/No-Go Framework for All AI Models
##### PURPOSE
This framework provides a standardized initial assessment for government solicitations. Any AI model (ChatGPT, Claude, Gemini, Perplexity, etc.) following these instructions will produce consistent and robust results.

##### CRITICAL RULES
1.  **Quote the government's exact language** - Never paraphrase or summarize.
2.  **Include page/section numbers** for every quote.
3.  **If information not found**, state "No [topic] language found in document".
4.  **Follow checks in exact order** - **Stop at first NO-GO**.
5.  **Hard stops OVERRIDE all positive indicators**. If a hard stop is identified, the opportunity is a **NO-GO** regardless of any other favorable conditions.
6.  **When in doubt**, default to "NEEDS FURTHER ANALYSIS".

---

#### PHASE 0: PRELIMINARY GATES
These checks ensure the opportunity is relevant and actionable before deeper analysis.

##### CHECK 0.1: IS THIS AVIATION-RELATED?
**Search for ANY of these terms:**
*   Aircraft types: aircraft, helicopter, rotorcraft, airplane
*   Manufacturers: Boeing, Airbus, Bell, Sikorsky, Lockheed, Northrop
*   Military designators: C-130, KC-46, P-8, F-16, UH-60, CH-47
*   Components: engine, avionics, landing gear, hydraulic, propeller
*   Support: ground support equipment, GSE, AGE, aerospace
*   Codes: PSC 15XX/16XX/17XX, NAICS 3364XX

**Decision Logic:**
*   IF aviation-related terms are **found** → **CONTINUE**
*   IF **NOT** aviation-related terms are found → **NO-GO** (Not aviation-related)

**Required Output:**
*   Quote: "[Exact aviation-related text from document]" (Page X)
*   Decision: CONTINUE or NO-GO (Not aviation-related)

##### CHECK 0.2: IS THIS OPPORTUNITY CURRENT?
**Search for:**
*   "Response due"
*   "Closing date"
*   "Proposal due"
*   "Deadline"
*   "Offers due"

**Decision Logic:**
*   IF a future or current date is specified → **CONTINUE**
*   IF the date is in the past (expired) → **NO-GO** (Expired)

**Required Output:**
*   Quote: "Response Due: [exact date from document]" (Page X)
*   Today's Date: [Current date]
*   Decision: CONTINUE or NO-GO (Expired)

##### CHECK 0.3: PLATFORM VIABILITY CHECK
This check identifies immediate disqualifiers based on aircraft platform type.
**Search for:** Any aircraft designation (e.g., F-15, C-17, KC-46, Boeing 737, Bell 407).

**Decision Logic (Referencing Platform Identification Guide):**
*   IF the primary platform is listed as **"PURE MILITARY - TYPICALLY NO-GO"** (e.g., F-15, F-22, AH-64 Apache, C-17 Globemaster III) → **NO-GO** (Pure Military Platform)
*   IF the primary platform is listed as **"CONDITIONAL"** (e.g., P-3 Orion, A-29 Super Tucano) → **REQUIRES ANALYSIS**
*   IF the primary platform is listed as **"ALWAYS GO"** (e.g., Boeing 737, KC-46, Bell 407, all pure civilian aircraft) → **PASS**

**Required Output:**
*   Quote: "[Exact platform designation from solicitation]" (Page X)
*   Decision: PASS / NO-GO (Pure Military Platform) / REQUIRES ANALYSIS

---

#### PHASE 1: HARD STOP ANALYSIS
**CRITICAL: These hard stops OVERRIDE ALL positive indicators. No exceptions.**
**Stop at first NO-GO**.

##### CHECK 1: SOURCE APPROVAL REQUIRED (SAR)
**Search for these exact phrases:**
*   "source approval required"
*   "approved source list"
*   "qualified suppliers list"
*   "QPL" (Qualified Products List)
*   "QML" (Qualified Manufacturers List)
*   "requires engineering source approval"
*   "Government source approval required"
*   "military specification"
*   Any AMC/AMSC code: AMC 3, AMC 4, AMC 5, AMSC C, AMSC D, AMSC P, AMSC R

**Decision Logic (Referencing SOS Capabilities and Bid Matrix):**
*   IF **"source approval required" AND military specification**, OR **AMC 3, AMC 4, AMC 5, AMSC C, AMSC D, AMSC P, AMSC R** is found → **NO-GO** (Military SAR Present)
    *   *Rationale:* SOS **cannot** provide Military Source Approval Required (SAR) items. Typical SAR timelines (6-18 months) make it low-ROI for one-off buys.
*   IF "FAA source approval" is found → **PASS** (SOS can meet FAA standards)
*   IF "QPL" or "QML" found AND opportunity **explicitly states a path to apply** or become a QPL source → **REQUIRES ANALYSIS**
*   IF **NOT** found → **PASS**

**Required Output:**
*   Quote: "[Exact source approval language or 'No source approval language found']" (Page X)
*   Decision: PASS / NO-GO (Military SAR Present) / REQUIRES ANALYSIS

##### CHECK 2: SOLE SOURCE JUSTIFICATION
**Search for:**
*   "sole source"
*   "only one responsible source"
*   "single source"
*   "brand name justification"
*   "intent to sole source"

**Decision Logic:**
*   IF "Sole source to [specific company]" (and **not** Source One Spares) → **NO-GO**
*   IF "intent to sole source" → **REQUIRES ANALYSIS** (can be challenged by SOS)
*   IF "brand name or equal" → **REQUIRES ANALYSIS** (opportunity exists unless SAR also present)
*   IF **NOT** found → **PASS**

**Required Output:**
*   Quote: "[Exact sole source language or 'No sole source language found']" (Page X)
*   Decision: PASS / NO-GO / REQUIRES ANALYSIS

##### CHECK 3: TECHNICAL DATA AVAILABILITY
**Search for:**
*   "drawings not available"
*   "technical data not available"
*   "data rights"
*   "proprietary data"
*   "government does not have"
*   "contractor will not receive"
*   "no GFI" (Government Furnished Information)
*   "OEM owns technical data"

**Decision Logic:**
*   IF "drawings not available" OR "technical data not available" OR "OEM owns technical data" OR "proprietary technical data" → **NO-GO**
    *   *Rationale:* SOS cannot manufacture without government-owned technical data.
*   IF "Limited technical data" or "some drawings" → **REQUIRES ANALYSIS**
*   IF "government owns technical data" OR "technical data available upon award" → **PASS**
*   IF **NOT** found → **PASS**

**Required Output:**
*   Quote: "[Exact technical data language or 'No technical data restrictions found']" (Page X)
*   Decision: PASS / NO-GO / REQUIRES ANALYSIS

##### CHECK 4: SECURITY CLEARANCE REQUIREMENTS
**Search for:**
*   "security clearance"
*   "secret"
*   "top secret"
*   "classified"
*   "facility clearance"
*   "personnel clearance"

**Decision Logic:**
*   IF "Secret clearance required" or similar (any security clearance) → **NO-GO**
    *   *Rationale:* SOS cannot provide items requiring security clearances.
*   IF "May require clearance" → **REQUIRES ANALYSIS**
*   IF "unclassified" explicitly stated OR **NOT** found → **PASS**

**Required Output:**
*   Quote: "[Exact security language or 'No security clearance requirements found']" (Page X)
*   Decision: PASS / NO-GO / REQUIRES ANALYSIS

##### CHECK 5: NEW PARTS ONLY RESTRICTION
**Search for:**
*   "factory new only"
*   "new manufacture only"
*   "no refurbished"
*   "no rebuilt"
*   "no overhauled"
*   "no used"
*   "new condition only"

**Decision Logic:**
*   IF any of the above phrases indicating *only* new parts are found → **NO-GO**
    *   *Rationale:* SOS specializes in refurbished, surplus, and USM parts.
*   IF "Prefer new" or "new for critical items" → **REQUIRES ANALYSIS**
*   IF "Refurbished acceptable" OR "new or refurbished" → **PASS** (positive indicator)
*   IF **NOT** found (no restriction on condition) → **PASS**

**Required Output:**
*   Quote: "[Exact parts condition language or 'No parts condition restrictions found']" (Page X)
*   Decision: PASS / NO-GO / REQUIRES ANALYSIS

##### CHECK 6: PROHIBITED CERTIFICATIONS
**Search for:**
*   "AS9100"
*   "NADCAP"
*   Other certifications SOS does NOT have (refer to SOS Certifications Held)

**Note:** SOS HAS: ISO 9001:2015, AS9120B, FAA certifications, ASA Accreditation (FAA AC 00-56).

**Decision Logic:**
*   IF "AS9100 required" → **NO-GO**
*   IF "NADCAP required" → **NO-GO**
    *   *Rationale:* SOS lacks AS9100 (manufacturing) and NADCAP certifications.
*   IF "ISO 9001 required" OR "AS9120 required" OR "FAA certification required" → **PASS** (SOS has these)
*   IF **NOT** found (no special certifications required) → **PASS**

**Required Output:**
*   Quote: "[Exact certification requirements or 'No special certifications required']" (Page X)
*   Decision: PASS / NO-GO

##### CHECK 7: ITAR/EXPORT CONTROL
**Search for:**
*   "ITAR"
*   "export control"
*   "export license required"
*   "EAR"
*   "international traffic in arms"

**Decision Logic (Referencing SOS Capabilities):**
*   IF "ITAR registration required" or "export license required" is found → **REQUIRES ANALYSIS**
    *   *Rationale:* SOS **supports ITAR compliance for exports where required** and is **CAPABLE** of handling ITAR compliance with planning. This is not an immediate NO-GO unless an explicit, unusual requirement is identified that SOS cannot meet.
*   IF **NOT** found → **PASS**

**Required Output:**
*   Quote: "[Exact ITAR/export language or 'No ITAR/export requirements found']" (Page X)
*   Decision: PASS / REQUIRES ANALYSIS

##### CHECK 8: OEM DISTRIBUTION RESTRICTIONS
**Search for:**
*   "OEM only"
*   "authorized distributor"
*   "OEM distributor"
*   "factory authorized dealer"
*   "Source-Control drawing" + "OEM list governs"
*   AMSC B (Item on Source-Control drawing – OEM list governs)

**Decision Logic (Referencing SOS Capabilities and Bid Matrix):**
*   IF "OEM only", "authorized distributor required", "OEM distributor only", "factory authorized dealer", OR **AMSC B** is found → **NO-GO**
    *   *Rationale:* SOS **cannot** provide OEM-only restricted parts unless via approved channels, and often cannot register as an authorized OEM distributor for all parts.
*   IF **NOT** found → **PASS**

**Required Output:**
*   Quote: "[Exact OEM restriction language or 'No OEM distribution restrictions found']" (Page X)
*   Decision: PASS / NO-GO

---

#### FINAL DECISION MATRIX
##### Decision Rules:
1.  **ANY hard NO-GO = NO-GO** (Stop immediately, report which check failed)
2.  **ANY "REQUIRES ANALYSIS" + No hard stops = REQUIRES ANALYSIS** (List all unclear items)
3.  **ALL PASS = GO** (Proceed to comprehensive assessment)

##### MANDATORY OUTPUT FORMAT

##### FOR "GO" DECISIONS - PIPELINE TITLE FORMAT
**Required Format:**
`PN: [Part Numbers] | Qty: [Quantity] | [Announcement Number] | [Aircraft] | [Description]`

**Examples:**
*   `PN: 145-2134, 145-2135 | Qty: 10 | W58RGZ-25-Q-0001 | KC-46 | overhaul hydraulic actuators`
*   `PN: Various | Qty: NA | N00244-25-R-0012 | P-8 Poseidon | spare parts indefinite delivery`
*   `PN: 70-4591 | Qty: 25 | FA8201-25-Q-0087 | Support Equipment | purchase test consoles`
*   `PN: Various | Qty: Unk | SPE4A7-25-R-0234 | C-130 | surplus avionics components`

**Extraction Rules:**
*   **Part Numbers:** Find in solicitation, max 3. If more than 3, use "Various".
*   **Quantity:** Extract exact number. If not specified, use "NA" or "Unk".
*   **Announcement:** Use full solicitation number.
*   **Aircraft:** Use specific model if mentioned. If not, use "Support Equipment," "NA/Unk," or "Mixed Fleet".
*   **Description:** 2-4 words max, action verb + item (e.g., "overhaul pumps," "purchase gear," "repair engines").

---

#### SPECIAL INSTRUCTIONS FOR NO-GO OUTCOMES
##### For Source Approval or OEM Restrictions:
If **NO-GO** due to source approval (Military SAR) or OEM-only requirements, document as "NO-GO - SAR Present (CO Contact Made)" or "NO-GO - OEM Distributor Required (CO Contact Made)."
**Action:** Contact the Contracting Officer (CO) with a message about SOS's specialization in FAA-certified refurbished and surplus parts, expressing interest if non-OEM sourcing becomes acceptable in future modifications or recompetes. This plants seeds for future business development.

##### For Intent to Sole Source:
If **REQUIRES ANALYSIS** due to intent to sole source, document as "RA - Intent to Sole Source (Challenge Opportunity)."
**Action:** Review "Sources Sought Template.pdf" for guidance on submitting a response challenging the sole source justification.

---

#### IMPLEMENTATION NOTES
1.  **This framework is platform-agnostic** - Works with any AI model or manual review.
2.  **Quotes are mandatory** - No exceptions, no paraphrasing.
3.  **Order matters** - Always check in sequence, stop at first hard NO-GO.
4.  **When in doubt** - Mark as REQUIRES ANALYSIS, not NO-GO.
5.  **Page numbers required** - Helps verify and locate information quickly.
6.  **Hard stops override everything** - No positive indicator matters if a hard stop is present.

---

*Version 4.0 - 07-30-25* *Created by Rob Fekete, Director, Government Business Engagement, Source One Spares, LLC*