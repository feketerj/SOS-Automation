# DISASTER RECOVERY INSTRUCTIONS
**Last Updated:** September 27, 2025
**Repository:** https://github.com/feketerj/SOS-Automation.git
**Latest Commit:** 254d837

## Quick Recovery Steps

### 1. Clone Repository
```bash
git clone https://github.com/feketerj/SOS-Automation.git
cd SOS-Automation
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
python RUN_ASSESSMENT.py
```

That's it! Everything is hardcoded and ready to run.

## What Was Backed Up

### Critical Code Files
- `RUN_ASSESSMENT.py` - The ONE pipeline runner (complete 3-stage)
- `pipeline_output_manager.py` - Comprehensive output tracking
- `sos_ingestion_gate_v419.py` - Fixed FAA 8130 exception
- `highergov_batch_fetcher.py` - No timeouts, hardcoded API key
- `ULTIMATE_MISTRAL_CONNECTOR.py` - Hardcoded credentials
- `BATCH_API_HANDLER.py` - Optional batch processing

### Configuration (All Hardcoded)
- HigherGov API Key: `2c38090f3cb0c56026e17fb3e464f22cf637e2ee`
- Mistral API Key: `2oAquITdDMiyyk0OfQuJSSqePn3SQbde`
- Batch Model: `ft:pixtral-12b-latest:d42144c7:20250912:f7d61150`
- Agent ID: `ag:d42144c7:20250911:untitled-agent:15489fc1`

### Documentation
- `HANDOFF_SEPTEMBER_27_2025.md` - Complete session handoff
- `CLIENT_CONFIG.md` - All hardcoded configurations
- `OUTPUT_FORMAT_COMPLETE.md` - Output format documentation
- `PIPELINE_FIXED.md` - Three-stage pipeline documentation
- `CONSOLIDATION_COMPLETE.md` - Consolidation summary
- `OPERATOR_RUNBOOK.md` - Complete operational guide

### UI Components
- `ui_service/app.py` - Streamlit dashboard
- `ui_service/field_mapper.py` - Field mapping for UI

## Critical Changes in This Version

### 1. FAA 8130 Exception Fixed
- Now only applies to commercial Navy platforms:
  - P-8 Poseidon, E-6B Mercury, C-40 Clipper, UC-35 Citation, C-12 Huron
- Was letting through 89% of opportunities, now ~60%

### 2. Complete Three-Stage Pipeline
- Stage 1: Regex (FREE) - knocks out obvious NO-GOs
- Stage 2: Batch (50% off) - processes GO/INDETERMINATE
- Stage 3: Agent (full price) - final verification
- ALL stages properly connected and flowing data

### 3. Consolidated to Single Entry Point
- Removed 16+ redundant runner scripts
- Everything runs through `RUN_ASSESSMENT.py`
- Archived old runners in `_ARCHIVED_RUNNERS_20250927/`

### 4. Hardcoded Configuration
- No environment variables needed
- All API keys hardcoded
- No .env files required
- Client-ready deployment

### 5. No Timeouts
- Document fetching: No timeout
- Batch processing: Up to 4+ hours
- Reliable for long operations

## Repository Structure

```
SOS-Assessment-Automation-Tool/
├── RUN_ASSESSMENT.py           # THE main runner
├── endpoints.txt               # Search IDs go here
├── SOS_Output/                 # All outputs
├── Master_Database/            # Aggregated results
├── ui_service/                 # Streamlit UI
├── Mistral_Batch_Processor/   # Batch tools
├── tests/                      # Test suite
└── _ARCHIVED_RUNNERS_20250927/ # Old scripts (archived)
```

## Recovery Validation

After recovery, test with:

```bash
# Check configuration
python -c "import RUN_ASSESSMENT; print('Config OK')"

# Run test assessment
echo "AR1yyM0PV54_Ila0ZV6J6" > endpoints.txt
python RUN_ASSESSMENT.py
```

Should see:
1. Three-stage pipeline execution
2. Proper knockouts at each stage
3. Complete output in SOS_Output/

## GitHub Repository

- **URL:** https://github.com/feketerj/SOS-Automation
- **Branch:** main
- **Latest Commit:** 254d837 (Sept 27, 2025)
- **Commit Message:** "CRITICAL: Complete three-stage pipeline implementation and consolidation"

## Backup Status

✅ All code backed up to GitHub
✅ All configurations documented
✅ All improvements preserved
✅ Ready for disaster recovery

## Contact

For issues with recovery, check:
- GitHub Issues: https://github.com/feketerj/SOS-Automation/issues
- Documentation: CLAUDE.md in repository