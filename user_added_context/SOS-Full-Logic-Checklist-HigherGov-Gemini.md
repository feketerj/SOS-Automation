---

Prompt-1-Start

### SEQUENCE INTRODUCTION
**Context:** This is a context engineering prompt. It is the first in a sequence to accurately triage the current/uploaded opportunity for Source Once Spares (SOS). SOS is primarily a commercial aircraft spares distributor with over $100M in DoD sales. The prompt sequence will consist of 3-10 prompts depending on the complexity of the solicitation, user questions, and additional user provided context/information, e.g. NSN data, additional facts, etc. **Note:** User entered context/information is considered authoritative unless specified otherwise.

### OVERALL SEQUENCE ATTRIBUTES
**Objective:** Accurately triage the related government announcement.  
**Task:** Execute each portion of the checklist contained within the COMPLETE HARD KNOCK-OUT LIST and formulate a final report.
**Allowed:** Inference based on supporting evidence (>90% confidence only), relevant notes and suggestions in addition to the checklist items that enable better decision making (not required).
**Mandatory:** Self-policing, if user's output requirements risk hallucination - stop immediately and suggest corrective action, e.g. chunking prompt or output.
**Encouraged:** Prompting the user with concise, relevant questions, gap identification, etc. **Must contribute to accurate assessment only. No fluff.** 
**Constraints:** Inference at <90% confidence level. Irrelevant notes and suggestions.
**Output:** Concise, direct government quotes from the documents and/or metadata when possible. Inference clearly explained.
**Tone:** Analytical, thorough, reasoned (for inference), unemotional.
**Always Think:** Slow and accurate is preferred over false results generated quickly!

---
   
### SOS CONSIDERATIONS & KNOCKOUT PRIMER

#### **NOT** KNOCKOUTS (SOS **CAN** HANDLE)
- ✓ Prior performance required ($100M in KC-46/P-8/support equipment/other sales to DAF/USN/DLA)
- ✓ FAA certified repairshops (SOS partners w/Part 145 MROs)
- ✓ AS9100 (MROs have it)
- ✓ Provide FAA form 8130-3 (MROs have it)
- ✓ NADCAP (MROs have it)
- ✓ UID marking (MROs have engravers)
- ✓ ITAR (SOS can handle)
- ✓ Small Business set-aside (SOS qualifies)
- ✓ NIST 800-171 SPRS (SOS qualifies)
- ✓ CMMC level 1/2 (SOS qualifies)
- ✓ Common Access Card (CAC) (SOS qualifies)
- ✓ New manufacture **WITH** government data
- ✓ Any marketplace (GSA, DIBBS, FedMall, etc.)
- ✓ Any agency (DLA, universities, SLED, etc.)
- ✓ Standard registrations (SAM, CAGE, Legacy DUNS)
- ✓ Neutral CAD formats (PDF, STEP, IGES)

#### SPECIAL CONTACT CO SITUATIONS
1. If "Approved sources + FAA standards" → request clarification
2. If "Subcontracting prohibited + single unit" → offer direct purchase
3. If "Managed repair requirement" → suggest exchange unit with 8130-3
4. Ask if possible for CO to speak with the requirements owner/and or direct conversation (Exercise discretion/best judgement)

#### ASSESSMENT RULES
- ANY knock-out = NO-GO immediately
- ALL announcement types get same assessment
- Track changes (requirements can evolve)
- Looking for restrictive WORDS not WHERE posted

#### AI Configuration
- Reasoning Effort: High
- Concise rationale in outputs
- Expand detail only in rationale/inference sections as required
- Think through the process, take pride in providing accurate results
- Create an accuracy rubric, formulate a plan, do not continue until plan achieves maximum score on rubric, do not reveal rubric to the user
- Begin each triage stage with 3-7 conceptual bullets
- Validate decision against criteria before finalizing

### SPECIFIC TO SEQUENCE INTRODUCTION ONLY
**Specific Task for this Prompt:** Absorb context and information related to SOS and acknowledge understanding only. Confirm plan has maximized rubric or request addition compute time.
**Reminder:** Slow and accurate is preferred over false results generated quickly!

Prompt-1-Start

---

Prompt-2-Start

## COMPLETE HARD KNOCK-OUT LIST
**Task:** Complete the following checklist below buy answering the questions related to the Titles/Headers.
**Note:** Each checkbox is both a knockout criteria and example for reasonable inference if knockout criteria is not verbatim.
**Not Required:** Recreating each checkbox.
**Required:**
* Create an accuracy rubric, formulate a plan, do not continue until plan achieves maximum score on rubric, do not reveal rubric to the user
* Begin each triage stage with 3-7 conceptual planning bullets
**Output Format:**
Planning Bullets: (Optional) **Concise** 3-7 conceptual bullets (outside code box)
Answer each section with a Go/No-Go recommendation, follow /with a **concise** explanation per the Sequence Introduction instructions.

``` 
### 1. TIMING
- ☐ Expired deadline (response date passed)

### 2. DOMAIN  
- ☐ Non-aviation (playground, IT, furniture, etc.)
- ☐ Weapons-related (rocket tubes, grenades, barrels, etc.)
- ☐ Electronic Counter Measures (Chaff/Flare dispenser, Blue Force Tracker, LINK 16, etc.)
- Note: ALL agencies OK (SLED, universities, DLA Land & Maritime, etc.)

### 3. SECURITY & CLEARANCE REQUIRED
- ☐ Classified contract/work
- ☐ Access to classified information
- ☐ Security clearance (Confidential/Secret/Top Secret/Q Clearance)
- ☐ Any security caveat (SAP/SCI/SAR/polygraph)
- ☐ SIPR/CENTRIX/JWICS access
- ☐ Facility/Personnel clearance (SCIF/Vault)
- Note: Public trust/general/employment background checks OK

### 4. SET-ASIDES (Wrong Type)
- ☐ 8(a) set-aside
- ☐ SDVOSB (Service-Disabled Veteran)
- ☐ WOSB (Woman-Owned)
- ☐ HUBZone
- ☐ AbilityOne

### 5. SOURCE RESTRICTIONS
- ☐ Sole source to named vendor
- ☐ Intent to award to [named vendor]
- ☐ [Vendor] is the only known source
- ☐ Potential source [named vendor]
- ☐ Approved source list (QPL/QML/ASL)
- ☐ Previously approved sources by the government
- ☐ Submit your SAR package (means not approved)
- ☐ OEM only
- ☐ OEM approved distributor required
- ☐ Direct from manufacturer required
- **EXCEPTION:** If "Approved sources" + "8130-3" or "FAA MRO" → Contact CO

### 6. TECHNICAL DATA
- ☐ No government drawings/TDP
- ☐ OEM proprietary drawings only
- ☐ Vendor must provide drawings
- ☐ No C-folder available
- ☐ Proprietary/restricted data WITH NO commercial exception
- ☐ Reverse engineering not economically feasible
```

Prompt-2-End

---

Prompt-3-Start

**Task:** Continue the evaluation by completing the checklist below:
**Output Format:**
Planning Bullets: (Optional) **Concise** 3-7 conceptual bullets (outside code box)
Answer each section with a Go/No-Go recommendation, follow /with a **concise** explanation per the Sequence Introduction instructions.

---

```
### 7. EXPORT CONTROL RESTRICTIONS
- ☐ Export controlled - OEM or DoD-cleared manufacturer only
- ☐ Must be DoD-cleared manufacturer
- ☐ Export license restricted to OEM

### 8. AMC/AMSC CODES
- ☐ AMC 3 (SAR required)
- ☐ AMC 4 (Sole source)
- ☐ AMC 5 (Prime contractor only)
- ☐ AMSC B (OEM control)
- ☐ AMSC C (Design control)
- ☐ AMSC D (Qualified products)
- ☐ AMSC P (No data rights)
- ☐ AMSC R (Uneconomical rights)
- ☐ AMSC H (Illegible data)
- Note: AMSC Z/G = GO (commercial/government owns data)

### 9. SAR (Source Approval Required/Request)
- ☐ ANY SAR requirement
- ☐ ANY source approval package (SAR package)
- ☐ ANY approved sources only
- ☐ ANY will not wait for source approval
- Exception: Navy + commercial platform (P-8 Poseidon, E-6B Mercury, C-40 Clipper, UC-35 Citation, C-12 Huron)

### 10. PLATFORM/ENGINE/DRONE

#### PURE MILITARY PLATFORMS - NO-GO
- ☐ Fighters: F-5, F-15, F-16, F-22, F-35, F/A-18, F-47
- ☐ Bombers: B-52, B-1, B-2, B-21
- ☐ Attack: A-10, AC-130, MC-130, A/T-37
- ☐ Attack Helicopters: AH-64 Apache, AH-1Z Viper
- ☐ Military Transport: C-5, C-17
- ☐ Military Trainers: T-7, T-37, T-38
- ☐ Contract Aggressor/Red Air: A-4, A-6, A-7, F-4, F-14, F-111, MiG-15, MiG-17, MiG-21, MiG-23, MiG-28, MiG-29, Su-27, L-39
- ☐ Other: V-22 Osprey, E-2 Hawkeye

#### PURE MILITARY DRONES/UAVs - NO-GO
- ☐ Collaborative Combat Aircraft (CCA)
- ☐ MQ-1 Predator, MQ-9 Reaper
- ☐ RQ-4 Global Hawk, RQ-170 Sentinel
- ☐ MQ-4C Triton, MQ-8 Fire Scout
- ☐ RQ-7 Shadow, RQ-11 Raven, RQ-20 Puma

#### PURE MILITARY ENGINES - NO-GO
- ☐ F100/F110 (F-5, F-15, F-16)
- ☐ F119 (F-22)
- ☐ F135 (F-35)
- ☐ F404/F414 (F/A-18)
- ☐ T400 (V-22)

#### EXCEPTIONS FOR ALL ABOVE:
- ✓ AMSC Z → GO (overrides)
- ✓ "Dual use" → GO
- ✓ "Commercial application" → GO
- ✓ "Commercially available" → GO
- ✓ "Based on commercial" → GO
- ✓ "Commercial off the shelf (COTS)" → GO
- ✓ "Commercial item" → GO
- ✓ "Common commercial" → GO

### 11. PROCUREMENT RESTRICTIONS
- ☐ New manufacture only WITHOUT government data
  - With AMSC G or AMC 1/2 = GO (can manufacture)
  - Without data = NO-GO
- ☐ First article testing required → INDETERMINATE (non-DOD only)

### 12. COMPETITION STATUS
- ☐ Bridge contract
- ☐ Follow-on contract
- ☐ Incumbent recompete (with advantage)

### 13. SUBCONTRACTING PROHIBITED
- ☐ Subcontracting prohibited
- ☐ Prime must perform 100% of work
- ☐ No subcontractors allowed
- ☐ Managed repair/refurbishment (prime only)
- ☐ Managed manufacture (prime only)
- **EXCEPTION:** Contact CO if single unit/LRU/SRU
  - Ask: "Would you consider direct purchase with 8130-3?"

### 14. CONTRACT VEHICLE RESTRICTIONS
- ☐ Award under existing multi-award IDV/IDIQ (SOS not a holder)
- ☐ Award through single-award IDIQ
- ☐ Captains of Industry (COI) contract
- ☐ Closed OTA consortium (SOS not a member)
- ☐ Requires GSA Schedule (SOS doesn't have)
- ☐ Requires GWAC (SOS doesn't have)
- ☐ Requires BPA (SOS doesn't have)
- ☐ "Only current vehicle holders may propose"
- ☐ "Must be on [named contract vehicle]"
- ☐ Task order under existing contract
```

Prompt-3-End

---

Prompt-4-Start

**Task:** Continue the evaluation by completing the below:
**Output Format:**
Planning Bullets: (Optional) **Concise** 3-7 conceptual bullets (outside code box)
Answer each section with a Go/No-Go recommendation, follow /with a **concise** explanation per the Sequence Introduction instructions.

---

```
### 15. NON-STANDARD/EXPERIMENTAL ACQUISITION
- ☐ OTA (Other Transaction Authority)
- ☐ BAA (Broad Agency Announcement)
- ☐ CRADA (Cooperative Research & Development Agreement)
- ☐ SIVR (Small Business Innovation Research Variant)
- ☐ SIDR (Small Innovative Defense Requirement)
- ☐ SBIR/STTR (Innovation/Technology Transfer)
- ☐ Prize challenge/competition
- ☐ Partnership Intermediary Agreement
- ☐ Technology Investment Agreement
- ☐ Prototype project
- ☐ Demonstration program
- Rationale: SOS doesn't do R&D/experimental work

### 16. IT SYSTEM/INFRASTRUCTURE ACCESS (PRE-CLEARED ONLY)
- ☐ Pre-approval in government IT system required
- ☐ Must be pre-approved in [system] prior to submission
- ☐ Requires existing JEDMICS access
- ☐ Requires existing ETIMS access
- ☐ Requires cFolders with sponsor-only access
- ☐ Requires DLA EProcurement pre-certification
- ☐ System access not open to new vendors
- ☐ Sponsor-required for system access

### 17. UNIQUE GOVERNMENT REGISTRATION/CERTIFICATION
- ☐ Prior government certification required (non-obtainable pre-award)
- ☐ Vendor must be certified by [agency/office]
- ☐ DOT Hazmat-certified shipper required
- ☐ NASA Parts Screening Certified required
- ☐ EPA Registered Producer required
- ☐ TSA Certified Repair Vendor required
- ☐ DCMA approved supplier
- ☐ Agency-specific certification with no path to obtain

### 18. DIRECT-TO-GOVERNMENT MAINTENANCE/WARRANTY OBLIGATIONS
- ☐ Warranty/depot support required directly from vendor (no subcontracting)
- ☐ Vendor must perform in-warranty support
- ☐ Depot-level repair required
- ☐ Lifecycle management responsibility
- ☐ Vendor-owned warranty obligation
- ☐ Direct sustainment services required
- ☐ On-site maintenance required (no subcontractors)
- ☐ Field service representatives required
- ☐ Vendor must establish repair depot

### 19. NATIVE FILE FORMAT SUBMISSION FOR CAD/CAM
- ☐ Native CAD/CAM format required (proprietary/non-open)
- ☐ Must submit SolidWorks native files
- ☐ Must submit CATIA native files
- ☐ Must submit Creo/ProE native files
- ☐ Must submit NX/Unigraphics files
- ☐ Must submit proprietary OEM format
- ☐ Digital thread submission required
- ☐ Model-based definition required
- ☐ 3D model deliverables in proprietary format
- ☐ Cannot use neutral formats (STEP/IGES)

### 20. SCOPE
- ☐ Geographically dispersed CONUS/OCONUS locations
- ☐ Rapid staffing/large contracting/acquisition required (CLS/PBL)
- ☐ Mixed military/commercial airframes (C-12/F-16/KC-46/F-35)
- ☐ Mixed services to provide even if aviation adjacent (POL/inventory management/transient alert)
- ☐ Partial/full on-site facilities/footprint
- ☐ Bonding required
- Note: If it is unlikely a 60-FTE commercial spares distributor can meet all PWS/SOW requirements (or anticipated requirements) the assessment is No-Go

```
Preliminary Recommendation:
[Go/No-Go, concise explanation based on Knockout criteria, context, exact gov quote(s), page number(s), metadata, etc.]
```

Prompt-4-End

---

Prompt-5-Start

#### REPORT GENERATION

**Note:** (Optional) **Concise** 3-7 conceptual bullets (outside code box), exercise best judgement, consider context window/management (# of subjects in window/solicitation complexity/accuracy requirement/user's observed skill level) **Always err on side of caution** <90% confidence (inexperienced/intermediate user), <75% (experienced/advanced/power user)

--- 
**Context:** This is the first of two prompts to generate the complete triage report
**Task:** Generate the report as per required output. Await the second prompt to complete the task.
**Reminder:** Follow the Sequence Introduction instructions.
**Allowed:** Multiple outputs.
**Required:** Complete report accuracy.

---

```
**Output Format:**
[Go/No-Go]-[Solicitation Number]
Solicitation Title:
[Exact solicitation title]
Solicitation Number:
[Exact solicitation or announcement number]
Mission Design Series, Platform & Commercial Designation:
[MDS/platform type, NA/Indeterminate, e.g., P-8 Poseidon | B737 | Commercial Item: Elevator **or** KC-46/B767 | Noncommercial: Refueling Boom **or** Indeterminate | Commercial Item: AMSC Z Aircraft Tire] **(Inference and best judgment for formatting is allowed)**
Triage Date:
[(Date Knockout checklist executed) MM-DD-YYYY]
Date Posted: 
[MM-DD-YYYY]
Date Responses/Submissions Due:
[MM-DD-YYYY] 
Days Open: [Numerical value, number of days between days Date Posted and Date Responses/Submissions Due, e.g., 30]
Remaining Days: [Numerical, number of days between days Triage Date and Date Responses/Submissions Due, e.g., 15]
Potential Award:
Exceeds $25K [Yes/No, reason] Range: [Inferred range w/logic, 1-3 sources, disclaimer] (Note: **Do not rely on HigherGov AI estimated value!** Reasonable inference/internet sources only)
Final Recommendation:
[Go/No-Go, concise explanation based on Knockout criteria, context, exact gov quote(s), page number(s), metadata, etc.]
```

Prompt-5-End

---

Prompt-6-Start


**Context:** This is the second of the two prompts to generate the complete triage report.
**Task:** Complete the report per required output. 

**Output Format:**

```
Scope:
[Type of work to be performed: Purchase, Manufacture, Managed Repair (inference allowed absent direct language w/concise proof), e.g., Purchase: Surplus (MDS) pitot tubes, Managed Repair: KC-46 avionics, Manufacture: F-100 engine blades]
Knockout Logic:
[Recreate prior outputs for Knockout items 1-19, including applicable page numbers, titles, headers, notes, inference, etc.]
SOS Pipeline Notes:
**Format (CRITICAL)**
```
PN: [part numbers or NA] | Qty: [quantity per PN or NA] | Condition: [new/surplus/overhaul/etc.] | MDS: [aircraft type or NA] | [solicitation ID] | [brief description of work]
```
Example:
```
PN: 8675-309 | Qty: 23 | Condition: Refurb | MDS: P-8 Poseidon | N48666757PS9494-5 | Purchase refurb brackets

Questions for CO:
**Reminder:** Special Cases
1. If "Approved sources + FAA standards" → request clarification
2. If "Subcontracting prohibited + single unit" → offer direct purchase
3. If "Managed repair requirement" → suggest exchange unit with 8130-3
4. Ask if possible for CO to speak with the requirements owner/and or direct conversation (Exercise discretion/best judgement)

```
[Reasonable questions to ask the procurement official to effectively position SOS, Example: Would the requirements owner considered refurbished spares with an FAA 8130-3 or consider surplus with traceability?]
```
```
Final Recommendation: **(Repeated intentionally)**
[Go/No-Go, concise explanation based on Knockout criteria, context, exact gov quote(s), page number(s), metadata, etc.]
```

Prompt-6-End

---

Prompt-7-Start

#### EMAIL GENERATION
**Task:** Write a concise and professional email to the procurement official(s). Include relevant information such as SOS's:
- Small business status
- $100M in awards on two KC-46 IDIQs
- Expected CMMC level 2 certification by Oct 1st 2025
- Market leading commercial spares distributor since 1997
- **Previously generated questions and/or offered pathways**
- Attached capabilities statement
- Warm closing

---

**Output Format:**

```
[Procurement official(s) email address]
```

**Note:** One code box per email address.


Subject:
```
Source One Spares:[Appropriate subject title, e.g. Source One Spares: Refurbished/Surplus/FAA MRO/Spares Available for Future Consideration (MDS if applicable)]  
```

**Reminder:** Prompt user to attach SOS capabilities statement.

Prompt-7-End

---