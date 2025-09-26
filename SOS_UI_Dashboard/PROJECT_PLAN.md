# SOS UI DASHBOARD - PROJECT PLAN

## Vision
Local desktop application that makes SOS assessments as easy as copy-paste, with beautiful visualizations and zero command-line interaction.

## User Workflow

### Daily Use Case
```
1. Open SOS Dashboard (desktop shortcut)
2. Copy URLs from HigherGov browser tabs
3. Paste into dashboard
4. Click "Run Assessment"
5. See progress in real-time
6. View results immediately
7. Export reports for stakeholders
```

## Development Roadmap

### Week 1: Foundation (Sept 4-11)
- [x] Create folder structure
- [x] Write continuity docs
- [ ] Generate comprehensive dummy data
- [ ] Choose tech stack (Streamlit vs Flask)
- [ ] Build basic UI skeleton
- [ ] Implement URL parser

### Week 2: Core Features (Sept 11-18)
- [ ] Tab 1: Assessment Runner
  - [ ] URL paste box
  - [ ] CSV upload
  - [ ] Search ID direct entry
  - [ ] Progress bar
- [ ] Tab 2: Results Viewer
  - [ ] Table with sorting
  - [ ] Detail view modal
  - [ ] Export to Excel

### Week 3: Dashboard (Sept 18-25)
- [ ] Tab 3: Analytics Dashboard
  - [ ] GO/NO-GO pie chart
  - [ ] Knockout reasons bar chart
  - [ ] Time series trends
  - [ ] Processing time metrics
- [ ] Tab 4: Settings
  - [ ] API key management
  - [ ] Delay configuration
  - [ ] Output preferences

### Week 4: Integration (Sept 25-Oct 2)
- [ ] Build runner_bridge.py
- [ ] Connect to real batch processor
- [ ] Test with live data
- [ ] Error handling
- [ ] Polish UI

### Week 5: Enhancement
- [ ] Auto-fetch new searches
- [ ] Email notifications
- [ ] Historical database
- [ ] Advanced filtering
- [ ] Custom reports

## Feature Specifications

### Input Handler
**Accepts:**
- HigherGov URLs: `https://app.highergov.com/search-manager/[ID]`
- HigherGov CSV exports
- Plain text search IDs
- endpoints.txt file

**Outputs:**
- Clean list of search IDs
- Validation errors
- Duplicate detection

### Dashboard Components

#### Summary Cards
- Today's Assessments: [Count]
- GO Rate: [Percentage]
- Average Processing Time: [Minutes]
- Pending Queue: [Count]

#### Charts
1. **Decision Distribution** (Pie)
   - GO: Green
   - NO-GO: Red
   - INDETERMINATE: Yellow

2. **Knockout Reasons** (Bar)
   - Top 10 reasons
   - Sortable by frequency
   - Drill-down capable

3. **Trend Analysis** (Line)
   - Daily assessment volume
   - GO rate over time
   - Processing speed

4. **Platform Analysis** (Stacked Bar)
   - Decisions by aircraft type
   - Military vs Commercial
   - Part categories

### Results Table

**Columns:**
- Assessment Date
- Search ID (linked)
- Title
- Decision (colored)
- Reasoning
- Priority Score
- Days Until Due
- Company
- Actions (View/Export)

**Features:**
- Sort any column
- Filter by decision
- Search by keyword
- Bulk export
- Date range selection

### Settings Management

**Configurable:**
- API Keys (masked input)
- Processing delay (5-30 seconds)
- Auto-run schedule
- Output directory
- Email notifications
- CSV field mapping

## Technical Architecture

### File Structure
```
app.py                  # Main application
requirements.txt        # Dependencies
config.yaml            # User settings
/components
  ├── input_parser.py   # URL/CSV handling
  ├── runner_bridge.py  # Core system interface
  ├── data_loader.py    # CSV/JSON reader
  └── visualizations.py # Chart generation
/data
  ├── dummy_assessment.csv
  ├── historical_data.json
  └── config_defaults.yaml
/templates (if Flask)
  └── index.html
/static (if Flask)
  └── style.css
```

### Data Flow
```
User Input (URLs/CSV/IDs)
    ↓
Input Parser (validation/extraction)
    ↓
endpoints.txt (written to parent dir)
    ↓
Runner Bridge (subprocess call)
    ↓
Core System (../BATCH_RUN.py)
    ↓
CSVs Generated (../SOS_Output/)
    ↓
Data Loader (reads CSVs)
    ↓
UI Updates (charts/tables)
```

### State Management
- Settings: config.yaml
- Current batch: session_state.json
- History: assessment_history.db (SQLite)
- Cache: .cache/ directory

## Success Metrics

### Performance
- Load time < 2 seconds
- Update refresh < 1 second
- Handle 1000+ assessments in table
- Chart rendering < 500ms

### Usability
- Zero command-line interaction
- One-click assessment run
- Intuitive navigation
- Clear error messages
- Helpful tooltips

### Reliability
- Graceful error handling
- Resume interrupted batches
- Backup assessment data
- Validate all inputs
- Log all operations

## Risk Mitigation

### Separation Risks
- **Risk:** Core changes break UI
- **Mitigation:** Version checking, CSV validation

### Performance Risks
- **Risk:** Large datasets slow UI
- **Mitigation:** Pagination, lazy loading

### Integration Risks
- **Risk:** Subprocess calls fail
- **Mitigation:** Error handling, status checking

## Definition of Done

### MVP Complete When:
- [ ] UI runs without command line
- [ ] Can paste URLs and run assessment
- [ ] Results display in table
- [ ] Basic charts working
- [ ] Export to Excel works
- [ ] Settings are persistent
- [ ] Error handling complete

### Production Ready When:
- [ ] All planned features complete
- [ ] Tested with 1000+ assessments
- [ ] Documentation complete
- [ ] Installer/package created
- [ ] User training materials ready