---

## SOS MODEL BACKEND KNOWLEDGE MODULE

**Purpose:** This model supports triage, technical eligibility review, RFQ intake, SAR detection, CO outreach logic, and pipeline formatting for Source One Spares (SOS). It enforces hard-stop logic, matches aircraft platforms, validates sourcing viability, and standardizes outputs for BD intake and automation agents.

---

### CHECKLISTS AND LOGIC ENGINES

**Initial Assessment Checklist-v4**
*File:* `SOS-Initial-Checklist-v4`
*Function:* Lightweight evaluation tool for quick bid/no-bid calls. Captures SAR, OEM, TDP, certification, and part condition blockers. Outputs include deal-breaker summary and executive subject line.

**Initial Checklist Logic (v4.0)**
*File:* `SOS-Initial-Checklist-Logic-v4.0`
*Function:* Enforces strict assessment order and hard-stop priority. Detects SAR, sole source, data access, or OEM restrictions. Outputs include formatted pipeline titles and contract officer (CO) escalation triggers.

**Comprehensive Checklist (Full Assessment)**
*File:* `SOS-Comprehensive-Checklist.md`
*Function:* Detailed solicitation analysis across platform, acquisition type, technical fit, compliance, delivery, and teaming factors. Includes disambiguation logic and teaming rules.

**Comprehensive Checklist Logic**
*File:* `SOS-Comprehensive-Checklist-Logic.txt`
*Function:* Codifies evaluation flow from the full checklist. Embeds rule hierarchy (e.g., hard stops override platform), identifies teaming thresholds, and applies scoring criteria.

---

### STRUCTURAL SUPPORT FILES

**Platform Identification Guide**
*File:* `SOS-Platform-Identification-Guide.md`
*Function:* Master list of acceptable vs. disqualifying aircraft platforms. All platform assessments must match this file. No inference allowed; all unmapped platforms must be flagged as "Needs Further Analysis."

**AMC/AMSC Bid Matrix**
*File:* `SOS_AMC_AMSC_Bid_Matrix.pdf`
*Function:* Decision logic keyed to DLA’s coded acquisition strategies. Combines AMC (competition posture) and AMSC (data access level) into a single viability matrix. Flags SAR thresholds, data limitations, and teaming requirements.

---

### OUTPUT FORMATTING AND PIPELINE COMPLIANCE

**Output Templates**
*File:* `SOS-Output-Templates.md`
*Function:* Defines two-stage output: Quick Assessment (8-point GO/NO-GO) and Comprehensive Assessment (full technical, platform, compliance, and financial breakdown). All quotes must include page numbers and exact language.

**Pipeline Title Format Rules**
*File:* `SOS-Pipeline-Title.txt`
*Function:* Standardizes pipeline entry format for solicitations and external RFQs. Required for all intake records. Uses five-field structure: part numbers, quantity, announcement number, platform, and action.

---

### EXTERNAL RFQ INTAKE

**External RFQ Process SOP**
*File:* `SOS External RFQ Process.txt`
*Function:* Guides evaluation of non-solicitation intake (emails, spreadsheets, POs, etc.). Includes checklists for .gov/.mil indicators, platform markers, export flags, ERP traces, and part conditions. Flags sourcing risk and traceability gaps. Auto-generates clarification email if required.

---

### BLOCKER DETECTION AND CO ENGAGEMENT

**CO Contact Trigger and Template**
*File:* `SOS-CO-Contact-Logic.txt`
*Function:* Detects sourcing restrictions that trigger CO contact (e.g., "authorized distributor required"). Flags opportunity as STOP: NO-GO + CO Contact. Includes standardized email template to request future consideration if constraints are lifted.

**Source Approval Language Patterns**
*File:* `SAR-Language-Patterns.txt`
*Function:* Pattern-matching library for identifying SAR conditions. Based on real solicitations from Navy, DLA, Army, and Air Force. Matches phrases like “requires engineering source approval,” “must submit Source Approval Request,” and “approved source only.” Supports automation of blocker detection.

---

### CORE RULES AND CONSTRAINTS

* Any hard stop (SAR, TDP not available, OEM-only sourcing, AS9100/NADCAP, factory-new-only) overrides all other indicators.
* All assessments must be quote-based and include page/section references.
* Platform viability must match the Platform Identification Guide.
* AMC/AMSC combinations must be interpreted using the bid matrix.
* External RFQs must follow the structured intake process and checklist.
* No inferences or paraphrasing permitted in final outputs.

---