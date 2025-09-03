# CLAUDE.md - Project Memory

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
# MAIN ASSESSMENT
python highergov_batch_fetcher.py SEARCH_ID    # Batch process from HigherGov
python sos_cli.py batch SEARCH_ID              # Alternative CLI
python run_full_pipeline.py SEARCH_ID          # Full pipeline with Mistral

# TEST MISTRAL AGENT
python test_sos_agent.py                       # Test suite for agent
python mistral_api_connector.py                # Test classifier

# CHECK MODEL STATUS
python check_training_status.py JOB_ID         # Check training progress

# VIEW REPORTS
python view_latest_report.py                   # Latest assessment
ls Reports/2025-09-02/                        # Today's reports
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

## Key Files
- **Training Data:** FINAL_MISTRAL_READY/SOS-Mistral-Train.jsonl (8,482 examples)
- **Validation:** FINAL_MISTRAL_READY/SOS-Mistral-Val.jsonl (942 examples)
- **Pipeline:** run_full_pipeline.py (complete HigherGov → Mistral flow)
- **Model Config:** model_config.py (easy model switching)
- **Production Settings:** production_settings.py (v1.4 locked)