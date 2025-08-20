# SOS COMBINED ASSESSMENT DOCUMENTS

*Single file for GPT upload efficiency - Each section is a standalone process*

---

# DOCUMENT 1: SOS INITIAL ASSESSMENT LOGIC v4.0

## SOURCE ONE SPARES - INITIAL ASSESSMENT LOGIC
### Universal Go/No-Go Framework for All AI Models

#### PURPOSE
This framework provides a standardized initial assessment for government solicitations. Any AI model (ChatGPT, Claude, Gemini, Perplexity, etc.) following these instructions will produce consistent and robust results.

#### CRITICAL RULES
1. **Quote the government's exact language** - Never paraphrase or summarize.
2. **Include page/section numbers** for every quote.
3. **If information not found**, state "No [topic] language found in document".
4. **Follow checks in exact order** - **Stop at first NO-GO**.
5. **Hard stops OVERRIDE all positive indicators**. If a hard stop is identified, the opportunity is a **NO-GO** regardless of any other favorable conditions.
6. **When in doubt**, default to "NEEDS FURTHER ANALYSIS".

### PHASE 0: PRELIMINARY GATES
These checks ensure the opportunity is relevant and actionable before deeper analysis.

#### CHECK 0.1: IS THIS AVIATION-RELATED?
**Search for ANY of these terms:**
- Aircraft types: aircraft, helicopter, rotorcraft, airplane
- Manufacturers: Boeing, Airbus, Bell, Sikorsky, Lockheed, Northrop
- Military designators: C-130, KC-46, P-8, F-16, UH-60, CH-47
- Components: engine, avionics, landing gear, hydraulic, propeller
- Support: ground support equipment, GSE, AGE, aerospace
- Codes: PSC 15XX/16XX/17XX, NAICS 3364XX

**Decision Logic:**
- IF aviation-related terms are **found** → **CONTINUE**
- IF **NOT** aviation-related terms are found → **NO-GO** (Not aviation-related)

**Required Output:**
- Quote: "[Exact aviation-related text from document]" (Page X)
- Decision: CONTINUE or NO-GO (Not aviation-related)

#### CHECK 0.2: IS THIS OPPORTUNITY CURRENT?
**Search for:**
- "Response due"
- "Closing date"
- "Proposal due"
- "Deadline"
- "Offers due"

**Decision Logic:**
- IF a future or current date is specified → **CONTINUE**
- IF the date is in the past (expired) → **NO-GO** (Expired)

**Required Output:**
- Quote: "Response Due: [exact date from document]" (Page X)
- Today's Date: [Current date]
- Decision: CONTINUE or NO-GO (Expired)

#### CHECK 0.3: PLATFORM VIABILITY CHECK
This check identifies immediate disqualifiers based on aircraft platform type.
**Search for:** Any aircraft designation (e.g., F-15, C-17, KC-46, Boeing 737, Bell 407).

**Decision Logic (Referencing Platform Identification Guide):**
- IF the primary platform is listed as **"PURE MILITARY - TYPICALLY NO-GO"** (e.g., F-15, F-22, AH-64 Apache, C-17 Globemaster III) → **NO-GO** (Pure Military Platform)
- IF the primary platform is listed as **"CONDITIONAL"** (e.g., P-3 Orion, A-29 Super Tucano) → **REQUIRES ANALYSIS**
- IF the primary platform is listed as **"ALWAYS GO"** (e.g., Boeing 737, KC-46, Bell 407, all pure civilian aircraft) → **PASS**

**Required Output:**
- Quote: "[Exact platform designation from solicitation]" (Page X)
- Decision: PASS / NO-GO (Pure Military Platform) / REQUIRES ANALYSIS

### PHASE 1: HARD STOP ANALYSIS
**CRITICAL: These hard stops OVERRIDE ALL positive indicators. No exceptions.**
**Stop at first NO-GO**.

#### CHECK 1: SOURCE APPROVAL REQUIRED (SAR)
**Search for these exact phrases:**
- "source approval required"
- "approved source list"
- "qualified suppliers list"
- "QPL" (Qualified Products List)
- "QML" (Qualified Manufacturers List)
- "requires engineering source approval"
- "Government source approval required"
- "military specification"
- Any AMC/AMSC code: AMC 3, AMC 4, AMC 5, AMSC C, AMSC D, AMSC P, AMSC R

**Decision Logic (Referencing SOS Capabilities and Bid Matrix):**
- IF **"source approval required" AND military specification**, OR **AMC 3, AMC 4, AMC 5, AMSC C, AMSC D, AMSC P, AMSC R** is found → **NO-GO** (Military SAR Present)
  - *Rationale:* SOS **cannot** provide Military Source Approval Required (SAR) items. Typical SAR timelines (6-18 months) make it low-ROI for one-off buys.
- IF "FAA source approval" is found → **PASS** (SOS can meet FAA standards)
- IF "QPL" or "QML" found AND opportunity **explicitly states a path to apply** or become a QPL source → **REQUIRES ANALYSIS**
- IF **NOT** found → **PASS**

**Required Output:**
- Quote: "[Exact source approval language or 'No source approval language found']" (Page X)
- Decision: PASS / NO-GO (Military SAR Present) / REQUIRES ANALYSIS

#### CHECK 2: SOLE SOURCE JUSTIFICATION
**Search for:**
- "sole source"
- "only one responsible source"
- "single source"
- "brand name justification"
- "intent to sole source"

**Decision Logic:**
- IF "Sole source to [specific company]" (and **not** Source One Spares) → **NO-GO**
- IF "intent to sole source" → **REQUIRES ANALYSIS** (can be challenged by SOS)
- IF "brand name or equal" → **REQUIRES ANALYSIS** (opportunity exists unless SAR also present)
- IF **NOT** found → **PASS**

**Required Output:**
- Quote: "[Exact sole source language or 'No sole source language found']" (Page X)
- Decision: PASS / NO-GO / REQUIRES ANALYSIS

#### CHECK 3: TECHNICAL DATA AVAILABILITY
**Search for:**
- "drawings not available"
- "technical data not available"
- "data rights"
- "proprietary data"
- "government does not have"
- "contractor will not receive"
- "no GFI" (Government Furnished Information)
- "OEM owns technical data"

**Decision Logic:**
- IF "drawings not available" OR "technical data not available" OR "OEM owns technical data" OR "proprietary technical data" → **NO-GO**
  - *Rationale:* SOS cannot manufacture without government-owned technical data.
- IF "Limited technical data" or "some drawings" → **REQUIRES ANALYSIS**
- IF "government owns technical data" OR "technical data available upon award" → **PASS**
- IF **NOT** found → **PASS**

**Required Output:**
- Quote: "[Exact technical data language or 'No technical data restrictions found']" (Page X)
- Decision: PASS / NO-GO / REQUIRES ANALYSIS

#### CHECK 4: SECURITY CLEARANCE REQUIREMENTS
**Search for:**
- "security clearance"
- "secret"
- "top secret"
- "classified"
- "facility clearance"
- "personnel clearance"

**Decision Logic:**
- IF "Secret clearance required" or similar (any security clearance) → **NO-GO**
  - *Rationale:* SOS cannot provide items requiring security clearances.
- IF "May require clearance" → **REQUIRES ANALYSIS**
- IF "unclassified" explicitly stated OR **NOT** found → **PASS**

**Required Output:**
- Quote: "[Exact security language or 'No security clearance requirements found']" (Page X)
- Decision: PASS / NO-GO / REQUIRES ANALYSIS

#### CHECK 5: NEW PARTS ONLY RESTRICTION
**Search for:**
- "factory new only"
- "new manufacture only"
- "no refurbished"
- "no rebuilt"
- "no overhauled"
- "no used"
- "new condition only"

**Decision Logic:**
- IF any of the above phrases indicating *only* new parts are found → **NO-GO**
  - *Rationale:* SOS specializes in refurbished, surplus, and USM parts.
- IF "Prefer new" or "new for critical items" → **REQUIRES ANALYSIS**
- IF "Refurbished acceptable" OR "new or refurbished" → **PASS** (positive indicator)
- IF **NOT** found (no restriction on condition) → **PASS**

**Required Output:**
- Quote: "[Exact parts condition language or 'No parts condition restrictions found']" (Page X)
- Decision: PASS / NO-GO / REQUIRES ANALYSIS

#### CHECK 6: PROHIBITED CERTIFICATIONS
**Search for:**
- "AS9100"
- "NADCAP"
- Other certifications SOS does NOT have (refer to SOS Certifications Held)

**Note:** SOS HAS: ISO 9001:2015, AS9120B, FAA certifications, ASA Accreditation (FAA AC 00-56).

**Decision Logic:**
- IF "AS9100 required" → **NO-GO**
- IF "NADCAP required" → **NO-GO**
  - *Rationale:* SOS lacks AS9100 (manufacturing) and NADCAP certifications.
- IF "ISO 9001 required" OR "AS9120 required" OR "FAA certification required" → **PASS** (SOS has these)
- IF **NOT** found (no special certifications required) → **PASS**

**Required Output:**
- Quote: "[Exact certification requirements or 'No special certifications required']" (Page X)
- Decision: PASS / NO-GO

#### CHECK 7: ITAR/EXPORT CONTROL
**Search for:**
- "ITAR"
- "export control"
- "export license required"
- "EAR"
- "international traffic in arms"

**Decision Logic (Referencing SOS Capabilities):**
- IF "ITAR registration required" or "export license required" is found → **REQUIRES ANALYSIS**
  - *Rationale:* SOS **supports ITAR compliance for exports where required** and is **CAPABLE** of handling ITAR compliance with planning. This is not an immediate NO-GO unless an explicit, unusual requirement is identified that SOS cannot meet.
- IF **NOT** found → **PASS**

**Required Output:**
- Quote: "[Exact ITAR/export language or 'No ITAR/export requirements found']" (Page X)
- Decision: PASS / REQUIRES ANALYSIS

#### CHECK 8: OEM DISTRIBUTION RESTRICTIONS
**Search for:**
- "OEM only"
- "authorized distributor"
- "OEM distributor"
- "factory authorized dealer"
- "Source-Control drawing" + "OEM list governs"
- AMSC B (Item on Source-Control drawing – OEM list governs)

**Decision Logic (Referencing SOS Capabilities and Bid Matrix):**
- IF "OEM only", "authorized distributor required", "OEM distributor only", "factory authorized dealer", OR **AMSC B** is found → **NO-GO**
  - *Rationale:* SOS **cannot** provide OEM-only restricted parts unless via approved channels, and often cannot register as an authorized OEM distributor for all parts.
- IF **NOT** found → **PASS**

**Required Output:**
- Quote: "[Exact OEM restriction language or 'No OEM distribution restrictions found']" (Page X)
- Decision: PASS / NO-GO

### FINAL DECISION MATRIX
#### Decision Rules:
1. **ANY hard NO-GO = NO-GO** (Stop immediately, report which check failed)
2. **ANY "REQUIRES ANALYSIS" + No hard stops = REQUIRES ANALYSIS** (List all unclear items)
3. **ALL PASS = GO** (Proceed to comprehensive assessment)

#### MANDATORY OUTPUT FORMAT

#### FOR "GO" DECISIONS - PIPELINE TITLE FORMAT
**Required Format:**
`PN: [Part Numbers] | Qty: [Quantity] | [Announcement Number] | [Aircraft] | [Description]`

**Examples:**
- `PN: 145-2134, 145-2135 | Qty: 10 | W58RGZ-25-Q-0001 | KC-46 | overhaul hydraulic actuators`
- `PN: Various | Qty: NA | N00244-25-R-0012 | P-8 Poseidon | spare parts indefinite delivery`
- `PN: 70-4591 | Qty: 25 | FA8201-25-Q-0087 | Support Equipment | purchase test consoles`
- `PN: Various | Qty: Unk | SPE4A7-25-R-0234 | C-130 | surplus avionics components`

**Extraction Rules:**
- **Part Numbers:** Find in solicitation, max 3. If more than 3, use "Various".
- **Quantity:** Extract exact number. If not specified, use "NA" or "Unk".
- **Announcement:** Use full solicitation number.
- **Aircraft:** Use specific model if mentioned. If not, use "Support Equipment," "NA/Unk," or "Mixed Fleet".
- **Description:** 2-4 words max, action verb + item (e.g., "overhaul pumps," "purchase gear," "repair engines").

### SPECIAL INSTRUCTIONS FOR NO-GO OUTCOMES
#### For Source Approval or OEM Restrictions:
If **NO-GO** due to source approval (Military SAR) or OEM-only requirements, document as "NO-GO - SAR Present (CO Contact Made)" or "NO-GO - OEM Distributor Required (CO Contact Made)."
**Action:** Contact the Contracting Officer (CO) with a message about SOS's specialization in FAA-certified refurbished and surplus parts, expressing interest if non-OEM sourcing becomes acceptable in future modifications or recompetes. This plants seeds for future business development.

#### For Intent to Sole Source:
If **REQUIRES ANALYSIS** due to intent to sole source, document as "RA - Intent to Sole Source (Challenge Opportunity)."
**Action:** Review "Sources Sought Template.pdf" for guidance on submitting a response challenging the sole source justification.

### IMPLEMENTATION NOTES
1. **This framework is platform-agnostic** - Works with any AI model or manual review.
2. **Quotes are mandatory** - No exceptions, no paraphrasing.
3. **Order matters** - Always check in sequence, stop at first hard NO-GO.
4. **When in doubt** - Mark as REQUIRES ANALYSIS, not NO-GO.
5. **Page numbers required** - Helps verify and locate information quickly.
6. **Hard stops override everything** - No positive indicator matters if a hard stop is present.

---

# DOCUMENT 2: PLATFORM IDENTIFICATION GUIDE

## Source One Spares - Platform Identification Guide

### CRITICAL INSTRUCTION
**DO NOT INFER platform relationships. Use ONLY the explicit mappings below. If a platform is not listed, mark as "NEEDS FURTHER ANALYSIS" rather than guessing.**

### MILITARY-TO-CIVILIAN PLATFORM MAPPINGS

#### Boeing Military Aircraft
| Military Designation | Civilian Equivalent | Parts Commonality | Assessment |
|---------------------|---------------------|-------------------|------------|
| KC-46 Pegasus | Boeing 767 | High | **GO** |
| P-8 Poseidon | Boeing 737 | High | **GO** |
| C-40 Clipper | Boeing 737 BBJ | Very High | **GO** |
| C-32 | Boeing 757 | High | **GO** |
| VC-25 (Air Force One) | Boeing 747 | High | **GO** |
| E-3 Sentry (AWACS) | Boeing 707 | Medium | **GO** |
| E-6 Mercury | Boeing 707 | Medium | **GO** |
| E-8 JSTARS | Boeing 707 | Medium | **GO** |
| KC-135 Stratotanker | Boeing 707 variant | Medium | **GO** |
| E-4B | Boeing 747 | High | **GO** |
| E-7 Wedgetail | Boeing 737 | High | **GO** |
| KC-10 Extender | McDonnell Douglas DC-10 | High | **GO** |
| C-17 Globemaster III | None - Pure Military | None | **NO-GO** |

#### Other Transport Aircraft
| Military Designation | Civilian Equivalent | Parts Commonality | Assessment |
|---------------------|---------------------|-------------------|------------|
| C-130 Hercules | L-100 (very limited civilian) | Low | **NO-GO** unless specifically L-100 |
| C-27J Spartan | G.222 (minimal civilian) | Very Low | **NO-GO** |
| C-12 Huron (all variants) | Beechcraft King Air 200/350 | Very High | **GO** |
| UC-12B/F/M/W | Beechcraft King Air | Very High | **GO** |
| C-26 Metroliner | Fairchild Metro/Merlin | High | **GO** |
| C-20 (A/B/C/D/E/F/G/H) | Gulfstream III/IV/V | Very High | **GO** |
| C-21 | Learjet 35 | Very High | **GO** |
| C-37 (A/B) | Gulfstream V/550 | Very High | **GO** |
| UC-35 (all variants) | Cessna Citation | Very High | **GO** |
| C-47 Skytrain | Douglas DC-3 | High | **GO** |
| P-3 Orion | L-188 Electra (limited) | Medium | **CONDITIONAL** |
| UV-18 Twin Otter | De Havilland DHC-6 | Very High | **GO** |
| C-23 Sherpa | Shorts 330/360 | High | **GO** |
| CN-235 | CASA CN-235 (civilian cargo) | High | **GO** |
| C-144 Ocean Sentry | CASA CN-235 | High | **GO** |
| HC-27J | C-27J (see above) | Military platform | **NO-GO** unless FAA standards |
| CL-415 | Pure civilian firefighter | Very High | **GO** |

#### Military Helicopters
| Military Designation | Civilian Equivalent | Parts Commonality | Assessment |
|---------------------|---------------------|-------------------|------------|
| UH-60 Black Hawk | Sikorsky S-70 | High | **GO** |
| MH-60 (all variants) | Sikorsky S-70 | High | **GO** |
| HH-60 Pave Hawk | Sikorsky S-70 | High | **GO** |
| VH-60 | Sikorsky S-70 | High | **GO** |
| MH-65 Dolphin | Eurocopter AS365 | Very High | **GO** |
| UH-72 Lakota | Eurocopter EC145 | Very High | **GO** |
| TH-57 Sea Ranger | Bell 206 | Very High | **GO** |
| UH-1 (all variants) | Bell 204/205/212 | High | **GO** |
| TH-67 Creek | Bell 206 | Very High | **GO** |
| OH-58 Kiowa | Bell 206/407 | High | **GO** |
| AH-64 Apache | None - Pure Military | None | **NO-GO** |
| CH-47 Chinook | Model 234 (very limited civilian) | Very Low | **NO-GO** unless specifically civilian |
| CH-53 (all variants) | Very limited civilian use | Very Low | **NO-GO** |

### PURE CIVILIAN AIRCRAFT - ALWAYS GO

#### General Aviation
- All Cessna models (172, 182, 206, 208 Caravan, Citations, etc.)
- All Piper models
- All Beechcraft models (Bonanza, Baron, King Air, etc.)
- All Cirrus models
- All Diamond models
- Mooney aircraft
- Pilatus PC-12
- TBM series

#### Regional/Commercial
- All Bombardier CRJ/Q-Series/Dash-8
- All Embraer E-Jets and ERJ series
- All ATR models
- All Saab 340/2000
- All Fokker models (if still in service)

#### Business Jets
- All Gulfstream models
- All Learjet models
- All Challenger/Global models
- All Dassault Falcon models
- All Hawker models
- All Citation models

#### Helicopters
- All Bell civilian models (206, 407, 412, 429, etc.)
- All Airbus Helicopters models (AS350, EC120, EC135, EC145, etc.)
- All Sikorsky S-76, S-92
- All AgustaWestland civilian models
- Robinson R22, R44, R66

### PURE MILITARY - TYPICALLY NO-GO

#### Fighter/Attack Aircraft
- F-15, F-16, F-18, F-22, F-35
- A-10 Thunderbolt II
- AV-8B Harrier
- All foreign fighters (Typhoon, Rafale, Gripen, etc.)

#### Bombers
- B-1B Lancer
- B-2 Spirit  
- B-52 Stratofortress
- B-21 Raider

#### Military-Unique Platforms
- C-5 Galaxy (limited L-500 civilian never produced)
- C-17 Globemaster III
- C-130 Hercules (unless specifically L-100 civilian variant)
- V-22 Osprey
- E-2 Hawkeye
- MQ-9 Reaper, MQ-1 Predator (UAVs)
- All pure fighter/attack aircraft

### SPECIAL CASES & RULES

#### Foreign Military Sales (FMS)
- FMS opportunities often have relaxed source requirements
- May allow commercial standard parts even for military aircraft
- Generally a **POSITIVE indicator**

#### Coast Guard/DHS/CBP Aircraft - ALL ARE GO
**All use civilian FAA standards and procurement rules**

| Aircraft | Base Platform | Parts Source | Assessment |
|----------|---------------|--------------|------------|
| HC-144A Ocean Sentry | CASA CN-235 | Civilian | **GO** |
| HC-130H/J Hercules | C-130H/J | Military platform | **NO-GO** unless FAA standards specified |
| HC-27J Spartan | C-27J | Military platform | **NO-GO** unless civilian procurement specified |
| MH-60T Jayhawk | Sikorsky S-70/UH-60 | Military/Civilian | **GO** |
| MH-65D/E Dolphin | Eurocopter AS365 | Pure Civilian | **GO** |
| HH-65 Dolphin (older) | AS365 Dauphin | Pure Civilian | **GO** |
| HU-25 Guardian | Dassault Falcon 20 | Pure Civilian | **GO** |
| HC-131A Samaritan | Convair C-131 | Civilian cargo | **GO** |
| C-143A | Dornier 328 | Pure Civilian | **GO** |

#### State & Local Government
- **ALL are GO** - Pure civilian market
- Police helicopters, firefighting aircraft, transport
- No military restrictions apply
- All use civilian FAA standards
- Common examples: Bell 407, AS350, Cessna 208, King Air

### Engine/Component Keywords
When solicitation mentions only engines or components:

**Commercial/Dual-Use Engines - GO:**
- CFM56 = Boeing 737, KC-135R, E-3/E-6 = **GO**
- CF6/F103 = Boeing 767, KC-10, C-5M = **GO**
- F117/PW2000 = Boeing 757, C-32 = **GO**
- PW4000 = Boeing 777, KC-46, C-17 = **GO**
- GE90 = Boeing 777 only = **GO**
- V2500 = Airbus A320 family = **GO**
- PT6 = King Air, Caravan, PC-12 = **GO**
- TFE731 = Various business jets = **GO**

**Fighter/Military Only Engines - NO-GO:**
- F100/F110 = F-15, F-16 only = **NO-GO**
- F119 = F-22 only = **NO-GO**
- F135 = F-35 only = **NO-GO**
- F404/F414 = F/A-18 only = **NO-GO**

### ASSESSMENT GUIDANCE

**ABSOLUTE RULES - NO EXCEPTIONS:**
1. **If hard stop present** → NO-GO regardless of platform
2. **If platform IS listed above** → Use the assessment provided
3. **If platform NOT listed** → Mark "NEEDS FURTHER ANALYSIS"
4. **Military SAR always wins** → Even on civilian platforms
5. **When in doubt** → Default to NO-GO or NEEDS ANALYSIS

---

# DOCUMENT 3: PIPELINE TITLE FORMAT

## SOS Pipeline Title Structure

### Any "Go," or entry into the SOS pipeline must be retitled via the SOS Pipeline Title structure. This is to ensure ease of upstream research and facilitate timely decision making.

**SAM or HigherGov Format:**
`PN: [part number or various] | Qty: [quantity] | [announcement #] | [aircraft or support equipment type OR NA, Unk] | [brief description, e.g. overhaul brake, purchase landing gear, surplus console]`

**Examples:**
- `PN: 8675-309 | Qty: 1 | SPE4A525R0274 | KC-46 | Overhaul Lav & Sink`
- `PN: 1313-MB-6060, various | Qty: 3, various | H9224025QE029 | Unk | Surplus purchase brakes, brackets, others`

**External RFQ Format:**
`External RFQ | PN: [part number or various] | Qty: [quantity] | Customer/PO: [Customer's Company and Purchase Order Number] | [aircraft type OR support equipment type OR NA, Unk] | Condition: [NE, OH, etc.] | [brief description, e.g. overhaul brake, purchase landing gear, surplus console]`

**Examples:**
- `External RFQ | PN: 33-T6500-1RF-GD | Qty: 10 | Customer/PO: Matrea PO: 928-3311677 | C-12 Huron | Condition: OH | Purchase overhauled gearbox, prop seal`
- `External RFQ | PN: 23-DON-1BGG-27WS, various | Qty: 2, various | Customer/PO: Acme Aviation PO: 99-2025-1 | KC-10, C-47 | Condition: NE | Purchase new landing light, nose cone, pullies`

---

# DOCUMENT 4: CONTRACTING OFFICER CONTACT LOGIC & TEMPLATE

## Logic for Triggering Contracting Officer (CO) Email

The decision to send an email to the Contracting Officer (CO) is primarily triggered when a solicitation contains specific sourcing restrictions that present a **hard "No-Go"** for Source One Spares (SOS). This approach aligns with the "BD Strategy for OEM Distribution Restrictions" and the "Military SAR Opportunities - Contact Contracting Officer Protocol" outlined in the sources, aiming to "plant seeds for future contract modifications or recompetes".

### Trigger Condition:

An email to the CO will be generated and the opportunity flagged as a **"STOP: NO-GO + CO Contact"** if the solicitation explicitly states any of the following requirements:

- "OEM direct traceability only"
- "authorized distributor required"
- "OEM distributor only"
- "factory authorized dealer"
- Any requirement implying that parts must come *only* from an OEM-approved source or authorized OEM channel

### Reasoning:

These requirements represent a **hard limitation** on who can supply the part, rather than just how the part's history is documented (e.g., "fully traceable to OEM," which SOS can manage). Such clauses are considered show-stoppers, similar to a Source Approval Requirement (SAR) where SOS is not an approved source. The goal of contacting the CO in these "No-Go" scenarios is not to bid on the current opportunity but to establish a relationship and inform the government about SOS's capabilities should future requirements become less restrictive.

### Contracting Officer (CO) Email Template

This template is designed to respectfully acknowledge the solicitation's requirements, state SOS's inability to meet the specific sourcing restrictions, and proactively position SOS for future opportunities by highlighting its core strengths.

**Subject: Sources Sought Response – [Insert Notice Title or Number] – Clarification on Sourcing Requirements**

[Contracting Officer(s) name],

Source One Spares LLC is pleased to submit this response to the Sources Sought Notice titled **[Insert Notice Title or Solicitation Number]**. We understand that this particular procurement requires parts to be **[Quote the exact restrictive language, e.g., "OEM direct traceability only"]**.

As a leader in the aviation aftermarket, Source One Spares specializes in providing **FAA-certified refurbished and surplus parts**, as well as new aftermarket components, for commercial and government aircraft operators worldwide. All SOS components are **fully traceable and tagged by leading FAA-certified repair facilities**, ensuring rigorous quality and compliance standards. We maintain an **extensive inventory** of both new and refurbished parts for nearly every aircraft type in operation today and operate a **"just-in-time" (JIT) delivery model** to minimize downtime. We also support ITAR compliance for exports where required.

While we understand that our current aftermarket sourcing model may not align with the stated requirement for **[re-iterate restrictive language, e.g., "OEM approved only"]** for this specific solicitation, we respectfully request to be considered should the scope or eligibility criteria evolve. We are adept at providing commercial parts with **full FAA Form 8130-3 traceability from aftermarket sources**, which could offer significant cost efficiencies and availability.

Should non-OEM sourcing become acceptable, or if there is ever a need for **FAA-certified refurbished or surplus parts**, we maintain extensive inventory and would welcome the opportunity to contribute to this effort under a revised framework. Our team is confident in our ability to provide effective support through our robust capabilities in part sourcing, global logistics, and repair coordination.

Please find our capability statement and past performance summary attached for your review. Should you require additional information or wish to schedule a capabilities briefing, we would be happy to coordinate at your convenience.

Respectfully,

[Your signature bloc]

---

# DOCUMENT 5: SOS General Outreach Email Logic

## Purpose
This document provides guidance for using the Source One Spares (SOS) general outreach email template for proactive business development with government contracting officers, depot maintenance activities, sustainment organizations, and potential teaming partners.

## When to Use This Template
- **Proactive Outreach:** Initial contact with organizations that may benefit from alternative aviation sourcing
- **Teaming Partner Introduction:** Reaching out to primes or other contractors for partnership opportunities
- **Market Research Responses:** Responding to Sources Sought notices where SOS capabilities align
- **Relationship Building:** Initial contact with new contracting offices, program managers, or industry partners
- **Capability Briefings:** Following up from conferences, meetings, or referrals

## Salutation Guidelines
- **If name is known:** Dear Mr./Ms. [Last Name],
- **If name is unknown:** Sir/Ma'am,
- **Never use:** "To Whom It May Concern"

## Recipient Categories & Customization

### For Contracting Officers
- Emphasize cost savings and contract compliance
- Reference small business status and socioeconomic benefits
- Focus on reducing administrative lead time (ALT)

### For Depot/Sustainment Organizations  
- Highlight carcass availability and piece part solutions
- Emphasize production lead time (PLT) reduction
- Focus on readiness rate improvements

### For Teaming Partners
- Emphasize complementary capabilities
- Highlight small business subcontracting opportunities
- Focus on fill rates and on-time delivery metrics

## Email Template

### General Aviation Sourcing Outreach

**Subject Line Options:**
- Alternative Aviation Sourcing Solutions - Source One Spares
- Teaming Opportunity for [Specific Program] - Source One Spares  
- Reducing ALT/PLT for [Organization] Aviation Requirements

**Body:**

Sir/Ma'am, [or Dear Mr./Ms. LastName,]

Source One Spares LLC specializes in providing cost-effective aviation sourcing solutions that directly support sustainment operations by reducing administrative and production lead times while maintaining full compliance with quality standards.

**Our Core Capabilities:**

- **FAA-Certified Refurbished Components** - Full FAA Form 8130-3 traceability offering 40-70% cost savings
- **Surplus New Parts** - Extensive inventory from fleet retirements and overstock
- **Piece Part Solutions** - Individual components to support repair operations when carcass availability is constrained
- **Commercial-Derivative Expertise** - Specialization in military platforms with civilian equivalents (KC-46/767, P-8/737, C-40/737 BBJ)
- **Just-In-Time Delivery** - 24/7 global support to reduce aircraft downtime and improve readiness rates

**Supporting Your Mission:**

[CUSTOMIZE THIS SECTION BASED ON RECIPIENT TYPE]

*For Contracting Officers:*
- Small business participation supporting socioeconomic goals
- Proven performance on USAF KC-46 program requirements
- Alternative sourcing strategies that maximize budget efficiency

*For Depot/Sustainment:*
- Solutions for carcass constraints through refurbished assemblies or piece parts
- Reduction of backorder situations through immediate availability
- Support for obsolescence management and diminishing manufacturing sources
- Surge capacity for unexpected maintenance demands

*For Teaming Partners:*
- Complementary capabilities enhancing total solution offerings
- Small business subcontracting opportunities
- Proven reliability with 27+ years of on-time delivery performance

**Our Qualifications:**
- **Certifications:** ISO 9001:2015, AS9120B, FAA AC 00-56
- **Experience:** 27+ years supporting commercial airlines and government operators
- **Contract Vehicles:** Active participant on USAF KC-46 sustainment contracts
- **Compliance:** ITAR registered, full technical documentation and traceability
- **Registration:** UEI: RTP4E5UBJ3B7 | CAGE: 95QA6

Understanding the balance between readiness requirements and fiscal constraints, we offer proven alternatives that can reduce both administrative and production lead times while maintaining the quality standards your mission demands.

I would welcome the opportunity to discuss how our capabilities align with your specific requirements or explore potential collaboration opportunities.

Respectfully,

[Your signature block]

**Attachment:** SOS Capability Statement

---

## Key Language for Defense Officials
Use these terms when customizing:
- **ALT** - Administrative Lead Time
- **PLT** - Production Lead Time  
- **Readiness Rate** - Mission capability rates
- **Carcass Constraints** - Core availability limitations
- **Piece Parts** - Individual components for repairs
- **Surge Requirements** - Unexpected demand spikes
- **Obsolescence Management** - Solutions for out-of-production items
- **Diminishing Manufacturing Sources** - Alternative to discontinued OEM parts

## Follow-Up Strategy
1. **Initial Send:** Document date and recipient details
2. **Two-Week Follow-Up:** Brief professional check-in
3. **Quarterly Updates:** Share relevant capability enhancements
4. **Event-Driven:** Follow up after industry days or conferences

## Documentation Requirements
Track all outreach in CRM/database with:
- **Recipient Name/Title:** [Full details]
- **Organization:** [Command/Company name and location]
- **Date Sent:** [Date]
- **Response Received:** [Yes/No/Date]
- **Next Action:** [Scheduled follow-up or notes]

---

# DOCUMENT 7: COMPLETE EXTERNAL RFQ AUTOMATED PROCESS LOGIC

### PHASE 1: INITIAL SCAN & CLASSIFICATION

**Search for Government Indicators (ANY = Government End User):**
```
IF email contains:
- Domain ending in .mil OR .gov → Government = YES
- "DoD" OR "USAF" OR "NAVAIR" OR "DLA" OR "GSA" OR "NAVSUP" → Government = YES
- Contract format matching [A-Z][0-9]{5}-[0-9]{2}-[A-Z]-[0-9]{4} → Government = YES
- "DO-A1" OR "DX" priority rating → Government = YES
- "KC-" OR "C-" OR "P-" OR "F-" OR "UH-" OR "MH-" OR "HH-" aircraft → Government = YES
- "no resale" OR "direct installation" OR "we are the end user" → Government = YES
- "SAPGov" OR "WAWF" OR "Go" OR "AMP" OR "ILSS" → Government = YES
- "ITAR" OR "EAR" OR "ECCN" OR "PMIC" OR "DMIL" → Government = YES + Export Control = YES
ELSE → Government = UNKNOWN
```

### PHASE 2: DATA EXTRACTION

**Extract Required Fields:**
```
Part Numbers:
- Search for patterns: [0-9]{2,}-[0-9]{4,} OR [A-Z0-9]{4,}-[A-Z0-9]{4,}
- If none found → Missing_Parts = TRUE

Quantities:
- Search for "QTY" OR "QUANTITY" OR "EA" followed by numbers
- If none found → Missing_Qty = TRUE

Condition:
- Search for "NE" OR "NEW" → Condition = NE
- Search for "OH" OR "OVERHAULED" → Condition = OH
- Search for "SV" OR "SERVICEABLE" → Condition = SV
- Search for "AR" OR "AS REMOVED" → Condition = AR
- Search for "NS" OR "NEW SURPLUS" → Condition = NS
- If none found → Missing_Condition = TRUE

Delivery:
- Search for date patterns: [0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}
- Search for "ASAP" OR "AOG" OR "URGENT" → Delivery = URGENT
- If none found → Missing_Delivery = TRUE

Contract/PO:
- Search for "CONTRACT" OR "PO" OR "PURCHASE ORDER" followed by alphanumeric
- If none found AND Government = YES → Missing_Contract = TRUE
```

### PHASE 3: AUTOMATED EMAIL GENERATION

**IF ANY Missing Fields OR Government = UNKNOWN, Generate Email:**

```python
email_subject = "RFQ Intake – Request for Clarification"
email_body = f"Dear {buyer_name or 'Team'},\n\n"
email_body += "Thank you for your RFQ submission. We are conducting our internal review and would appreciate clarification on the following items to proceed:\n\n"

questions = []

if Government == "UNKNOWN":
    questions.append("• Who is the end user for these parts? (Government agency, commercial operator, or other?)")

if Missing_Contract and Government == "YES":
    questions.append("• What is the contract number or purchase order reference for this requirement?")

if Government == "YES" and not priority_rating_found:
    questions.append("• Does this requirement have a priority rating (DO-A1, DX, etc.)?")

if Missing_Condition:
    questions.append("• What condition codes are acceptable for these parts? (NE = New, OH = Overhauled, SV = Serviceable, AR = As Removed, NS = New Surplus)")

if Export_Control == "YES" and export_details_unclear:
    questions.append("• Are there specific export control requirements (ITAR registration, export license, end-use statements) we should be aware of?")

if Missing_Delivery:
    questions.append("• What is your required delivery date?")

if "no resale" in email_text or "direct installation" in email_text:
    questions.append("• Can you confirm this is for direct government/military installation and not for resale?")

if Missing_Parts:
    questions.append("• Could you please provide the specific part numbers required?")

if Missing_Qty:
    questions.append("• What quantities are needed for each part number?")

email_body += "\n".join(questions)
email_body += "\n\nOnce we receive your feedback, we will route and respond accordingly.\n\n"
email_body += "Best regards,\n[Sender Name]\nSource One Spares – RFQ Intake"
```

### PHASE 4: PIPELINE TITLE GENERATION

```python
if not Missing_Parts and not Missing_Qty:
    # Extract first 2 part numbers max
    part_nums = extracted_parts[:2]
    if len(extracted_parts) > 2:
        part_display = "Various"
    else:
        part_display = ", ".join(part_nums)
    
    # Extract aircraft if mentioned
    aircraft = extract_aircraft(email_text) or "Unk"
    
    # Format condition
    condition = extracted_condition or "Unk"
    
    # Extract customer info
    customer = extract_company_name(email_from) or "Unknown Customer"
    po_number = extracted_po or "TBD"
    
    # Generate description (2-4 words)
    if "overhaul" in email_text.lower():
        description = "overhaul request"
    elif "repair" in email_text.lower():
        description = "repair services"
    elif "purchase" in email_text.lower():
        description = "parts purchase"
    else:
        description = "parts inquiry"
    
    pipeline_title = f"External RFQ | PN: {part_display} | Qty: {quantities} | Customer/PO: {customer} {po_number} | {aircraft} | Condition: {condition} | {description}"
```

### PHASE 5: HIGHERGOV ENTRY

```python
highergov_entry = {
    "pursuit_type": "External Pursuit",
    "title": email_subject or f"RFQ from {customer}",
    "prime": "Source One Spares",
    "source": "External RFQ",
    "notes": f"""
End User: {Government or 'Unknown'}
Contract Ref: {extracted_contract or 'None identified'}
Priority: {priority_rating or 'None identified'}
Export Flags: {', '.join(export_flags) or 'None identified'}
Condition Required: {condition or 'Not specified'}
Government Indicators Found: {', '.join(gov_indicators) or 'None'}
    """
}
```

### PHASE 6: ROUTING DECISION

```python
if questions:  # Missing critical info
    route_to = "HOLD - Awaiting Customer Response"
    action = "Send clarification email"
elif Government == "YES" and Export_Control == "YES":
    route_to = "Compliance Team"
    action = "Review export requirements"
elif Government == "YES":
    route_to = "Government BD Team"
    action = "Process as government requirement"
elif condition == "NE" and no_government_indicators:
    route_to = "Commercial Sourcing"
    action = "Standard commercial quote"
else:
    route_to = "BD Team"
    action = "Evaluate and assign"
```

### COMPLETE OUTPUT STRUCTURE

```
=== EXTERNAL RFQ EVALUATION RESULTS ===

CLASSIFICATION: [Government / Commercial / Unknown]
EXPORT CONTROL: [Yes / No / Unknown]
ROUTING: [Team assignment]
ACTION: [Next step]

MISSING INFORMATION:
[List any missing fields]

PIPELINE TITLE:
[Generated title]

HIGHERGOV ENTRY:
[Formatted entry data]

CUSTOMER EMAIL:
[Complete generated email if needed, or "No clarification needed"]
```
---

# DOCUMENT 7: SOS CONTEXT SUMMARY

## Source One Spares (SOS) - Core Capabilities Reference

### Company Overview
- Houston-based aviation aftermarket distributor founded in 1997
- Specializes in airframe and engine components for commercial and government aircraft
- Headquarters: 12121 Winchester Lane, Suite 725, Houston, Texas 77079
- Warehouse: 4302 Buckingham Road, Fort Worth, Texas 76155
- UEI: RTP4E5UBJ3B7
- CAGE Code: 95QA6

### Key Contracts & Experience
- Two USAF KC-46 Aerial Tanker Program contracts totaling $2.37 billion over five years
- $1.89 billion USAF contract for initial spare parts on KC-46 fleets
- Active contract N0038325PT087 ($1.3M) with Naval Supply Systems Command

### Core Capabilities
- **Inventory:** New and refurbished parts for nearly every aircraft type in operation
- **Delivery:** "Just-in-time" (JIT) delivery model, 24/7 global support
- **Specialization:** FAA-certified refurbished and surplus parts, new aftermarket components
- **Traceability:** All components fully traceable and tagged by FAA-certified repair facilities
- **Support:** ITAR compliance for exports where required

### Certifications Held
- ASA Accreditation (FAA Advisory Circular 00-56)
- ISO 9001:2015 (Quality Management)
- AS9120B (Aerospace Distributor Requirements)
- FAA certifications

### Certifications NOT Held
- AS9100 (Manufacturing)
- NADCAP

### Parts Types Handled
- Common commercial items
- COTS (Commercial off-the-shelf)
- Surplus/excess inventory
- Rotable components
- Refurbished/overhauled parts
- New aftermarket parts

### Military Parts Types Handled Equivalents
- Reprables
- Line Replaceable Units (LRU)
- Shop Replaceable Units (SRU)
- Carcasses
- Piece parts
- Consumables

### Small Business Status
- Qualifies as Small Business under most NAICS codes

---

# END OF COMBINED DOCUMENTS

*This file contains 6 separate process documents for SOS opportunity assessment. Each document section operates independently while sharing common context and decision logic.*