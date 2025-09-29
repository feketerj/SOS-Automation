# Debugging Plan for unified_pipeline_output.py

## Issues to Check

### 1. Schema Compliance
- [ ] Check if output matches exact schema requirements
- [ ] Verify required fields are present
- [ ] Check enum values are correct
- [ ] Validate field types match schema

### 2. Data Handling Issues
- [ ] Handle None values properly
- [ ] Handle missing keys in dictionaries
- [ ] Handle empty lists/arrays
- [ ] Handle special characters in strings

### 3. Edge Cases
- [ ] What if stage_results is empty?
- [ ] What if no knockout occurred (all stages passed)?
- [ ] What if opportunity metadata is missing?
- [ ] What if URLs are malformed or missing?

### 4. Integration Issues
- [ ] Check compatibility with existing Decision enum from multi_stage_pipeline
- [ ] Verify stage name mappings are complete
- [ ] Test with actual pipeline output (not just test data)
- [ ] Check if CSV headers match expected format

### 5. File Writing Issues
- [ ] Handle directory creation errors
- [ ] Handle file write permissions
- [ ] Handle existing files (overwrite behavior)
- [ ] Ensure CSV escaping for special characters

## Test Cases to Run

### Test 1: Empty/None Values
```python
# Test with minimal data
test_empty = {
    "search_id": None,
    "metadata": {}
}
```

### Test 2: Full Pipeline Completion (No Knockout)
```python
# All 20 stages complete with GO
test_complete = {
    "final_decision": "GO",
    "stages_processed": 20,
    "knockout_stage": None
}
```

### Test 3: Special Characters
```python
# Test with quotes, commas, newlines
test_special = {
    "title": 'Parts for "Special" Aircraft, Inc.',
    "rationale": "Line 1\nLine 2\nLine 3"
}
```

### Test 4: Integration with Actual Pipeline
```python
# Import and test with real pipeline
from multi_stage_pipeline import MultiStagePipeline, Decision
```

## Fixes Needed

1. **Missing stage mappings** - Only has 2 stages mapped, needs all 20
2. **Enum compatibility** - Uses string "NO-GO" but pipeline uses Decision.NO_GO enum
3. **Evidence handling** - Currently creates empty list for knock_pattern
4. **GO-only CSV** - Not created because result="NO-GO" in test
5. **Missing fields** - Some schema fields not included (e.g., knock_out_reasons)

## Implementation Plan

1. Fix stage mapping dictionary
2. Add enum conversion helper
3. Fix evidence/knock_pattern extraction
4. Add comprehensive error handling
5. Test with real pipeline integration
6. Add validation for all schema fields