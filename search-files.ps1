$projectPath = "C:\Users\feket\OneDrive\Desktop\excelsior\r_staff\r_3\Deployed_Code_Op_Locations\SOS-Assessment-Automation-Tool"
$excludeDirs = @(".git", "node_modules", "ops", "qa", "continuity", ".github")
$extensions = @("*.pdf", "*.csv", "*.xlsx", "*.json", "*.txt")

# Get all matching files
$allFiles = @()
foreach ($ext in $extensions) {
    $files = Get-ChildItem -Path $projectPath -Filter $ext -Recurse -File -ErrorAction SilentlyContinue | 
        Where-Object { 
            $relativePath = $_.FullName.Substring($projectPath.Length + 1)
            $excluded = $false
            foreach ($excludeDir in $excludeDirs) {
                if ($relativePath -like "$excludeDir\*" -or $relativePath -like "$excludeDir/*") {
                    $excluded = $true
                    break
                }
            }
            -not $excluded
        }
    $allFiles += $files
}

# Sort by LastWriteTime (descending) then by size (descending) to get most recent & largest
$sortedFiles = $allFiles | Sort-Object -Property @{Expression="LastWriteTime";Descending=$true}, @{Expression="Length";Descending=$true}

# Get top 5
$top5 = @($sortedFiles | Select-Object -First 5 | ForEach-Object { $_.FullName })

# Create JSON output
$result = @{
    Mode = "ASK"
    RuleZeroCandidateCount = $allFiles.Count
    DefaultCandidate = if ($sortedFiles.Count -gt 0) { $sortedFiles[0].FullName } else { $null }
    Top5 = $top5
}

$result | ConvertTo-Json -Depth 10