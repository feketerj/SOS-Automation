# Repository Cleanup Analysis - SOS Assessment Tool

## Current State: 53 Python files in root

## FILES TO DELETE (No current value, unlikely future use)

### Test Files That Already Passed (Can be archived or deleted)
1. **test_8130_capability.py** - Specific test for FAA 8130, already verified
2. **test_exact_schema.py** - Schema test, functionality now in unified_pipeline_output
3. **test_hardcoded_pipeline.py** - Old test for hardcoded config, superseded
4. **test_part_145_logic.py** - Specific FAA Part 145 test, already verified
5. **test_pattern_integration.py** - Pattern test, already verified
6. **test_pipeline_schema_integration.py** - Old schema test, superseded by unified
7. **test_unified_pipeline.py** - Duplicate of test_integrated_pipeline.py
8. **test_unified_output_debug.py** - Debug tests that all passed, no longer needed
9. **test_pipeline_with_docs.py** - Document test, functionality verified
10. **debug_pattern.py** - Pattern debugging, no longer needed
11. **DEBUG_PATTERNS.py** - Old pattern debug, superseded

### Duplicate/Superseded Output Managers
12. **pipeline_output_manager.py** - Superseded by enhanced_output_manager
13. **unified_output_formatter.py** - Superseded by unified_pipeline_output.py

### Old Emergency/Rollback Scripts (Not applicable to new pipeline)
14. **emergency_rollback.py** - For old pipeline emergencies
15. **rollback_safety_check.py** - For old pipeline rollback

### Deprecated Connectors/Handlers
16. **BATCH_API_HANDLER.py** - Functionality in FULL_BATCH_PROCESSOR
17. **mistral_api_connector.py** - Superseded by ULTIMATE_MISTRAL_CONNECTOR

### Old Utility Scripts
18. **create_icon.py** - Icon creation, one-time use
19. **SAVE_ERRORS.py** - Error saving utility, not used
20. **json_to_ui_formatter.py** - UI formatting, not currently used
21. **launch_dashboard.py** - Dashboard launcher, UI not implemented

### Single-Purpose Verification Scripts (Already verified)
22. **VERIFY_SET_ASIDE_LOGIC.py** - Set-aside verification, already done
23. **verify_batch_format.py** - Batch format verified

### Old Download Scripts (Functionality elsewhere)
24. **DOWNLOAD_RESULTS.py** - Old downloader
25. **PARSE_BATCH_RESULTS.py** - Parsing now integrated

### Unused Components
26. **quality_control_validator.py** - Not integrated, using qc_agents.py
27. **unified_prompt_injector.py** - Prompt injection handled in pipeline
28. **pipeline_title_generator.py** - Title generation integrated elsewhere
29. **parts_condition_checker.py** - Specific checker, not currently used

## FILES TO KEEP (Currently used or likely future use)

### PRODUCTION CRITICAL (DO NOT DELETE)
- **LOCKED_PRODUCTION_RUNNER.py** - Main production runner
- **ULTIMATE_MISTRAL_CONNECTOR.py** - Main API connector
- **sos_ingestion_gate_v419.py** - Regex engine (497 patterns)
- **enhanced_output_manager.py** - Primary output manager
- **highergov_batch_fetcher.py** - HigherGov API integration
- **decision_sanitizer.py** - Decision normalization
- **API_KEYS.py** - API credentials
- **model_config.py** - Model configuration

### NEW PIPELINE (Keep for future)
- **multi_stage_pipeline.py** - 20-stage pipeline
- **context_accumulator.py** - Context management
- **document_fetcher.py** - Document fetching
- **qc_agents.py** - QC verification
- **pipeline_config.py** - Pipeline configuration
- **unified_pipeline_output.py** - Unified output system

### BATCH PROCESSING (Still needed)
- **DOWNLOAD_BATCH_RESULTS.py** - Batch result downloader
- **MONITOR_PROGRESS.py** - Progress monitoring

### ACTIVE TEST FILES (Keep for now)
- **test_multi_stage_pipeline.py** - Main pipeline test
- **test_pipeline_mock.py** - Mock mode testing
- **test_integrated_pipeline.py** - Integration testing
- **test_production_limits.py** - Production config verification
- **debug_pipeline.py** - Debug utilities

### SIMPLE RUNNERS (User-friendly)
- **RUN_ASSESSMENT.py** - Simple assessment runner
- **run_batch_single.py** - Single batch runner
- **run_simple_assessment.py** - Simple runner

### PLATFORM SPECIFIC
- **platform_mapper_v419.py** - Platform mapping logic

## Summary

### To Delete: 29 files
- Removes ~55% of Python files in root
- Eliminates duplicates and test files
- Removes superseded components

### To Keep: 24 files
- All production-critical files preserved
- New pipeline components retained
- Active development files kept

### Space Savings
- Estimated 200-300 KB removed
- Significant token reduction for agents
- Cleaner repository structure

## Safe Deletion Commands

```bash
# Create backup first
mkdir _BACKUP_BEFORE_CLEANUP_2025_09_28
cp *.py _BACKUP_BEFORE_CLEANUP_2025_09_28/

# Then delete identified files
del test_8130_capability.py
del test_exact_schema.py
del test_hardcoded_pipeline.py
del test_part_145_logic.py
del test_pattern_integration.py
del test_pipeline_schema_integration.py
del test_unified_pipeline.py
del test_unified_output_debug.py
del test_pipeline_with_docs.py
del debug_pattern.py
del DEBUG_PATTERNS.py
del pipeline_output_manager.py
del unified_output_formatter.py
del emergency_rollback.py
del rollback_safety_check.py
del BATCH_API_HANDLER.py
del mistral_api_connector.py
del create_icon.py
del SAVE_ERRORS.py
del json_to_ui_formatter.py
del launch_dashboard.py
del VERIFY_SET_ASIDE_LOGIC.py
del verify_batch_format.py
del DOWNLOAD_RESULTS.py
del PARSE_BATCH_RESULTS.py
del quality_control_validator.py
del unified_prompt_injector.py
del pipeline_title_generator.py
del parts_condition_checker.py
```