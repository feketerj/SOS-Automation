# SOS UI Service

This package exposes a lightweight FastAPI server that wraps the existing pipeline scripts.

## Quick start

1. Install dependencies (once):
   ```bash
   python -m pip install -r ui_service/requirements.txt
   ```
2. Build static assets (optional – already run once):
   ```bash
   python SOS_UI_Dashboard/build_static.py
   ```
3. Launch the dashboard:
   ```bash
   python -m ui_service
   ```
   or double-click `START_DASHBOARD.bat`.
4. Open <http://127.0.0.1:8090/dashboard/> (the batch file opens this automatically).

## Key endpoints
- `POST /api/runs` – write `endpoints.txt` and spawn `RUN_FULL_PIPELINE.py`.
- `GET /api/runs/{run_id}/logs` – live log stream.
- `GET /api/runs/{run_id}/summary` – metadata, counts, assessments, artifact links.
- Static artifacts are served from `/artifacts/...` (read-only view of `SOS_Output/`).

## Notes
- The service prevents concurrent runs to avoid clobbering `endpoints.txt`.
- All API keys remain in the existing places (`API_KEYS.py` or env vars).
- Logs and endpoint snapshots are stored under `ui_service/runs/<run_id>/` for audit.
