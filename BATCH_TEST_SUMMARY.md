# BATCH PROCESSOR TEST RESULTS
**Test Date:** September 11, 2025
**Batch Job ID:** 7fae976f-0361-4e60-982e-f1799dfb0ef6

## Test Configuration
- **Endpoints Tested:** 2 search IDs
- **Total Opportunities:** 87
- **Regex Knockouts:** 15 (17%)
- **Sent to Batch AI:** 72 (83%)

## Processing Results

### Stage 1: Regex Filtering (FREE)
- Filtered out 15 opportunities as NO-GO
- Categories knocked out:
  - Set-asides (service-disabled veteran-owned)
  - Set-asides (HUBZone small business)
  - Set-asides (8(a) minority-owned)

### Stage 2: Batch AI Processing (50% off)
- **Model:** ft:mistral-medium-latest:d42144c7:20250902:908db254
- **Total Processed:** 72 opportunities
- **Results:**
  - GOs: 29 (40%)
  - NO-GOs: 42 (58%)
  - UNKNOWN: 1 (1%)

### Overall Statistics
- **Total NO-GOs:** 57 (15 regex + 42 AI) = 66%
- **Total GOs:** 29 = 33%
- **Unknown:** 1 = 1%

## Cost Analysis
- **Regex Filtering:** FREE (saved 17% of AI costs)
- **Batch Processing:** 50% discount on 72 assessments
- **Effective Savings:** ~58% compared to real-time agent processing

## Key Findings
1. **System Works:** Three-stage pipeline successfully processes opportunities
2. **JSON Parsing Fixed:** Model returns proper JSON format with recommendations
3. **High NO-GO Rate:** 66% filtered out (good for focusing on viable opportunities)
4. **Cost Effective:** Regex + Batch combination saves >50% on processing costs

## Sample Decisions
- **GO Example:** "BOLT, MACHINE" - Standard commercial hardware with no restrictions
- **NO-GO Examples:** 
  - Set-aside restrictions
  - Military platform limitations
  - OEM requirements

## Next Steps
1. Run full 17-endpoint test from endpoints.txt
2. Compare batch results with agent verification
3. Fine-tune model if needed to reduce UNKNOWN responses