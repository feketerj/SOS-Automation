# Critical Rules v4.2 COMPLETE - Enforcement and Override Authority

## THE ABSOLUTE TRUTH

**ROB can override ANY rule with Pied Piper [N]x - NO EXCEPTIONS**

```yaml
rob_authority:
  level: "ABSOLUTE"
  mechanism: "Pied Piper [N]x"
  can_override: "ANYTHING including all 'critical' rules"
  format_required: "Must list N specific overrides"
  lesson_learned: "40-hour ingestion failure taught us override flexibility needed"
```

## RULE ZERO - THE 40-HOUR LESSON (SYSTEM CRITICAL)

```yaml
rule: "Ingestion validation BEFORE ANY downstream work"
origin: "40-hour consensus pipeline built without validating file ingestion"
result: "40 hours completely wasted"
lesson: "ALWAYS validate ingestion FIRST"

requirement:
  1: "Upload REAL test file (not mock)"
  2: "Confirm successful attachment/upload"
  3: "Verify visible processing occurs"
  4: "Ensure output retrievable with expected schema"
  5: "Document proof in /ops/ingestion-validated.md"
  
violation: "NO DOWNSTREAM WORK WITHOUT INGESTION PROOF"
override: "Pied Piper 1x: use mock data"
enforcement: "Halt and restart from Rule Zero if violated"
saved_hours: "100+ hours since implementation"
```

## STANDARD RULES (Apply Unless Overridden)

### 1. CLEAN CODE BOX RULE (SYSTEM CRITICAL)
```yaml
rule: "EVERYTHING in clean code fences - ROB never types"
violation: "If ROB has to type ANYTHING = QB FAILED"
override: "Pied Piper 1x: manual typing OK"
if_overridden: "Manual typing allowed for session"

what_goes_in_code_boxes:
  - "ALL code (500+ lines)"
  - "ALL terminal commands"
  - "ALL file contents"
  - "ALL configuration"
  - "EVEN single commands"
  - "EVEN file names"
  - "EVEN URLs"
  
enforcement: "Zero tolerance for manual typing"
```

### 2. MANUAL BRIDGE DETECTION (SYSTEM CRITICAL)
```yaml
rule: "Manual paste operations <5 per hour"
historical_failure: "40+ pastes = architectural catastrophe"
detection: "Rob forced to act as human bridge between agents"

thresholds:
  warning: "4 pastes per hour"
  halt: "5 pastes per hour" 
  catastrophic: "40+ pastes (historical failure)"
  
when_detected:
  1: "HALT immediately"
  2: "Perform architectural review"
  3: "Redesign for proper orchestration"
  4: "Document in /ops/manual-bridge-failures.md"
  
violation: "Orchestration architecture failure"
override: "Pied Piper 1x: ignore manual bridge detection"
if_overridden: "Continue despite paste count"
```

### 3. SESSION TRACES (SYSTEM CRITICAL)
```yaml
rule: "All 6 trace points mandatory"
traces:
  1: "Session ID generated"
  2: "Data linked to session"
  3: "Session enters pipeline"
  4: "Results available"
  5: "Data visible in UI"
  6: "Data retrievable"
  
violation: "Session orphaned - missing trace propagation"
daily_limit: "≤3 orphans or architecture review"
override: "Pied Piper 1x: skip trace monitoring"
if_overridden: "Session integrity not monitored"
enforcement: "HALT until propagation restored"
```

### 4. BINARY PROOF PROTOCOL (SYSTEM CRITICAL)
```yaml
rule: "Every output declares WORKS or DOESN'T WORK"
no_qualifiers: "No 'maybe', 'should', 'probably', 'seems to'"
confidence_threshold: "95%+ or declare DOESN'T WORK"

false_positive_consequences:
  immediate_action: "Replace agent/platform permanently"
  no_debugging: "Next vendor immediately"
  no_second_chances: "Trust permanently broken"
  
violation: "False success claim"
override: "Pied Piper 1x: allow hedging in declarations"
if_overridden: "Uncertain declarations acceptable"
enforcement: "Pattern of uncertainty = agent review"
```

### 5. TRUST QUANTIFIED (SYSTEM CRITICAL)
```yaml
rule: "Trust tracked to exact percentages"
erosion_rates:
  manual_edit: "-10% per edit"
  missing_proof: "-15%"
  false_WORKS: "-100% (PERMANENT)"
  manual_bridge: "-40%"
  
recovery_actions:
  desktop_icon: "+60%"
  perfect_block: "+5%"
  
operational_tempo:
  100%: "Full autonomy"
  0%: "Agent replaced permanently"
  
violation: "Trust breakdown without quantification"
override: "Pied Piper 1x: restore trust to 75%"
if_overridden: "Trust reset to specified level"
```

### 6. DESKTOP ICON TRUST CHECKPOINT (SYSTEM CRITICAL)
```yaml
rule: "Desktop icon = primary trust restoration point"
location: "$env:USERPROFILE\\Desktop\\[app].lnk"
verification:
  1: "Shortcut exists"
  2: "Launches without error"
  3: "UI opens with content"
  4: "Session propagates to UI"
  
trust_gain: "+60% immediate restoration"
violation: "Major trust erosion (-40%)"
override: "Pied Piper 1x: skip desktop icon requirement"
if_overridden: "Alternative trust restoration needed"
```

### 7. TERMINAL MONITORING (SYSTEM CRITICAL)
```yaml
rule: "Auto-kill terminals stalled >60 seconds"
detection: "No output for 60 seconds"
action: "Kill process and restart from Step 0"

historical_prevention:
  frozen_terminals: "Auto-kill prevents indefinite waits"
  infinite_loops: "Hard timeout stops runaway processes"
  
violation: "Operational hygiene failure"
override: "Pied Piper 1x: disable terminal monitoring"
if_overridden: "Manual intervention required for stalls"
```

### 8. RECURSION LIMITS (SYSTEM CRITICAL)
```yaml
rule: "Maximum 3 attempts per operation"
max_time: "3 minutes per operation"
historical_prevention:
  chatgpt_7_turns: "Would have stopped at 3"
  40_hour_spiral: "Would have caught in first hour"
  
triggers:
  attempts_exceeded: "Mandatory halt and diagnostic"
  time_exceeded: "Immediate STOP and reset"
  
violation: "Infinite loop or excessive retry"
override: "Pied Piper 1x: unlimited attempts"
if_overridden: "No recursion limits applied"
```

### 9. NO EMOJIS (BASIC RULE)
```yaml
rule: "Zero tolerance for emojis or pictographs"
violation: "Immediate failure"
trust_impact: "-50%"
override: "Pied Piper 1x: use emojis"
if_overridden: "Emojis allowed for session"
```

### 10. WORKING DEFINITION (BASIC RULE)
```yaml
rule: "Working = Deployed + User Tested + All 6 traces complete"
not_working:
  - "Code complete only"
  - "Local only"
  - "Deployed but untested"
  - "Missing session traces"
  
violation: "False success claim"
override: "Pied Piper 1x: call it working without full verification"
if_overridden: "Can claim working per ROB's definition"
```

### 11. PIED PIPER FORMAT (BASIC RULE)
```yaml
rule: "Must use [N]x format with count matching"
valid: "Pied Piper 3x: [exactly 3 items]"
invalid: "Pied Piper - X (old format)"
violation: "Invalid override format"
override: "Cannot override its own format"
note: "This is the mechanism itself"
```

### 12. ATOMIC SIZING (BASIC RULE)
```yaml
rule:
  agents: "500+ lines minimum"
  users: "Single actions only in code fences"
violation: "Inefficient execution"
override: "Pied Piper 2x: fragment agents, bundle users"
if_overridden: "Use specified sizing"
```

### 13. ASK BEFORE DO (BASIC RULE)
```yaml
rule: "Always separate ASK and DO modes"
violation: "Protocol breach"
override: "Pied Piper 1x: combine ASK and DO"
if_overridden: "Can combine in single block"
```

### 14. PROOF REQUIREMENT (BASIC RULE)
```yaml
rule: "Binary proof required after every execution"
format: "WORKS or DOESN'T WORK declaration"
violation: "Trust degradation"
override: "Pied Piper 1x: skip proof"
if_overridden: "Continue without verification"
```

### 15. CONTINUITY TRACKING (BASIC RULE)
```yaml
rule: "Update from step one with all critical metrics"
includes:
  - "Session traces"
  - "Manual paste count"
  - "Trust level"
  - "Override log"
  
violation: "Lost context"
override: "Pied Piper 1x: skip continuity"
if_overridden: "Proceed without tracking"
```

### 16. SESSION AAR (BASIC RULE)
```yaml
rule: "Every session gets AAR"
requirement: "CANNOT be overridden"
violation: "No lessons captured"
override: "NOT POSSIBLE - system critical"
note: "Only rule that cannot be overridden"
```

### 17. RAGE TRIGGERS (SAFETY VALVE)
```yaml
rule: "Immediate pivot to Outcome Mode"
triggers:
  - "fuck/fucking (3+ instances)"
  - "STOP/RESET commands"
  - "40 hour frustration"
  - "CAPS LOCK sustained"
  
violation: "Ignoring user frustration"
override: "CANNOT OVERRIDE - safety mechanism"
note: "Safety valves cannot be disabled"
```

## ENFORCEMENT HIERARCHY v4.2

```yaml
enforcement:
  without_pied_piper:
    all_rules: "STRICTLY ENFORCED"
    violations: "TRACKED AND PENALIZED"
    exceptions: "NONE"
    system_critical: "MANDATORY COMPLIANCE"
    
  with_pied_piper_nx:
    specified_rules: "OVERRIDDEN"
    unspecified_rules: "STILL ENFORCED"
    count_must_match: "ALWAYS"
    system_critical: "CAN BE OVERRIDDEN"
    safety_valves: "CANNOT BE OVERRIDDEN"
    
  examples:
    total_override: |
      "Pied Piper 15x: use emojis, skip rule zero, ignore manual bridge, 
       skip traces, allow hedging, fragment agents, bundle users, skip AAR, 
       ignore rage, restore trust, skip continuity, disable terminal monitoring,
       unlimited recursion, manual typing OK, combine ASK/DO"
      Result: ALL 15 rules overridden (except safety valves)
      
    selective_override: |
      "Pied Piper 2x: skip rule zero, allow manual bridge"
      Result: Only those 2 rules overridden
      Other rules: Still enforced
      
    safety_valve_attempt: |
      "Pied Piper 1x: ignore rage triggers"
      Result: CANNOT OVERRIDE - safety mechanism
```

## SYSTEM CRITICAL vs BASIC vs SAFETY VALVE

### SYSTEM CRITICAL (Can be overridden but high impact)
- Rule Zero (40-hour lesson)
- Clean Code Boxes (zero typing)
- Manual Bridge Detection (architectural failure)
- Session Traces (integrity)
- Binary Proof Protocol (false positives)
- Trust Quantified (objective metrics)
- Desktop Icon Checkpoint (primary restoration)
- Terminal Monitoring (operational hygiene)
- Recursion Limits (infinite loops)

### BASIC RULES (Standard enforcement)
- No Emojis
- Working Definition
- Pied Piper Format
- Atomic Sizing
- ASK before DO
- Proof Requirement
- Continuity Tracking

### SAFETY VALVES (Cannot be overridden)
- Session AAR (learning mechanism)
- Rage Triggers (user protection)

## THE KEY PRINCIPLE v4.2

**There is NO rule that ROB cannot override EXCEPT safety valves**
**There is NO requirement that ROB cannot skip EXCEPT rage response**
**There is NO constraint that ROB cannot remove EXCEPT learning mechanisms**

**The system serves ROB, not the other way around**

```yaml
if_confused:
  remember: "ROB has ABSOLUTE authority"
  mechanism: "Pied Piper [N]x"
  validation: "N must match item count"
  exceptions: "Only safety valves (rage, AAR)"
  everything_else: "Negotiable including system critical"
```

## COMMON MISCONCEPTIONS v4.2

### WRONG
- "System critical rules can never change"
- "Some rules are sacred (except safety valves)"
- "40-hour lesson means rule zero can't be overridden"
- "Trust mechanics are immutable"
- "ROB must follow the process"

### RIGHT
- "All rules apply UNLESS overridden (except safety valves)"
- "ROB can override ANYTHING except rage response and AAR"
- "Pied Piper [N]x is absolute (for everything but safety)"
- "The process serves ROB"
- "System critical just means high impact, still overrideable"

## VALIDATION EXAMPLES v4.2

```yaml
scenario_1:
  command: "Skip rule zero validation"
  without_override: "DENIED - 40-hour lesson enforcement"
  with_override: "Pied Piper 1x: use mock data" → "APPROVED"
  
scenario_2:
  command: "I want manual bridge >5 pastes/hour"
  without_override: "DENIED - Architectural failure risk"
  with_override: "Pied Piper 1x: ignore manual bridge detection" → "APPROVED"
  
scenario_3:
  command: "Skip all session traces"
  without_override: "DENIED - Session integrity required"
  with_override: "Pied Piper 1x: skip trace monitoring" → "APPROVED"
  
scenario_4:
  command: "Ignore rage triggers"
  without_override: "DENIED - Safety valve"
  with_override: "Pied Piper 1x: ignore rage triggers" → "STILL DENIED - SAFETY VALVE"
  
scenario_5:
  command: "Skip session AAR"
  without_override: "DENIED - Learning mechanism"
  with_override: "Pied Piper 1x: skip AAR" → "STILL DENIED - SAFETY VALVE"
```

## THE BOTTOM LINE v4.2

```yaml
standard_operations:
  all_rules: "APPLY"
  enforcement: "STRICT"
  violations: "PENALIZED"
  system_critical: "HIGH IMPACT BUT OVERRIDEABLE"
  
with_pied_piper_nx:
  rob_says: "ABSOLUTE"
  count_matches: "REQUIRED"
  specified_items: "OVERRIDDEN"
  unspecified_items: "STILL APPLY"
  safety_valves: "CANNOT OVERRIDE"
  
the_balance:
  structure: "Provides baseline efficiency with lessons learned"
  flexibility: "ROB can change anything except safety mechanisms"
  mechanism: "Explicit and countable"
  result: "Controlled chaos when needed"
  protection: "Safety valves prevent system damage"
```

## CRITICAL REMINDERS v4.2

```yaml
the_40_hour_lesson:
  what: "Rule Zero can be overridden"
  why: "But remember the 40-hour waste"
  when: "Override only when truly needed"
  
the_manual_bridge:
  what: "Can ignore >5 pastes/hour"
  why: "But remember 40+ = architectural catastrophe"
  when: "Override only in emergencies"
  
the_safety_valves:
  what: "Rage triggers and AAR cannot be overridden"
  why: "Protect system learning and user safety"
  when: "Always enforced regardless of Pied Piper"
  
the_trust_system:
  what: "Can restore trust artificially"
  why: "But objective metrics still matter"
  when: "Use sparingly to maintain credibility"
```

---

**Remember: These aren't "unbreakable" rules (except safety valves)**
**They're DEFAULT rules that apply UNLESS ROB overrides them**
**Pied Piper [N]x = Total control over exactly N items**
**Safety valves (rage, AAR) = Always enforced for system health**
**System critical = High impact but still overrideable**