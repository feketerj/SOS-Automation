# Mistral Batch Processor - SEPARATE FROM MAIN SYSTEM

## Overview
This is a **completely separate** batch processing system that won't affect your main pipeline.
It uses Mistral's batch API to process all opportunities at once instead of one-by-one.

## Benefits
- **Speed**: Submit all at once, get results in one batch
- **Cost**: Mistral offers discounts for batch processing  
- **Reliability**: One job instead of many API calls
- **No interference**: Completely separate from LOCKED_PRODUCTION_RUNNER

## Workflow

### Step 1: Collect Opportunities
```bash
cd Mistral_Batch_Processor
python BATCH_COLLECTOR.py
```
This will:
- Read ../endpoints.txt
- Fetch all opportunities using existing fetcher
- Run regex filter (knock out obvious NO-GOs)
- Create `batch_input_[timestamp].jsonl` with all opportunities needing model assessment
- Save `batch_metadata_[timestamp].json` for later processing

### Step 2: Submit to Mistral
```bash
python BATCH_SUBMITTER.py
```
This will:
- Upload the JSONL file to Mistral
- Create a batch job
- Give you a batch ID for tracking

### Step 3: Check Status
```bash
python BATCH_SUBMITTER.py --status [batch_id]
```
Shows progress of your batch job.

### Step 4: Download Results
```bash
python BATCH_SUBMITTER.py --download [batch_id]
```
Downloads completed results as `batch_results_[timestamp].jsonl`

### Step 5: Parse Results
```bash
python BATCH_RESULTS_PARSER.py
```
This will:
- Parse the results
- Match them with original opportunities
- Create `batch_assessment_[timestamp].csv` (same format as main system)
- Generate summary statistics

## File Structure
```
Mistral_Batch_Processor/
├── BATCH_COLLECTOR.py       # Collects opportunities and creates JSONL
├── BATCH_SUBMITTER.py       # Submits to Mistral batch API
├── BATCH_RESULTS_PARSER.py # Parses results and creates CSV
├── batch_input_*.jsonl     # Input files for Mistral
├── batch_metadata_*.json   # Metadata for matching results
├── batch_results_*.jsonl   # Downloaded results from Mistral
└── batch_assessment_*.csv  # Final output (same format as main)
```

## Comparison with Main System

| Aspect | Main System (BATCH_RUN.py) | Batch Processor |
|--------|----------------------------|-----------------|
| Processing | One at a time | All at once |
| Time | ~30 seconds per opportunity | Submit once, wait for batch |
| API Calls | One per opportunity | One batch submission |
| Delays | 15 seconds between each | None needed |
| Cost | Standard API pricing | Batch discount pricing |
| Output | Real-time progress | Results when complete |

## Important Notes

1. **This doesn't replace your main system** - it's an alternative method
2. **Uses the same regex filter** - obvious NO-GOs still knocked out locally
3. **Same model** - ag:d42144c7:20250902:sos-triage-agent:73e9cddd
4. **Same output format** - CSVs are compatible

## When to Use Each

**Use Main System (BATCH_RUN.py) when:**
- You need real-time progress
- Processing small batches
- Want to see results immediately
- Testing/debugging

**Use Batch Processor when:**
- Processing large volumes (50+ opportunities)
- Cost is a concern
- Can wait for batch completion
- Want maximum efficiency

## No Risk to Main System

- Separate folder
- No shared files except reading endpoints.txt
- Different output location
- Can delete entire folder without affecting main pipeline