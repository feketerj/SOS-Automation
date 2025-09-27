# Codex UI To-Do (Tonight) — Safe, Modular, Do-No-Harm

**⚠️ CRITICAL ISSUE: Streamlit UI is broken and does not run the pipeline. See UI_BROKEN_HANDOFF.md for details. UI displays placeholder data regardless of input. Command line pipeline works perfectly. Consider fixing UI subprocess execution as highest priority.**

This plan is designed to be incremental, reversible, and non‑disruptive. No pipeline logic changes. Favor read‑only tooling and non‑network unit tests. Defaults remain unchanged for any optional features.

## 1) Testing (Priority 3)
- Move next small batch of non‑network tests into `tests/` (10 files max). Verify imports via `tests/conftest.py`.
- Add 4–6 focused unit tests (no network, no I/O outside temp dirs):
  - DecisionSanitizer edge cases (nested legacy, None/empty variants)
  - EnhancedOutputManager: URL synthesis, title/ID fallbacks, CSV resilience
  - Verify Master_Database daily/all‑time updates with temp base path
- Do NOT run or modify network‑dependent scripts; keep them outside `tests/`.

## 2) Validation/Audits (Priority 2)
- Extend `tools/verify_integrity.py` to write a small diff file (read‑only) when drift is detected (IDs/Titles/URLs).
- Add a read‑only “schema diff summary” mode to compare two data.json files and list first invalid fields (do not gate runs).
- Produce a markdown “Field Mapping Report” via `tools/audit_field_mappings.py --markdown`; no code changes.

## 3) Decision Logic Insights (Priority 2.3)
- Use `tools/decision_audit.py` with `--csv` to export disagreement hotspots; generate one short CSV for latest run.
- Summarize hotspots (category/agency) in a markdown note; do not change logic.

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

