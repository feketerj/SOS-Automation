# Unified Logic Audit - Regex Pattern Contradictions

## Critical Logic Issues Found

### 1. ❌ FAA 8130 Exception Too Broad
**Current Logic (PROBLEMATIC):**
- Code automatically marks as GO when: Navy + SAR + FAA 8130
- Location: `sos_ingestion_gate_v419.py` line 687-724

**New Manual Prompt Logic:**
- "Approved sources + FAA standards → Contact CO"
- Should NOT be automatic GO
- Requires human verification

**REQUIRED FIX:**
Change from automatic GO to CONTACT_CO status when approved sources + FAA 8130

### 2. ✅ Source Restrictions (ALIGNED)
**Current Categories:**
- Sole source patterns (line 165)
- Intent to award patterns (line 175)
- Approved source only patterns (line 184)
- OEM only patterns (line 195)

**Manual Prompt Alignment:**
- All correctly marked as knockouts
- QPL/QML/ASL properly included
- OEM restrictions properly handled

### 3. ⚠️ Missing Nuance for "Only Known Source"
**Current:** Simple pattern match for knockout
**Manual Prompt:** "[Vendor] is the only known source" as knockout
**Issue:** No exception handling for commercial equivalents

### 4. ✅ AMSC Override Logic (CORRECT)
**Current:** AMSC Z/G/A codes override military restrictions
**Manual Prompt:** Same - AMSC Z/G/A override
**Status:** Properly implemented

### 5. ⚠️ Subcontracting Prohibited Logic
**Current:** Simple knockout
**Manual Prompt Special Case:**
- "Subcontracting prohibited + single unit → offer direct purchase" (Contact CO)
- Need to detect single unit/LRU/SRU context

### 6. ⚠️ Managed Repair Requirement
**Current:** Likely marked as knockout
**Manual Prompt Special Case:**
- "Managed repair requirement → suggest exchange unit with 8130-3" (Contact CO)

## Contradictory Pattern Analysis

### Patterns That Need Context-Aware Logic:

#### 1. Approved Sources + FAA 8130
```yaml
# CURRENT (Too Permissive):
if has_approved_sources and has_faa_8130:
    return GO  # WRONG!

# SHOULD BE:
if has_approved_sources and has_faa_8130:
    return CONTACT_CO  # Need clarification
```

#### 2. OEM Only Requirements
```yaml
# CURRENT:
OEM_only → NO-GO

# SHOULD CHECK:
if OEM_only:
    if has_faa_8130_mentioned:
        return CONTACT_CO  # Might accept FAA certified equivalent
    else:
        return NO-GO
```

#### 3. SAR (Source Approval Request)
```yaml
# CURRENT:
SAR → NO-GO
Exception: Navy + commercial platform (P-8, E-6B, etc.)

# CORRECT - Matches manual prompt
```

## Unified Decision Logic Recommendations

### 1. Add CONTACT_CO Decision Type
Currently have: GO, NO-GO, INDETERMINATE
Need to add: CONTACT_CO

### 2. Context-Aware Pattern Matching
Instead of simple pattern → decision, need:
```python
def evaluate_source_restrictions(text):
    has_approved_sources = check_pattern("approved source|QPL|QML|ASL")
    has_faa_8130 = check_pattern("FAA 8130|airworthy")
    has_oem_only = check_pattern("OEM only")

    # Special case handling
    if has_approved_sources and has_faa_8130:
        return Decision.CONTACT_CO, "Approved sources with FAA standards - needs clarification"

    if has_oem_only and not has_faa_8130:
        return Decision.NO_GO, "OEM only without FAA exception"

    # etc.
```

### 3. Single Unit Detection for Subcontracting
```python
def evaluate_subcontracting(text):
    has_subcontract_prohibited = check_pattern("subcontracting prohibited")
    is_single_unit = check_pattern("single unit|1 each|one unit|LRU|SRU")

    if has_subcontract_prohibited and is_single_unit:
        return Decision.CONTACT_CO, "Single unit - offer direct purchase"
    elif has_subcontract_prohibited:
        return Decision.NO_GO, "Subcontracting prohibited"
```

## Priority Fixes

### High Priority (Business Impact):
1. **Fix FAA 8130 exception logic** - Currently too permissive
2. **Add CONTACT_CO decision type** - Missing critical business logic
3. **Fix approved sources + FAA logic** - Should be Contact CO, not GO

### Medium Priority:
1. **Single unit detection** for subcontracting exceptions
2. **Managed repair** detection for exchange unit suggestions
3. **OEM + FAA** combination handling

### Low Priority:
1. Additional context refinements
2. Edge case handling

## Implementation Notes

The current system is mostly aligned but has critical gaps in handling special cases that require CO contact. The biggest issue is the FAA 8130 exception being too permissive - it should trigger a CONTACT_CO status for human review, not automatic GO.

The regex patterns themselves are good - it's the decision logic that needs refinement to handle the nuanced cases in the manual prompt.