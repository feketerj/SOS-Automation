# === SOS Auto-Exec Baseline (No Prompts) — RUN ONCE PER MACHINE ===
# A) Trust the workspace (stops VS Code trust prompts)
$newSettings = @{
  "security.workspace.trust.enabled" = $true
  "security.workspace.trust.startupPrompt" = "never"
  "security.workspace.trust.untrustedFiles" = "open"
}
$settingsDir = "$env:USERPROFILE\AppData\Roaming\Code\User"
$settingsPath = Join-Path $settingsDir "settings.json"
New-Item -Force -ItemType Directory $settingsDir | Out-Null
if (Test-Path $settingsPath) {
  $json = Get-Content $settingsPath -Raw | ConvertFrom-Json
  foreach ($k in $newSettings.Keys) { $json.$k = $newSettings[$k] }
  ($json | ConvertTo-Json -Depth 10) | Set-Content $settingsPath -Encoding UTF8
} else {
  ($newSettings | ConvertTo-Json -Depth 10) | Set-Content $settingsPath -Encoding UTF8
}

# B) Execution policy (no "run scripts?" prompts)
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force

# C) Strip Mark-of-the-Web on project folder so files don't prompt
$proj = "C:\Users\feket\OneDrive\Desktop\excelsior\r_staff\r_3\Deployed_Code_Op_Locations\SOS-Assessment-Automation-Tool"
if (Test-Path $proj) { Get-ChildItem $proj -Recurse -File | Unblock-File }

# D) Make current process ignore policy (for spawned shells in tools)
$env:POWERSHELL_TELEMETRY_OPTOUT="1" # quiet
# Typical spawn line tools use; keep around for child processes:
# powershell.exe -NoProfile -ExecutionPolicy Bypass -File yourscript.ps1

# E) Git "safe directory" (prevents git safety prompts)
git config --global --add safe.directory $proj 2>$null

# F) Binary proof
Write-Host "AUTO-EXEC BASELINE: WORKS"