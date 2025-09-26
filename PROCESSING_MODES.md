# SOS Assessment Processing Modes

## Overview
ALL modes use Regex filtering first (it's FREE!). You choose what happens to the remaining opportunities.

## Three Processing Modes

### 1. BATCH ONLY MODE (Cheapest)
**Double-click:** `RUN_BATCH_ONLY.bat`  
**Command line:** `python RUN_MODES.py --mode batch`

**Pipeline:**
```
Regex (FREE) → Batch API (50% off)
```

**When to use:**
- Maximum cost savings needed
- Large volume processing
- Acceptable accuracy from fine-tuned model
- **Cost:** ~70% savings

### 2. AGENT ONLY MODE (Most Accurate)
**Double-click:** `RUN_AGENT_ONLY.bat`  
**Command line:** `python RUN_MODES.py --mode agent`

**Pipeline:**
```
Regex (FREE) → Agent API (full price)
```

**When to use:**
- Highest accuracy required
- Smaller volumes
- Critical assessments
- **Cost:** ~40% savings (from regex only)

### 3. BATCH + AGENT MODE (Balanced)
**Double-click:** `RUN_BATCH_AGENT.bat`  
**Command line:** `python RUN_MODES.py --mode batch-agent`

**Pipeline:**
```
Regex (FREE) → Batch API (50% off) → Agent Verification (selective)
```

**When to use:**
- Balance of cost and accuracy
- Agent only verifies GOs and INDETERMINATEs
- Best for production use
- **Cost:** ~58% savings

## Cost Comparison (per 100 opportunities)

Assuming 40% regex knockouts, $0.002 per API call:

| Mode | Pipeline | Cost | Savings |
|------|----------|------|---------|
| No Pipeline | All Agent | $0.200 | 0% |
| Batch Only | Regex→Batch | $0.060 | 70% |
| Agent Only | Regex→Agent | $0.120 | 40% |
| Batch+Agent | Regex→Batch→Agent | $0.084 | 58% |

## Quick Decision Guide

### Choose BATCH ONLY when:
- Processing 100+ opportunities
- Cost is primary concern
- 80-90% accuracy is acceptable

### Choose AGENT ONLY when:
- Processing <50 opportunities
- Need 95%+ accuracy
- Cost is not primary concern

### Choose BATCH+AGENT when:
- Need high accuracy AND cost savings
- Processing mixed complexity opportunities
- Want disagreement tracking for model improvement

## File Locations

### Batch Files (Windows)
- `RUN_BATCH_ONLY.bat` - Batch processing only
- `RUN_AGENT_ONLY.bat` - Agent processing only
- `RUN_BATCH_AGENT.bat` - Full three-stage pipeline

### Python Scripts
- `RUN_MODES.py` - Interactive mode selector
- `BATCH_RUN.py` - Direct agent processing
- `Mistral_Batch_Processor/FULL_BATCH_PROCESSOR.py` - Batch processor

### Configuration
- `production_config.json` - System configuration
- `endpoints.txt` - Input search IDs

## Output Files

All modes generate the same output files:
- `data.json` - Complete structured data
- `assessment.csv` - Spreadsheet format
- `report.md` - Executive summary
- `GO_opportunities.csv` - Actionable items only

Location: `SOS_Output/YYYY-MM/Run_[timestamp]/` or `Run_[timestamp]_BATCH/`

## Environment Variables

### Skip Agent Verification
```bash
set SKIP_AGENT_VERIFICATION=1
```
This converts Batch+Agent mode to Batch Only mode.

## Testing Different Modes

### Test with sample data:
1. Add test search IDs to `test_endpoints.txt`
2. Run each mode to compare results
3. Check disagreement tracking in Batch+Agent mode

### Monitor costs:
- Batch Only: Check Mistral batch API usage
- Agent Only: Check Mistral agent API usage
- Batch+Agent: Check both API usages

## Recommendations

### For Daily Operations:
Use **BATCH+AGENT** mode for best balance

### For Large Backlogs:
Use **BATCH ONLY** mode to process quickly

### For Critical Assessments:
Use **AGENT ONLY** mode for highest accuracy

### For Testing:
Try all three modes on same dataset to understand differences

---
**All modes include regex filtering first - it's FREE and eliminates 40-60% of opportunities!**