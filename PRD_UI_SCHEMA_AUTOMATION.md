# PRODUCT REQUIREMENTS DOCUMENT
## UI Enhancements, Output Schema v2, and Basic Automation

**Document Version:** 1.0
**Date:** September 27, 2025
**Author:** SOS Automation Team
**Status:** Draft
**Review Cycle:** 30 days

---

## EXECUTIVE SUMMARY

This PRD outlines three critical enhancements to the SOS Assessment Automation Tool that will transform it from a functional pipeline into a production-ready enterprise solution. These enhancements focus on user experience, data richness, and operational efficiency while maintaining the core assessment accuracy that has been validated.

### Scope
1. **UI Enhancements** - Transform the basic Streamlit interface into a comprehensive operations dashboard
2. **Output Schema v2** - Enrich assessment data with confidence scores, timing metrics, and structured reasoning
3. **Basic Automation** - Implement daily scheduled runs with email notifications

### Timeline
- **Total Duration:** 3-4 weeks
- **Start Date:** Post-validation (est. October 1, 2025)
- **Target Completion:** October 31, 2025

### Investment
- **Development Hours:** 120 hours
- **Testing Hours:** 40 hours
- **Documentation:** 20 hours
- **Total Effort:** 180 hours (4.5 weeks @ 40 hrs/week)

---

## 1. UI ENHANCEMENTS

### 1.1 Problem Statement

**Current State:**
- Basic Streamlit interface showing static data tables
- No real-time progress indication during assessment
- Limited filtering and search capabilities
- No export functionality beyond manual copy/paste
- Lack of visual representation of pipeline flow
- No cost tracking visibility

**User Pain Points:**
- Cannot monitor assessment progress in real-time
- Difficult to find specific opportunities in large result sets
- Manual effort required to export data for reporting
- No visual understanding of where opportunities fail
- Unclear cost implications of running assessments

### 1.2 Proposed Solution

#### 1.2.1 Real-Time Progress Indicator
**Feature:** Live status bar showing current pipeline stage and progress

**User Story:** As an operator, I want to see which stage is currently processing so I know the assessment is running and how long it might take.

**Acceptance Criteria:**
- Progress bar shows 3 stages with current stage highlighted
- Display count of opportunities processed vs. total
- Show estimated time remaining based on historical data
- Update every 2 seconds during processing

**Technical Implementation:**
```python
# Streamlit component
import streamlit as st

def show_pipeline_progress(current_stage, current_count, total_count):
    progress = current_count / total_count
    st.progress(progress)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Stage 1: Regex",
                  "✅ Complete" if current_stage > 1 else "🔄 Processing")
    with col2:
        st.metric("Stage 2: Batch",
                  "✅ Complete" if current_stage > 2 else
                  "🔄 Processing" if current_stage == 2 else "⏳ Waiting")
    with col3:
        st.metric("Stage 3: Agent",
                  "✅ Complete" if current_stage > 3 else
                  "🔄 Processing" if current_stage == 3 else "⏳ Waiting")
```

#### 1.2.2 Advanced Filtering and Search
**Feature:** Multi-field filtering with saved filter sets

**User Story:** As an analyst, I want to filter results by multiple criteria simultaneously so I can focus on specific opportunity types.

**Acceptance Criteria:**
- Filter by: Result (GO/NO-GO/INDETERMINATE)
- Filter by: Agency (multi-select dropdown)
- Filter by: Date range (start/end date pickers)
- Filter by: Knockout category (multi-select)
- Search by: Keywords in title/description
- Save/load filter configurations
- Clear all filters button

**UI Mockup:**
```
┌─────────────────────────────────────────────┐
│ 🔍 Filters                                  │
├─────────────────────────────────────────────┤
│ Result:    [✓] GO [✓] NO-GO [ ] INDET      │
│ Agencies:  [Navy ▼] [Air Force ▼] [+]      │
│ Date:      [09/01/25] to [09/30/25]        │
│ Category:  [Military ▼] [Set-aside ▼]       │
│ Search:    [________________] 🔍            │
│                                             │
│ [Apply] [Clear] [Save Filter] [Load ▼]     │
└─────────────────────────────────────────────┘
```

#### 1.2.3 Export to Excel
**Feature:** One-click export to formatted Excel workbook

**User Story:** As a manager, I want to export assessment results to Excel so I can create custom reports and share with stakeholders.

**Acceptance Criteria:**
- Export includes all visible columns based on current filters
- Excel file has multiple sheets:
  - Summary sheet with statistics
  - Detailed results sheet
  - GO opportunities sheet
  - Knockout analysis sheet
- Formatted with headers, colors, and frozen panes
- Auto-sized columns for readability
- Include charts for key metrics

**Technical Approach:**
```python
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font
from openpyxl.chart import PieChart, Reference

def export_to_excel(filtered_data):
    with pd.ExcelWriter('SOS_Assessment_Export.xlsx',
                       engine='openpyxl') as writer:
        # Summary sheet
        summary_df = create_summary(filtered_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        # Detailed results
        filtered_data.to_excel(writer, sheet_name='All Results', index=False)

        # GO opportunities only
        go_data = filtered_data[filtered_data['result'] == 'GO']
        go_data.to_excel(writer, sheet_name='GO Opportunities', index=False)

        # Format workbook
        workbook = writer.book
        for sheet in workbook.worksheets:
            format_sheet(sheet)

        add_charts(workbook)

    return 'SOS_Assessment_Export.xlsx'
```

#### 1.2.4 Pipeline Visualization
**Feature:** Interactive flow diagram showing opportunity progression

**User Story:** As a team lead, I want to visualize how opportunities flow through the pipeline so I can identify bottlenecks and optimize the process.

**Acceptance Criteria:**
- Sankey diagram showing flow from input through three stages
- Numbers at each stage showing count and percentage
- Click on stage to see list of opportunities
- Color coding: Green (GO), Red (NO-GO), Yellow (INDETERMINATE)
- Hover tooltips with additional details

**Visual Design:**
```
Input (100) ─────┬──→ Regex ────┬──→ Batch ────┬──→ Agent ────→ Output
                 │      │        │      │       │      │
                 │      ▼        │      ▼       │      ▼
                 │   NO-GO(40)   │   NO-GO(20)  │   NO-GO(10)
                 │               │              │
                 └── Bypass(0) ──┴── Manual(0) ─┴── Review(5)

Legend: ━ Flow  ▬ Knockout  ═ Special Path
```

#### 1.2.5 Cost Tracking Display
**Feature:** Real-time cost accumulator with projections

**User Story:** As a budget owner, I want to see how much each assessment run costs so I can manage expenses and predict monthly costs.

**Acceptance Criteria:**
- Display current run cost in real-time
- Show cost breakdown by stage (Batch vs Agent)
- Display month-to-date total costs
- Project monthly cost based on run rate
- Cost per opportunity metric
- Savings from regex filtering displayed

**Metrics Display:**
```python
def show_cost_metrics(run_data):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Current Run", f"${run_data.current_cost:.4f}",
                  delta=f"${run_data.cost_per_opp:.4f}/opp")
    with col2:
        st.metric("MTD Total", f"${run_data.mtd_total:.2f}",
                  delta=f"{run_data.day_of_month} days")
    with col3:
        st.metric("Projected Monthly", f"${run_data.projected:.2f}",
                  delta=f"vs budget ${run_data.budget:.2f}")
    with col4:
        st.metric("Regex Savings", f"${run_data.savings:.2f}",
                  delta=f"{run_data.savings_pct:.0%} saved")
```

### 1.3 Success Metrics

| Metric | Current | Target | Measurement Method |
|--------|---------|--------|-------------------|
| Time to find specific opportunity | 2+ minutes | <10 seconds | User testing |
| Export preparation time | 15 minutes | <1 minute | Automated |
| Pipeline visibility | None | 100% real-time | System monitoring |
| Cost awareness | Post-run only | Real-time | Dashboard metrics |
| User satisfaction | N/A | >8/10 | Survey |

---

## 2. OUTPUT SCHEMA V2

### 2.1 Problem Statement

**Current State:**
- Basic decision data (GO/NO-GO/INDETERMINATE) with limited context
- No confidence scoring to indicate decision reliability
- Missing performance metrics for optimization
- Unstructured reasoning text difficult to analyze
- No versioning for backward compatibility

**Business Impact:**
- Cannot prioritize high-confidence GOs
- Unable to identify slow pipeline stages
- Difficult to analyze patterns in reasoning
- No cost attribution per opportunity
- Breaking changes risk with schema updates

### 2.2 Proposed Solution

#### 2.2.1 Confidence Scoring
**Feature:** Numerical confidence score (0-1) for each decision

**Calculation Method:**
```python
def calculate_confidence(opportunity):
    confidence = 1.0

    # Factors that reduce confidence
    if opportunity.get('document_length', 0) < 1000:
        confidence *= 0.8  # Limited documentation

    if opportunity.get('stage2_batch') != opportunity.get('stage3_agent'):
        confidence *= 0.7  # Disagreement between models

    if 'INDETERMINATE' in opportunity.get('stage1_regex', ''):
        confidence *= 0.9  # Unclear from regex

    # Factors that increase confidence
    if all_stages_agree(opportunity):
        confidence = min(confidence * 1.2, 1.0)

    return round(confidence, 3)
```

**Usage:**
- Prioritize high-confidence GOs for immediate action
- Flag low-confidence NO-GOs for manual review
- Track confidence trends over time
- Identify opportunities needing human verification

#### 2.2.2 Performance Metrics
**Feature:** Detailed timing and cost breakdown

**Schema Addition:**
```json
{
    "performance_metrics": {
        "total_processing_time_ms": 4567,
        "stage_timings": {
            "regex_ms": 23,
            "batch_queue_ms": 1200,
            "batch_processing_ms": 2100,
            "agent_ms": 1244
        },
        "document_fetch_ms": 890,
        "api_costs": {
            "batch_cost": 0.0021,
            "agent_cost": 0.0054,
            "total_cost": 0.0075,
            "cost_per_1k_chars": 0.0003
        },
        "token_usage": {
            "batch_input_tokens": 2100,
            "batch_output_tokens": 450,
            "agent_input_tokens": 3200,
            "agent_output_tokens": 680,
            "total_tokens": 6430
        }
    }
}
```

**Benefits:**
- Identify performance bottlenecks
- Optimize slow stages
- Track cost per opportunity
- Monitor token efficiency
- Predict processing times

#### 2.2.3 Structured Reasoning
**Feature:** Parse reasoning into analyzable components

**Schema Structure:**
```json
{
    "structured_reasoning": {
        "decision_factors": {
            "primary": [
                {
                    "factor": "military_platform",
                    "value": "F-16",
                    "impact": "negative",
                    "weight": 0.9
                }
            ],
            "secondary": [
                {
                    "factor": "set_aside",
                    "value": "small_business",
                    "impact": "negative",
                    "weight": 0.6
                }
            ]
        },
        "risk_assessment": {
            "technical_risk": "low",
            "compliance_risk": "high",
            "competition_risk": "medium"
        },
        "exceptions_considered": [
            {
                "exception": "FAA_8130",
                "applicable": false,
                "reason": "Not a commercial platform"
            }
        ],
        "recommendation": {
            "action": "NO_BID",
            "confidence": 0.95,
            "alternative": "Monitor for amendments"
        }
    }
}
```

**Analysis Capabilities:**
- Aggregate common knockout factors
- Identify pattern exceptions
- Track risk distributions
- Analyze recommendation patterns
- Machine learning training data

#### 2.2.4 Schema Versioning
**Feature:** Version tracking with migration support

**Implementation:**
```python
SCHEMA_VERSION = "2.0"
SCHEMA_COMPATIBILITY = ["1.0", "1.1", "2.0"]

def migrate_schema(data, from_version, to_version):
    """Migrate data between schema versions"""
    if from_version == "1.0" and to_version == "2.0":
        # Add new fields with defaults
        data['confidence_score'] = calculate_confidence(data)
        data['performance_metrics'] = get_default_metrics()
        data['structured_reasoning'] = parse_reasoning(data.get('rationale', ''))
        data['schema_version'] = "2.0"
    return data

def validate_schema(data):
    """Ensure data conforms to current schema"""
    required_fields = [
        'schema_version',
        'confidence_score',
        'performance_metrics',
        'structured_reasoning'
    ]
    return all(field in data for field in required_fields)
```

### 2.3 Success Metrics

| Metric | Current | Target | Measurement Method |
|--------|---------|--------|-------------------|
| Decision confidence visibility | None | 100% | Schema validation |
| Performance tracking | None | All stages | Metrics collection |
| Reasoning analysis | Manual | Automated | Query capability |
| Schema compatibility | N/A | 100% backward | Migration testing |
| Data completeness | 60% | 95% | Field population |

---

## 3. BASIC AUTOMATION

### 3.1 Problem Statement

**Current State:**
- Manual execution required for each assessment run
- No scheduled or triggered assessments
- Manual monitoring for completion
- Results must be manually distributed
- No automatic cleanup of old data

**Operational Impact:**
- Requires dedicated operator time
- Assessments may be delayed or missed
- Inconsistent run schedules
- Manual effort for report distribution
- Storage accumulation without cleanup

### 3.2 Proposed Solution

#### 3.2.1 Scheduled Daily Runs
**Feature:** Windows Task Scheduler integration for automated execution

**Configuration:**
```xml
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2025-10-01T06:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Actions>
    <Exec>
      <Command>C:\Python39\python.exe</Command>
      <Arguments>C:\SOS-Automation\automation\daily_runner.py</Arguments>
      <WorkingDirectory>C:\SOS-Automation</WorkingDirectory>
    </Exec>
  </Actions>
  <Settings>
    <Priority>7</Priority>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
    </IdleSettings>
  </Settings>
</Task>
```

**Daily Runner Script:**
```python
# automation/daily_runner.py
import sys
import os
from datetime import datetime
import logging

sys.path.append('..')

def run_daily_assessment():
    logging.info(f"Starting daily run at {datetime.now()}")

    try:
        # 1. Fetch latest endpoints from HigherGov saved searches
        endpoints = fetch_saved_searches()

        # 2. Write to endpoints.txt
        with open('../endpoints.txt', 'w') as f:
            f.write('\n'.join(endpoints))

        # 3. Run assessment
        from RUN_ASSESSMENT import run_assessment
        success = run_assessment()

        # 4. Generate report
        if success:
            report = generate_daily_report()

            # 5. Send email
            send_email_report(report)

            # 6. Archive old results
            archive_old_results(days=30)

        logging.info("Daily run completed successfully")

    except Exception as e:
        logging.error(f"Daily run failed: {e}")
        send_error_notification(e)

if __name__ == "__main__":
    run_daily_assessment()
```

#### 3.2.2 Email Report Generation
**Feature:** Automated HTML email reports with attachments

**Email Template:**
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { background: #2c3e50; color: white; padding: 20px; }
        .summary { background: #f8f9fa; padding: 15px; margin: 20px 0; }
        .metrics { display: flex; justify-content: space-around; }
        .metric { text-align: center; padding: 10px; }
        .metric .number { font-size: 2em; font-weight: bold; }
        .go-list { background: #d4edda; padding: 15px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="header">
        <h1>SOS Daily Assessment Report</h1>
        <p>{{ date }}</p>
    </div>

    <div class="summary">
        <h2>Executive Summary</h2>
        <div class="metrics">
            <div class="metric">
                <div class="number">{{ total_assessed }}</div>
                <div>Total Assessed</div>
            </div>
            <div class="metric" style="color: green;">
                <div class="number">{{ go_count }}</div>
                <div>GO Opportunities</div>
            </div>
            <div class="metric" style="color: red;">
                <div class="number">{{ nogo_count }}</div>
                <div>NO-GO</div>
            </div>
            <div class="metric">
                <div class="number">${{ total_cost }}</div>
                <div>Assessment Cost</div>
            </div>
        </div>
    </div>

    {% if go_opportunities %}
    <div class="go-list">
        <h2>🎯 Action Required - GO Opportunities</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Agency</th>
                <th>Confidence</th>
                <th>Action</th>
            </tr>
            {% for opp in go_opportunities %}
            <tr>
                <td>{{ opp.id }}</td>
                <td>{{ opp.title }}</td>
                <td>{{ opp.agency }}</td>
                <td>{{ opp.confidence }}%</td>
                <td><a href="{{ opp.url }}">View →</a></td>
            </tr>
            {% endfor %}
        </table>
    </div>
    {% endif %}

    <div class="footer">
        <p>Full report attached. For questions, contact sos-automation@company.com</p>
    </div>
</body>
</html>
```

**Email Configuration:**
```python
# automation/email_config.py
EMAIL_CONFIG = {
    "smtp_server": "smtp.office365.com",
    "smtp_port": 587,
    "use_tls": True,
    "sender": "sos-automation@company.com",
    "sender_password": "ENCRYPTED_PASSWORD_HERE",
    "recipients": [
        "team-lead@company.com",
        "analyst@company.com",
        "manager@company.com"
    ],
    "cc_on_go": [
        "contracts@company.com"
    ],
    "error_recipients": [
        "it-support@company.com"
    ]
}
```

#### 3.2.3 Auto-fetch Saved Searches
**Feature:** Automatically pull configured HigherGov searches

**Configuration File:**
```json
{
    "saved_searches": [
        {
            "name": "Daily Aviation Parts",
            "search_id": "AR1yyM0PV54_Ila0ZV6J6",
            "enabled": true,
            "frequency": "daily"
        },
        {
            "name": "Navy Solicitations",
            "search_id": "BR2xxN1QW65_Jmb1YW7K7",
            "enabled": true,
            "frequency": "daily"
        },
        {
            "name": "Emergency Requirements",
            "search_id": "CR3zzP2RX76_Knc2ZX8L8",
            "enabled": true,
            "frequency": "hourly",
            "priority": "high"
        }
    ]
}
```

#### 3.2.4 Results Archival
**Feature:** Automatic cleanup of old results to manage storage

**Archival Strategy:**
```python
def archive_old_results(days=30):
    """Archive results older than specified days"""
    archive_date = datetime.now() - timedelta(days=days)
    archive_path = Path("SOS_Output_Archive") / archive_date.strftime("%Y-%m")

    for run_folder in Path("SOS_Output").glob("*/Run_*"):
        run_date = extract_date_from_folder(run_folder)

        if run_date < archive_date:
            # Compress before archiving
            zip_path = archive_path / f"{run_folder.name}.zip"
            compress_folder(run_folder, zip_path)

            # Verify compression
            if verify_zip(zip_path):
                # Delete original
                shutil.rmtree(run_folder)
                logging.info(f"Archived {run_folder.name}")
            else:
                logging.error(f"Failed to archive {run_folder.name}")

    # Clean up very old archives (>90 days)
    cleanup_old_archives(days=90)
```

### 3.3 Success Metrics

| Metric | Current | Target | Measurement Method |
|--------|---------|--------|-------------------|
| Manual intervention required | 100% | <5% | Operation logs |
| Assessment delay | Variable | <1 hour | Timestamp tracking |
| Report distribution time | Manual | <5 min after completion | Email timestamps |
| Storage growth | Unlimited | Controlled (<100GB) | Disk monitoring |
| Missed assessments | Unknown | 0 | Run history |

---

## TECHNICAL REQUIREMENTS

### Infrastructure
- **Python:** 3.9+ with packages: streamlit, pandas, openpyxl, plotly, schedule
- **Windows:** Task Scheduler enabled with appropriate permissions
- **Email:** SMTP server access with authentication
- **Storage:** 100GB available for results and archives
- **Memory:** 8GB RAM minimum for large assessments

### API Considerations
- HigherGov API rate limits respected (100 req/min)
- Mistral API concurrency limits (5 parallel)
- Email server connection limits (10/min)

### Security Requirements
- Email passwords encrypted in configuration
- API keys remain hardcoded (not in emails)
- Sensitive data not included in reports
- Archive access restricted to authorized users

### Performance Requirements
- UI updates within 2 seconds
- Export generation <30 seconds
- Email send <10 seconds
- Daily run completion <2 hours

---

## RISKS AND MITIGATION

### Risk Matrix

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|-------------------|
| UI performance degradation | Medium | High | Pagination, lazy loading |
| Schema breaking changes | Low | High | Version migration, testing |
| Email delivery failures | Medium | Medium | Retry logic, fallback storage |
| Storage overflow | Low | High | Aggressive archival, alerts |
| Scheduled run failures | Medium | High | Error notifications, manual trigger |

### Rollback Plan
1. All features behind feature flags
2. Previous version maintained in parallel
3. One-click rollback script prepared
4. Data export before any schema changes
5. Email lists backed up before automation

---

## TESTING STRATEGY

### Test Coverage Requirements

| Component | Unit Tests | Integration Tests | E2E Tests | User Acceptance |
|-----------|------------|------------------|-----------|-----------------|
| UI Enhancements | 80% | 70% | 100% | Required |
| Schema v2 | 95% | 90% | 100% | Required |
| Automation | 90% | 85% | 100% | Required |

### Test Scenarios
1. **Load Testing:** 1000+ opportunities in UI
2. **Schema Migration:** v1.0 → v2.0 with real data
3. **Automation Reliability:** 30-day continuous run
4. **Email Delivery:** Various recipient configs
5. **Error Recovery:** Network, API, storage failures

---

## SUCCESS CRITERIA

### Phase Completion Checklist

#### UI Enhancements ✓
- [ ] Progress indicator updating in real-time
- [ ] Filters working with 1000+ records
- [ ] Excel export <30 seconds
- [ ] Pipeline visualization accurate
- [ ] Cost tracking within 1% accuracy

#### Output Schema v2 ✓
- [ ] 100% backward compatibility
- [ ] Confidence scores validated
- [ ] Performance metrics accurate
- [ ] Reasoning properly structured
- [ ] Migration tool tested

#### Basic Automation ✓
- [ ] 30 consecutive daily runs successful
- [ ] Email delivery rate >99%
- [ ] Storage maintained <100GB
- [ ] Error notifications working
- [ ] Manual override available

### Business Outcomes
- **Efficiency:** 80% reduction in manual effort
- **Visibility:** 100% of assessments trackable
- **Reliability:** 99.5% uptime
- **Satisfaction:** User NPS >8
- **ROI:** 200% within 3 months

---

## APPENDICES

### A. UI Mockups
[Detailed Figma mockups would be linked here]

### B. Schema Documentation
[Complete JSON schema specifications]

### C. API Documentation
[Email, scheduling, and integration APIs]

### D. Operational Runbook
[Step-by-step operational procedures]

### E. Training Materials
[User guides and video tutorials]

---

## APPROVAL

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | | | |
| Technical Lead | | | |
| QA Lead | | | |
| Operations Manager | | | |
| Finance Approver | | | |

---

**Document Control:**
- Version 1.0: Initial draft
- Review Period: September 27 - October 7, 2025
- Implementation Start: October 8, 2025
- Target Completion: October 31, 2025