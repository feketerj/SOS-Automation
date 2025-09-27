# Codex UI To-Do (Tonight) — Safe, Modular, Do-No-Harm

**✅ UI FIXED (Sept 27): Streamlit UI now fully operational. Replaced subprocess with direct Python imports. See CRITICAL_FIXES_LOG.md for details.**

This plan is designed to be incremental, reversible, and non‑disruptive. No pipeline logic changes. Favor read‑only tooling and non‑network unit tests. Defaults remain unchanged for any optional features.

## 1) Testing (Priority 3)
- ✅ COMPLETED: Added test_decision_sanitizer_edge_cases.py (6 tests)
- ✅ COMPLETED: Added test_output_manager_edge_cases.py (6 tests)
- ✅ COMPLETED: Created test_pipeline_runner.py (validation suite)
- ✅ COMPLETED: Created test_failure_scenarios.py (failure injection)
- REMAINING: Move more non‑network tests into `tests/` (10 files max)
- REMAINING: Verify Master_Database daily/all‑time updates with temp base path

## 2) Validation/Audits (Priority 2)
- ✅ COMPLETED: Extended verify_integrity.py with diff output
- ✅ COMPLETED: Created schema_diff.py for comparing data.json files
- ✅ COMPLETED: Generated field_mapping_report.md via audit_field_mappings.py

## 3) Decision Logic Insights (Priority 2.3)
- ✅ COMPLETED: Generated decision_audit_summary.csv for latest run
- ✅ COMPLETED: Created decision audit markdown report with hotspots

## 4) Performance (Priority 4, opt‑in; defaults OFF)
- Leave `pipeline.parallel_fetch` and `pipeline.document_cache` disabled by default.
- Add a tiny dry‑run capacity print in collector (counts, capped by `batch_size_limit` if set). No functional change.
- Provide an example `config/settings.json` snippet in docs for enabling parallel fetch with small `max_workers` (2).

## 5) Docs & Operator Ergonomics (Priority 1)
- Update `CLAUDE.md` “Environment Setup” with a short “Config Quickstart” (keys to override, safe defaults).
- Add a one‑page “Operator Runbook” snippet: preflight (health/endpoints), run, postflight (checklist), with commands.

## Guardrails
- Do NOT modify pipeline logic (Regex → Batch → Agent) or change defaults.
- Keep changes additive and opt‑in; prefer read‑only tools and unit tests.
- Batch changes in small PR‑sized commits; verify `pytest -q tests` locally.

## Quick Commands
- Local tests: `RUN_TESTS_LOCAL.bat` or `pytest -q tests/`
- Post‑run checklist: `RUN_POSTRUN_CHECK.bat`
- Decision audit CSV: `python tools/decision_audit.py SOS_Output/YYYY-MM/Run_*/ --csv decision_audit_summary.csv`
- Integrity check: `python tools/verify_integrity.py --meta Mistral_Batch_Processor/batch_metadata_*.json --run SOS_Output/YYYY-MM/Run_*/`
- Regex audit: `python tools/regex_pattern_audit.py packs/regex_pack_v419_complete.yaml`

