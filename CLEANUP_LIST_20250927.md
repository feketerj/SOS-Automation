# Repository Cleanup List - September 27, 2025

## Summary
Identified 62 files for deletion to reduce repository bloat and improve organization.
Estimated space savings: ~5-10MB

## Files to Delete

### 1. Test/Temporary Files (8 files)
**Current Value:** Zero
**Future Use:** Zero
**Justification:** Temporary test files, endpoints.txt is the main file

- TEST_DIRECT.py - Temporary test script
- test_endpoint.txt - Duplicate test endpoint
- test_3_endpoints.txt - Duplicate test endpoint
- test_single_url.txt - Duplicate test endpoint
- test_single_endpoint.txt - Duplicate test endpoint
- endpoints_test.txt - Duplicate test endpoint
- endpoints_backup.txt - Old backup, already committed
- script_output.txt - Old output file

### 2. Old Session Documentation (4 files)
**Current Value:** Zero
**Future Use:** Zero
**Justification:** Replaced by SESSION_27_EXTENDED_CONTINUITY.md

- SESSION_21_CONTINUITY.md
- SESSION_25_CONTINUITY.md
- SESSION_26_CONTINUITY.md
- SESSION_27_COMPLETION.md

### 3. Old Bug/QC Reports (6 files)
**Current Value:** Zero
**Future Use:** Zero
**Justification:** Consolidated into CRITICAL_FIXES_LOG.md

- BUG_3_DOUBLE_SANITIZATION_FIX.md
- BUG_FIXES_SUMMARY_SESSION_27.md
- QUALITY_CONTROL_ISSUES_REPORT.md
- QUALITY_CONTROL_SUMMARY.md
- QC_FIXES_COMPLETE_REPORT.md
- FIX_OUTPUT_MANAGER_INDETERMINATE.md

### 4. Outdated Status Documentation (4 files)
**Current Value:** Zero
**Future Use:** Zero
**Justification:** Replaced by CLAUDE.md and NIGHTLY_UPDATE.md

- BATCH_PROCESSOR_STATUS.md
- BATCH_TEST_SUMMARY.md
- WHAT_WORKS.md
- CODEBASE_ANALYSIS.md

### 5. Completed Cleanup Documentation (2 files)
**Current Value:** Zero
**Future Use:** Zero
**Justification:** Cleanup already completed

- CLEANUP_PLAN.md
- CLEANUP_COMPLETE.md

### 6. Duplicate Documentation (2 files)
**Current Value:** Zero
**Future Use:** Zero
**Justification:** Duplicates of existing docs

- field_mapping_report.md (duplicate of FIELD_MAPPING_DOCUMENTATION.md)
- GIT_SYNC_STATUS.md (one-time status report)

### 7. Old Batch Metadata (36 files)
**Current Value:** Zero
**Future Use:** Zero
**Justification:** Results already saved in SOS_Output

All batch_metadata_*.json files from September 11-26:
- batch_info_093e8420.json
- batch_info_7f54cd9d.json
- batch_info_d88d3fe5.json
- batch_metadata_20250911_*.json (9 files)
- batch_metadata_20250912_*.json (6 files)
- batch_metadata_20250913_*.json (1 file)
- batch_metadata_20250924_*.json (2 files)
- batch_metadata_20250925_*.json (10 files)
- batch_metadata_20250926_*.json (5 files)

## Files to KEEP

### Critical Files
- CLAUDE.md - Main agent instructions
- NIGHTLY_UPDATE.md - Current updates
- SESSION_27_EXTENDED_CONTINUITY.md - Latest session
- CRITICAL_FIXES_LOG.md - Production fix tracking
- UI_BROKEN_HANDOFF.md - Current UI status
- TODO_CodexUI.md - Active TODO list
- PROGRESS.md - Progress tracking
- README.md - Repository documentation
- requirements.txt - Python dependencies
- endpoints.txt - Active endpoint file
- endpoints.sample.txt - Documentation

### UI Test Files (Consider Moving)
These could be moved to tests/ but are currently in use:
- ui_service/test_pipeline_runner.py
- ui_service/test_failure_scenarios.py
- ui_service/run_pipeline_direct.py (old version, but might be referenced)

## Space Savings
- Documentation files: ~500KB
- Batch metadata: ~3-5MB
- Test files: ~50KB
- **Total: ~5-10MB**

## Token Savings
Removing these files will reduce context for future agents by approximately 20-30%.

## Safety Check
✅ All files backed up in Git history
✅ No active code dependencies
✅ No OS functionality impact
✅ Pipeline will continue working