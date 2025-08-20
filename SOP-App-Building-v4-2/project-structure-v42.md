# Project Structure Template v4.2
**Standard folder layout with v4.2 enhancements**
**Clean Code Box Commands - Zero Manual Typing**
**Session Trace Monitoring - Manual Bridge Detection - Trust Tracking**

---

## FOLDER_CREATION_COMMAND_V42

```powershell
# COMPLETE PASTE-READY BLOCK - Zero edits needed
# Enhanced for v4.2 tracking and monitoring

$projectName = "your-project-name"  # CHANGE THIS ONLY
$basePath = "C:/workspace"
$sessionDate = Get-Date -Format 'yyyy-MM-dd'
$sessionName = "$projectName-session-1-$sessionDate"
$sessionId = "sess-" + (Get-Date -Format 'HHmmss')

# Create all folders in one operation (v4.2 enhanced)
$folders = @(
    "$basePath/$projectName",
    "$basePath/$projectName/src",
    "$basePath/$projectName/src/server",
    "$basePath/$projectName/src/client", 
    "$basePath/$projectName/src/shared",
    "$basePath/$projectName/docs",
    "$basePath/$projectName/planning",
    "$basePath/$projectName/continuity",
    "$basePath/$projectName/continuity/$sessionName",
    "$basePath/$projectName/fixtures",
    "$basePath/$projectName/qa",
    "$basePath/$projectName/qa/proofs",
    "$basePath/$projectName/qa/test-results",
    "$basePath/$projectName/qa/session-traces",  # NEW v4.2
    "$basePath/$projectName/ops",
    "$basePath/$projectName/ops/amendments",
    "$basePath/$projectName/ops/trust-tracking",  # NEW v4.2
    "$basePath/$projectName/ops/manual-paste-log",  # NEW v4.2
    "$basePath/$projectName/ops/terminal-monitoring",  # NEW v4.2
    "$basePath/$projectName/ops/agent-violations",  # NEW v4.2
    "$basePath/$projectName/.github",
    "$basePath/$projectName/.github/workflows"
)

# Create directories
$folders | ForEach-Object { 
    New-Item -ItemType Directory -Force -Path $_ | Out-Null
}

# Initialize git
Set-Location "$basePath/$projectName"
git init --quiet
git branch -M main

# Create initial files with v4.2 tracking
@"
# $projectName
Session: $sessionName
Status: Pre-flight
Trust Level: 100%
Session ID: $sessionId
Manual Paste Count: 1 (this creation block)
"@ | Out-File README.md -Encoding UTF8

@"
# Build State v4.2
Project: $projectName
Status: Pre-flight
Session: 1
Date: $sessionDate
Session ID: $sessionId
Trust Level: 100%
Manual Paste Count: 1/5 per hour
Terminal Status: Active
Orphan Sessions: 0
"@ | Out-File ops/state.md -Encoding UTF8

# Create v4.2 enhanced continuity prompt
@"
## CONTINUITY PROMPT #1 | Build: $sessionName

### SESSION INFO
- **Project Name:** $projectName
- **Session Number:** 1
- **Session ID:** $sessionId
- **Local Path:** $basePath/$projectName/
- **Git Repo:** github.com/[user]/$projectName (pending)
- **Trust Level:** 100%
- **Manual Paste Count:** 1/5 per hour
- **Terminal Status:** Active

### SESSION TRACE POINTS (v4.2)
| Trace Point | Status | Session ID | Timestamp |
|-------------|--------|------------|-----------|
| 1. Creation | ✓ | $sessionId | $(Get-Date -Format 'HH:mm:ss') |
| 2. Data Attach | PENDING | - | - |
| 3. Processing | PENDING | - | - |
| 4. Complete | PENDING | - | - |
| 5. UI Render | PENDING | - | - |
| 6. Export Ready | PENDING | - | - |

### ACTIVE OVERRIDES (Pied Piper)
| Rule/Process | Override | Timestamp | Declaration |
|-------------|----------|-----------|-------------|
| (none yet) | | | |

### MANUAL BRIDGE TRACKING (v4.2)
- **Current Hour Pastes:** 1/5 (SAFE)
- **Bridge Pattern:** None detected
- **Historical Alert:** >5 = architecture failure
- **Remember:** 40+ pastes = catastrophic failure pattern

### TRUST TRACKING (v4.2)
- **Starting Trust:** 100%
- **Current Trust:** 100%
- **Last Change:** None yet
- **Desktop Icon:** Not created
- **Agent Violations:** None

### TERMINAL MONITORING (v4.2)
- **Last Output:** $(Get-Date -Format 'HH:mm:ss')
- **Stall Count:** 0
- **Restart Count:** 0
- **Status:** Active

### Next Atomic Step
**Platform:** QB Orchestrator
**Mode:** DO
**Action:** Create app definition or invoke override
**Expected:** Rule Zero validation or Pied Piper bypass

[Do not repeat this back - execute next step]
"@ | Out-File "continuity/$sessionName/prompt.md" -Encoding UTF8

# Create v4.2 tracking files
@"
# Session Trace Log v4.2
Session ID: $sessionId
Project: $projectName
Date: $sessionDate

## Trace Points Status
1. Creation: COMPLETE at $(Get-Date -Format 'HH:mm:ss')
2. Data Attach: PENDING
3. Processing: PENDING  
4. Complete: PENDING
5. UI Render: PENDING
6. Export Ready: PENDING

## Orphan Detection
- Missing traces will be logged here
- Daily limit: 3 orphans before architecture review
- Current orphan count: 0
"@ | Out-File "qa/session-traces/trace-log-$sessionId.md" -Encoding UTF8

@"
# Manual Paste Tracking v4.2
Session: $sessionName
Hour: $(Get-Date -Format 'HH:00')

## Paste Operations
1. $(Get-Date -Format 'HH:mm:ss') - Project creation block (this operation)

## Thresholds
- Warning: 4 pastes/hour
- HALT: 5 pastes/hour  
- Catastrophic historical pattern: 40+ pastes
- Architecture failure trigger: >5/hour

## Current Status: 1/5 (EXCELLENT)
"@ | Out-File "ops/manual-paste-log/paste-log-$(Get-Date -Format 'yyyy-MM-dd-HH').md" -Encoding UTF8

@"
# Trust Tracking Log v4.2
Session: $sessionName
Starting Trust: 100%

## Trust Changes
- $(Get-Date -Format 'HH:mm:ss'): Started at 100%

## Trust Thresholds
- 100%: Full autonomy
- 75-99%: Standard oversight  
- 50-74%: Restricted mode
- 25-49%: Outcome mode only
- 1-24%: Single actions only
- 0%: Agent replaced permanently

## Desktop Icon Status
- Created: NO
- Working: NO
- Trust Bonus: Pending (+60% when working)
"@ | Out-File "ops/trust-tracking/trust-log-$sessionId.md" -Encoding UTF8

@"
# Terminal Monitoring Log v4.2
Session: $sessionName

## Activity Log
- $(Get-Date -Format 'HH:mm:ss'): Session started
- Status: Active
- Last output: $(Get-Date -Format 'HH:mm:ss')

## Stall Detection
- Timeout threshold: 60 seconds
- Auto-kill enabled: YES
- Stall count: 0
- Restart count: 0

## Current Status: ACTIVE
"@ | Out-File "ops/terminal-monitoring/terminal-log-$sessionId.md" -Encoding UTF8

@"
# Agent Violation Tracking v4.2
Session: $sessionName

## Violation Patterns
- VS Code: Path validation failures
- GitHub Copilot: STOP command ignoring
- Perplexity: Silent truncation
- Claude: localStorage usage attempts
- Vibe Coding: Multi-block generation

## Current Session Violations: 0

## Trust Impact Scale
- Minor violation: -10% to -25%
- Major violation: -50%
- False WORKS claim: -100% (permanent replacement)

## Agent Status: All at 100% trust
"@ | Out-File "ops/agent-violations/violations-$sessionId.md" -Encoding UTF8

@"
node_modules/
.env
.env.local
*.log
dist/
build/
.DS_Store
# v4.2 specific
/ops/trust-tracking/
/ops/manual-paste-log/
/ops/terminal-monitoring/
/qa/session-traces/
"@ | Out-File .gitignore -Encoding UTF8

# Success confirmation with v4.2 metrics
Write-Host "SUCCESS: Project structure created at $basePath/$projectName" -ForegroundColor Green
Write-Host "Session ID: $sessionId" -ForegroundColor Cyan
Write-Host "Manual Paste Count: 1/5 for this hour" -ForegroundColor Yellow
Write-Host "Trust Level: 100%" -ForegroundColor Green
Write-Host "Session Traces: 1/6 complete" -ForegroundColor Yellow
Write-Host "Terminal Status: Active" -ForegroundColor Green
Get-ChildItem -Directory | Select-Object Name
```

---

## STANDARD_STRUCTURE_V42

```yaml
project_root:
  name_format: "[project-name]/"
  location: "C:/workspace/[project-name]/"
  
  directories:
    github:
      path: ".github/"
      contents:
        workflows: "CI/CD workflows (main branch only)"
        
    src:
      path: "src/"
      subdirs:
        server: "Backend code"
        client: "Frontend code"
        shared: "Shared utilities"
        
    docs:
      path: "docs/"
      files:
        - README.md: "Main documentation"
        - API.md: "API documentation"
        - ARCHITECTURE.md: "Technical design"
        
    planning:
      path: "planning/"
      files:
        - app-definition.md: "Complete app spec"
        - mockups/: "Visual designs"
      override: "Pied Piper 1x: skip app definition"
      
    continuity:
      path: "continuity/"
      session_format: "[project]-session-[#]-[date]/"
      session_contents:
        - prompt.md: "v4.2 enhanced continuity prompt"
        - aar.md: "After Action Review (mandatory)"
        - overrides.md: "Pied Piper [N]x log"
        - summary.md: "Session summary"
        - trust-changes.md: "Trust trajectory log"  # NEW v4.2
        - paste-count.md: "Manual paste operations"  # NEW v4.2
      rule: "CANNOT_SKIP_AAR"
      
    fixtures:
      path: "fixtures/"
      contents:
        - sample-input.*: "Test input data"
        - expected-output.*: "Expected results"
      override: "Pied Piper 1x: use mock data"
      
    qa:
      path: "qa/"
      subdirs:
        test-results: "Test outputs"
        proofs: "Execution proofs"
        session-traces: "v4.2 session tracking"  # NEW
      override: "Pied Piper 1x: skip tests"
      
    ops:
      path: "ops/"
      files:
        - state.md: "Current build state"
        - sop-v4.md: "Active SOP version"
        - amendments/: "Override logs"
      subdirs:  # NEW v4.2 operational tracking
        trust-tracking: "Trust percentage logs"
        manual-paste-log: "Paste operation tracking"
        terminal-monitoring: "Terminal stall detection"
        agent-violations: "Agent failure patterns"
        
  root_files:
    - .env.example: "Environment template"
    - .gitignore: "Git exclusions (v4.2 enhanced)"
    - package.json: "Node dependencies"
    - README.md: "Project overview with metrics"
```

---

## SESSION_FOLDERS_V42

### NAMING_PATTERN_V42
```yaml
format: "[project]-session-[#]-[YYYY-MM-DD]"
session_id_format: "sess-[HHMMSS]"

examples:
  - pdf-processor-session-1-2025-01-21
  - pdf-processor-session-2-2025-01-22
  - pdf-processor-session-3-2025-01-23

location: "continuity/"

structure_v42:
  continuity/:
    session-1-2025-01-21/:
      - prompt.md: "v4.2 enhanced continuity"
      - prompt-final.md: "Closing continuity"
      - aar.md: "After Action Review (mandatory)"
      - overrides.md: "Pied Piper [N]x log"
      - summary.md: "Accomplishments"
      - blockers.md: "Unresolved issues"
      - trust-changes.md: "Trust trajectory (NEW v4.2)"
      - paste-operations.md: "Manual paste log (NEW v4.2)"
      - session-traces.md: "6-point trace log (NEW v4.2)"
      - terminal-activity.md: "Terminal monitoring (NEW v4.2)"
      - agent-performance.md: "Agent success/violation rates (NEW v4.2)"
```

### SESSION_CONTENTS_TEMPLATE_V42
```markdown
# prompt.md template v4.2
## CONTINUITY PROMPT #[N] | Build: [project]-session-[#]-[date]

### SESSION INFO (v4.2 Enhanced)
- Trust Level: [%]
- Manual Paste Count: [#/5 per hour]
- Session ID: [sess-HHMMSS]
- Terminal Status: [Active|Stalled|Restarted]

### SESSION TRACE POINTS (v4.2 Mandatory)
| Trace Point | Status | Session ID | Timestamp |
|-------------|--------|------------|-----------|
| 1. Creation | [✓|PENDING] | [id] | [time] |
| 2. Data Attach | [✓|PENDING] | [id] | [time] |
| 3. Processing | [✓|PENDING] | [id] | [time] |
| 4. Complete | [✓|PENDING] | [id] | [time] |
| 5. UI Render | [✓|PENDING] | [id] | [time] |
| 6. Export Ready | [✓|PENDING] | [id] | [time] |

### MANUAL BRIDGE TRACKING (v4.2)
- Current Hour: [#/5 pastes]
- Pattern: [Normal|Warning|CRITICAL]
- Bridge Detection: [None|Active]

### ACTIVE OVERRIDES (Pied Piper)
| Rule/Process | Override | Timestamp | Declaration |
|-------------|----------|-----------|-------------|
| [rule] | [override] | [time] | Pied Piper [N]x |

# trust-changes.md template v4.2
## Trust Trajectory Log
Session: [session-name]
Starting: [%]

### Trust Events
- [timestamp]: [event] ([±%]) → [new total]
- [timestamp]: Desktop icon working (+60%) → [total]

### Agent Performance
| Agent | Actions | Success Rate | Trust Impact |
|-------|---------|--------------|--------------|

# paste-operations.md template v4.2
## Manual Paste Log
Session: [session-name]
Target: <5 pastes/hour

### Paste Events
- [timestamp]: [description] - Count: [#/5]
- [timestamp]: [Block type] - Count: [#/5]

### Threshold Monitoring
- Warning: 4/hour
- HALT: 5/hour
- Status: [SAFE|WARNING|CRITICAL]

# session-traces.md template v4.2
## Session Trace Monitoring
Session ID: [sess-id]

### Trace Completion Status
- All 6 Complete: [YES/NO]
- Orphan Risk: [LOW/HIGH]
- Daily Orphan Count: [#/3]

### Trace Details
[Full trace log with timestamps]

# terminal-activity.md template v4.2
## Terminal Monitoring
Session: [session-name]

### Activity Log
- [timestamp]: [activity]
- Last Output: [timestamp]
- Stall Count: [#]
- Restart Count: [#]

### Performance
- Longest Wait: [seconds]
- Under 60s Limit: [YES/NO]

# agent-performance.md template v4.2
## Agent Success/Violation Tracking
Session: [session-name]

### Performance Summary
| Agent | Blocks | Success % | Violations | Trust Impact |
|-------|--------|-----------|------------|--------------|

### Violation Details
[Specific patterns and consequences]

# aar.md template v4.2
[Generated by outside agent - enhanced with v4.2 metrics]
- Manual paste analysis
- Session trace health
- Trust trajectory
- Terminal efficiency
- Agent violation patterns
```

---

## V42_TRACKING_COMMANDS

### Session_Monitoring_Script
```powershell
# V4.2 ENHANCED SESSION MONITORING - Copy and paste complete block

function Monitor-SessionV42 {
    param(
        [string]$ProjectPath = (Get-Location),
        [string]$SessionId = "sess-" + (Get-Date -Format 'HHmmss')
    )
    
    $timestamp = Get-Date -Format 'HH:mm:ss'
    
    # Update trust tracking
    $trustPath = "$ProjectPath/ops/trust-tracking/trust-log-$SessionId.md"
    if (Test-Path $trustPath) {
        Add-Content $trustPath "`n- $timestamp`: Session monitoring check"
    }
    
    # Update manual paste count
    $pastePath = "$ProjectPath/ops/manual-paste-log/paste-log-$(Get-Date -Format 'yyyy-MM-dd-HH').md"
    if (Test-Path $pastePath) {
        $pasteCount = (Get-Content $pastePath | Where-Object { $_ -match "^\d+\." }).Count
        Write-Host "Manual Paste Count: $pasteCount/5 for this hour" -ForegroundColor $(if($pasteCount -lt 4){"Green"}elseif($pasteCount -eq 4){"Yellow"}else{"Red"})
    }
    
    # Check session traces
    $tracePath = "$ProjectPath/qa/session-traces/trace-log-$SessionId.md"
    if (Test-Path $tracePath) {
        $completeTraces = (Get-Content $tracePath | Where-Object { $_ -match "COMPLETE" }).Count
        Write-Host "Session Traces: $completeTraces/6 complete" -ForegroundColor $(if($completeTraces -eq 6){"Green"}else{"Yellow"})
    }
    
    # Terminal status check
    $terminalPath = "$ProjectPath/ops/terminal-monitoring/terminal-log-$SessionId.md"
    if (Test-Path $terminalPath) {
        Add-Content $terminalPath "`n- $timestamp`: Monitoring check - Active"
        Write-Host "Terminal Status: Active" -ForegroundColor Green
    }
    
    # Agent violation check
    $violationPath = "$ProjectPath/ops/agent-violations/violations-$SessionId.md"
    if (Test-Path $violationPath) {
        $violations = (Get-Content $violationPath | Where-Object { $_ -match "VIOLATION:" }).Count
        Write-Host "Agent Violations: $violations" -ForegroundColor $(if($violations -eq 0){"Green"}else{"Red"})
    }
    
    Write-Host "`nV4.2 Session Health: $(if($pasteCount -lt 5 -and $violations -eq 0){"EXCELLENT"}else{"NEEDS ATTENTION"})" -ForegroundColor $(if($pasteCount -lt 5 -and $violations -eq 0){"Green"}else{"Yellow"})
}

# Run monitoring
Monitor-SessionV42
```

### Trust_Update_Command
```powershell
# TRUST LEVEL UPDATE - Copy and paste complete block

function Update-TrustV42 {
    param(
        [string]$ProjectPath = (Get-Location),
        [string]$SessionId,
        [int]$TrustChange,
        [string]$Reason,
        [string]$Agent = "Unknown"
    )
    
    $timestamp = Get-Date -Format 'HH:mm:ss'
    $trustPath = "$ProjectPath/ops/trust-tracking/trust-log-$SessionId.md"
    
    # Get current trust level
    $currentTrust = 100  # Default
    if (Test-Path $trustPath) {
        $lastEntry = Get-Content $trustPath | Where-Object { $_ -match "Current Trust:" } | Select-Object -Last 1
        if ($lastEntry -match "(\d+)%") {
            $currentTrust = [int]$matches[1]
        }
    }
    
    $newTrust = [Math]::Max(0, $currentTrust + $TrustChange)
    $changeSymbol = if ($TrustChange -gt 0) { "+" } else { "" }
    
    # Log trust change
    Add-Content $trustPath "`n- $timestamp`: $Agent - $Reason ($changeSymbol$TrustChange%) → $newTrust%"
    Add-Content $trustPath "`nCurrent Trust: $newTrust%"
    
    # Update agent violations if negative
    if ($TrustChange -lt 0) {
        $violationPath = "$ProjectPath/ops/agent-violations/violations-$SessionId.md"
        Add-Content $violationPath "`n- $timestamp`: $Agent VIOLATION: $Reason ($changeSymbol$TrustChange%)"
    }
    
    # Display result
    $statusColor = switch ($newTrust) {
        { $_ -ge 75 } { "Green" }
        { $_ -ge 50 } { "Yellow" }
        { $_ -ge 25 } { "Orange" }
        default { "Red" }
    }
    
    Write-Host "Trust Update: $currentTrust% → $newTrust% ($changeSymbol$TrustChange%)" -ForegroundColor $statusColor
    Write-Host "Reason: $Reason" -ForegroundColor White
    Write-Host "Agent: $Agent" -ForegroundColor White
    
    # Check thresholds
    if ($newTrust -eq 0) {
        Write-Host "CRITICAL: Agent $Agent must be replaced permanently" -ForegroundColor Red
    } elseif ($newTrust -lt 25) {
        Write-Host "WARNING: Single actions only for $Agent" -ForegroundColor Yellow
    } elseif ($newTrust -lt 50) {
        Write-Host "WARNING: Outcome mode required" -ForegroundColor Yellow
    }
}

# Example usage:
# Update-TrustV42 -SessionId "sess-142201" -TrustChange 60 -Reason "Desktop icon working" -Agent "User"
# Update-TrustV42 -SessionId "sess-142201" -TrustChange -25 -Reason "Path validation failed" -Agent "VS Code"
```

### Manual_Paste_Logger
```powershell
# MANUAL PASTE LOGGER - Copy and paste complete block

function Log-ManualPasteV42 {
    param(
        [string]$ProjectPath = (Get-Location),
        [string]$Description,
        [string]$BlockType = "Code Block"
    )
    
    $timestamp = Get-Date -Format 'HH:mm:ss'
    $hour = Get-Date -Format 'yyyy-MM-dd-HH'
    $pastePath = "$ProjectPath/ops/manual-paste-log/paste-log-$hour.md"
    
    # Count current pastes for this hour
    $currentPastes = 0
    if (Test-Path $pastePath) {
        $currentPastes = (Get-Content $pastePath | Where-Object { $_ -match "^\d+\." }).Count
    }
    
    $newCount = $currentPastes + 1
    
    # Log the paste
    if (!(Test-Path $pastePath)) {
        @"
# Manual Paste Tracking v4.2
Hour: $hour
Project: $(Split-Path $ProjectPath -Leaf)

## Paste Operations
"@ | Out-File $pastePath -Encoding UTF8
    }
    
    Add-Content $pastePath "$newCount. $timestamp - $Description ($BlockType)"
    
    # Update status
    $status = switch ($newCount) {
        { $_ -le 3 } { "EXCELLENT" }
        4 { "WARNING" }
        { $_ -ge 5 } { "CRITICAL - HALT" }
    }
    
    $statusColor = switch ($newCount) {
        { $_ -le 3 } { "Green" }
        4 { "Yellow" }
        { $_ -ge 5 } { "Red" }
    }
    
    Add-Content $pastePath "`n## Current Status: $newCount/5 ($status)"
    
    Write-Host "Manual Paste Logged: $newCount/5 for hour" -ForegroundColor $statusColor
    Write-Host "Status: $status" -ForegroundColor $statusColor
    Write-Host "Description: $Description" -ForegroundColor White
    
    # Check thresholds
    if ($newCount -eq 4) {
        Write-Host "WARNING: Approaching 5-paste limit" -ForegroundColor Yellow
    } elseif ($newCount -ge 5) {
        Write-Host "CRITICAL: Manual bridge pattern detected - Architecture review required" -ForegroundColor Red
        Write-Host "Historical context: 40+ pastes = catastrophic failure" -ForegroundColor Red
    }
    
    return $newCount
}

# Example usage:
# Log-ManualPasteV42 -Description "Project creation block"
# Log-ManualPasteV42 -Description "Server.js complete file" -BlockType "500+ line block"
```

---

## VERIFICATION_COMMANDS_V42

```powershell
# V4.2 ENHANCED VERIFICATION - Copy complete block and run

function Verify-ProjectStructureV42 {
    param([string]$ProjectPath = (Get-Location))
    
    Write-Host "V4.2 PROJECT STRUCTURE VERIFICATION" -ForegroundColor Cyan
    Write-Host "=" * 40 -ForegroundColor Cyan
    
    # Check directory structure
    Write-Host "`nDIRECTORY STRUCTURE:" -ForegroundColor Yellow
    $requiredDirs = @(
        "src", "docs", "planning", "continuity", "fixtures", "qa", "ops",
        "qa/session-traces", "ops/trust-tracking", "ops/manual-paste-log", 
        "ops/terminal-monitoring", "ops/agent-violations"
    )
    
    foreach ($dir in $requiredDirs) {
        $exists = Test-Path "$ProjectPath/$dir"
        $status = if ($exists) { "✓" } else { "✗" }
        $color = if ($exists) { "Green" } else { "Red" }
        Write-Host "  $status $dir" -ForegroundColor $color
    }
    
    # Check v4.2 tracking files
    Write-Host "`nV4.2 TRACKING FILES:" -ForegroundColor Yellow
    $trackingFiles = Get-ChildItem "$ProjectPath/ops" -Recurse -Filter "*.md" | 
                     Where-Object { $_.Name -match "(trust-log|paste-log|terminal-log|violations)" }
    
    foreach ($file in $trackingFiles) {
        Write-Host "  ✓ $($file.Name)" -ForegroundColor Green
    }
    
    # Check git status
    Write-Host "`nGIT STATUS:" -ForegroundColor Yellow
    try {
        $gitStatus = git status --porcelain 2>$null
        if ($gitStatus) {
            Write-Host "  Modified files detected" -ForegroundColor Yellow
        } else {
            Write-Host "  ✓ Clean working directory" -ForegroundColor Green
        }
        
        $branch = git branch --show-current 2>$null
        Write-Host "  Current branch: $branch" -ForegroundColor White
    } catch {
        Write-Host "  ✗ Git not initialized" -ForegroundColor Red
    }
    
    # Check session tracking
    Write-Host "`nSESSION TRACKING:" -ForegroundColor Yellow
    $continuityFiles = Get-ChildItem "$ProjectPath/continuity" -Recurse -Filter "prompt.md"
    Write-Host "  Sessions found: $($continuityFiles.Count)" -ForegroundColor White
    
    $traceFiles = Get-ChildItem "$ProjectPath/qa/session-traces" -Filter "*.md" -ErrorAction SilentlyContinue
    Write-Host "  Trace logs: $($traceFiles.Count)" -ForegroundColor White
    
    # Check manual paste status
    Write-Host "`nMANUAL PASTE STATUS:" -ForegroundColor Yellow
    $currentHour = Get-Date -Format 'yyyy-MM-dd-HH'
    $pasteLog = "$ProjectPath/ops/manual-paste-log/paste-log-$currentHour.md"
    
    if (Test-Path $pasteLog) {
        $pasteCount = (Get-Content $pasteLog | Where-Object { $_ -match "^\d+\." }).Count
        $status = if ($pasteCount -le 3) { "EXCELLENT" } elseif ($pasteCount -eq 4) { "WARNING" } else { "CRITICAL" }
        $color = if ($pasteCount -le 3) { "Green" } elseif ($pasteCount -eq 4) { "Yellow" } else { "Red" }
        Write-Host "  Current hour: $pasteCount/5 ($status)" -ForegroundColor $color
    } else {
        Write-Host "  No paste activity this hour" -ForegroundColor Green
    }
    
    # Overall health check
    Write-Host "`nV4.2 HEALTH CHECK:" -ForegroundColor Yellow
    $hasRequiredDirs = ($requiredDirs | ForEach-Object { Test-Path "$ProjectPath/$_" }) -contains $false
    $hasTracking = $trackingFiles.Count -gt 0
    $gitOk = (git status 2>$null) -ne $null
    
    if (-not $hasRequiredDirs -and $hasTracking -and $gitOk) {
        Write-Host "  ✓ EXCELLENT - All v4.2 systems operational" -ForegroundColor Green
    } else {
        Write-Host "  ✗ ISSUES DETECTED - Check above for details" -ForegroundColor Red
    }
    
    # File count summary
    Write-Host "`nFILE SUMMARY:" -ForegroundColor Yellow
    $totalFiles = (Get-ChildItem -File -Recurse).Count
    $trackingFiles = (Get-ChildItem "ops" -File -Recurse -ErrorAction SilentlyContinue).Count
    Write-Host "  Total files: $totalFiles" -ForegroundColor White
    Write-Host "  Tracking files: $trackingFiles" -ForegroundColor White
    
    Write-Host "`nV4.2 verification complete." -ForegroundColor Cyan
}

# Run verification
Verify-ProjectStructureV42
```

---

## DEPLOYMENT_SPECIFIC_ADDITIONS_V42

```yaml
replit_additions_v42:
  files:
    - .replit: "Replit configuration"
    - replit.nix: "System packages"
    - ops/replit-monitoring.md: "Platform-specific tracking"
  
  config_example: |
    run = "npm start"
    entrypoint = "server.js"
    
    [env]
    PORT = "3000"
    SESSION_TRACKING = "enabled"
    TRUST_MONITORING = "enabled"
    
vercel_additions_v42:
  files:
    - vercel.json: "Deployment config"
    - next.config.js: "Next.js config"
    - ops/vercel-monitoring.md: "Deploy tracking"
    
  config_example: |
    {
      "builds": [
        { "src": "*.js", "use": "@vercel/node" }
      ],
      "env": {
        "TRUST_TRACKING": "enabled",
        "SESSION_TRACES": "enabled"
      }
    }
    
docker_additions_v42:
  files:
    - Dockerfile: "Container definition"
    - docker-compose.yml: "Service orchestration"
    - .dockerignore: "Build exclusions"
    - ops/docker-monitoring.md: "Container tracking"
```

---

## OVERRIDE_PATTERNS_V42

```yaml
common_overrides_v42:
  speed_mode:
    command: "Pied Piper 4x: skip planning, skip tests, skip tracking, deploy immediately"
    creates: "minimal structure, reduced monitoring"
    
  prototype_mode:
    command: "Pied Piper 3x: skip app definition, use mock data, relaxed paste limits"
    creates: "standard structure, flexible tracking"
    
  production_mode:
    command: "No overrides"
    creates: "complete structure with full v4.2 monitoring"
    
  monitoring_disabled:
    command: "Pied Piper 5x: skip trust tracking, skip paste counting, skip session traces, skip terminal monitoring, skip agent violations"
    creates: "structure without v4.2 enhancements"
```

---

## CRITICAL_RULES_V42

```yaml
enforcement:
  project_name:
    format: "lowercase-with-hyphens"
    drives: "all paths and references"
    change_after_creation: NEVER
    
  session_tracking:
    every_session_has_folder: true
    aar_required: true
    trust_tracking: mandatory
    paste_counting: mandatory
    session_traces: "all 6 required"
    override_aar: CANNOT_SYSTEM_CRITICAL
    
  continuity:
    from_step_1: true
    update_every_step: true
    track_overrides: true
    v42_enhancements: required
    
  clean_code_boxes:
    everything_in_fences: true
    zero_manual_typing: true
    paste_operations_logged: true
    
  manual_bridge_detection:
    paste_limit: "5/hour"
    architecture_failure: ">5/hour"
    catastrophic_pattern: "40+"
    
  trust_quantification:
    exact_percentages: required
    agent_tracking: mandatory
    desktop_icon_checkpoint: "+60%"
    
  session_traces:
    all_six_mandatory: true
    orphan_detection: enabled
    daily_limit: "3 orphans max"
    
  terminal_monitoring:
    stall_timeout: "60 seconds"
    auto_kill: enabled
    restart_logging: required
    
  deployment:
    not_working: "until user tested"
    working: "deployed + tested"
    desktop_icon: "primary checkpoint"
```

---

## THE_V42_DIFFERENCE

```yaml
new_in_v42:
  operational_discipline:
    - "Clean code boxes eliminate manual typing"
    - "Manual paste counting prevents architecture failure"
    - "Session traces provide complete visibility"
    - "Trust quantification enables precise adjustments"
    - "Terminal monitoring prevents stalls"
    - "Agent violation tracking improves reliability"
    - "Desktop icon provides reliable checkpoint"
    
  tracking_systems:
    - "Every paste operation logged"
    - "Trust changes tracked to exact percentages"
    - "All 6 session traces monitored"
    - "Terminal activity continuously watched"
    - "Agent performance quantified"
    - "Orphan session detection"
    
  failure_prevention:
    - "40-hour lesson: Rule Zero enforcement"
    - "5-paste limit prevents manual bridge"
    - "60-second timeout prevents terminal stalls"
    - "Binary proof eliminates hedging"
    - "Trust thresholds trigger interventions"
    - "AAR captures all lessons"
```

---

**This structure is created ONCE per project with v4.2 enhancements**
**Session folders track trust, pastes, traces, and terminal activity**
**Clean code boxes ensure zero manual typing**
**Manual bridge detection prevents catastrophic failure patterns**
**Session traces provide complete operational visibility**
**Trust tracking quantifies exact agent performance**
**Pied Piper [N]x overrides tracked but structure remains disciplined**