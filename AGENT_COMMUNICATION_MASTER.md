# AGENT COMMUNICATION MASTER
**Last Updated:** $(Get-Date -Format "yyyy-MM-dd HH:mm" )

## Mission
You are the coding agent responsible for maintaining the SOS Assessment Automation Tool. Accuracy beats speed. Follow the checklist below before executing any changes.

## Immediate Priorities
1. Treat `HANDOFF_CONTINUITY_MASTER.md` as the single source of truth for project status.
2. Never modify `packs/regex_pack_v419_complete.yaml` unless "PIED PIPER" authorization is logged.
3. When updating prompts, edit `prompt_templates.py` first, then regenerate the Markdown prompt packs in `user_added_context/`.
4. Preserve evidence fidelity: every knockout must carry the government quote + citation.

## Workflow Checklist
- **Environment**: Python 3.12, `pipeline_config.py` contains hardcoded API keys (Mistral + HigherGov). Activate `.venv` if available.
- **Regression Tests**: run `python test_enhanced_pipeline.py` and `python test_regex_fix.py` after structural changes.
- **Manual Spot Checks**: execute `python RUN_ASSESSMENT.py --search-id <ID>` on a known opportunity to verify end-to-end behavior.
- **Outputs**: confirm JSON/CSV/Markdown in `SOS_Output/` align with the canonical schema (knockout_phase/share-friendly stage labels, etc.).

## Communication Guidelines
- Log significant changes or discoveries inside `HANDOFF_CONTINUITY_MASTER.md` under a dated sub-heading.
- For experimental work, create a short note in `handoff_archive/experiments_<date>.md` so the main doc stays clean.
- Use clear commit messages referencing the area touched (e.g., `prompts: tighten agent 6 platform guidance`).

## Reference Materials
- Prompt research: `user_added_context/optimal_mistral_agent_sys_prompt_config.md`
- SOS doctrine & knockout primer: `user_added_context/sos_agent_sys_prompt_logic_3.md`
- Prompt packs for agent provisioning: `user_added_context/batch_stage_prompts.md`, `agent_stage_prompts.md`, `report_stage_prompts.md`
- Pipeline prompts: `prompt_templates.py`

## When in Doubt
- Default to accuracy; stop and document open questions in the master handoff.
- Do not delete files without explicit instruction; archive instead.
- If regex edits are required, gather diffs first, then request / log "PIED PIPER" authorization.
