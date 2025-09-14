# Project Progress Snapshot

Last update: Now

## Where Things Stand

- Pipeline: Regex → Batch → Agent flow is stable; no logic changes introduced.
- Config: Central loader in place (`config/loader.py`); runners/connectors optionally read env > `config/settings.json` > example > defaults.
- Validation & Audits:
  - Output, batch input/results, metadata validators
  - Schema validation (JSON Schema) with `--summary` mode
  - Decision audit (markdown + optional CSV) with hotspot summaries
  - Integrity checker between batch metadata and saved runs
  - CSV validator for assessment.csv
  - Post-run checklist orchestrates the above
- Performance (opt-in):
  - `pipeline.batch_size_limit` guard (collector + full processor)
  - HigherGov document cache with TTL; cache maintenance tool
  - Parallel document fetch (collector) with `max_workers` (default off)
- Regex pack: audit tool compiles patterns, reports counts and errors
- Tests: Curated `tests/` with non-network unit tests around normalization, output manager, CSVs, and master DB files

## Next Steps (Safe & Incremental)

1. Continue test consolidation and add 4–6 small unit tests (no network)
2. Extend integrity tooling to write a small diff when drift is detected (read-only)
3. Consider adding a schema “diff summary” across runs (read-only)
4. (Optional) Add a config-gated `max_pages` for smoke/collector to bound demo/test fetches
5. Keep documentation and examples in sync as features remain opt-in by default

## Orientation for the Next Agent

- Do No Harm: Keep pipeline logic unchanged; favor read-only tools and unit tests.
- Config changes must remain opt-in; defaults should match current behavior.
- Use the post-run checklist and decision audit to understand outputs before proposing code changes.

