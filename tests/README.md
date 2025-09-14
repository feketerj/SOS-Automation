Tests overview

This project contains a mix of pure unit tests and utility/debug scripts that were used during development.

Guidance:
- Prefer running targeted tests in `tests/` (import-stable via `conftest.py`).
- Some legacy test scripts outside `tests/` may require network access or API keys; avoid running them by default.
- To run with pytest: `pytest -q tests/`

Notes:
- Set `PYTHONPATH` to the repo root if running tests directly via `python`.
- Environment variables may be required for a subset of tests: `HIGHERGOV_API_KEY`, `MISTRAL_API_KEY`.

