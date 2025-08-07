# Source One Spares - Optimized Opportunity Assessment Framework

## CRITICAL BASELINE: SOS CAPABILITIES & CONSTRAINTS

### What SOS CAN Provide:
- FAA-certified refurbished/overhauled parts
- Surplus and used serviceable material (USM)
- Common commercial items
- COTS (Commercial Off-The-Shelf) parts
- New aftermarket parts (non-OEM)
- Parts with FAA Form 8130-3 certification
- Rotable components
- JIT (Just-In-Time) delivery
- 24/7 AOG support

### What SOS CANNOT Provide:
- Military Source Approval Required (SAR) items
- Manufacturing without government-owned technical data
- OEM-only restricted parts (unless via approved channels)
- Items requiring security clearances
- Brand new OEM parts (in most cases)
- Items with restricted/proprietary technical data

### SOS Certifications Held:
- ASA Accreditation (FAA AC 00-56)
- ISO 9001:2015
- AS9120B
- FAA-certified repair station network access

---

## SECTION 1: IMMEDIATE DISQUALIFIERS (Hard Stop Analysis)

**CRITICAL: These hard stops OVERRIDE ALL positive indicators. No exceptions.**

### 1.1 Source Approval Requirements (SAR)
**Search Terms:** "source approval", "approved source", "qualified products list", "QPL", "QML", "source qualification", "approved manufacturer", "military specification"

**Decision Logic:**
- IF contains "source approval required" AND military specification → **STOP: NO-GO**
- IF contains "FAA source approval" → **CONTINUE** (SOS can meet)
- IF no source approval mentioned → **CONTINUE**

**BD Strategy for Military SAR:**
When military SAR is present (always NO-GO), but parts have civilian equivalents:
- Track as "NO-GO - SAR Present (CO Contact Made)"
- Send message about future refurbished acceptability
- Only worth contacting if civilian parts availability exists

### 1.2 Sole Source Justification
**Search Terms:** "sole source", "only one responsible source", "brand name or equal", "single source", "proprietary", "exclusive", "intent to award"

**Decision Logic:**
- IF "sole source" to named vendor (not SOS) → **STOP: NO-GO**
- IF "brand name or equal" AND no SAR → **CONTINUE** (opportunity exists)
- IF "brand name or equal" AND SAR present → **STOP: NO-GO** (SAR wins)
- IF "intent to sole source" → **CONTINUE** (NOT a disqualifier - can be challenged)

### 1.3 Technical Data Restrictions
**Search Terms:** "technical data package", "TDP", "drawings", "proprietary data", "data rights", "government furnished", "GFI", "GFP", "technical data not available", "OEM owns data", "proprietary technical data"

**Decision Logic:**
- IF "drawings not available" → **STOP: NO-GO**
- IF "OEM owns technical data" → **STOP: NO-GO**
- IF "proprietary technical data" → **STOP: NO-GO**
- IF "government owns technical data" → **CONTINUE**
- IF "technical data available upon award" → **CONTINUE**
- IF repair/overhaul AND "FAA standards apply" → **CONTINUE**

### 1.4 Security Clearance Requirements
**Search Terms:** "security clearance", "secret", "top secret", "classified", "security requirements", "personnel clearance", "facility clearance"

**Decision Logic:**
- IF requires any security clearance → **STOP: NO-GO**
- IF "unclassified" explicitly stated → **CONTINUE**

### 1.5 New Parts Only Restriction
**Search Terms:** "factory new only", "new manufacture only", "no refurbished", "no rebuilt", "no overhauled", "no used"

**Decision Logic:**
- IF "factory new only" or equivalent → **STOP: NO-GO**
- IF "new or refurbished" → **CONTINUE**

---

## SECTION 2: OPPORTUNITY CLASSIFICATION

### 2.1 Acquisition Type Identification
**Search Terms:** "manufacture", "repair", "overhaul", "refurbish", "spare parts", "rotable", "consumable", "modification", "sustainment", "contractor logistics support"

**Classification Logic:**
- Contains "spare parts" + "delivery" → **Spares Supply** ✓
- Contains "repair" OR "overhaul" → **Managed Repair** ✓
- Contains "manufacture" + "government owns data" → **Manufacturing** (conditional)
- Contains "manufacture" WITHOUT data rights → **NO-GO**
- Contains "CLS" or "contractor logistics" → **Evaluate complexity**

### 2.2 Commercial vs Military Platform
**Search Terms:** 
- Commercial indicators: "FAR Part 12", "commercial item", "FAA certified", "14 CFR", "AC 00-56"
- Military indicators: "MIL-SPEC", "military standard", "MILSTD", "defense", "weapon system"
- Platform names: "Boeing 737", "KC-46", "C-130", "P-8", etc.
- Engine models: "CFM56", "PW4000", "CF6", "PT6", etc.

**Decision Logic:**
- IF FAR Part 12 mentioned → **STRONG POSITIVE** (commercial procedures)
- IF military platform WITH commercial equivalent → **EVALUATE** (may be viable)
- IF pure military platform with MIL-SPECs → **CAUTION** (check other factors)
- IF commercial engine model → **POSITIVE** (wide parts availability)
- IF fighter engine (F100, F119, etc.) → **NEGATIVE** (military only)

---

## SECTION 3: TECHNICAL ACCEPTABILITY MATRIX

### 3.1 Parts Acceptability
**Search Terms:** "new", "refurbished", "overhauled", "repaired", "surplus", "excess", "used", "serviceable", "condition code", "factory new"

**Scoring Matrix:**
| Requirement | SOS Capability | Score |
|------------|----------------|--------|
| "refurbished acceptable" | YES | +3 |
| "surplus acceptable" | YES | +3 |
| "used serviceable" | YES | +3 |
| "overhauled components" | YES | +3 |
| "new or refurbished" | YES | +2 |
| "factory new only" | LIMITED | -3 |
| "OEM new required" | NO | -5 |

### 3.2 Traceability Requirements
**Search Terms:** "traceability", "pedigree", "documentation", "8130-3", "certificate", "OEM trace", "chain of custody", "authorized distributor", "OEM distributor", "authorized dealer", "factory authorized"

**Decision Logic:**
- IF "FAA Form 8130-3" → **YES** (SOS provides)
- IF "full traceability required" + FAA → **YES**
- IF "OEM direct traceability only" → **NO-GO + CO Contact**
- IF "authorized distributor required" → **NO-GO + CO Contact**
- IF "OEM distributor only" → **NO-GO + CO Contact**
- IF "factory authorized dealer" → **NO-GO + CO Contact**
- IF "military traceability" + no commercial equivalent → **NO-GO**

**BD Strategy for OEM Distribution Restrictions:**
When OEM-only distribution requirements present (normally NO-GO):
- Track as "NO-GO - OEM Distributor Required (CO Contact Made)"
- Message: "We provide these commercial parts with full FAA 8130-3 traceability from aftermarket sources. If non-OEM sourcing becomes acceptable, we maintain extensive inventory."
- Same seed-planting strategy as SAR restrictions

### 3.3 Certification Requirements
**Search Terms:** "ISO", "AS9100", "AS9120", "NADCAP", "FAA", "repair station", "14 CFR Part 145"

**Capability Check:**
- ISO 9001 → **SOS HAS** ✓
- AS9120B → **SOS HAS** ✓
- FAA certifications → **SOS HAS** ✓
- AS9100 (manufacturing) → **SOS LACKS** ✗
- NADCAP → **SOS LACKS** ✗

---

## SECTION 4: DELIVERY & LOGISTICS EVALUATION

### 4.1 Delivery Timeline Analysis
**Search Terms:** "delivery", "ARO", "after receipt of order", "lead time", "urgent", "AOG", "expedited"

**Viability Scale:**
- 30+ days ARO → **EXCELLENT** (standard capability)
- 15-30 days → **GOOD** (achievable)
- 7-14 days → **EVALUATE** (depends on parts)
- <7 days → **CHALLENGING** (only for in-stock items)
- "AOG support" → **STRENGTH** (24/7 capability)

### 4.2 Geographic & Compliance Factors
**Search Terms:** "OCONUS", "overseas", "export", "ITAR", "import", "customs", "international"

**Assessment Logic:**
- Domestic US only → **OPTIMAL**
- ITAR compliance required → **CAPABLE** (with planning)
- Foreign military sales → **EVALUATE** case-by-case
- Restricted access areas → **CHECK** escort provisions

---

## SECTION 5: STRATEGIC OPPORTUNITY SCORING

### 5.1 Contract Value Indicators
**Search Terms:** "estimated value", "ceiling", "IDIQ", "maximum", "funded", "option years"

**Value Tiers:**
- Under $100K → Quick win potential
- $100K - $1M → Standard opportunity
- $1M - $10M → Strategic priority
- Over $10M → Executive review required

### 5.2 Competition Indicators
**Search Terms:** "incumbent", "previous awardee", "historical", "currently performed by"

**Competition Assessment:**
- No incumbent mentioned → **OPEN FIELD** (+2)
- Incumbent identified + recompete → **COMPETITIVE** (0)
- Strong incumbent language → **ENTRENCHED** (-2)

### 5.3 Small Business Preferences
**Search Terms:** "small business", "set-aside", "8(a)", "SDVOSB", "WOSB", "HUBZone", "socioeconomic"

**SOS Status:** Qualifies as Small Business under most NAICS codes

**Preference Hierarchy:**
- Total small business set-aside → **PREFERRED** ✓
- Partial set-aside → **OPPORTUNITY** ✓
- No set-aside + large business → **TEAM POTENTIAL**

---

## SECTION 7: DISAMBIGUATION RULES - HANDLING CONFLICTS & AMBIGUITY

### 7.1 Hierarchy of Decision Making
**When conflicting indicators exist, this hierarchy ALWAYS applies:**

1. **Hard Stops Win** - Any hard stop = NO-GO regardless of positive indicators
   - Example: "FAR Part 12 commercial item" + "source approval required" = **NO-GO**
   - Example: "Refurbished acceptable" + "military SAR" = **NO-GO**

2. **Worst Platform Rules** - In mixed platform solicitations
   - "C-130 and Boeing 737 parts" = Assess as **NO-GO** (C-130 drives decision)
   - Each platform assessed separately, worst case governs overall

3. **Treat Ambiguity as Restrictive**
   - "May require source approval" = Assume **YES, SAR required**
   - "Could include military items" = Assume **YES, military items**
   - "Potentially restricted data" = Assume **YES, restricted**

### 7.2 IDIQ Assessment Rules
**Base vs Ceiling Evaluation:**
- Base order <$100K but ceiling >$10M = **Still evaluate as strategic**
- Focus on ceiling value for GO/NO-GO decision
- Small base orders often just establish contract vehicle

### 7.3 "Or Equal" Language
**Only positive if no other restrictions:**
- "Brand name or equal" + No SAR = **Opportunity**
- "Brand name or equal" + SAR present = **NO-GO** (SAR wins)
- "OEM or equal" + OEM distributor required = **NO-GO**

### 7.4 Contractor Logistics Support (CLS)
**CLS typically means more than just parts:**
- Usually includes on-site support = Evaluate capability
- Often requires inventory management = Consider resources
- May need technical reps = Check personnel requirements
- Default assessment: **NEEDS FURTHER ANALYSIS**

### 7.5 Mixed Requirements
**When some items allow refurb, others require new:**
- "Refurbished acceptable except flight critical" = **NEEDS ANALYSIS**
- List which items SOS can provide vs cannot
- May pursue for partial award

### 7.6 Federal vs Commercial Entities
**Procurement rules follow the contracting agency:**
- Federal agency buying civilian aircraft = May still use federal rules
- State/local buying military aircraft = Usually civilian rules
- When unclear = Check solicitation for FAR vs state procurement code

---

## SECTION 8: SPECIAL OPPORTUNITY CATEGORIES

### 6.1 SLED Market (State/Local/Education) Opportunities
**Search Terms:** "state", "county", "city", "municipal", "school district", "university", "state agency"

**SLED Special Rules:**
- **ALL civilian aircraft parts → VIABLE** (no military restrictions)
- Less stringent source approval requirements
- Often more flexible on refurbished/surplus
- Shorter procurement cycles
- Lower competition from large primes

### 6.2 Dual-Use Parts Logic
**Search Terms:** "engine", "avionics", "hydraulic", "landing gear", "fuel system", "electrical"

**Decision Framework:**
- IF part used on BOTH military AND civilian variants → **PURSUE**
- IF engine component (CFM56, PW4000, etc.) → **LIKELY DUAL-USE**
- IF standard avionics/electrical → **CHECK CIVILIAN APPLICATIONS**
- IF structural component + commercial equivalent exists → **VIABLE**

**Examples of Dual-Use Winners:**
- 737 parts used on P-8 Poseidon
- 767 parts used on KC-46 Pegasus
- Common engines across military/civilian fleets
- Standard hydraulic/pneumatic components

---

## SECTION 9: TEAMING & PARTNERSHIP DECISION MATRIX

### 7.1 Prime vs Subcontractor Decision Tree

**When to Pursue as PRIME:**
- Total contract value <$5M
- SOS can fulfill 75%+ of requirements
- No complex integration required
- Standard commercial items/parts
- Direct relationship with end user desired

**When to Pursue as SUBCONTRACTOR:**
- Large IDIQ or enterprise contracts
- Complex systems integration required
- Prime has complementary capabilities
- Risk mitigation needed
- Past performance gaps

**When to PARTNER/TEAM:**
- Geographic coverage needed
- Specialized certifications required (AS9100, NADCAP)
- Volume exceeds SOS capacity
- Strategic market entry

### 7.2 Identifying Potential Primes
**Search Terms:** "incumbent", "current contractor", "previous awardee", "awarded to"

**Partner Identification Strategy:**
1. Check previous award history in solicitation
2. Search SAM.gov for recent similar awards
3. Target primes who won but may need suppliers:
   - Large defense contractors for parts supply
   - MRO providers for surge capacity
   - Systems integrators for components

---

## SECTION 8: PAST PERFORMANCE & QUALIFICATIONS

### 8.1 Past Performance Requirements Analysis
**Search Terms:** "past performance", "relevant experience", "similar contracts", "CPARS", "references"

**SOS Past Performance Strategy:**
- **Direct Experience:** KC-46 contracts ($2.37B) for similar size/scope
- **Relevant Experience:** 27+ years aviation aftermarket
- **Subcontractor Experience:** Counts if properly documented
- **Commercial Experience:** Often acceptable for government work

**When Past Performance May Block:**
- Requires 3+ identical contracts → **EVALUATE CAREFULLY**
- Specific agency experience required → **CHECK SUBS**
- Classified contract experience → **NO-GO**

### 8.2 Financial Capability Indicators
**Search Terms:** "bonding", "financial capability", "payment bond", "performance bond", "line of credit"

**Thresholds:**
- Bonding <$500K → **MANAGEABLE**
- Bonding $500K-$2M → **EVALUATE WITH CFO**
- Bonding >$2M → **STRATEGIC DECISION**
- No bonding mentioned → **POSITIVE INDICATOR**

---

## SECTION 9: AIRCRAFT PLATFORM QUICK REFERENCE

### 9.1 Military-to-Commercial Equivalents
| Military Platform | Commercial Equivalent | Parts Commonality |
|------------------|----------------------|-------------------|
| KC-46 Pegasus | Boeing 767 | ~85% common |
| P-8 Poseidon | Boeing 737 | ~80% common |
| C-40 Clipper | Boeing 737 | ~90% common |
| C-32 | Boeing 757 | ~85% common |
| VC-25 (Air Force One) | Boeing 747 | ~75% common |
| E-3 Sentry (AWACS) | Boeing 707 | ~70% common |
| E-6 Mercury | Boeing 707 | ~70% common |
| C-12 Huron | Beechcraft King Air | ~95% common |

### 9.2 Engine Cross-Reference
| Engine Model | Military Applications | Commercial Applications |
|--------------|---------------------|------------------------|
| CFM56 | KC-135R, E-3, E-6 | Boeing 737, A320 |
| F117 (CF6) | C-5M Super Galaxy | Boeing 767, 747 |
| PW4000 | KC-46, C-17 | Boeing 777, A330 |
| T56/501D | C-130, P-3 | L-100 (civilian C-130) |

---

## SECTION 12: DECISION LOGIC FLOWCHART

```
START ASSESSMENT
    ↓
[Check Section 1: ALL Hard Stops]
    ├─ ANY hard stop found? → STOP: NO-GO
    │   └─ If parts available in civilian market → CO CONTACT
    └─ All clear? → CONTINUE
         ↓
[Apply Disambiguation Rules if Conflicts]
    ├─ Conflicting signals? → HARD STOPS WIN
    └─ Continue
         ↓
[Is this SLED opportunity?]
    ├─ YES → ENHANCED VIABILITY (skip military restrictions)
    └─ NO → CONTINUE STANDARD PATH
         ↓
[Check Dual-Use Parts?]
    ├─ YES → BONUS POINTS (+5)
    └─ NO → CONTINUE
         ↓
[Score Section 3: Technical Fit]
    ├─ Score < -5? → STOP: TECHNICAL MISMATCH
    └─ Score ≥ 0? → CONTINUE
         ↓
[Evaluate IDIQ Ceiling vs Base]
    ├─ High ceiling value? → WEIGHT ACCORDINGLY
    └─ Continue
         ↓
[Calculate Composite Score]
    └─ Apply thresholds:
         ├─ 80%+ → PURSUE AGGRESSIVELY
         ├─ 60-79% → PURSUE WITH CAUTION
         ├─ 40-59% → EVALUATE PARTNERSHIP
         └─ <40% → DECLINE OR MONITOR
              ↓
[If 40-79%: Check Teaming Options]
    ├─ Strong prime available? → PURSUE AS SUB
    ├─ Gaps fillable by partner? → CREATE TEAM
    └─ No viable options? → DECLINE
```

---

## SECTION 13: NOTEBOOKLM EXTRACTION PRIORITIES

### Primary Extraction Targets:
1. **Announcement Number** - First page, top section
2. **NAICS/PSC Codes** - Usually in overview or Section B
3. **Set-aside Status** - Block 10 of SF1449 or synopsis
4. **Technical Requirements** - Section C (Statement of Work)
5. **Evaluation Criteria** - Section M
6. **Key Dates** - Section L or cover page

### Critical Phrases to Flag:
- ❌ "Source approval required"
- ❌ "Drawings not available"
- ❌ "Factory new only"
- ❌ "Security clearance required"
- ✓ "Commercial item acquisition"
- ✓ "FAR Part 12"
- ✓ "Refurbished acceptable"
- ✓ "Or equal"

### Inference Rules for Ambiguous Language:
1. **Default to restrictive interpretation** - "May require" = "Does require"
2. If "spare parts" + military aircraft → Check for hard stops first
3. If FAA mentioned + military platform → Still check SAR requirements
4. If "common use item" → Positive ONLY if no SAR
5. If export mentioned + no ITAR → Flag for clarification
6. **Never assume** - If unclear, mark NEEDS FURTHER ANALYSIS
7. **Hard stops override everything** - No positive indicator matters if hard stop present

---

## FINAL ASSESSMENT OUTPUT TEMPLATE

**Opportunity:** [Announcement Number]
**Recommendation:** GO / NO-GO / NEEDS ANALYSIS / PURSUE AS SUB
**Confidence Level:** HIGH / MEDIUM / LOW
**Pursuit Strategy:** PRIME / SUBCONTRACTOR / TEAM LEAD / TEAM MEMBER

**Rationale:**
- Hard Stops Cleared: YES/NO (list any failures)
- Technical Alignment: [Score]
- Commercial Indicators: [Count]
- SLED Opportunity: YES/NO
- Dual-Use Parts: YES/NO
- Risk Factors: [List]
- Teaming Options: [If applicable]
- Next Actions: [Specific steps]

**One-Line Justification:** [For pipeline entry]

**Quick Reference Flags:**
- 🟢 FAR Part 12 Commercial
- 🟢 Refurbished Acceptable  
- 🟢 Dual-Use Parts
- 🟢 SLED Market
- 🟡 Intent to Award (can challenge)
- 🟡 Teaming Opportunity
- 🔴 Military SAR Required
- 🔴 Security Clearance Needed