# SOS Assessment Tool - Codebase Analysis
**Date:** 2025-09-09
**Status:** NEEDS MAJOR CLEANUP

## WORKING COMPONENTS

### Core Pipeline (THESE WORK)
1. **LOCKED_PRODUCTION_RUNNER.py** - Main single assessment runner
   - Takes one search ID as argument
   - Does regex first, then Mistral if needed
   - Outputs to SOS_Output/

2. **BATCH_RUN.py** - Batch processor (partially working)
   - Reads endpoints.txt
   - Calls assessments sequentially
   - Has 15-second delays between calls
   - Issue: Hangs on HigherGov API calls sometimes

3. **ULTIMATE_MISTRAL_CONNECTOR.py** - Mistral API connector
   - Hardcoded API key: 1BPmHydlQmz81Z1edAs1ssQX3DbmW0Yf
   - Has HTTP fallback if mistralai package missing
   - Works with the production model

### Supporting Files (ESSENTIAL)
- **highergov_batch_fetcher.py** - Fetches opportunity data from HigherGov
- **sos_ingestion_gate_v419.py** - Regex engine with 497 patterns
- **enhanced_output_manager.py** - Creates CSV/JSON/MD outputs
- **model_config.py** - Model configuration
- **mistral_api_connector.py** - Secondary Mistral connector

### Utility Scripts (WORK)
- **CHECK_SETUP.py** - System health check
- **CHECK_DEPENDENCIES.py** - Dependency checker

## BROKEN/QUESTIONABLE

### Multiple Versions of Same Thing
- **run_full_pipeline_v2.py** - Old version
- **run_full_pipeline_v5.py** - Doesn't do regex→model correctly
- **run_assessment.py** - Duplicate functionality
- **run_complete_assessment.py** - Another duplicate
- **run_sos.py** - Yet another runner

### Test/Debug Files (NOT NEEDED)
- **test_copilot.py**
- **test_copilot_trigger.js**
- **test_sos_agent.py** (deleted?)
- **comprehensive_test.py**
- **quick_test.py**

### Standalone Versions (DUPLICATES)
- **STANDALONE_MISTRAL_CONNECTOR.py** - Duplicate of ULTIMATE
- **mistral_json_only.py** - Limited version

### CLI Versions (MULTIPLE ATTEMPTS)
- **sos_cli.py**
- **sos_cli_enhanced.py**
- **sos_cli_v419.py**
- **SIMPLE_RUN.py** - Interactive runner

### Architecture/Documentation (OUTDATED)
- **ARCHITECTURE_VERIFICATION.py**
- **ARCHITECTURE_STATUS.py**
- **PARANOIA_CHECK.py**
- **PIPELINE_HEALTH_CHECK.py**

### Batch Upload System (SEPARATE WORKFLOW)
- **Mistral_Batch_Processor/** folder - For manual batch uploads to Mistral

## FILES TO KEEP (ESSENTIAL ONLY)

### Must Keep:
1. LOCKED_PRODUCTION_RUNNER.py
2. BATCH_RUN.py
3. ULTIMATE_MISTRAL_CONNECTOR.py
4. highergov_batch_fetcher.py
5. sos_ingestion_gate_v419.py
6. enhanced_output_manager.py
7. model_config.py
8. mistral_api_connector.py
9. CHECK_SETUP.py
10. endpoints.txt
11. RUN_BATCH.bat

### Keep for Reference:
- Mistral_Batch_Processor/ (separate workflow)
- SOS_Output/ (results)
- CLAUDE.md (documentation)

## FILES TO DELETE/ARCHIVE

### Delete These (30+ files):
- All run_*.py files except LOCKED_PRODUCTION_RUNNER
- All test*.py files
- All sos_cli*.py files
- STANDALONE_MISTRAL_CONNECTOR.py
- mistral_json_only.py
- All ARCHITECTURE*.py files
- PARANOIA_CHECK.py
- PIPELINE_HEALTH_CHECK.py
- fix_copilot*.ps1
- All test*.js files

## THE ACTUAL WORKING WORKFLOW

### For Single Assessment:
```bash
python LOCKED_PRODUCTION_RUNNER.py [SEARCH_ID]
```

### For Batch (from endpoints.txt):
```bash
python BATCH_RUN.py
# or
RUN_BATCH.bat
```

### For Manual Batch Upload:
```bash
cd Mistral_Batch_Processor
python BATCH_COLLECTOR.py
# Manual upload to Mistral
python BATCH_RESULTS_PARSER.py
```

## PROBLEMS TO FIX

1. **Too many duplicate runners** - 5+ versions doing same thing
2. **Naming confusion** - "pipeline", "runner", "cli" all do similar things
3. **HigherGov API timeouts** - Need better error handling
4. **No clear entry point** - Users don't know what to run
5. **Test files mixed with production** - Clutters the directory

## RECOMMENDED CLEANUP

1. Create folders:
   - `/core` - Essential files only
   - `/archive` - Old versions
   - `/tests` - Test files
   - `/docs` - Documentation

2. Rename for clarity:
   - LOCKED_PRODUCTION_RUNNER.py → run_single.py
   - BATCH_RUN.py → run_batch.py

3. Create single entry point:
   - `run.py` - Asks user for single or batch mode

4. Delete all duplicate/test files

Would you like me to proceed with this cleanup?