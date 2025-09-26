# HOW TO RUN SOS ASSESSMENTS - QUICK GUIDE

## THE ONLY TWO COMMANDS YOU NEED

### Option 1: Run ONE Opportunity
```bash
python LOCKED_PRODUCTION_RUNNER.py [SEARCH_ID]
```
Example:
```bash
python LOCKED_PRODUCTION_RUNNER.py f5KQeEYWpQ4FtgSOPd6Sm
```

### Option 2: Run MULTIPLE Opportunities
1. Edit `endpoints.txt` - add search IDs (one per line)
2. Run:
```bash
python BATCH_RUN.py
```
Or double-click `RUN_BATCH.bat`

### NEW: Simple Wrapper (Either Mode)
```bash
# For single:
python RUN.py [SEARCH_ID]

# For batch (reads endpoints.txt):
python RUN.py
```

## WHERE ARE MY RESULTS?
```
SOS_Output/
  └── 2025-09/
      └── Run_[timestamp]_[search_id]/
          ├── assessment_results.csv
          ├── [search_id]_assessment.json
          └── [search_id]_assessment.md
```

## WHAT IT DOES
1. Fetches full documents from HigherGov (up to 400K chars)
2. Runs regex patterns FIRST (497 patterns)
3. If regex says NO-GO → stops there
4. If regex says GO/INDETERMINATE → sends to Mistral AI
5. Saves results in multiple formats

## CHECK IF SYSTEM IS READY
```bash
python CHECK_SETUP.py
```

## IGNORE EVERYTHING ELSE
- There are 46 Python files here
- Only 11 actually work
- IGNORE all the test*.py, run_*.py, sos_cli*.py files
- See IGNORE_THESE.txt for full list of deprecated files

## TROUBLESHOOTING
- If hanging: HigherGov API is slow, try different search ID
- API key is hardcoded in ULTIMATE_MISTRAL_CONNECTOR.py
- Model: ag:d42144c7:20250902:sos-triage-agent:73e9cddd

---
Last Updated: 2025-09-09
Working Version: LOCKED_PRODUCTION_RUNNER.py + BATCH_RUN.py