# COMPLETE PIPELINE OUTPUT FORMAT
**Date:** September 27, 2025
**Status:** IMPLEMENTED - Full visibility across all stages

## What You Get: Complete Pipeline Visibility

When you run `python RUN_ASSESSMENT.py`, you get comprehensive output showing EXACTLY what happened at each stage.

## Output Files Generated

Each run creates these files in `SOS_Output/YYYY-MM/Run_[timestamp]_[search_id]/`:

### 1. `pipeline_results.csv` - Complete Pipeline Tracking
Shows every opportunity with full journey tracking:
- **result** - Final decision (GO/NO-GO/INDETERMINATE)
- **pipeline_stage** - Where it stopped (REGEX/BATCH/AGENT)
- **assessment_type** - Type of assessment at stop point
- **stage1_regex_decision** - What regex said
- **stage1_regex_reason** - Why regex made that decision
- **stage2_batch_decision** - What batch model said (if reached)
- **stage2_batch_reason** - Why batch made that decision
- **stage3_agent_decision** - What agent said (if reached)
- **stage3_agent_reason** - Why agent made that decision
- **knockout_category** - Category code (KO-01, KO-02, etc.)
- **knock_pattern** - Specific pattern that triggered knockout
- **document_length** - How many chars of documents fetched
- **document_fetched** - YES/NO if documents were available

### 2. `pipeline_report.md` - Human-Readable Report
Comprehensive markdown showing:
- **Pipeline Statistics** - How many at each stage
- **Stage 1 Knockouts** - List of regex knockouts with reasons
- **Stage 2 Knockouts** - List of batch knockouts with journey
- **Stage 3 Final Decisions** - Grouped by GO/NO-GO/INDETERMINATE with full journey

### 3. `stage_summary.txt` - Quick Statistics
Fast overview showing:
```
STAGE 1 (REGEX - FREE):
  Input: 100 opportunities
  Knocked Out: 40
  Passed: 60

STAGE 2 (BATCH MODEL - 50% OFF):
  Input: 60 opportunities
  Knocked Out: 30
  Passed: 30

STAGE 3 (AGENT - FULL PRICE):
  Input: 30 opportunities
  GO: 10
  NO-GO: 15
  INDETERMINATE: 5

COST OPTIMIZATION:
  Regex saved: 40 AI calls (100% savings)
  Batch saved: 15.0 full-price calls (50% savings)
```

### 4. `knockouts.md` - Detailed Knockout Analysis
Shows all knockouts grouped by:
- Stage where knocked out
- Reason for knockout
- Count by category
- Examples of each type

### 5. `data.json` - Complete JSON Data
Full data structure with:
- All opportunity details
- Complete pipeline_tracking objects
- Metadata and statistics
- Document text (capped at 50k chars)

### 6. `GO_opportunities.csv` - Actionable Items
Just the GO decisions with:
- announcement_number
- announcement_title
- agency
- highergov_url
- pipeline_journey (e.g., "FURTHER_ANALYSIS→GO→GO")
- assessment_timestamp

## Example Pipeline Journey

For each opportunity, you can see its complete journey:

### Example 1: Knocked out at Stage 1
```
Title: "F-16 Fighter Jet Maintenance"
Journey: NO-GO (stopped at REGEX)
Reason: "Military aircraft pattern: F-16"
Category: KO-10 (Military Platform)
```

### Example 2: Knocked out at Stage 2
```
Title: "Aircraft Parts Manufacturing"
Journey: FURTHER_ANALYSIS → NO-GO (stopped at BATCH)
Stage 1: Passed regex (no military patterns)
Stage 2: Batch model identified OEM restrictions
```

### Example 3: Made it through all stages
```
Title: "Boeing 737 Commercial Parts"
Journey: GO → GO → GO (completed all stages)
Stage 1: Regex found commercial pattern
Stage 2: Batch confirmed commercial
Stage 3: Agent verified GO
```

## Console Output

While running, you see real-time progress:

```
==================================================
STAGE 1: FETCHING OPPORTUNITIES & REGEX FILTERING
==================================================

Fetching: AR1yyM0PV54_Ila0ZV6J6
  Found 45 opportunities
    Fetched 12,456 chars of documents
    • F-16 Fighter Maintenance: NO-GO
    • Boeing 737 Parts: GO
    • Weapons System Upgrade: NO-GO
    ...

Stage 1 Complete:
  Knocked out: 20
  Continuing: 25

==================================================
STAGE 2: BATCH MODEL PROCESSING
==================================================
Submitting batch of 25 requests...
Batch submitted! Job ID: 7fae976f-0361-4e60-982e-f1799dfb0ef6
Waiting for completion...
  Status: RUNNING (15/25 complete)
  Status: SUCCEEDED (25/25 complete)

  Aircraft Parts Manufacturing: NO-GO
  Commercial Avionics: GO
  ...

Stage 2 Complete:
  Knocked out: 10
  Continuing: 15

==================================================
STAGE 3: AGENT VERIFICATION
==================================================
Verifying 15 opportunities with agent...

  Verifying: Commercial Avionics
    Final: GO

  Verifying: Dual-Use Component
    Final: INDETERMINATE
  ...

Stage 3 Complete:
  GO: 5
  NO-GO: 7
  INDETERMINATE: 3
```

## Key Features

1. **Complete Tracking** - Nothing is lost, every decision is recorded
2. **Clear Reasons** - You know WHY each decision was made
3. **Cost Visibility** - See how much money saved at each stage
4. **Progressive Detail** - Quick summary or deep dive available
5. **Actionable Output** - GO opportunities separated for action

## This Addresses Your Requirement

You asked for "consistent output" where you can "see the whole job" including "what got knocked out where and for what reason."

This implementation provides:
✅ Complete tracking through all stages
✅ Clear reasons for every knockout
✅ Full journey visibility for every opportunity
✅ Multiple output formats for different needs
✅ Cost optimization tracking
✅ Nothing hidden or lost in the pipeline