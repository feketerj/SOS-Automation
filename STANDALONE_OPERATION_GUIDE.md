# STANDALONE OPERATION GUIDE
**NO AGENT OR CLAUDE REQUIRED - FULLY AUTONOMOUS**

## QUICK START (5 STEPS)

1. **Add Search IDs**
   ```
   notepad endpoints.txt
   ```
   Add one search ID per line (e.g., rFRK9PaP6ftzk1rokcKCT)

2. **Run Batch Processor**
   ```bash
   cd Mistral_Batch_Processor
   python FULL_BATCH_PROCESSOR.py
   ```

3. **Note the Job ID**
   Look for: `Batch job created: 7fae976f-0361-4e60-982e-f1799dfb0ef6`

4. **Check Status**
   ```bash
   python CHECK_BATCH_STATUS.py 7fae976f-0361-4e60-982e-f1799dfb0ef6
   ```

5. **Download Results**
   ```bash
   python DOWNLOAD_BATCH_RESULTS.py 7fae976f-0361-4e60-982e-f1799dfb0ef6
   ```

## PROCESSING MODES

### Mode 1: BATCH ONLY (70% Cost Savings) - RECOMMENDED
```bash
# Windows
Double-click RUN_BATCH_ONLY.bat

# Command Line
cd Mistral_Batch_Processor
set SKIP_AGENT_VERIFICATION=1
python FULL_BATCH_PROCESSOR.py
```
- Uses fine-tuned model at 50% discount
- Regex pre-filtering saves additional 20%
- Best for bulk processing

### Mode 2: AGENT ONLY (40% Cost Savings)
```bash
# Windows
Double-click RUN_AGENT_ONLY.bat

# Command Line
python BATCH_RUN.py
```
- Uses production agent in real-time
- Regex pre-filtering saves 40%
- Best for high-accuracy needs

### Mode 3: COMBINED (58% Cost Savings)
```bash
# Windows
Double-click RUN_BATCH_AGENT.bat

# Command Line
cd Mistral_Batch_Processor
python FULL_BATCH_PROCESSOR.py
# (with SKIP_AGENT_VERIFICATION not set)
```
- Batch processes first, agent verifies GOs
- Balance of cost and accuracy

## COMPLETE FILE LIST

### Input Files
- `endpoints.txt` - List of search IDs (one per line)
- `Mistral_Batch_Processor/endpoints.txt` - Copy for batch mode

### Main Scripts
- `FULL_BATCH_PROCESSOR.py` - Main batch processor
- `CHECK_BATCH_STATUS.py` - Check Mistral job status
- `DOWNLOAD_BATCH_RESULTS.py` - Download completed batches
- `BATCH_RUN.py` - Agent-only processing
- `RUN_MODES.py` - Interactive mode selector

### Helper Scripts
- `RUN_TEST_BATCH.py` - Test with 3 endpoints
- `RUN_FULL_BATCH.py` - Process all endpoints
- `MONITOR_PROGRESS.py` - Live progress tracking
- `CHECK_SETUP.py` - Verify system configuration

### Windows Batch Files
- `RUN_BATCH_ONLY.bat` - Batch-only launcher
- `RUN_AGENT_ONLY.bat` - Agent-only launcher
- `RUN_BATCH_AGENT.bat` - Combined launcher
- `RUN_17_ENDPOINTS.bat` - Full run launcher
- `QUICK_STATUS.bat` - Quick status check

### Output Location
```
SOS_Output/
└── 2025-09/
    ├── Run_20250911_143022/      # Agent-only results
    └── Run_20250911_143022_BATCH/ # Batch results
        ├── assessment_results.csv
        ├── assessment_results.json
        └── assessment_summary.md
```

## PROCESSING TIMES

### Per Endpoint
- API Fetch: 30-60 seconds
- Regex Filter: <1 second
- Batch Prep: 2-3 seconds per opportunity

### Total Times (17 endpoints)
- Phase 1 (Fetch): 8-17 minutes
- Phase 2 (Filter): Instant
- Phase 3 (Batch): 1-2 minutes
- Phase 4 (Submit): Instant
- Mistral Processing: 5-10 minutes
- **Total: 15-30 minutes**

## TROUBLESHOOTING

### Issue: "Using TEST endpoints"
**Solution:** Remove or rename test_endpoints.txt files:
```bash
mv test_endpoints.txt test_endpoints.txt.old
cd Mistral_Batch_Processor
rm -f test_endpoints.txt
```

### Issue: No output from batch processor
**Cause:** Document fetching takes time (30-60s per endpoint)
**Solution:** Wait or use MONITOR_PROGRESS.py

### Issue: Batch job stuck in QUEUED
**Solution:** Normal - Mistral processes in queue order
```bash
python CHECK_BATCH_STATUS.py [job_id]
```

### Issue: Can't find results
**Location:** SOS_Output/2025-09/Run_[timestamp]_BATCH/
```bash
dir SOS_Output\2025-09\Run_*_BATCH
```

## COST BREAKDOWN

| Mode | Regex | Batch | Agent | Total Savings |
|------|-------|-------|-------|---------------|
| Batch Only | FREE | 50% off | Skip | 70% |
| Agent Only | FREE | Skip | Full | 40% |
| Combined | FREE | 50% off | Selective | 58% |

## IMPORTANT NOTES

1. **No Manual Intervention:** Scripts auto-answer all prompts
2. **Parallel Processing:** Batch API handles multiple requests simultaneously
3. **Error Handling:** Failed assessments logged but don't stop processing
4. **Incremental Results:** Can check partial results while batch runs
5. **Reusable Jobs:** Same job ID can be downloaded multiple times

## COMMAND REFERENCE

```bash
# Process new endpoints
cd Mistral_Batch_Processor
python FULL_BATCH_PROCESSOR.py

# Check all jobs
python CHECK_BATCH_STATUS.py

# Check specific job
python CHECK_BATCH_STATUS.py 7fae976f-0361-4e60-982e-f1799dfb0ef6

# Download results
python DOWNLOAD_BATCH_RESULTS.py 7fae976f-0361-4e60-982e-f1799dfb0ef6

# Monitor progress
python MONITOR_PROGRESS.py

# Test setup
python CHECK_SETUP.py
```

## SUPPORT

If you see this error: "EOFError: EOF when reading a line"
- This is normal - the script auto-answers 'n' to monitoring
- The batch job was still submitted successfully
- Check status with CHECK_BATCH_STATUS.py

---
**Remember:** The system is FULLY STANDALONE. You never need an agent to run assessments!