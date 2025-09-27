# CLIENT CONFIGURATION - HARDCODED FOR PRODUCTION
**Date:** September 27, 2025
**Status:** COMPLETE - All credentials hardcoded, no timeouts

## Configuration Summary

All API keys and model IDs are **HARDCODED** directly in the code. No environment variables needed.

### Hardcoded Credentials

#### 1. HigherGov API
- **File:** `highergov_batch_fetcher.py`
- **API Key:** `2c38090f3cb0c56026e17fb3e464f22cf637e2ee`
- **Location:** Line 38
- **Status:** Hardcoded for client use

#### 2. Mistral API
- **File:** `RUN_ASSESSMENT.py`
- **API Key:** `2oAquITdDMiyyk0OfQuJSSqePn3SQbde`
- **Batch Model:** `ft:pixtral-12b-latest:d42144c7:20250912:f7d61150`
- **Agent ID:** `ag:d42144c7:20250911:untitled-agent:15489fc1`
- **Location:** Lines 30-33
- **Status:** All hardcoded for client use

#### 3. Mistral Connector
- **File:** `ULTIMATE_MISTRAL_CONNECTOR.py`
- **API Key:** `2oAquITdDMiyyk0OfQuJSSqePn3SQbde`
- **Agent ID:** `ag:d42144c7:20250911:untitled-agent:15489fc1`
- **Location:** Lines 15 and 39
- **Status:** Hardcoded for client use

### Timeout Configuration

All timeouts have been **REMOVED or EXTENDED** to handle long document fetching:

#### Document Fetching
- **Request Timeout:** `None` (no timeout)
- **Document Timeout:** `None` (no timeout)
- **Max Retries:** 10 attempts
- **Initial Delay:** 2.0 seconds
- **Retry Backoff:** 1.5x multiplier

#### Batch Processing
- **Max Polls:** 1000 (essentially no timeout)
- **Poll Interval:** 15 seconds
- **Total Wait Time:** Up to 4+ hours if needed

#### Agent Verification
- **Rate Limit:** 2 seconds between calls
- **No timeout on individual calls**

## Client Usage

### No Setup Required
The client can run immediately without any configuration:

```bash
# Just run - no API keys to set
python RUN_ASSESSMENT.py
```

### No Environment Variables
The application does **NOT** use or require:
- No `HIGHERGOV_API_KEY` environment variable
- No `MISTRAL_API_KEY` environment variable
- No `.env` files
- No config files

Everything is hardcoded for immediate client use.

### Document Processing

The system is configured to handle:
- Long document fetching times (no timeouts)
- Large batch processing jobs (hours if needed)
- Automatic retries with exponential backoff
- Graceful fallbacks on errors

### Security Note

This configuration is for **CLIENT-FACING APP ONLY**. The API keys are:
- Private to this application
- Not meant to be shared
- Specific to the SOS Assessment use case

## Testing

To verify the configuration:

1. Check HigherGov API:
```python
# Should fetch without timeout
python -c "from highergov_batch_fetcher import HigherGovBatchFetcher; f = HigherGovBatchFetcher(); print(f.api_key)"
# Output: 2c38090f3cb0c56026e17fb3e464f22cf637e2ee
```

2. Check Mistral API:
```python
# Should show hardcoded key
python -c "import RUN_ASSESSMENT; print(RUN_ASSESSMENT.MISTRAL_API_KEY)"
# Output: 2oAquITdDMiyyk0OfQuJSSqePn3SQbde
```

3. Run full pipeline:
```bash
python RUN_ASSESSMENT.py
# Should run without any API key prompts or timeout errors
```

## Summary

✅ All API keys hardcoded
✅ No environment variables needed
✅ No timeouts on document fetching
✅ Extended timeouts on batch processing
✅ Client-ready configuration
✅ No setup or configuration required