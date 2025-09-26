# REPO CLEANUP PLAN - 3GB TO <500MB

## Current State (BLOATED - 2.96 GB)
- Total Size: 2.96 GB with 56,750 files
- Main Culprits:
  - `.venv/`: 11,174 files (Python virtual environment - NEVER belongs in repo)
  - `_ARCHIVE*` folders: ~20,000 files (old backups)
  - `SOS_Output*/`: ~15,000 files (test outputs)
  - Various batch output JSONLs: Hundreds of large files
  - `.history/`: VS Code local history
  - `__pycache__/`: Python bytecode everywhere

## SAFE TO DELETE IMMEDIATELY

### 1. Python Virtual Environment (DELETE NOW)
```
.venv/                     # 11,174 files - NEVER commit this
```
**Action:** Delete completely. Recreate locally with `python -m venv .venv`

### 2. Python Cache Files (DELETE NOW)
```
__pycache__/               # All instances
*.pyc                      # Compiled Python
*.pyo                      # Optimized Python
*.pyd                      # Python DLL
```
**Action:** Delete all. Python recreates as needed.

### 3. VS Code Local Files (DELETE NOW)
```
.history/                  # VS Code file history
```
**Action:** Delete. This is local editor history.

### 4. Old Archive Folders (DELETE AFTER REVIEW)
```
_ARCHIVE_2025_09_03/       # Sept 3 archive
_ARCHIVE_2025_09_04/       # Sept 4 archive
_ARCHIVE_OLD_FILES_2025_09_09/  # Sept 9 archive
_BACKUP_BEFORE_CLEANUP_2025_09_25/  # Sept 25 backup
```
**Action:** Check if anything critical, then delete. Already backed up by name.

### 5. Test Outputs (DELETE OLD ONES)
```
SOS_Output/2025-09/Run_*   # Keep only latest 2-3 runs
SOS_Output_TEST/           # Test outputs
Reports/                   # Old reports
Master_Analytics/          # Old analytics
Gov-Test-Docs/            # Test documents
```
**Action:** Keep latest run for reference, delete rest.

### 6. Batch Processing Artifacts (DELETE OLD)
```
batch_output_*.jsonl       # Old batch outputs (large!)
batch_results_*.jsonl      # Old batch results
batch_summary_*.txt        # Old summaries
checkpoint_*.txt           # Old checkpoints
Mistral_Batch_Processor/batch_input_*.jsonl
Mistral_Batch_Processor/batch_output_*.jsonl
Mistral_Batch_Processor/batch_metadata_*.json
Mistral_Batch_Processor/SOS_Output/
```
**Action:** Delete all except current/active batch job files.

### 7. Duplicate/Temp Files (DELETE NOW)
```
script_output.txt
pipeline_output.log
*.backup
backups/
tests_archive/
nul                        # Windows artifact
```
**Action:** Delete all.

### 8. Redundant Debug Scripts (DELETE)
```
debug1.bat
debug2.bat
debug3.bat
debug4.bat
paren_test.bat
test.bat
```
**Action:** Delete. Not needed in production.

## KEEP THESE (Critical for Operation)

### Core Pipeline Files
- `LOCKED_PRODUCTION_RUNNER.py`
- `ULTIMATE_MISTRAL_CONNECTOR.py`
- `FULL_BATCH_PROCESSOR.py`
- `enhanced_output_manager.py`
- `sos_ingestion_gate_v419.py`
- `decision_sanitizer.py`

### Configuration
- `config/` folder (except settings.json with secrets)
- `packs/regex_pack_v419_complete.yaml`
- `endpoints.txt` (current input)

### Batch Scripts (User Interface)
- `RUN_BATCH_AGENT.bat`
- `RUN_BATCH_ONLY.bat`
- `RUN_SMOKE.bat`
- `RUN_TESTS_LOCAL.bat`

### Documentation
- `CLAUDE.md` (project memory)
- `README.md`
- `requirements.txt`
- Session continuity docs

### Tests
- `tests/` folder (keep the curated tests)

## Expected Size After Cleanup
- Target: <100 MB (from 2,960 MB)
- File count: <500 files (from 56,750)

## Cleanup Commands

```bash
# 1. Remove Python artifacts
Remove-Item -Recurse -Force .venv
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force

# 2. Remove VS Code history
Remove-Item -Recurse -Force .history

# 3. Remove archives (AFTER CHECKING)
Remove-Item -Recurse -Force _ARCHIVE*
Remove-Item -Recurse -Force _BACKUP*

# 4. Remove old outputs (keep latest)
# Keep only latest 2 runs in SOS_Output

# 5. Remove batch artifacts
Remove-Item batch_output_*.jsonl
Remove-Item batch_results_*.jsonl
Remove-Item batch_summary_*.txt
Remove-Item checkpoint_*.txt

# 6. Remove temp files
Remove-Item *.backup
Remove-Item -Recurse -Force backups
Remove-Item -Recurse -Force tests_archive
```

## Post-Cleanup Checklist
- [ ] Verify pipeline still runs: `RUN_SMOKE.bat`
- [ ] Check git status is clean
- [ ] Update .gitignore is working
- [ ] VS Code no longer crashes
- [ ] Repository under 100MB
- [ ] Commit the cleanup