# SOS UI DASHBOARD - CONTINUITY DOCUMENT

## Project Status
**Created:** 2025-09-04
**Purpose:** Standalone UI for SOS Assessment Tool
**Principle:** Complete separation from core processing logic

## Architecture Philosophy

### Separation of Concerns
```
SOS_UI_Dashboard/          (This UI - completely independent)
    ↓ 
    Writes to: endpoints.txt or calls subprocess
    ↓
Core System/              (Existing assessment engine)
    ↓
    Outputs to: SOS_Output/
    ↓
SOS_UI_Dashboard/         (Reads CSVs for display)
```

### Key Design Decisions

1. **NO DIRECT INTEGRATION**
   - UI never imports core modules
   - Communication only through files/subprocess
   - Can develop/test without core running

2. **URL HANDLING**
   - User pastes: `https://app.highergov.com/search-manager/ABC123`
   - UI extracts: `ABC123`
   - Passes to core as search ID

3. **CSV AS CONTRACT**
   - CSV format is the API between UI and core
   - UI development uses dummy CSVs
   - When ready, update core to match ideal format

## Folder Structure

```
SOS_UI_Dashboard/
├── UI_CONTINUITY.md        (this file)
├── PROJECT_PLAN.md         (development roadmap)
├── data/
│   ├── dummy_assessment.csv    (mock data for testing)
│   ├── dummy_history.json      (historical data mock)
│   └── sample_endpoints.txt    (test inputs)
├── mockups/
│   └── ui_wireframe.md     (interface design)
├── components/
│   ├── input_handler.py    (URL/CSV/text processing)
│   ├── dashboard.py        (main statistics view)
│   ├── results_viewer.py   (assessment browser)
│   └── runner_bridge.py    (calls core system)
└── assets/
    └── styles.css          (if web-based)

```

## Current Dummy Data Fields

### Ideal CSV Structure
```csv
assessment_id, search_id, opportunity_id, title, decision, reasoning, 
knockout_patterns, priority_score, days_until_due, solicitation_number,
part_numbers, quantity, condition, platform, company_name, cage_code,
assessment_date, processing_time, document_pages, model_used
```

### Additional Dashboard Metrics
- GO vs NO-GO ratio
- Average processing time
- Most common knockout reasons
- Daily/weekly/monthly trends
- Success rate by platform type

## Development Phases

### Phase 1: Static UI (Current)
- Build with dummy data
- Perfect the interface
- Test all visualizations
- No connection to core

### Phase 2: Integration
- Add runner_bridge.py
- Connect to real endpoints.txt
- Read actual CSVs from SOS_Output
- Keep core untouched

### Phase 3: Enhancement
- Modify enhanced_output_manager.py to match ideal CSV
- Add enrichment fields
- Historical tracking database

## Tech Stack Options

### Option A: Streamlit (Recommended)
- **Pros:** Beautiful, fast to build, built-in components
- **Cons:** Requires `pip install streamlit`
- **Run:** `streamlit run app.py`

### Option B: Flask + Bootstrap
- **Pros:** Flexible, runs in browser, good for future web deployment
- **Cons:** More setup work
- **Run:** Opens at `localhost:5000`

### Option C: Tkinter
- **Pros:** No dependencies, native desktop feel
- **Cons:** Dated appearance, limited charts
- **Run:** Double-click .py file

### Option D: Dash/Plotly
- **Pros:** Best visualizations, interactive charts
- **Cons:** Learning curve
- **Run:** Opens in browser

## Integration Points

### Input Methods
1. **Paste URLs** → Extract search IDs → Write endpoints.txt
2. **Upload CSV** → Parse HigherGov export → Extract IDs
3. **Direct entry** → Search IDs directly → Write endpoints.txt
4. **Auto-fetch** → Scheduled API calls → Get new searches

### Trigger Methods
- Write endpoints.txt then call `subprocess.run(['python', 'BATCH_RUN.py'])`
- OR direct call with IDs as arguments
- OR watch folder for new CSVs

### Output Reading
- Poll SOS_Output/ directory for new folders
- Read CSVs as they're created
- Parse batch_summary_*.txt for status

## Testing Strategy

1. **Dummy Data Testing**
   - UI fully functional with mock CSVs
   - All charts/filters work
   - No core dependency

2. **Integration Testing**  
   - Test subprocess calls
   - Verify file writing
   - Check CSV parsing

3. **End-to-End Testing**
   - Real search IDs
   - Full processing
   - Results display

## DO NOT

- Import any files from parent directory
- Modify core processing logic
- Assume specific core behavior
- Couple UI to implementation details

## REMEMBER

- CSV format is the contract
- UI can evolve independently
- Core can evolve independently
- Integration is just file I/O

## Next Session Notes

When returning to this project:
1. Check if core CSV format has changed
2. Review dummy data for accuracy
3. Test integration bridge if connected
4. Keep separation absolute