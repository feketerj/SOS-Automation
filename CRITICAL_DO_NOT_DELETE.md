# CRITICAL: DOCUMENT INGESTION CONFIGURATION
**DO NOT MODIFY - LOCKED 2025-09-03**

## THE PROBLEM WE SOLVED (DO NOT REPEAT)
Documents were NOT being used in assessments even though they were being fetched. The assessment logic was only looking at titles, not the full 200KB+ of document text available.

## THE SOLUTION (LOCKED IN)

### 1. Documents ARE Being Fetched
- HigherGov API endpoint: `https://www.highergov.com/api-external/opportunity/`
- Each opportunity includes:
  - `description_text`: ~2,000-600,000 characters of FULL document text
  - `ai_summary`: ~1,000 character summary
  - `document_path`: Path to fetch additional documents if needed

### 2. Documents ARE Being Processed
The `highergov_batch_fetcher.py` correctly:
- Line 140-155: Combines `description_text` + `ai_summary` into `full_text`
- Line 164: Stores this in opportunity['text'] field
- Result: Each opportunity has 200KB+ of document text on average

### 3. Assessment MUST Use the 'text' Field
**CRITICAL:** The assessment must use `opportunity.get('text')` which contains ALL documents.
- NOT `opportunity.get('description')` - this is truncated
- NOT `opportunity.get('brief_description')` - this is truncated  
- USE `opportunity.get('text')` - this has EVERYTHING

## VERIFICATION CHECKLIST
When running assessments, verify:
```
✓ Average text length: ~200,000+ characters
✓ Document coverage: 12/12 (or close to 100%)
✓ Total text processed: 2,000,000+ characters for 12 opportunities
```

If you see:
- Average text < 50,000 chars → DOCUMENTS NOT BEING USED
- Coverage < 90% → FETCH FAILING
- Only 500-1000 chars → USING WRONG FIELD

## PRODUCTION RUNNER
Use `LOCKED_PRODUCTION_RUNNER.py` which:
1. ALWAYS fetches documents
2. ALWAYS uses the 'text' field
3. WARNS if text seems low
4. Shows document statistics

## DO NOT:
- Change the API endpoint from api-external
- Use description instead of text field
- Skip the process_opportunity step
- Ignore document coverage warnings

## CORRECT USAGE:
```python
# FETCH
raw_opps = fetcher.fetch_all_opportunities(search_id)

# PROCESS (CRITICAL STEP)
processed_opps = []
for opp in raw_opps:
    processed = fetcher.process_opportunity(opp)  # THIS GETS DOCUMENTS
    processed_opps.append(processed)

# ASSESS
for opp in processed_opps:
    full_text = opp.get('text', '')  # THIS HAS ALL DOCUMENTS
    # Now assess with 200KB+ of text
```

**This configuration is LOCKED. Do not troubleshoot document ingestion - it is working.**