Centralized configuration

This directory centralizes configuration for the SOS Assessment Automation Tool per TODO_CODEX Module 1.2. Goals:

- Use environment variables for secrets (API keys, tokens).
- Keep environment-specific overrides under `config/environments/<env>/`.
- Avoid hardcoded values in code; load via a small config layer.

Configuration precedence (read-only loader):

- Environment variables (highest)
- `config/settings.json` (optional; not committed)
- `config/settings.example.json` (template)
- Internal defaults (lowest)

Keys (current consumers respect these if present):

- HigherGov
  - `highergov.api_key` (or env `HIGHERGOV_API_KEY`)
  - `highergov.base_url` (or env `HG_API_BASE_URL`)
- Mistral / Model
  - `mistral.api_key` (or env `MISTRAL_API_KEY`)
  - `mistral.model_id` (agent/model id)
  - `mistral.base_url` (or env `MISTRAL_API_BASE_URL`, optional)
- Pipeline
  - `pipeline.max_documents`
  - `pipeline.text_extraction_char_limit`
  - `pipeline.batch_size_limit` (optional cap; respected by batch collector/processor)
  - `pipeline.document_cache.enabled` (bool; default false)
  - `pipeline.document_cache.ttl_days` (int; default 7)
  - `pipeline.document_cache.dir` (string; default `cache/hg_docs`)
- Network (optional)
  - `HTTP_PROXY`, `HTTPS_PROXY` (env only)

Example `config/settings.json`:

```
{
  "highergov": {
    "api_key": "${HIGHERGOV_API_KEY}",
    "base_url": "https://www.highergov.com/api-external/opportunity/"
  },
  "mistral": {
    "api_key": "${MISTRAL_API_KEY}",
    "model_id": "ag:...:sos-triage-agent:..."
  },
  "pipeline": {
    "text_extraction_char_limit": 400000,
    "batch_size_limit": 100,
    "document_cache": {
      "enabled": true,
      "ttl_days": 7,
      "dir": "cache/hg_docs"
    }
  }
}
```

Notes:

- Secrets should be set via environment or a local `.env` (see `.env.example`).
- Runners and connectors respect these values if present; otherwise fall back to existing env/defaults.
