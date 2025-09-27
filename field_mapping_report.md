# Field Mapping Audit

Root: C:\Users\feket\OneDrive\Desktop\excelsior\r_staff\r_3\Deployed_Code_Op_Locations\SOS-Assessment-Automation-Tool

## Counts by Field
- result: 59960
- decision: 13051
- final_decision: 206
- classification: 1850
- processing_method: 553
- pipeline_stage: 84
- assessment_type: 175
- rationale: 7790
- reasoning: 2746
- sos_pipeline_title: 2272
- sam_url: 138
- hg_url: 76
- highergov_url: 71

## Examples

### result
- AGENT_COMMUNICATION.md:23 :: put broken  ### Pipeline Test Results: - 45 opportunities tested -
- AGENT_COMMUNICATION.md:90 ::  only mode]")        verified_results = batch_results  # Use batch
- AGENT_COMMUNICATION.md:90 ::      verified_results = batch_results  # Use batch results as-is  
- AGENT_COMMUNICATION.md:90 ::  = batch_results  # Use batch results as-is    ```  2. **Cost Anal
- AGENT_COMMUNICATION.md:140 :: g, doc_length, etc.  ### Test Results Successfully tested with tes

### decision
- AGENT_COMMUNICATION.md:6 :: ut_manager.py not recognizing decisions - everything shows INDETERMI
- AGENT_COMMUNICATION.md:10 :: ified output is broken: - All decisions show as INDETERMINATE (shoul
- AGENT_COMMUNICATION.md:11 :: t_manager.py not recognizing 'decision' field - RUN_FULL_PIPELINE.py
- AGENT_COMMUNICATION.md:31 :: _manager.py - not recognizing decision fields 2. RUN_FULL_PIPELINE.p
- AGENT_COMMUNICATION.md:38 :: at Required: ```python {     'decision': 'GO|NO-GO|INDETERMINATE',  

### final_decision
- AGENT_COMMUNICATION.md:135 :: ch_id, opportunity_id, title, final_decision - **Processing Fields:** proc
- AGENT_COMMUNICATION.md:185 :: ch_id, opportunity_id, title, final_decision - **Processing:** processing_
- AGENT_COMMUNICATION.md:1117 :: h_results:         if result['final_decision'] in ['GO', 'INDETERMINATE']:
- AGENT_COMMUNICATION.md:1136 :: ision': item['batch_result']['final_decision'],             'agent_decisio
- AGENT_COMMUNICATION.md:1138 :: ement': item['batch_result']['final_decision'] != agent_result['decision']

### classification
- AGENT_COMMUNICATION.md:227 :: e batch API returns identical classifications  #### Phase 2: Shadow Collec
- CLAUDE.md:95 :: TE_MISTRAL_CONNECTOR returns `classification` not `decision`  **Option 1: 
- CLAUDE.md:100 :: KNOWN')` → `agent_result.get('classification', 'UNKNOWN')` - Risk: ZERO - 
- CLAUDE.md:106 :: Return `decision` instead of `classification` - Risk: MEDIUM - Could break
- CLAUDE.md:112 :: ent verification phase - Map `classification` → `decision` before processi

### processing_method
- AGENT_COMMUNICATION.md:136 :: sion - **Processing Fields:** processing_method, knock_pattern, knockout_cate
- AGENT_COMMUNICATION.md:186 :: al_decision - **Processing:** processing_method, knock_pattern, knockout_cate
- AGENT_COMMUNICATION.md:1147 :: reasoning', ''),             'processing_method': 'AGENT_VERIFIED'         })
- AGENT_COMMUNICATION.md:1416 :: inal_decision - ✅ Processing: processing_method, knock_pattern, knockout_cate
- AGENT_COMMUNICATION.md:1792 :: entical output structure    - Processing_method field correctly identifies mo

### pipeline_stage
- AGENT_COMMUNICATION.md:39 :: HIS FIELD NOT RECOGNIZED     'pipeline_stage': 'REGEX|BATCH|AGENT',     'a
- BUG_3_DOUBLE_SANITIZATION_FIX.md:28 :: ied_markers = ['_sanitized', 'pipeline_stage', 'assessment_type']     has_
- CLAUDE.md:141 :: ng",   "hg_url": "string",   "pipeline_stage": "APP|BATCH|AGENT",   "asses
- CLAUDE.md:242 ::  GO/NO-GO/INDETERMINATE    - `pipeline_stage`: REGEX/BATCH/AGENT    - `ass
- decision_sanitizer.py:82 ::  'INDETERMINATE']         has_pipeline_stage = 'pipeline_stage' in data an

### assessment_type
- AGENT_COMMUNICATION.md:40 :: e': 'REGEX|BATCH|AGENT',     'assessment_type': 'REGEX_KNOCKOUT|MISTRAL_BAT
- BUG_3_DOUBLE_SANITIZATION_FIX.md:28 :: anitized', 'pipeline_stage', 'assessment_type']     has_markers = all(key i
- BUG_FIXES_SUMMARY_SESSION_27.md:21 ::  decision_sanitizer.py (added ASSESSMENT_TYPE_MAP) - Added _normalize_asses
- BUG_FIXES_SUMMARY_SESSION_27.md:22 :: _TYPE_MAP) - Added _normalize_assessment_type() method **Test:** test_asses
- BUG_FIXES_SUMMARY_SESSION_27.md:23 :: _type() method **Test:** test_assessment_type_fix.py (16 test cases pass)  

### rationale
- batch_format_verification.json:11 :: "result",     "summary",     "rationale",     "recommendation",     "
- batch_format_verification.json:35 :: (military transport)",       "rationale": "Regex knockout: Category 8
- batch_format_verification.json:60 :: with no restrictions",       "rationale": "Commercial aircraft parts 
- batch_format_verification.json:85 :: clear specifications",       "rationale": "Requires further analysis 
- CLAUDE.md:87 :: nified schema fields (result, rationale) - **FULL_BATCH_PROCESSOR.py*

### reasoning
- AGENT_COMMUNICATION.md:138 :: d - **Metadata:** timestamps, reasoning, doc_length, etc.  ### Test R
- AGENT_COMMUNICATION.md:188 :: d - **Metadata:** timestamps, reasoning, doc_length, agency, naics, p
- AGENT_COMMUNICATION.md:1146 :: omparison,             'agent_reasoning': agent_result.get('reasoning
- AGENT_COMMUNICATION.md:1146 :: reasoning': agent_result.get('reasoning', ''),             'processin
- BATCH_PROCESSOR_STATUS.md:44 :: INDETERMINATEs     - Detailed reasoning and analysis     - Maybe 10-2

### sos_pipeline_title
- batch_format_verification.json:16 :: ",     "special_action",     "sos_pipeline_title",     "highergov_link",     "
- batch_format_verification.json:42 :: special_action": null,       "sos_pipeline_title": "PN: NA | Qty: NA | Conditi
- batch_format_verification.json:67 :: special_action": null,       "sos_pipeline_title": "PN: NA | Qty: NA | Conditi
- batch_format_verification.json:92 :: special_action": null,       "sos_pipeline_title": "PN: NA | Qty: NA | Conditi
- CLAUDE.md:138 :: recommendation": "string",   "sos_pipeline_title": "string",   "sam_url": "str

### sam_url
- BUG_3_DOUBLE_SANITIZATION_FIX.md:61 :: ng fallback: `source_path` → `sam_url` - Added missing fallback: `p
- BUG_FIXES_SUMMARY_SESSION_27.md:10 ::  Very Low **Solution:** Added sam_url and hg_url field preservation
- CLAUDE.md:77 ::  10. **URL Fields Working** - sam_url and hg_url properly preserved
- CLAUDE.md:139 :: pipeline_title": "string",   "sam_url": "string",   "hg_url": "stri
- CLAUDE.md:193 :: g URL Fields** - Fixed: Added sam_url and hg_url preservation throu

### hg_url
- BUG_3_DOUBLE_SANITIZATION_FIX.md:62 :: d missing fallback: `path` → `hg_url` - Preserves direct fields wh
- BUG_FIXES_SUMMARY_SESSION_27.md:10 :: Solution:** Added sam_url and hg_url field preservation **Files Mo
- CLAUDE.md:77 :: ields Working** - sam_url and hg_url properly preserved 11. **Agen
- CLAUDE.md:140 :: g",   "sam_url": "string",   "hg_url": "string",   "pipeline_stage
- CLAUDE.md:193 :: ** - Fixed: Added sam_url and hg_url preservation throughout pipel

### highergov_url
- CLAUDE.md:474 :: ne URL present: `sam_url` or `highergov_url` - Basic type sanity for key 
- decision_sanitizer.py:223 ::  data.get('hg_url', data.get('highergov_url', data.get('path', data.get('
- decision_sanitizer.py:243 ::         'knockout_category', 'highergov_url', 'assessment_timestamp']:   
- enhanced_output_manager.py:233 :: t('sam_url', ''))             highergov_url = (                 assessmen
- enhanced_output_manager.py:235 ::            or assessment.get('highergov_url')                 or assessme
