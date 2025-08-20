# Federal and SLED contracting language detection patterns

This comprehensive research identifies exact language patterns from federal and SLED contracting databases for automated detection and classification systems, organized into 11 categories with implementation-ready patterns for Python and regex matching.

## Source Approval Required (SAR) language variants

The federal government uses highly standardized SAR terminology across agencies. **"Source approval required"** appears as the primary pattern, with exact regulatory language stating "source approval is required prior to procurement" in DoD and NASA contracts. The Qualified Products List (QPL) and Qualified Manufacturers List (QML) represent formal pre-approval mechanisms, appearing as "products must appear on the current QPL/QML" in procurement documents.

Key SAR detection patterns include: "source approval required from [AGENCY] prior to bid submission", "contractors must obtain source approval for all [ITEM TYPE]", "only approved sources will be considered", "source qualification required", and "pre-approved vendor list". These patterns maintain consistency across federal agencies, with variations primarily in the agency name field.

For regex implementation, the comprehensive pattern captures all variants:
```regex
(?i)(source\s+approval\s+required|approved\s+sources?\s+list|qualified\s+products?\s+list|QPL|qualified\s+manufacturers?\s+list|QML|source\s+qualification\s+required)
```

## Sole source justification patterns

Federal sole source patterns center on FAR 6.302 statutory authorities, with **"only one responsible source"** as the most frequent phrase directly from FAR 6.302-1. The complete regulatory phrase "no other supplies or services will satisfy agency requirements" appears in formal justifications, while "sole source" serves as the general procurement term across informal communications.

Capability-based justifications use specific language: "unique capabilities" (FAR 6.302-1(b)(1)(i)), "unique supplies or services available from only one source", and "services not otherwise available to the Government". Intellectual property justifications invoke "patent rights", "proprietary technology", "exclusive licensing agreement", "limited rights in data", "copyrights", or "control of basic raw material".

The FAR provides seven distinct statutory authorities (6.302-1 through 6.302-7), each with unique triggering language. FAR 6.302-2 uses "unusual and compelling urgency" where "delay in award would result in serious injury". FAR 6.302-3 covers "industrial mobilization" and "expert or neutral person" for litigation support. FAR 6.302-4 addresses "international agreement" requirements, while 6.302-5 covers procurements "authorized or required by statute".

Brand name specifications under FAR 6.302-1(c) use "brand name or equal", "brand-name product", or "item peculiar to one manufacturer". J&A documents include standardized components: "Justification and Approval", "Other than Full and Open Competition", "Statutory Authority Permitting Other Than Full and Open Competition", and certification language stating "I certify that the facts and representations under my cognizance".

## Intent to award notification patterns

Federal notifications follow FAR Part 5 standards with **"Notice of Intent to Award"** as the primary pattern on SAM.gov. Pre-solicitation uses "presolicitation notice" (FAR 5.204), "special notice" (FAR 5.205(c)), and "sources sought" for market research. "Request for information" or "RFI" indicates pricing estimates and technical recommendations are being gathered.

Timing language demonstrates precise regulatory requirements: "14 calendar days" for GAO protest reporting, "10 calendar days" for bid protest filing deadlines, "30 days prior" for solicitations exceeding simplified acquisition threshold (FAR 5.203(c)), "15 days before issuance" for notice publication (FAR 5.203(a)), and "40 days" for WTO Government Procurement Agreement compliance.

Protest period language includes "protest period", "file a protest", "10 days of when a protester knows or should know of the basis" (GAO standard), "Days are calendar days" (GAO clarification), and "actual or constructive knowledge" as the trigger for timing. State variations include New York's "Intent to Award Notification" and California's "Award Notifications", showing regional terminology differences.

## OEM and authorized distributor language

OEM verification patterns center on **"original equipment manufacturer"** or **"OEM"** as primary designations. Distribution channels use "authorized dealer", "authorized distributor", and "authorized reseller" (especially common in GSA Schedule contracts). Authorization documentation requirements specify "letter of authorization from OEM", "manufacturer's authorization", "factory authorized", and "certified dealer" status.

Supply chain authenticity language includes "direct from manufacturer" and warranty provisions tied to authorization status. NASA SEWP explicitly states "you didn't buy through an authorized reseller, we're not going to give you a warranty", demonstrating the critical link between OEM authorization and warranty validity. GSA Schedule contracts require an "Authorized Government Reseller Agreement" for technology products.

## Traceability and chain of custody requirements

Material traceability uses **"Certificate of Conformance (CoC)"** as the primary document, with variations including "Certificate of Conformity", "C of C", and "Certificate of Compliance". These certify products meet specified standards and regulatory requirements, including product identification, conformity statements, and authorized signatures.

Chain of custody documentation requires "traceability documentation", "chain of custody", "material traceability", and "lot traceability". Specific tracking includes "batch tracking", "heat number traceability", "serial number tracking", and "unique serialization within enterprise identifier or within part, lot, or batch numbers" per DFARS warranty requirements.

DFARS 252.225-7009 mandates specialty metals traceability through mill products forms (bar, billet, wire, slab, plate, sheet), requiring metals be melted or produced in qualifying countries. DFARS 252.246-7003 requires notification within 72 hours for critical safety item nonconformances, with written notification within 5 working days including chronology and affected items identification.

Material certification uses "Material Test Certificate (MTC)" or "Mill Test Reports (MTR)" certifying compliance with ASTM/ASME/UNS standards. These include chemical composition, mechanical properties, and material heat numbers, essential for pressure-retaining components in federal construction projects.

## Set-aside program indicators

Federal set-aside programs use precise terminology tied to SBA certifications. **"8(a) set-aside"** indicates the 8(a) Business Development Program with sole-source thresholds of $7 million (manufacturing) and $4.5 million (other acquisitions). "Service-Disabled Veteran-Owned Small Business (SDVOSB)" requires SBA VetCert certification as of January 2024, eliminating self-certification.

"Women-Owned Small Business (WOSB)" and "Economically Disadvantaged Women-Owned Small Business (EDWOSB)" require MySBA Certifications with 51% ownership by women U.S. citizens. EDWOSB adds personal net worth limits ($850,000), adjusted gross income limits ($400,000 over 3 years), and personal asset limits ($6.5 million).

"HUBZone set-aside" requires business location in designated Historically Underutilized Business Zones with 51% U.S. citizen ownership and 10% price evaluation preference in full competitions. "Small business set-aside" and "total small business set-aside" trigger automatic set-asides for contracts $10,000-$250,000 when two qualified small businesses are available.

"Veteran-Owned Small Business (VOSB)" requires SBA VetCert certification for VA sole-source and set-aside contracts, with VA setting aside 7% annually for VOSB/SDVOSB combined. Each program requires three-year recertification, creating ongoing compliance obligations.

## Contract vehicle references

GSA Schedules appear as **"GSA Schedule"**, **"GSA MAS"**, or **"Multiple Award Schedule"** with 20-year potential duration (5-year base plus four 5-year options). These IDIQ contracts generated $51.5 billion in FY 2024 sales, accessible to federal, state, local, and tribal agencies under FAR Subpart 8.4.

Major GWACs include NASA SEWP V/VI with $20B ceilings and 0.34% access fees, NITAAC CIO-SP3 with 137+ labor categories extended through April 2026, GSA Alliant 2 with $50B total program ceiling running 2018-2028, 8(a) STARS III with $50B program ceiling for small disadvantaged businesses, and VETS 2 with $5B for service-disabled veteran-owned businesses.

"IDIQ" or "Indefinite Delivery Indefinite Quantity" contracts require minimum and maximum quantities under FAR 16.504, typically with 5-year base periods and fair opportunity provisions. "BPA" or "Blanket Purchase Agreement" represents agreements rather than contracts under FAR 13.303, with single-award BPAs limited to 1 year plus four 1-year options.

Professional services vehicles include OASIS+ replacing legacy OASIS contracts, structured across six IDIQ contracts based on business size/type with 0.75% access fees. The system covers program management, management consulting, scientific, engineering, logistics, and financial services through functionally aligned domains.

## Compliance and regulatory clauses

FAR clauses follow the pattern **"FAR 52.[part].[sequential]"** with critical cybersecurity provisions in FAR 52.204-21 (Basic Safeguarding), FAR 52.204-25 (Telecommunications Prohibition), and FAR 52.204-30 (FASCSA implementation effective December 2023). These require 15 basic security controls, prohibit Huawei/ZTE equipment, and implement supply chain security.

DFARS clauses use **"DFARS 252.[part].[7000-series]"** with cybersecurity focus on DFARS 252.204-7012 requiring NIST SP 800-171 compliance for CUI, DFARS 252.204-7019/7020 for assessment requirements, and DFARS 252.204-7021 for CMMC implementation over three years. Supply chain clauses include DFARS 252.225-7001 (Buy American), 252.225-7009 (Specialty Metals), and 252.225-7012 (Domestic Commodities).

"ITAR compliance" invokes International Traffic in Arms Regulations administered by State Department's DDTC, controlling defense articles on the US Munitions List. "Buy American Act" and "BAA compliant" require 50% domestic content with 6-12% evaluation penalties for foreign products. "TAA compliant" prohibits products from non-designated countries above $182,000 thresholds.

CMMC implementation includes three levels: Foundational (FAR 52.204-21 controls), Advanced (NIST 800-171), and Expert (NIST 800-172 subset), with third-party assessments required. CUI protection covers Controlled Technical Information with specific marking and handling requirements per NARA guidelines.

## Aviation/aerospace platform identifiers

Military aircraft use standardized designators: **F-35** (Lightning II), **C-130** (Hercules), **UH-60** (Black Hawk), with variants like F-35A/B/C indicating specific configurations. Pattern recognition follows [Letter]-[Number][Optional Letter] for fighters, [Letter][Letter]-[Number] for helicopters, and [Manufacturer] [Number] for commercial aircraft.

"Flight critical", "flight safety critical", and "airworthiness" indicate safety-critical components. Aviation Critical Safety Item (CSI) per FAR 252.209-7010 means parts whose "failure, malfunction, or absence could cause catastrophic or critical failure resulting in loss of or serious damage to aircraft, unacceptable risk of personal injury or loss of life, or uncommanded engine shutdown jeopardizing safety".

Platform classifications distinguish "rotorcraft", "fixed-wing", "unmanned aircraft system (UAS)", and "remotely piloted aircraft (RPA)". Exclusion patterns include "ground support equipment", "non-flight hardware", "training only", and "static displays" indicating non-airworthy items.

Quality standards require **AS9100D** for aerospace organizations, AS9110C for MRO operations, AS9120B for stockist distributors, and AS6081 for counterfeit prevention. Software safety follows DO-178B/C with Level A (catastrophic) through Level E (no safety effect) classifications. "First article testing (FAT) required" indicates mandatory pre-production validation.

## Risk indicators and critical safety items

Critical safety classifications use **"Critical Safety Item (CSI)"** and **"Critical Application Item (CAI)"** as primary identifiers. Risk levels include "catastrophic" (loss of life), "hazardous" (large negative safety impact), "major" (significant operational impact), "high risk", "mission critical", and "life support" designations.

Quality assurance provisions specify "higher-level quality requirements", "heightened quality assurance surveillance", "risk-based surveillance", and "first article testing (FAT) required". Critical characteristics divide into Manufacturing (M) for production dimensions/processes, Depot (D) for maintenance/overhaul, and Installation (I) for sequence/torque requirements.

Detection language includes "The following items have been designated aviation critical safety items", "Subject to heightened, risk-based surveillance", "Critical characteristic identification required", and "Airworthiness certification compliance". These trigger enhanced oversight and documentation requirements throughout the supply chain.

## SLED-specific patterns differing from federal

State procurement uses **"Invitation to Bid (ITB)"** rather than federal "IFB", with Florida's unique **"Invitation to Negotiate (ITN)"** allowing collaborative negotiations. State contract vehicles include Texas "DIR contracts" for IT with "DIR first" requirements, California "CMAS" based on GSA schedules, and state-specific e-procurement systems.

Educational patterns include **"E-rate eligible"** for FCC telecommunications discounts (20-90% based on poverty/rural status), "Title I funding" ($16.5 billion for low-income schools), and "ESSER funds" ($190 billion COVID relief, expired September 2024). Cooperative purchasing uses "TIPS", "OMNIA Partners" (90,000+ agencies), "Sourcewell" (2,021 contracts), and "BuyBoard" (2,605 contracts).

State preferences include "resident vendor preference" and "in-state preference" with reciprocal systems applying home-state advantages. "Certified MBE/WBE/DBE" indicates state-level minority/women/disadvantaged certifications distinct from federal programs. "Piggyback clause" and "cooperative purchasing clause" enable shared procurement across jurisdictions without separate competitive bidding.

State thresholds often differ significantly from federal levels, with many states maintaining lower competitive bidding thresholds (California $100,000 vs federal $250,000). This decentralized structure across 50 states, 3,033 counties, and 90,000+ political subdivisions creates substantial variation from standardized federal patterns, requiring vendors to understand multiple rule sets and terminology variations.