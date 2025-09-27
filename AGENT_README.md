# AGENT NAVIGATION GUIDE
**For AI Agents Working on This Repository**

## 🎯 QUICK START - THE ONE THING TO KNOW

**To run assessments:** `python RUN_ASSESSMENT.py`

That's it. Everything else is supporting code.

## 📂 REPOSITORY STRUCTURE

### Core Files (Start Here)
```
RUN_ASSESSMENT.py           # ⭐ THE MAIN SCRIPT - Run this
endpoints.txt              # Input file - add search IDs here
CLAUDE.md                 # Project memory and context
README.md                 # Basic documentation
```

### Pipeline Components
```
sos_ingestion_gate_v419.py     # Stage 1: Regex filtering
BATCH_API_HANDLER.py           # Stage 2: Batch processing (optional)
ULTIMATE_MISTRAL_CONNECTOR.py  # Stage 3: Agent verification
pipeline_output_manager.py     # Output formatting
highergov_batch_fetcher.py     # API integration
```

### Output Locations
```
SOS_Output/                # All assessment results go here
  └── YYYY-MM/            # Organized by year-month
      └── Run_*/          # Individual run folders
Master_Database/          # Aggregated results database
```

### UI Components
```
ui_service/               # Streamlit dashboard
  ├── app.py             # Main UI application
  └── field_mapper.py    # Field mapping logic
```

### Supporting Files
```
decision_sanitizer.py         # Data normalization
enhanced_output_manager.py    # Legacy output manager
pipeline_title_generator.py   # Title generation
model_config.py              # Model configuration
```

### Tests
```
tests/                   # All test files (40+ tests)
```

### Documentation
```
CLIENT_CONFIG.md              # Hardcoded credentials info
OUTPUT_FORMAT_COMPLETE.md     # Output format details
PIPELINE_FIXED.md            # Pipeline documentation
OPERATOR_RUNBOOK.md          # Operational guide
RECOVERY_INSTRUCTIONS.md     # Disaster recovery
```

### Archived (Ignore These)
```
_ARCHIVED_RUNNERS/           # Old scripts from previous sessions
_ARCHIVED_RUNNERS_20250927/  # Recently archived redundant files
```

## 🚨 IMPORTANT NOTES FOR AGENTS

### 1. DO NOT USE ENVIRONMENT VARIABLES
All API keys are **hardcoded**:
- HigherGov: `2c38090f3cb0c56026e17fb3e464f22cf637e2ee`
- Mistral: `2oAquITdDMiyyk0OfQuJSSqePn3SQbde`
- Agent ID: `ag:d42144c7:20250911:untitled-agent:15489fc1`

### 2. SINGLE ENTRY POINT
There is **ONLY ONE WAY** to run assessments:
```bash
python RUN_ASSESSMENT.py
```
Do not use any of the archived runners.

### 3. THREE-STAGE PIPELINE
The pipeline has three stages that MUST flow data:
1. **Regex** (FREE) - Knocks out obvious NO-GOs
2. **Batch** (50% off) - Processes GO/INDETERMINATE
3. **Agent** (full price) - Final verification

### 4. NO TIMEOUTS
Document fetching has **no timeouts** - it can take minutes.

### 5. OUTPUT TRACKING
Every opportunity is tracked through all stages with complete visibility.

## 🔍 COMMON AGENT TASKS

### Run an Assessment
```bash
echo "SEARCH_ID_HERE" > endpoints.txt
python RUN_ASSESSMENT.py
```

### Check Output
```bash
ls -la SOS_Output/YYYY-MM/Run_*/
```

### View UI
```bash
streamlit run ui_service/app.py
```

### Run Tests
```bash
pytest tests/
```

## 📝 KEY DECISIONS

### FAA 8130 Exception
Only applies to these commercial Navy platforms:
- P-8 Poseidon
- E-6B Mercury
- C-40 Clipper
- UC-35 Citation
- C-12 Huron

### Pipeline Flow Rules
- NO-GO at any stage = STOP
- GO/INDETERMINATE = Continue to next stage
- All decisions tracked with reasons

## ⚠️ WARNINGS

1. **DO NOT** create new runner scripts - use RUN_ASSESSMENT.py
2. **DO NOT** move files to different directories
3. **DO NOT** change hardcoded API keys
4. **DO NOT** add environment variable logic
5. **DO NOT** break the three-stage pipeline flow

## 📊 Repository Stats

- **Total Files:** ~150
- **Core Python Files:** 20
- **Test Files:** 40+
- **Documentation:** 30+ MD files
- **Archived:** 60+ old files

## 🎯 AGENT CHECKLIST

When working on this repo:
- [ ] Start with RUN_ASSESSMENT.py
- [ ] Check CLAUDE.md for context
- [ ] Use hardcoded credentials
- [ ] Preserve three-stage pipeline
- [ ] Save outputs to SOS_Output/
- [ ] Run tests after changes
- [ ] Don't create new entry points

## 💡 TIPS FOR AGENTS

1. **Read CLAUDE.md first** - It has complete project context
2. **Use existing patterns** - Don't reinvent the wheel
3. **Test incrementally** - Run after each change
4. **Check output format** - Use pipeline_output_manager.py
5. **Preserve tracking** - Keep pipeline_tracking dict intact

## 🚀 GETTING STARTED

```bash
# 1. Clone if needed
git clone https://github.com/feketerj/SOS-Automation.git

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run assessment
python RUN_ASSESSMENT.py
```

That's all you need to know to work effectively on this repository!