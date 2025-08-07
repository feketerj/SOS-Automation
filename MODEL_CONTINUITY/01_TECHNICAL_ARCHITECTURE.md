# TECHNICAL ARCHITECTURE OVERVIEW

## SYSTEM DESIGN PHILOSOPHY

**Design Pattern:** Hierarchical filtering with fail-fast logic
**Performance Strategy:** Deterministic pre-filtering to minimize LLM inference costs
**Reliability Strategy:** Comprehensive logging and error recovery
**Maintainability Strategy:** Modular architecture with clear separation of concerns

---

## CORE ASSESSMENT LOGIC (filters/sos_official_filter.py)

### Two-Phase Assessment Structure

**Phase 0 - Preliminary Gates (Quick Elimination):**
1. **Aviation Check**: Must be aviation-related opportunity
2. **Currency Check**: Must be current opportunity (not expired)  
3. **Platform Viability**: Must be viable aircraft platform

**Phase 1 - Hard Stops (Detailed Compliance):**
1. **SAR Detection**: Source Approval Request requirements
2. **Sole Source**: Restricted to specific vendors
3. **Technical Data**: Requires proprietary technical data
4. **Security Clearance**: Requires security clearances
5. **New Parts Only**: Excludes refurbished/surplus parts
6. **Prohibited Certifications**: Requires specific certifications
7. **ITAR/Export Control**: Export control restrictions
8. **OEM Restrictions**: Original Equipment Manufacturer only

### Decision Flow
```
Opportunity → Phase 0 (Aviation?) → NO → NO-GO
                     ↓ YES
            Phase 0 (Current?) → NO → NO-GO  
                     ↓ YES
            Phase 0 (Platform?) → NO → NO-GO
                     ↓ YES
            Phase 1 (SAR?) → YES → NO-GO
                     ↓ NO
            Phase 1 (Sole Source?) → YES → NO-GO
                     ↓ NO
            Phase 1 (Tech Data?) → YES → NO-GO
                     ↓ NO
            [Continue all Phase 1 checks...]
                     ↓ ALL PASS
                    GO
```

---

## REGEX PATTERN LIBRARY

### Aviation Detection (40+ patterns)
```python
# Aircraft designators
r'\b(C-130|KC-46|P-8|F-16|UH-60|CH-47|F-15|F-18|F-22|F-35|A-10|B-1B|B-2|B-52)\b'

# Aviation keywords
r'\b(aircraft|helicopter|rotorcraft|airplane|aviation|aerospace)\b'

# Aviation components
r'\b(avionics|flight\s+control|landing\s+gear|aircraft\s+engine)\b'
```

### SAR Detection (30+ patterns)
```python
# Direct SAR references
r'(source\s+approval\s+request|SAR\s+package|design\s+control\s+activity)'

# Contextual SAR indicators
r'(engineering\s+source\s+approval|approved\s+source\s+only|DLA\s+does\s+not\s+possess)'
```

### Platform Classification
- **Pure Military**: F-16, UH-60, CH-47, etc. (immediate pass)
- **Civilian Equivalent**: C-130 (civilian L-100), 737 (military P-8), etc.
- **Restricted Platforms**: Classified or export-controlled aircraft

---

## API INTEGRATION ARCHITECTURE

### HigherGov API Client (api_clients/highergov_client_enhanced.py)

**Core Functions:**
```python
def get_saved_search_opportunities(search_id, limit=50)
def get_opportunity_details(opportunity_id)  
def search_opportunities(query, filters=None)
```

**Error Handling:**
- Automatic retry on API failures
- Graceful fallback to mock data for testing
- Comprehensive API call logging

**Performance Features:**
- Configurable pagination
- Rate limiting compliance
- Response caching for development

---

## ENHANCED LOGGING SYSTEM

### Five Specialized Log Files

1. **`logs/sos_pipeline.log`** - Main application flow
2. **`logs/api_calls.log`** - All API interactions
3. **`logs/filter_decisions.log`** - Detailed filter decisions
4. **`logs/performance.log`** - Function execution timing
5. **`logs/errors.log`** - Errors and exceptions

### Machine-Readable Debug Data
- **`logs/debug_decisions.jsonl`** - Structured decision data for analysis
- **FilterDecisionLogger** - Tracks every filter step with context
- **Performance decorators** - Automatic timing of critical functions

### Debug Analysis Tools
- **SOSDebugAnalyzer** - Automated log analysis
- **Pattern enhancement recommendations**
- **Performance bottleneck identification**
- **Error pattern categorization**

---

## DATA FLOW ARCHITECTURE

### Input Processing
```
HigherGov API Response
    ↓
Text Extraction (title, description, documents)
    ↓
Pattern Matching (regex-based assessment)
    ↓
Decision Logic (hierarchical evaluation)
    ↓
Result Generation (structured output)
```

### Output Format
```json
{
  "opportunity_id": "SPE4A525T634Q",
  "final_decision": "GO",
  "phase_0": {
    "aviation": "PASS - Aviation-related: 'AIRCRAFT' in context",
    "currency": "PASS - Current (0 days old)",
    "platform_viability": "PASS - General aviation"
  },
  "phase_1": {
    "sar": "PASS - No SAR requirements detected",
    "sole_source": "PASS - No sole source restrictions",
    "technical_data": "PASS - No technical data requirements"
  },
  "reasoning": ["All assessment criteria met - viable opportunity"]
}
```

---

## PERFORMANCE CHARACTERISTICS

### Benchmarks (Based on Aug 5, 2025 Test)
- **Processing Rate**: 25 opportunities/second
- **Memory Usage**: <50MB for 900 opportunity dataset
- **API Response Time**: ~150ms average per saved search call
- **Filter Execution Time**: ~2ms per opportunity average
- **Success Rate**: 99.9% successful API calls

### Scalability Considerations
- **Current Limit**: 100 opportunities per API call (pagination required for 900+)
- **Memory Efficiency**: Streaming processing for large datasets
- **CPU Efficiency**: Pre-compiled regex patterns
- **Storage Efficiency**: Compressed JSON output

---

## ERROR RECOVERY STRATEGIES

### API Failures
1. **Automatic retry** with exponential backoff
2. **Mock data fallback** for development/testing
3. **Comprehensive error logging** for debugging

### Data Processing Errors
1. **Graceful degradation** - continue processing other opportunities
2. **Context preservation** - log problematic text samples
3. **Pattern validation** - regex error handling

### System Resilience
1. **Input validation** - handle malformed API responses
2. **Output validation** - ensure consistent result format
3. **Resource management** - automatic cleanup and rotation

---

## INTEGRATION POINTS

### Current Integrations
- **HigherGov API** - Federal opportunity data
- **Environment Variables** - API keys and configuration
- **File System** - Output storage and logging

### Future Integration Possibilities
- **Database storage** - Opportunity history and analytics
- **Notification systems** - Real-time alerts for high-value opportunities
- **Business intelligence** - Performance dashboards and reporting
- **External APIs** - Additional data enrichment sources

---

## SECURITY CONSIDERATIONS

### API Key Management
- **Environment variables** - Secure storage of credentials
- **Key rotation support** - Easy credential updates
- **Access logging** - Track API usage

### Data Handling
- **No sensitive data storage** - Process and discard pattern
- **Audit trail** - Comprehensive decision logging
- **Export control compliance** - Proper ITAR/EAR handling

---

**END OF TECHNICAL ARCHITECTURE**
