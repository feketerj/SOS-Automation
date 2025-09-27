# NEXT SPRINT PLAN - POST-VALIDATION
**Created:** September 27, 2025
**Status:** Planning Document
**Prerequisites:** System validation complete with consistent results

## SPRINT 1: UI ENHANCEMENT PACKAGE
**Duration:** 1 week
**Goal:** Make the UI production-ready

### Tasks
```yaml
UI_001:
  task: Add real-time progress indicator
  effort: 4 hours
  files: ui_service/app.py
  description: Show which stage is currently processing

UI_002:
  task: Implement filtering and search
  effort: 6 hours
  files: ui_service/app.py
  description: Filter by GO/NO-GO, agency, date range

UI_003:
  task: Add export to Excel button
  effort: 3 hours
  dependencies: pandas, openpyxl
  description: Export current view to .xlsx

UI_004:
  task: Create pipeline visualization
  effort: 8 hours
  files: ui_service/pipeline_viz.py (new)
  description: Visual flow diagram with counts

UI_005:
  task: Add cost tracking display
  effort: 2 hours
  files: ui_service/app.py
  description: Show cumulative API costs
```

---

## SPRINT 2: OUTPUT SCHEMA V2
**Duration:** 3 days
**Goal:** Enhanced output with more metadata

### Schema Changes
```python
# Current fields + new additions
{
    # Existing fields...
    "confidence_score": 0.95,        # NEW: 0-1 confidence
    "processing_time_ms": 4500,      # NEW: Total time
    "stage_timings": {               # NEW: Per-stage timing
        "regex_ms": 50,
        "batch_ms": 3000,
        "agent_ms": 1450
    },
    "api_costs": {                   # NEW: Cost breakdown
        "batch": 0.002,
        "agent": 0.005,
        "total": 0.007
    },
    "structured_rationale": {        # NEW: Structured reasoning
        "primary_factors": [...],
        "risk_factors": [...],
        "mitigating_factors": [...]
    },
    "metadata_version": "2.0"       # NEW: Schema version
}
```

### Implementation Files
- `pipeline_output_manager.py` - Update save methods
- `RUN_ASSESSMENT.py` - Add timing collection
- `cost_tracker.py` (new) - Cost calculation module

---

## SPRINT 3: VERIFICATION AGENT
**Duration:** 1 week
**Goal:** Add 4th stage for GO verification

### Architecture
```
Stage 1: Regex (FREE)
Stage 2: Batch (50% off)
Stage 3: Agent (full price)
Stage 4: Verification (full price, GO only) ← NEW
```

### Implementation
```python
# In RUN_ASSESSMENT.py, after Stage 3
if final_decision == "GO":
    verification = verify_go_decision(opportunity)
    if verification.disagrees:
        final_decision = "NEEDS_REVIEW"
        add_to_review_queue(opportunity)
```

### Files to Modify
- `RUN_ASSESSMENT.py` - Add Stage 4
- `verification_agent.py` (new) - Verification logic
- `pipeline_output_manager.py` - Add verification tracking

---

## SPRINT 4: BASIC AUTOMATION
**Duration:** 3 days
**Goal:** Daily automated runs

### Windows Task Scheduler Setup
```xml
<Task>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2025-09-28T06:00:00</StartBoundary>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Actions>
    <Exec>
      <Command>python</Command>
      <Arguments>C:\...\RUN_ASSESSMENT.py</Arguments>
    </Exec>
  </Actions>
</Task>
```

### Automation Features
- [ ] Auto-fetch saved searches from HigherGov
- [ ] Run assessment pipeline
- [ ] Generate daily report
- [ ] Send email summary
- [ ] Archive old results

### New Files
- `automation/daily_runner.py`
- `automation/email_sender.py`
- `automation/report_generator.py`

---

## SPRINT 5: EMAIL NOTIFICATIONS
**Duration:** 2 days
**Goal:** Send GO opportunities via email

### Email Template
```html
<h2>SOS Assessment Results</h2>
<p>Date: {date}</p>
<p>Total Assessed: {total}</p>
<p>GO Opportunities: {go_count}</p>

<h3>Action Required - GO Opportunities</h3>
<table>
  <tr>
    <th>ID</th>
    <th>Title</th>
    <th>Agency</th>
    <th>Link</th>
  </tr>
  {go_opportunities_rows}
</table>
```

### Implementation
```python
# email_notifier.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_go_notifications(results):
    go_opps = [r for r in results if r['result'] == 'GO']
    if go_opps:
        send_email(
            to=CONFIG['email_recipients'],
            subject=f"SOS: {len(go_opps)} GO Opportunities Found",
            body=render_template(go_opps)
        )
```

---

## SPRINT 6: ZAPIER WEBHOOKS
**Duration:** 1 week
**Goal:** Enable Zapier integration

### Webhook Endpoints
```python
# api/webhooks.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook/assessment-complete', methods=['POST'])
def assessment_complete():
    # Trigger Zapier when assessment finishes
    return jsonify({"status": "received"})

@app.route('/webhook/go-found', methods=['POST'])
def go_found():
    # Trigger Zapier for each GO
    return jsonify({"status": "received"})

@app.route('/webhook/trigger-assessment', methods=['POST'])
def trigger_assessment():
    # Allow Zapier to trigger new assessment
    data = request.json
    queue_assessment(data['search_id'])
    return jsonify({"status": "queued"})
```

### Zapier App Configuration
```json
{
  "triggers": {
    "assessment_complete": {
      "noun": "Assessment",
      "display": "New Assessment Complete"
    },
    "go_opportunity": {
      "noun": "GO Opportunity",
      "display": "New GO Found"
    }
  },
  "actions": {
    "run_assessment": {
      "noun": "Assessment",
      "display": "Run New Assessment"
    }
  }
}
```

---

## SPRINT 7: HIGHERGOV INTEGRATION
**Duration:** 2 weeks
**Goal:** Deep bidirectional integration

### Phase 1: Enhanced Pull
- [ ] Subscribe to opportunity updates
- [ ] Download all attachments
- [ ] Track amendments
- [ ] Monitor Q&A sections

### Phase 2: Push Capabilities
- [ ] Mark as reviewed in HigherGov
- [ ] Add assessment tags
- [ ] Create custom fields
- [ ] Sync status updates

### Implementation Approach
```python
# highergov_sync.py
class HigherGovSync:
    def setup_webhook(self):
        # Subscribe to HigherGov webhooks

    def on_opportunity_update(self, opp_id):
        # Re-run assessment on updates

    def push_assessment(self, assessment):
        # Send results back to HigherGov
```

---

## IMPLEMENTATION NOTES

### Priority Order (After Validation)
1. **UI Enhancements** - Immediate user value
2. **Email Notifications** - Critical for GO alerts
3. **Basic Automation** - Reduce manual work
4. **Output Schema V2** - Better tracking
5. **Zapier Webhooks** - External integrations
6. **Verification Agent** - Accuracy improvement
7. **HigherGov Integration** - Full circle

### Risk Mitigation
- Keep old code paths until new ones proven
- Version all API changes
- Test each sprint independently
- Maintain rollback capability
- Document all changes

### Success Criteria Per Sprint
- No degradation in existing functionality
- All tests still pass
- Cost increase < 10%
- User acceptance confirmed
- Documentation updated

### Development Pattern
```python
# For each new feature
def implement_feature():
    # 1. Create feature flag
    if FEATURE_FLAGS.get('new_feature', False):
        # New implementation
    else:
        # Existing implementation

    # 2. Test thoroughly
    # 3. Gradual rollout
    # 4. Monitor metrics
    # 5. Full deployment
```

This plan provides concrete, implementable tasks that can begin as soon as the current system is validated and producing consistent results.