#region === CONFIG ===
$ErrorActionPreference = 'Stop'

# Session constants
$ProjectName   = 'sos-assessment-automation-tool'
$SessionNumber = 1
$Today         = Get-Date -Format 'yyyy-MM-dd'
$SessionName   = "$ProjectName-session-$SessionNumber-$Today"
$SessionId     = 'sess-' + (Get-Date -Format 'HHmmss')
$TrustLevel    = 50 # starting from continuity prompt #1
$ManualPasteCountHour = 0

# Paths
$ProjectPath = 'C:\Users\feket\OneDrive\Desktop\excelsior\r_staff\r_3\Deployed_Code_Op_Locations\SOS-Assessment-Automation-Tool'
$GitRemoteUrl = ''  # blank; repo not created yet

# Derived paths
$ContinuityDir = Join-Path $ProjectPath "continuity\$SessionName"
$OpsDir        = Join-Path $ProjectPath 'ops'
$QAPath        = Join-Path $ProjectPath 'qa\session-traces'
$GhWorkflows   = Join-Path $ProjectPath '.github\workflows'

# Colors (fallback-safe)
function Info($msg){ Write-Host $msg -ForegroundColor Cyan }
function Good($msg){ Write-Host $msg -ForegroundColor Green }
function Warn($msg){ Write-Host $msg -ForegroundColor Yellow }
function Bad($msg){ Write-Host $msg -ForegroundColor Red }
#endregion === CONFIG ===


#region === CREATE FOLDERS (v4.2 structure) ===
Info "Creating v4.2 project structure at: $ProjectPath"
$Folders = @(
  $ProjectPath,
  (Join-Path $ProjectPath 'src'),
  (Join-Path $ProjectPath 'docs'),
  (Join-Path $ProjectPath 'planning'),
  (Join-Path $ProjectPath 'continuity'),
  $ContinuityDir,
  (Join-Path $ProjectPath 'fixtures'),
  (Join-Path $ProjectPath 'qa'),
  $QAPath,
  $OpsDir,
  (Join-Path $OpsDir 'trust-tracking'),
  (Join-Path $OpsDir 'manual-paste-log'),
  (Join-Path $OpsDir 'terminal-monitoring'),
  (Join-Path $OpsDir 'agent-violations'),
  (Join-Path $ProjectPath '.github'),
  $GhWorkflows
)
foreach($f in $Folders){ New-Item -ItemType Directory -Force -Path $f | Out-Null }
Good  "Folders ensured."
#endregion


#region === INITIAL FILES & GUARDRAILS ===
Info "Writing README.md and guardrail files..."

# README.md
@"
# $ProjectName

**Session:** $SessionName  
**Status:** Pre-flight (Phase -1 — Git Repository)  
**Rule Zero:** NOT VALIDATED (no ingestion proof yet)  
**Trust Level:** $TrustLevel%  
**Session ID:** $SessionId

This repo is managed under SOP v4.2: clean code boxes, binary proof, session traces, manual bridge detection, and quantified trust.
"@ | Out-File (Join-Path $ProjectPath 'README.md') -Encoding UTF8

# .gitignore
@"
# Node / Python / OS common
node_modules/
dist/
build/
*.log
.env
.env.*
.DS_Store
Thumbs.db

# v4.2 operational logs (kept, but optional to ignore in VCS)
ops/trust-tracking/
ops/manual-paste-log/
ops/terminal-monitoring/
qa/session-traces/
"@ | Out-File (Join-Path $ProjectPath '.gitignore') -Encoding UTF8

# .gitattributes (normalize line endings; optional but helpful)
@"
* text=auto
"@ | Out-File (Join-Path $ProjectPath '.gitattributes') -Encoding ASCII

# /ops/state.md
@"
# Build State v4.2
Project: $ProjectName
Phase: -1 (Git Repository)
Date: $Today
Session: $SessionNumber
Session ID: $SessionId
Trust Level: $TrustLevel%
Manual Paste Count (hour): $ManualPasteCountHour/5
Terminal Status: N/A
"@ | Out-File (Join-Path $OpsDir 'state.md') -Encoding UTF8

# /continuity/[session]/prompt.md (v4.2 continuity)
@"
## CONTINUITY PROMPT #1 | Build: $SessionName

### SESSION INFO
- **Project Name:** $ProjectName
- **Session Number:** $SessionNumber
- **Session Name:** $SessionName
- **Local Path:** $ProjectPath
- **Git Repo:** (not created)
- **Session Duration:** (live)
- **Trust Level:** $TrustLevel%
- **Manual Paste Count:** $ManualPasteCountHour/5 (this hour)
- **Terminal Status:** N/A

### ACTIVE OVERRIDES (Pied Piper)
| Rule/Process | Override | Timestamp | Declaration |
|-------------|----------|-----------|-------------|
| (none) | - | - | - |

### BUILD STATE
- **Current Phase:** -1 — Git Repository
- **Rule Zero Status:** NOT VALIDATED
- **Last Successful Action:** Project path confirmed
- **Current Blockers:** Repo not initialized; no ingestion proof
- **Deployment Status:** Not deployed
- **Working Status:** NOT WORKING (v4.2 requires deployed + user tested + 6 traces)

### PROOF TRACKING
- **Last Proof Received:** None
- **Proofs Pending:** Git repo init; guardrails committed

### ATOMIC EXECUTION STATUS
| Platform | Last Block Size | Proof Status | Success | Trust Impact |
|----------|------------------|--------------|---------|--------------|
| PowerShell Agent | 500+ lines | PENDING | - | Pending |

### SESSION TRACE POINTS (CRITICAL v4.2)
| Trace Point | Status | Session ID | Timestamp | Notes |
|-------------|--------|------------|-----------|-------|
| 1. Creation | PENDING | - | - | Start after git init |
| 2. Data Attach | PENDING | - | - | - |
| 3. Processing | PENDING | - | - | - |
| 4. Complete | PENDING | - | - | - |
| 5. UI Render | PENDING | - | - | - |
| 6. Export Ready | PENDING | - | - | - |

### MANUAL PASTE COUNT (v4.2)
- Current Hour: $ManualPasteCountHour/5 (SAFE)

### NEXT ACTION (QB)
- Initialize Git, add guardrails, first commit with binary proof.

[End of continuity]
"@ | Out-File (Join-Path $ContinuityDir 'prompt.md') -Encoding UTF8

# /qa/session-traces/trace-log-[session].md
@"
# Session Trace Log v4.2
Session ID: $SessionId
Project: $ProjectName
Date: $Today

## Trace Points
1. Creation: PENDING
2. Data Attach: PENDING
3. Processing: PENDING
4. Complete: PENDING
5. UI Render: PENDING
6. Export Ready: PENDING

## Orphan Detection
- Daily limit: 3 orphans before architecture review
"@ | Out-File (Join-Path $QAPath "trace-log-$SessionId.md") -Encoding UTF8

# /ops/manual-paste-log/paste-log-[hour].md
$PasteLogPath = Join-Path $OpsDir ("manual-paste-log\paste-log-{0}.md" -f (Get-Date -Format 'yyyy-MM-dd-HH'))
if(-not (Test-Path $PasteLogPath)){
@"
# Manual Paste Tracking v4.2
Hour: $(Get-Date -Format 'yyyy-MM-dd-HH')
Project: $ProjectName

## Paste Operations
1. $(Get-Date -Format 'HH:mm:ss') - Repo bootstrap block (this operation)

## Thresholds
- Warning: 4 pastes/hour
- HALT: 5 pastes/hour
- Historical: 40+ pastes = catastrophic failure

## Current Status: 1/5 (EXCELLENT)
"@ | Out-File $PasteLogPath -Encoding UTF8
} else {
Add-Content $PasteLogPath "1. $(Get-Date -Format 'HH:mm:ss') - Repo bootstrap block (this operation)"
Add-Content $PasteLogPath "`n## Current Status: 1/5 (EXCELLENT)"
}

# /ops/trust-tracking/trust-log-[session].md
$TrustLog = Join-Path $OpsDir ("trust-tracking\trust-log-$SessionId.md")
@"
# Trust Tracking Log v4.2
Session: $SessionName
Starting Trust: $TrustLevel%

## Trust Events
- $(Get-Date -Format 'HH:mm:ss'): Session started at $TrustLevel%

## Thresholds
- 75–100%: Standard
- 50–74%: Restricted
- 25–49%: Outcome only
- 0–24%: Single actions
"@ | Out-File $TrustLog -Encoding UTF8
Good "Guardrail files written."
#endregion


#region === GITHUB WORKFLOW (CI SCAFFOLD) ===
Info "Creating minimal CI workflow (lint/test placeholders)..."
$WorkflowPath = Join-Path $GhWorkflows 'ci.yml'
@"
name: CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Node setup
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install
        run: |
          if [ -f package.json ]; then
            npm ci
          else
            echo "No package.json; skipping install."
          fi
      - name: Lint & Test (placeholder)
        run: |
          echo "No tests yet; placeholder CI passing."
"@ | Out-File $WorkflowPath -Encoding UTF8
Good "CI workflow ensured."
#endregion


#region === GIT INIT / FIRST COMMIT (idempotent) ===
Info "Initializing Git repository (idempotent)..."
Set-Location $ProjectPath

$gitExists = Test-Path (Join-Path $ProjectPath '.git')
if(-not $gitExists){
  git init | Out-Null
  Good "Initialized empty Git repository."
} else {
  Warn ".git already present — continuing."
}

# Ensure main branch
try{
  $currentBranch = (git rev-parse --abbrev-ref HEAD 2>$null).Trim()
} catch { $currentBranch = $null }

if([string]::IsNullOrWhiteSpace($currentBranch) -or $currentBranch -eq 'HEAD'){
  git checkout -b main | Out-Null
  Good "Switched to new branch: main"
} elseif($currentBranch -ne 'main'){
  git branch -M main | Out-Null
  Good "Renamed current branch to main"
} else {
  Info "Already on main."
}

# Stage and first commit
git add . | Out-Null
$hasAnythingToCommit = (& git status --porcelain).Length -gt 0
if($hasAnythingToCommit){
  git commit -m "chore: v4.2 bootstrap — structure, guardrails, CI, continuity ($SessionId)" | Out-Null
  Good "First commit created."
} else {
  Warn "Nothing to commit (working tree clean)."
}

# Optional: set remote if available (kept empty per continuity)
if($GitRemoteUrl -and $GitRemoteUrl.Trim().Length -gt 0){
  if(-not (git remote 2>$null | Select-String -Quiet 'origin')){
    git remote add origin $GitRemoteUrl | Out-Null
    Good "Remote 'origin' set to $GitRemoteUrl"
  } else {
    Info "Remote 'origin' already configured."
  }
} else {
  Warn "No remote configured (continuity indicates repo not created)."
}

# Show status summary for binary proof capture
$BranchOut = git status -b --porcelain=2
$HeadSha   = (git rev-parse --short HEAD)
Info  "----- GIT STATUS (for proof) -----"
Write-Host $BranchOut
Info  "HEAD: $HeadSha"
#endregion


#region === BINARY PROOF ECHO ===
# Evaluate proof conditions
$gitDirOk   = Test-Path (Join-Path $ProjectPath '.git')
$branchOk   = ($BranchOut -match 'branch\.head main')
$commitOk   = $HeadSha -and $HeadSha.Trim().Length -ge 7

$proof =
@{
  Path                    = $ProjectPath
  GitDirPresent           = $gitDirOk
  BranchIsMain            = $branchOk
  HeadShortSHA            = $HeadSha
  WorkflowFilePresent     = (Test-Path $WorkflowPath)
  GuardrailsPresent       = (Test-Path (Join-Path $ProjectPath 'README.md')) -and (Test-Path (Join-Path $ProjectPath '.gitignore'))
  ContinuityPromptPresent = (Test-Path (Join-Path $ContinuityDir 'prompt.md'))
  SessionTraceLogPresent  = (Test-Path (Join-Path $QAPath "trace-log-$SessionId.md"))
}

Info "----- BINARY PROOF CHECK -----"
$proof.GetEnumerator() | Sort-Object Name | ForEach-Object { "{0}: {1}" -f $_.Key, $_.Value } | ForEach-Object { Write-Host $_ }

if($gitDirOk -and $branchOk -and $commitOk){
  Good "BINARY RESULT: WORKS - Repo initialized on 'main' with initial commit and guardrails."
} else {
  Bad  "BINARY RESULT: DOESN'T WORK - Check status and rerun block."
}
#endregion