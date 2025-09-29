# HANDOFF & CONTINUITY MASTER
**Last Updated:** $(Get-Date -Format "yyyy-MM-dd HH:mm" )

## 1. Snapshot
- **Project:** SOS Assessment Automation Tool (regex-first, 20-stage pipeline)
- **Environment:** Local CLI, Python 3.12, hardcoded API keys (Mistral + HigherGov)
- **Status:** Regex pack locked; prompt refactor complete; pipeline wired with long-form prompts + QC overrides.

## 2. Current State Highlights
- `packs/regex_pack_v419_complete.yaml` restored to authorized baseline; further edits require "PIED PIPER" compliance (see `HANDOFF_RULES.md`).
- Prompt architecture centralized in `prompt_templates.py`; generated Markdown copies live in `user_added_context/` for agent provisioning.
- Pipeline stages (`enhanced_pipeline.py`):
  - Regex gate ? 10 batch processors (parallel) ? 10 triage agents (sequential) ? QC checks on each high-confidence NO-GO ? two report writers.
  - Prompts reference shared doctrine, SOS capabilities, and injection defenses pulled from `user_added_context` research docs.
- Knockout reporting returns obfuscated stage buckets (`pattern`, `batch`, `agent`, `qc`) while keeping full government evidence + rationale.

## 3. Key Assets
| Purpose | Path |
| --- | --- |
| Prompt builders | `prompt_templates.py` |
| Batch prompt handbook | `user_added_context/batch_stage_prompts.md` |
| Agent prompt handbook | `user_added_context/agent_stage_prompts.md` |
| Report prompt handbook | `user_added_context/report_stage_prompts.md` |
| Latest rules/continuity archive | `handoff_archive/` |
| Regex schema reference | `schemas/regex_assessment.schema.json` |
| Prompt research | `user_added_context/optimal_mistral_agent_sys_prompt_config.md`, `user_added_context/sos_agent_sys_prompt_logic_3.md` |

## 4. Operational Runbook
1. (Optional) create `.venv` and install requirements in root
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate
   pip install -r requirements.txt
   ```
2. Execute a single opportunity run:
   ```powershell
   python RUN_ASSESSMENT.py --search-id <HigherGov ID>
   ```
3. Batch validation / tests (new prompt stack):
   ```powershell
   python test_enhanced_pipeline.py
   python test_regex_fix.py
   ```
4. Review results under `SOS_Output/` (CSV + JSON + Markdown). Knockout summaries include `knockout_phase` + `knockout_reason` plus verbatim quotes.

## 5. Outstanding Items
- **Token measurements:** confirm final prompts stay within 5k–7k tokens once populated with real metadata and opportunities.
- **Adversarial testing:** stress the new injection defenses with hostile solicitations.
- **Output alignment:** final report should map to the canonical schema described in `regex_assessment.schema.json` (stage label obfuscation already in place).
- **UI sync:** if dashboard consumes earlier filenames, point it to the new master docs and obfuscated stage labels.

## 6. Compliance / Security
- All regex modifications require "PIED PIPER" authorization trail.
- API keys are hardcoded in `pipeline_config.py`; treat repo as sensitive.
- QC agent enforces =95% confidence before overriding a NO-GO.
- Audit trail: every stage stores confidence, rationale, evidence, and QC results in memory (expand to disk logging if needed).

## 7. Contact / Next Steps
- For further development, start with this master file then consult `handoff_archive/` for historical lessons learned.
- Keep `prompt_templates.py` and the Markdown prompt packs synchronized whenever prompts evolve.
- Update this master document at the end of each working session.
