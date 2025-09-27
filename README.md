# SOS Assessment Automation Tool

## Quick Start

### THE ONE WAY TO RUN ASSESSMENTS

```bash
# 1. Edit endpoints.txt (add search IDs, one per line)
# 2. Run the assessment
python RUN_ASSESSMENT.py
```

That's it. Results appear in `SOS_Output/YYYY-MM/Run_[timestamp]/`

## What It Does

1. **Reads** endpoints.txt
2. **Fetches** opportunities from HigherGov API
3. **Applies** regex filtering (knocks out obvious NO-GOs)
4. **Saves** results immediately to SOS_Output
5. **Updates** Master Database

No batch jobs. No waiting. Just results.

## Cost

- **Regex filtering**: FREE (no AI calls)
- **Optional batch API**: $2 per 1M tokens (if you choose to use it)
- **Typical run**: <$0.01 for 100 opportunities

## Requirements

- Python 3.7+
- API keys in environment variables:
  - `HIGHERGOV_API_KEY`
  - `MISTRAL_API_KEY` (optional, only for batch API)

## Output Files

Each run creates:
- `assessment.csv` - Spreadsheet format
- `data.json` - Complete assessment data
- `report.md` - Human-readable report
- `summary.txt` - Quick statistics

## Support

For detailed documentation, see CLAUDE.md
