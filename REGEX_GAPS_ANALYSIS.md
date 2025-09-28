# Regex Pattern Gap Analysis
## Comparison: Current Implementation vs New Manual Prompt Checklist

### ✅ Currently Implemented Patterns

#### Category 12: Competition Status
- [x] Bridge contract patterns
- [x] Follow-on contract patterns
- [x] Incumbent advantage patterns

#### Category 15: Non-Standard Acquisition
- [x] OTA (Other Transaction Authority)
- [x] BAA (Broad Agency Announcement)
- [x] SBIR (Small Business Innovation Research)
- [x] CRADA (Cooperative Research and Development Agreement)

### ❌ Missing Pattern Categories

#### Category 16: IT System/Infrastructure Access (MISSING ENTIRELY)
- [ ] JEDMICS access required
- [ ] ETIMS access required
- [ ] cFolders with sponsor-only access
- [ ] DLA EProcurement pre-certification
- [ ] System access not open to new vendors
- [ ] Sponsor-required for system access
- [ ] Pre-approval in government IT system required

#### Category 17: Unique Government Registration (PARTIALLY MISSING)
- [ ] DOT Hazmat-certified shipper required
- [ ] NASA Parts Screening Certified required
- [ ] EPA Registered Producer required
- [ ] TSA Certified Repair Vendor required
- [ ] DCMA approved supplier
- [ ] Agency-specific certification with no path to obtain

#### Category 18: Depot/Warranty Obligations (MISSING ENTIRELY)
- [ ] Warranty/depot support required directly from vendor
- [ ] Vendor must perform in-warranty support
- [ ] Depot-level repair required
- [ ] Lifecycle management responsibility
- [ ] Vendor-owned warranty obligation
- [ ] Direct sustainment services required
- [ ] On-site maintenance required (no subcontractors)
- [ ] Field service representatives required
- [ ] Vendor must establish repair depot

#### Category 19: Native CAD Format Requirements (MISSING ENTIRELY)
- [ ] Native CAD/CAM format required (proprietary/non-open)
- [ ] Must submit SolidWorks native files
- [ ] Must submit CATIA native files
- [ ] Must submit Creo/ProE native files
- [ ] Must submit NX/Unigraphics files
- [ ] Must submit proprietary OEM format
- [ ] Digital thread submission required
- [ ] Model-based definition required
- [ ] 3D model deliverables in proprietary format
- [ ] Cannot use neutral formats (STEP/IGES)

### 🔧 Logic Updates Needed

#### AMSC Code Override Logic
**Current:** Only AMSC Z overrides military restrictions
**Required:** AMSC Z, G, and A should ALL override military restrictions

#### Contact CO Logic (NEW FEATURE NEEDED)
**Current:** Simple NO-GO decisions
**Required:** Special "Contact CO" status for:
1. Approved sources + FAA standards
2. Subcontracting prohibited + single unit
3. Managed repair requirement (suggest exchange unit with 8130-3)

#### Missing Experimental Types
Need to add patterns for:
- [ ] STTR (Small Business Technology Transfer)
- [ ] SIVR (Small Business Innovation Research Variant)
- [ ] SIDR (Small Innovative Defense Requirement)
- [ ] Prize challenge/competition
- [ ] Partnership Intermediary Agreement
- [ ] Technology Investment Agreement
- [ ] Prototype project
- [ ] Demonstration program

### 📊 Implementation Priority

1. **High Priority** (Direct business impact)
   - IT System access requirements
   - Native CAD format requirements
   - AMSC G/A override logic
   - Contact CO special cases

2. **Medium Priority** (Accuracy improvement)
   - Depot/warranty obligations
   - Additional experimental acquisition types
   - Government registration requirements

3. **Low Priority** (Edge cases)
   - Prize challenges
   - Partnership agreements
   - Demonstration programs

### Next Steps
1. Add IT system access patterns (Category 16)
2. Add native CAD format patterns (Category 19)
3. Update AMSC override logic to include G and A codes
4. Implement "Contact CO" decision type alongside GO/NO-GO/INDETERMINATE