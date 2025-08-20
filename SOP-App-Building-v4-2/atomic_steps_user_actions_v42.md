# Atomic Steps - When They Apply to USER Actions v4.2 COMPLETE
**Critical Addition to SOP Section 1 with v3.1 Field Lessons**
**Last Updated:** 2025-01-21
**Authority:** ROB

---

## WHEN ATOMIC STEPS APPLY TO THE USER

### The Exception to Maximum Combination: USER MANUAL ACTIONS

**When the USER must perform manual steps, EACH becomes atomic AND must be in clean code boxes**

While QB combines maximum code into single blocks, USER actions must be separated and explicit. The user cannot "undo" a partial manual process, so each manual step must be isolated and verified.

**CRITICAL ENHANCEMENT v4.2:** Even individual user actions must be provided in clean code boxes to ensure zero manual typing.

---

## CLEAN CODE BOX RULE FOR USER ACTIONS

### Zero Manual Typing Applies to Users Too

```yaml
user_action_format:
  even_single_commands: "Must be in code fence"
  even_file_names: "Must be in code fence"
  even_urls: "Must be in code fence"
  no_typing_ever: "Cut and paste only"
  
examples:
  wrong: "Open file myfile.txt"
  right: |
    ```bash
    # Copy and paste this command
    notepad myfile.txt
    ```
    
  wrong: "Navigate to http://localhost:3000"
  right: |
    ```text
    # Copy this URL to browser
    http://localhost:3000
    ```
    
enforcement: "If ROB has to type ANYTHING = QB FAILED"
```

---

## USER ATOMIC STEP RULES WITH CLEAN CODE BOXES

### When to Break Into Atomic Steps for Users:

```yaml
user_must_do_atomic_when:
  manual_file_operations:
    - "Merge these 3 chunks into final-sop.md"
    - "Delete the old nervous-system.md"
    - "Copy AAR to session folder"
    RULE: Each is separate atomic step with verification
    FORMAT: Each command in clean code fence
    
  external_platform_actions:
    - "Go to Stripe dashboard"
    - "Copy the API key"
    - "Add to .env file"
    RULE: Each platform interaction is atomic
    FORMAT: Each URL/action in clean code fence
    
  deployment_verification:
    - "Open deployed URL"
    - "Test upload feature"
    - "Confirm error handling"
    RULE: Each test is atomic step
    FORMAT: Each URL/action in clean code fence
    
  manual_bridge_prevention:
    purpose: "Prevent >5 manual pastes per hour"
    historical_lesson: "40+ pastes = architectural failure"
    enforcement: "Individual steps prevent bridge patterns"
```

### The Critical Difference:

```yaml
FOR_AGENTS:
  instruction: "Complete authentication system with all routes and tests"
  size: 500_lines
  handoffs: 1
  format: "Single clean code fence"
  reason: "Agent pastes once and it's done"

FOR_USER:
  instruction_1: |
    ```bash
    # Copy and paste this command
    notepad final-sop-part1.md
    ```
  instruction_2: |
    ```bash
    # Copy and paste this command (Ctrl+A then Ctrl+C)
    # Select all content and copy
    ```
  instruction_3: |
    ```bash
    # Copy and paste this command
    notepad final-sop.md
    ```
  instruction_4: |
    ```bash
    # Paste content (Ctrl+V)
    ```
  instruction_5: |
    ```bash
    # Copy and paste this command (Ctrl+S)
    # Save the file
    ```
  instruction_6: |
    ```powershell
    # Copy and paste this command to check line count
    (Get-Content final-sop.md | Measure-Object -Line).Lines
    ```
  handoffs: 6
  format: "Each step in clean code fence"
  reason: "User might miss step 4 if bundled, and must never type manually"
```

---

## EXAMPLES OF USER ATOMIC STEPS WITH CLEAN CODE BOXES

### ❌ WRONG - Combined User Actions
```markdown
## Next Step:
User: Merge the three SOP chunks, delete old files, commit and push to GitHub, then verify deployment
```
**Problem:** If user forgets step 2, whole sequence breaks
**Problem:** User has to type commands manually

### ✅ CORRECT - Atomic User Actions with Clean Code Boxes
```markdown
## Next Atomic Step:
**Platform:** User
**Mode:** MANUAL
**Action:** Merge SOP chunks into final file

**Execute:**
```powershell
# Copy and paste this entire block
$part1 = Get-Content "final-sop-part1.md" -Raw
$part2 = Get-Content "final-sop-part2.md" -Raw  
$part3 = Get-Content "final-sop-part3.md" -Raw
$combined = $part1 + $part2 + $part3
$combined | Out-File "final-sop-v4.2.md" -Encoding UTF8
```

**Expected Proof:**
- File exists: final-sop-v4.2.md
- Line count: ~3000
- All sections present: 1-53

[After verification]

## Next Atomic Step:
**Platform:** User  
**Mode:** MANUAL
**Action:** Delete old files

**Execute:**
```powershell
# Copy and paste this command
Remove-Item "nervous-system.md" -Force
```

**Expected Proof:**
- File no longer exists
- Git status shows deletion

[After verification]

## Next Atomic Step:
**Platform:** User
**Mode:** MANUAL
**Action:** Commit and push changes

**Execute:**
```bash
# Copy and paste these commands one by one
git add .
git commit -m "Merge SOP v4.2 complete"
git push origin main
```

**Expected Proof:**
- Commit successful
- Push successful
- Changes visible on GitHub
```

---

## THE USER MANUAL STEP PROTOCOL v4.2

### 1. Identify Manual Requirements
```yaml
if_user_must:
  - edit_file: ATOMIC + CLEAN_CODE_FENCE
  - run_command: ATOMIC + CLEAN_CODE_FENCE
  - check_result: ATOMIC + CLEAN_CODE_FENCE
  - make_decision: ATOMIC + CLEAN_CODE_FENCE
  - copy_paste_between_apps: ATOMIC + CLEAN_CODE_FENCE
  - navigate_to_url: ATOMIC + CLEAN_CODE_FENCE
  - click_in_ui: ATOMIC + CLEAN_CODE_FENCE
```

### 2. Provide Clear Instructions in Clean Code Boxes
```markdown
## User Action Required:

**Step 1:**
```bash
# Copy and paste this command
cd C:/workspace/project-name
```
[Verify: Terminal in correct directory?]

**Step 2:**
```bash
# Copy and paste this command  
npm test
```
[Verify: All tests pass?]

**Step 3:**
```text
# Copy this URL to browser
http://localhost:3000/health
```
[Verify: Returns {"status": "ok"}?]

**Step 4:**
Report result: [What you see]

NOT: "Run tests and deploy if passing"
```

### 3. Verify Each Step with Trust Tracking
```yaml
after_each_user_action:
  qb_asks: "What was the result?"
  user_provides: "Proof or error"
  qb_continues: "Based on proof"
  trust_impact: "No change for successful atomic steps"
  trust_erosion: "-5% if user reports confusion or issues"
```

---

## SPECIAL CASES WITH CLEAN CODE BOXES

### Multi-File Merges
```yaml
NEVER:
  "Merge all 3 files and upload"
  
ALWAYS:
  Step 1: |
    ```powershell
    # Copy and paste to merge part 1
    $content1 = Get-Content "part1.md" -Raw
    $content1 | Out-File "final.md" -Encoding UTF8
    ```
  Step 2: |
    ```powershell
    # Copy and paste to append part 2
    $content2 = Get-Content "part2.md" -Raw
    $content2 | Out-File "final.md" -Append -Encoding UTF8
    ```
  Step 3: |
    ```powershell
    # Copy and paste to append part 3
    $content3 = Get-Content "part3.md" -Raw
    $content3 | Out-File "final.md" -Append -Encoding UTF8
    ```
  Step 4: |
    ```powershell
    # Copy and paste to verify line count
    (Get-Content "final.md" | Measure-Object -Line).Lines
    ```
  Step 5: |
    ```bash
    # Copy and paste to upload
    git add final.md && git commit -m "Merged files" && git push
    ```
```

### Environment Setup
```yaml
NEVER:
  "Configure your environment and test"
  
ALWAYS:
  Step 1: |
    ```bash
    # Copy and paste to create .env file
    echo "DATABASE_URL=your_url_here" > .env
    ```
  Step 2: |
    ```bash
    # Copy and paste to add API key
    echo "API_KEY=your_key_here" >> .env
    ```
  Step 3: |
    ```bash
    # Copy and paste to add port
    echo "PORT=3000" >> .env
    ```
  Step 4: |
    ```bash
    # Copy and paste to verify file
    cat .env
    ```
  Step 5: |
    ```bash
    # Copy and paste to start server
    npm start
    ```
  Step 6: |
    ```text
    # Copy this URL to browser to verify
    http://localhost:3000/health
    ```
```

### Deployment Verification with Session Traces
```yaml
NEVER:
  "Deploy and verify it's working"
  
ALWAYS:
  Step 1: |
    ```bash
    # Copy and paste deployment command
    npm run deploy
    ```
  Step 2: |
    ```bash
    # Copy and paste to wait for completion
    echo "Waiting for deployment completion..."
    ```
  Step 3: |
    ```text
    # Copy deployment URL to browser
    https://your-app.vercel.app
    ```
  Step 4: |
    ```text
    # Copy this URL to test upload
    https://your-app.vercel.app/upload
    ```
  Step 5: |
    ```bash
    # Copy and paste to check session trace
    curl https://your-app.vercel.app/api/session-status
    ```
  Step 6: |
    ```markdown
    # Verify all 6 trace points complete:
    ✓ Creation
    ✓ Data Attach  
    ✓ Processing
    ✓ Completion
    ✓ UI Render
    ✓ Export Ready
    ```
```

---

## MANUAL BRIDGE PREVENTION (FROM v3.1)

### How User Atomic Steps Prevent Bridges
```yaml
problem_pattern:
  user_as_bridge: "Rob copying outputs between agents"
  manual_pastes: ">5 per hour = architectural failure"
  historical_example: "40+ pastes in failed builds"
  
solution_pattern:
  individual_steps: "Each user action verified separately"
  clean_code_boxes: "No manual typing or interpretation"
  atomic_verification: "Proof after each step"
  trust_tracking: "Objective success metrics"
  
enforcement:
  count_pastes: "Every manual operation logged"
  warning_at: "4 pastes per hour"
  halt_at: "5 pastes per hour"
  remember: "40+ pastes = architectural catastrophe"
```

---

## THE OVERRIDE

```bash
# If user is experienced and wants bundled instructions
"Pied Piper 1x: combine user manual steps"

# Return to safety
"Pied Piper cancel: combine user manual steps"

# If user wants to type manually (NOT RECOMMENDED)
"Pied Piper 1x: manual typing OK"
```

---

## SESSION TRACE INTEGRATION

### User Steps Must Support Trace Propagation
```yaml
when_user_tests_deployment:
  step_1: "Access deployed URL"
  step_2: "Upload test file"
  step_3: "Verify processing occurs"
  step_4: "Check session ID propagation"
  step_5: "Confirm all 6 traces complete"
  step_6: "Export data to verify retrieval"
  
  each_step_verifies:
    - "Session ID present and unchanged"
    - "Trace point completed"
    - "No orphaned sessions"
    
  if_trace_missing:
    action: "HALT - session orphaned"
    recovery: "Investigate trace propagation"
    document: "/ops/orphaned-sessions.md"
```

---

## TRUST IMPLICATIONS FOR USER STEPS

### Trust Tracking for User Actions
```yaml
successful_user_step:
  trust_impact: "Neutral (0%)"
  reason: "Expected behavior"
  
user_confusion_or_error:
  trust_impact: "-5% QB guidance clarity"
  reason: "Instructions not clear enough"
  
user_skips_verification:
  trust_impact: "-10% process compliance"
  reason: "Safety step bypassed"
  
user_reports_manual_typing_needed:
  trust_impact: "-10% QB code box failure"
  reason: "Clean code box rule violated"
  
perfect_user_execution:
  trust_impact: "+5% if complex sequence"
  reason: "Good instruction design confirmed"
```

---

## THE GOLDEN RULES v4.2

### For Agent Code:
**COMBINE MAXIMUM** - 500 lines in one clean code fence

### For User Manual Actions:
**SEPARATE EVERYTHING** - One action per step, each in clean code fence

### For ALL Instructions:
**CLEAN CODE BOXES ALWAYS** - Zero manual typing ever

### The Reason:
- **Agents:** Can paste 500 lines perfectly
- **Users:** Might skip line 237 in manual process  
- **Agents:** Have undo/retry built in
- **Users:** Can't undo partial manual changes
- **Both:** Must never type manually - everything paste-ready

---

## ENFORCEMENT v4.2

**If QB combines manual user steps that could be error-prone, QB has failed**

**If user has to do 3 manual things and QB provides them as one instruction, QB has failed**

**If QB provides ANY instruction that requires manual typing, QB has failed**

**If user reports needing to type anything manually, QB has failed**

**Exception: Experienced user explicitly requests combined steps via Pied Piper**

---

## SUMMARY v4.2

```yaml
atomic_steps_apply_to:
  agents:
    rule: "Maximum safe combination"
    size: "Complete features (500+ lines)"
    format: "Single clean code fence"
    reason: "Speed through fewer handoffs"
    
  users:
    rule: "Individual manual actions"
    size: "One action per step"
    format: "Each step in clean code fence"
    reason: "Humans miss things in lists and can't type reliably"
    
the_key_insight: "Agents are perfect at execution, humans are not"
the_v4.2_addition: "Clean code boxes prevent ALL manual typing"
the_trust_element: "User confusion indicates QB failure"
the_bridge_prevention: "Individual steps prevent architectural failure"
```

**When the user MUST do manual work, especially 2-3 steps, EACH becomes atomic AND goes in clean code boxes**

**CRITICAL v4.2: Even single user actions must be in clean code fences to ensure zero manual typing**