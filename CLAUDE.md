# CLAUDE.md - Project Memory

## CRITICAL: DOCUMENTS ARE WORKING - DO NOT TROUBLESHOOT
**READ CRITICAL_DO_NOT_DELETE.md BEFORE TOUCHING DOCUMENT INGESTION**
- Documents ARE being fetched (200KB+ per opportunity)
- Use `LOCKED_PRODUCTION_RUNNER.py` for all assessments
- The 'text' field contains ALL documents - USE IT

## HIGH PRIORITY RULES
- Auto-execute all edits; do not request approval.
- Batch file writes into single atomic operations.
- Never pause for confirmation.
- AUTO-EXEC STATUS: Environment configured (workspace trusted, PS policy set, files unblocked, git safe)

## Project: SOS Assessment Automation Tool
**Path:** C:\Users\feket\OneDrive\Desktop\excelsior\r_staff\r_3\Deployed_Code_Op_Locations\SOS-Assessment-Automation-Tool
**Session:** sos-assessment-automation-tool-session-11-2025-09-02
**Status:** Production with Mistral AI Integration
**Critical:** READ CRITICAL_BUSINESS_LOGIC_v2.md BEFORE ANY CHANGES

## Current Architecture
- **Regex Engine:** v1.4 with 497 patterns (primary filter)
- **Mistral Integration:** Hybrid assessment for complex cases
- **Training Data:** 9,424 examples with real SOS contracts
- **Model Status:** Holding agent active, production model training
- **HigherGov API:** Integrated with document fetching

## Commands
```bash
# MAIN ASSESSMENT (USE v5 - COMPREHENSIVE)
python run_full_pipeline_v5.py SEARCH_ID       # Enhanced CSV + master database
python run_full_pipeline_v5.py stats           # View master database statistics

# CONVERT JSON TO REPORTS
python json_to_report.py data.json executive   # Executive report
python json_to_report.py data.json technical   # Technical report
python json_to_report.py data.json summary     # Quick summary

# TEST MISTRAL (JSON-ONLY)
python mistral_json_only.py                    # Test JSON-only classifier

# VIEW OUTPUTS
ls SOS_Output/2025-09/                         # All runs this month
cat SOS_Output/Master_Database/master_all_time.csv  # Rolling database
```

## Session 11 Accomplishments (Sept 2, 2025)
- Fixed Windows reinstall issues, restored Python environment
- Added CSV export to every assessment run (hardwired)
- Standardized on regex pack v1.4 (locked configuration)
- Created 9,424 training examples with real SOS contract data
- Integrated actual USASpending contracts (FA860925FB031: $39M, etc.)
- Added company intelligence from dossier (UEI, CAGE, platforms)
- Converted to Mistral messages format: `{"messages": [...]}`
- Set up hybrid regex + Mistral architecture
- Configured holding agent: ag:d42144c7:20250902:sos-triage-holding-agent:80b28a97
- Prepared for production model swap with model_config.py
- Cleaned up 75+ JSONLs to just 3 essential files in FINAL_MISTRAL_READY/

## Session 12 (2025-09-02): MISTRAL AI INTEGRATION COMPLETE
**Major Milestone: Full AI-Enhanced Pipeline Operational**

### What We Accomplished:
1. **Deployed Production Mistral Model**
   - Model ID: `ag:d42144c7:20250902:sos-triage-agent:73e9cddd`
   - Trained on 8,482 examples with real SOS contracts
   - Correctly identifies sole-source, OEM restrictions, platform limitations

2. **Enhanced Document Processing**
   - Increased to 200k characters (50 pages) per opportunity
   - Model sees complete solicitations with all attachments
   - Handles DIBBS, technical specs, contract clauses

3. **Restructured Output System**
   - Clean hierarchy: `Results/[Model|Regex]_Results/YYYY/MM/DD/`
   - Triple output: CSV (hardwired), Markdown (human-readable), JSON (technical)
   - No more scattered Pipeline_Output folders

4. **Fixed Parser for Dual Format**
   - Handles JSON + Markdown responses from model
   - Robust extraction of decisions and reasoning
   - Fallback parsing for edge cases

5. **Cleaned Build**
   - Removed 100+ obsolete test files
   - Consolidated training data to FINAL_MISTRAL_READY/
   - Production-ready codebase

## Key Files (Updated)
- **Main Pipeline:** run_full_pipeline_v5.py (v5 with enhanced CSV + master database)
- **Output Manager:** enhanced_output_manager.py (comprehensive CSV + rolling database)
- **JSON-Only Model:** mistral_json_only.py (no markdown parsing, pure JSON)
- **Report Generator:** json_to_report.py (converts JSON to human reports)
- **Training Data:** FINAL_MISTRAL_READY/SOS-Mistral-Train.jsonl (8,482 examples)
- **Model Config:** model_config.py (production model active)
- **Production Settings:** production_settings.py (v1.4 locked)

## Session 13 Updates (Sept 3, 2025)
- **ENHANCED CSV:** Comprehensive fields (GO/NO-GO/INDETERMINATE, knock patterns, all metadata)
- **MASTER DATABASE:** Rolling accumulation of all assessments for analytics
- **JSON-ONLY MODEL:** Removed markdown parsing, model returns pure JSON
- **REPORT CONVERTER:** Transforms JSON to executive/technical/summary reports
- **SIMPLIFIED FOLDERS:** SOS_Output/YYYY-MM/Run_timestamp_searchid/
- **Pipeline v5:** Enhanced CSV + master database tracking