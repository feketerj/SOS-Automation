# Operator Runbook - SOS Assessment Tool

## Quick Start (Complete Pipeline)

### 1. Preflight Checks
```bash
# Verify environment
python tools/health_check.py

# Validate endpoints (optional)
python tools/validate_endpoints.py endpoints.txt

# Check config (shows resolved settings)
python config/loader.py
```

### 2. Run Pipeline
```bash
# Edit endpoints.txt (add search IDs, one per line)
notepad endpoints.txt

# Full pipeline (Regex → Batch → Agent)
python Mistral_Batch_Processor/FULL_BATCH_PROCESSOR.py

# Alternative: Use Windows launcher
RUN_BATCH_AGENT.bat
```

### 3. Monitor Progress
```bash
# View batch status (note job ID from step 2)
python Mistral_Batch_Processor/CHECK_BATCH_STATUS.py [job_id]

# Live monitoring (optional)
python Mistral_Batch_Processor/MONITOR_PROGRESS.py
```

### 4. Post-Run Verification
```bash
# Run comprehensive checks on latest output
python tools/postrun_checklist.py

# Or check specific run
python tools/postrun_checklist.py SOS_Output/2025-09/Run_*/
```

## Output Locations

### Primary Outputs
- `SOS_Output/YYYY-MM/Run_*/assessment.csv` - Main results spreadsheet
- `SOS_Output/YYYY-MM/Run_*/GO_opportunities.csv` - Actionable items only
- `SOS_Output/YYYY-MM/Run_*/data.json` - Complete data with all fields
- `SOS_Output/YYYY-MM/Run_*/report.md` - Human-readable report

### Master Database
- `Master_Database/master_YYYY-MM-DD.csv` - Daily aggregation
- `Master_Database/master_all_time.csv` - Historical record

## Processing Modes

### Batch Only (70% cost savings)
```bash
RUN_BATCH_ONLY.bat
# Or: python RUN_MODES.py --mode batch-only
```

### Agent Only (Real-time, full price)
```bash
RUN_AGENT_ONLY.bat
# Or: python RUN_MODES.py --mode agent-only
```

### Combined Pipeline (Recommended)
```bash
RUN_BATCH_AGENT.bat
# Or: python RUN_MODES.py --mode batch-agent
```

## Troubleshooting

### Common Issues

**API Keys Missing**
```bash
# Set environment variables
set HIGHERGOV_API_KEY=your_key_here
set MISTRAL_API_KEY=your_key_here
```

**Batch Job Stuck**
```bash
# Check status
python Mistral_Batch_Processor/CHECK_BATCH_STATUS.py

# Download partial results if available
python Mistral_Batch_Processor/DOWNLOAD_BATCH_RESULTS.py [job_id]
```

**UI Not Working**
```bash
# Test UI directly
streamlit run ui_service/app.py

# Run validation tests
python tests/test_ui_pipeline_runner.py
```

## Performance Settings (Optional)

### Enable Parallel Fetching
Edit `config/settings.json`:
```json
{
  "pipeline": {
    "parallel_fetch": {
      "enabled": true,
      "max_workers": 2
    }
  }
}
```

### Set Batch Size Limit
Edit `config/settings.json`:
```json
{
  "pipeline": {
    "batch_size_limit": 100
  }
}
```

## Daily Operations Checklist

### Morning
1. Pull latest code: `git pull origin main`
2. Review NIGHTLY_UPDATE.md for changes
3. Run health check: `python tools/health_check.py`
4. Check endpoints.txt for new search IDs

### Processing
1. Update endpoints.txt with search IDs
2. Run pipeline: `RUN_BATCH_AGENT.bat`
3. Monitor batch job progress
4. Verify outputs with postrun checklist

### Evening
1. Archive old runs (>30 days): `python tools/archive_outputs.py --days 30`
2. Review Master_Database for trends
3. Check decision audit for disagreements
4. Commit any configuration changes

## Key Metrics

### Success Indicators
- Regex knockout rate: 40-60% (saves money)
- Batch → Agent agreement: >70% (model quality)
- Processing time: <5 min for 100 opportunities
- Error rate: <1% (pipeline stability)

### Cost Tracking
- Batch API: $1 per 1M tokens (50% discount)
- Agent API: $2 per 1M tokens (full price)
- Expected monthly: $5-10 for 500-2000 opportunities

## Emergency Contacts

- GitHub Issues: https://github.com/feketerj/SOS-Automation/issues
- Config Documentation: See CLAUDE.md for detailed settings
- Pipeline Architecture: See SESSION_27_EXTENDED_CONTINUITY.md

---
Last Updated: September 27, 2025
Version: 1.0