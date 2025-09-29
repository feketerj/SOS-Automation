# Repository Cleanup Plan

## Status
- ✅ New 20-stage pipeline: WORKING (mock mode tested)
- ✅ Unified output: INTEGRATED and tested
- ⚠️ Real API testing: NOT YET DONE (needs real agents created)

## SAFE TO CLEAN (Low Risk)

### 1. Test Files - Move to tests/ folder
```bash
# Create tests folder if not exists
mkdir tests

# Move test files (keeping backups)
move test_*.py tests/
move debug_*.py tests/
```

### 2. Temporary Test Outputs
```bash
# Remove test output directories
rmdir /s test_output
rmdir /s test_special_output
rmdir /s test_go_output
rmdir /s integrated_test_output
```

### 3. Old Debug Reports
- `DEBUG_REPORT_*.md` - Can archive after review
- `DEBUG_PLAN_*.md` - Can archive

## NEEDS REVIEW BEFORE CLEANUP (Medium Risk)

### 1. Output Managers (Have 6, need 2)
**KEEP:**
- `enhanced_output_manager.py` - Current production
- `unified_pipeline_output.py` - New unified system

**CONSIDER REMOVING:**
- `pipeline_output_manager.py` - Check if used
- `unified_output_formatter.py` - Check dependencies

### 2. API Connectors (Multiple versions)
**KEEP:**
- `ULTIMATE_MISTRAL_CONNECTOR.py` - Main production
- `mistral_api_connector.py` - Check if needed

**REVIEW:**
- `BATCH_API_HANDLER.py` - May be duplicate

## DO NOT REMOVE (Critical)

### Production Files
- `LOCKED_PRODUCTION_RUNNER.py` - Main runner
- `sos_ingestion_gate_v419.py` - Regex engine
- `API_KEYS.py` - Credentials
- `endpoints.txt` - Input file
- `model_config.py` - Model configuration

### New Pipeline Files (Keep for future)
- `multi_stage_pipeline.py` - 20-stage pipeline
- `context_accumulator.py` - Context management
- `document_fetcher.py` - Document fetching
- `qc_agents.py` - QC verification
- `pipeline_config.py` - Pipeline configuration
- `stage_processors/` folder - Individual stages

### Batch Processing (Still needed)
- `Mistral_Batch_Processor/` folder - All batch processing
- `FULL_BATCH_PROCESSOR.py` - Main batch processor

## Recommended Cleanup Sequence

### Phase 1: Organize Tests (SAFE)
1. Create `tests/` folder
2. Move all `test_*.py` files
3. Move all `debug_*.py` files
4. Update any import paths if needed

### Phase 2: Clean Temp Files (SAFE)
1. Remove test output directories
2. Archive old debug reports
3. Clean up `__pycache__` directories

### Phase 3: Consolidate (NEEDS TESTING)
1. Test which output managers are actually used
2. Identify duplicate API connectors
3. Create deprecation notices before removing

## Commands for Safe Cleanup

```bash
# Create archive folder
mkdir _ARCHIVE_2025_09_28

# Move test files
mkdir tests
move test_*.py tests/
move debug_*.py tests/

# Archive old reports
move DEBUG_*.md _ARCHIVE_2025_09_28/
move *_PLAN_*.md _ARCHIVE_2025_09_28/

# Clean temp directories
rmdir /s /q test_output
rmdir /s /q test_*_output
rmdir /s /q __pycache__

# Count what's left
dir *.py | find /c ".py"
```

## Statistics Before Cleanup
- Python files in root: ~50+
- Test files: ~15
- Output managers: 6
- Total repository size: [Check with: dir /s]

## Expected After Cleanup
- Python files in root: ~25-30 (essential only)
- Test files: 0 (all in tests/)
- Output managers: 2 (production + unified)
- Cleaner structure, easier navigation

## Risk Assessment
- **Phase 1 (Tests)**: ✅ LOW RISK - Just organizing
- **Phase 2 (Temp)**: ✅ LOW RISK - Removing generated files
- **Phase 3 (Consolidate)**: ⚠️ MEDIUM RISK - Need to verify dependencies

## DO NOT CLEAN YET
- Stage processor implementations (not created yet)
- Agent creation scripts (future work)
- Training data folders (needed for new agents)
- Production logs (if any exist)