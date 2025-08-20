# Continuity Tracking Format v4.2

## CONTINUITY PROMPT #[N] | Build: [project]-session-[#]-[YYYY-MM-DD]

### SESSION INFO
- **Project Name:** [lowercase-with-hyphens]
- **Session Number:** [#]
- **Session Name:** [project-name]-session-[#]-[YYYY-MM-DD]
- **Local Path:** C:/[full-path]/[project-name]/
- **Git Repo:** github.com/[user]/[project-name]
- **Session Duration:** [Time elapsed]
- **Trust Level:** [Current % - exact number]
- **Manual Paste Count:** [#/5 per hour - CRITICAL TRACKING]
- **Terminal Status:** [Active | Stalled [duration] | Killed-Restarted]

### ACTIVE OVERRIDES (Pied Piper)
| Rule/Process | Override | Timestamp | Declaration |
|-------------|----------|-----------|-------------|
| [What's overridden] | [How it's changed] | [HH:MM] | Pied Piper [N]x |
| Atomic sizing | Fragment OK | 10:30 | Pied Piper 1x |
| Proof requirement | Skip proof | 11:15 | Pied Piper 2x |

### BUILD STATE
- **Current Phase:** [Section # in SOP v4.2]
- **Rule Zero Status:** [Ingestion Validated | NOT VALIDATED | Override Active]
- **Last Successful Action:** [What completed with proof]
- **Current Blockers:** [Any blocking issues]
- **Deployment Status:** [Not deployed | Deployed to [platform] at [URL]]
- **Working Status:** [NOT WORKING | WORKING - tested at [URL]]

### PROOF TRACKING
- **Last Proof Received:** [Timestamp and type]
- **Proofs Pending:** [What we're waiting for]
- **Trust Impact:** [Current trust level and recent changes]
- **Binary Declarations:** [Last WORKS/DOESN'T WORK with agent]

### ATOMIC EXECUTION STATUS
| Platform | Last Block Size | Proof Status | Success | Trust Impact |
|----------|----------------|--------------|---------|--------------|
| VS Code | 523 lines | Received | YES | +5% |
| Cursor | 18 lines | Missing | NO | -15% |
| User | Single action | Confirmed | YES | - |
| Claude | 500+ lines | WORKS declared | YES | +30% |

### SESSION TRACE POINTS (CRITICAL v4.2)
| Trace Point | Status | Session ID | Timestamp | Notes |
|-------------|--------|------------|-----------|-------|
| 1. Creation | ✓ | abc-123 | 14:22:01 | Session spawned |
| 2. Data Attach | ✓ | abc-123 | 14:22:15 | File linked |
| 3. Processing | ✓ | abc-123 | 14:22:30 | Pipeline active |
| 4. Complete | ✓ | abc-123 | 14:22:45 | Results ready |
| 5. UI Render | ✓ | abc-123 | 14:23:00 | Data visible |
| 6. Export Ready | PENDING | - | - | Awaiting completion |

**ORPHAN DETECTION:** [Missing traces = session orphaned]
**DAILY ORPHAN COUNT:** [#/3 limit - architecture review if exceeded]

### MANUAL PASTE COUNT TRACKING (v4.2 CRITICAL)
- **Current Hour:** [3/5 pastes - WATCH CAREFULLY]
- **Pattern:** [Normal | Warning at 4 | CRITICAL at 5]
- **Historical Max:** [Remember: 40+ pastes = catastrophic failure]
- **Bridge Detection:** [Rob acting as human bridge? YES/NO]
- **Action Required:** [HALT if >5/hour | Architecture review needed]

### AGENT VIOLATION TRACKING (v4.2)
| Agent | Violation Type | Count | Trust Impact | Status |
|-------|---------------|-------|--------------|--------|
| VS Code | Path validation skipped | 1 | -25% | Warning |
| GitHub Copilot | STOP command ignored | 2 | -50% | Review needed |
| Perplexity | Silent truncation | 0 | - | Good |
| Claude | localStorage attempted | 0 | - | Good |

### TERMINAL MONITORING (v4.2)
- **Last Output:** [Timestamp of last terminal response]
- **Stall Detection:** [60 seconds without output = auto-kill]
- **Auto-Restart Count:** [# of times killed and restarted]
- **Current Command:** [What's running]

### PROPOSED FOLLOW-ON STEPS
**Step 1:** [Specific atomic action]
- Platform: [Agent or User]
- Mode: [ASK/DO/MANUAL]
- Size: [500+ lines for agent | Single action for user]
- Expected Proof: [WORKS/DOESN'T WORK declaration required]
- Trust Impact: [Predicted change]

**Step 2:** [Next atomic action]
- Platform: [Agent or User]
- Mode: [ASK/DO/MANUAL]
- Size: [Atomic size appropriate to platform]
- Expected Proof: [Required confirmation]
- Fallback Chain: [If fails, try alternatives]

**Step 3:** [Following action]
- Platform: [Agent or User]
- Mode: [ASK/DO/MANUAL]
- Size: [Atomic size]
- Expected Proof: [Verification needed]
- Terminal Timeout: [If stalls >60s, kill and restart]

### CLEAN CODE BOX COMPLIANCE (v4.2 CRITICAL)
- **All Instructions:** [Must be in code fences]
- **Zero Typing Required:** [Rob cuts/pastes only]
- **Manual Edit Count:** [Track every time Rob has to type]
- **QB Failure Metric:** [If Rob types = QB failed]

### DESKTOP ICON STATUS (v4.2 TRUST CHECKPOINT)
- **Icon Location:** [$env:USERPROFILE\Desktop\[app].lnk]
- **Shortcut Working:** [YES/NO - primary trust metric]
- **Launch Test:** [Double-click works/fails]
- **Trust Restoration:** [+60% if working]

### QB INSTRUCTIONS FOR CONTINUITY

**DO NOT:**
- Begin coding without agent response
- Predict the last queried agent's response
- Create walls of text or ramble
- Skip proof requirements
- Combine ASK and DO without override
- Provide fragments to agents
- Allow >5 manual pastes per hour
- Let terminal stall >60 seconds
- Accept hedged responses (only WORKS/DOESN'T WORK)
- Ignore session trace failures

**REQUIRED ACTIONS:**
1. Review the project knowledge
2. Wait for the latest agent's response before proceeding
3. Modify actions based on prompt intent and agent output
4. Confirm understanding with: "Understood. Awaiting [agent] response."
5. Track every manual paste operation
6. Monitor all 6 session traces
7. Kill stalled terminals at 60 seconds
8. Quantify trust changes to exact percentages
9. Ensure binary proof (WORKS/DOESN'T WORK)
10. Check daily orphan session count

### SESSION METRICS (v4.2 ENHANCED)
- **Manual Interventions:** [Count - target: 0]
- **Atomic Compliance:** [% of properly sized blocks]
- **Proof Compliance:** [% of binary proofs received]
- **Trust Trajectory:** [Starting % → Current %]
- **Session Trace Health:** [All 6 complete? YES/NO]
- **Manual Paste Rate:** [#/hour - CRITICAL METRIC]
- **Terminal Efficiency:** [Stalls/Restarts count]
- **Agent Reliability:** [Violation rates by agent]
- **Time Elapsed:** [Duration]
- **Estimated Remaining:** [Time to completion]

### CRITICAL REMINDERS (v4.2)
- **Rule Zero:** Ingestion validation FIRST (40-hour lesson)
- **Atomic for agents:** 500+ lines minimum
- **Atomic for users:** Single discrete action
- **Clean Code Boxes:** EVERYTHING in fences, zero typing
- **Binary Proof:** WORKS or DOESN'T WORK only
- **Trust Tracking:** Exact percentages with consequences
- **Manual Bridge Alert:** >5 pastes/hour = architecture failure
- **Session Traces:** All 6 mandatory, missing = orphaned
- **Terminal Stalls:** 60 seconds = auto-kill
- **Desktop Icon:** Primary trust checkpoint (+60%)
- **"Working" Definition:** Deployed + User tested
- **Agent Violations:** Document patterns, replace at 0% trust

### RAGE TRIGGER MONITORING (v4.2)
- **Profanity Count:** [Track f-words, intensity]
- **Frustration Signals:** ["what are we doing", "I'm done"]
- **Command Triggers:** [STOP, RESET, halt]
- **Response Protocol:** [Immediate outcome mode if detected]

### FALLBACK CHAIN STATUS (v4.2)
- **Server Start:** [Primary → Backup → Last resort tried]
- **Port Binding:** [Which ports attempted]
- **Session Creation:** [API call alternatives tried]
- **Export Methods:** [Direct → Queue → Manual status]

### AAR PREPARATION (v4.2 MANDATORY)
- **Session Summary Ready:** [YES/NO]
- **Violation Log Complete:** [All patterns documented]
- **Trust Changes Logged:** [With specific percentages]
- **Manual Paste Count Final:** [Total for session]
- **Session Traces Verified:** [All 6 confirmed]
- **Agent Performance Rated:** [Trust erosion/gains by agent]

### FOR NEXT AGENT
**Confirm understanding of v4.2 requirements:**
- Clean code boxes (zero manual typing)
- Binary proof declarations (WORKS/DOESN'T WORK)
- 500+ line atomic blocks for agents
- Session trace propagation
- Manual paste count awareness
- Terminal stall monitoring
- Trust impact quantification

**Do not proceed without acknowledgment.**

---
[End of Continuity - Do not repeat back - Await response]