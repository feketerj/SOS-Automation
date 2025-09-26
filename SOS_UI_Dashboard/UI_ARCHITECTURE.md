# SOS UI Service & Dashboard Blueprint

## Goals
- Preserve existing pipeline scripts as the single execution path.
- Allow operators to paste HigherGov search IDs, run the end-to-end pipeline, and stay within the UI the entire time.
- Surface live run status plus rich results (GO/NO-GO reasons, model narratives) without digging into JSON.
- Provide one-click access to generated files (CSV, Markdown, full-model report).
- Launch everything through a single shortcut/batch so VS Code is unnecessary.

## High-Level Architecture
`
+-------------+       HTTP API        +-------------------------------+
|  Web UI     | <--------------------> |  ui_service (FastAPI wrapper) |
| (dashboard) |   /runs, /logs, etc.   |  - writes endpoints.txt       |
+-------------+                        |  - spawns RUN_FULL_PIPELINE   |
        ^                               |  - tails logs & summarizes   |
        |                               +-------------------------------+
        |                                               |
        |                                               v
        |                                 +-----------------------------+
        |                                 | Existing pipeline runners   |
        |                                 | (RUN_FULL_PIPELINE.py, etc) |
        |                                 +-----------------------------+
        |                                               |
        |                                               v
        |                                 +-----------------------------+
        |                                 | SOS_Output/Run_*/ artifacts |
        |                                 +-----------------------------+
`

## Backend Wrapper (ui_service)
- Location: ui_service/
- Stack: FastAPI + Uvicorn
- Key endpoints:
  1. POST /runs
     - Body: { "endpoints": "<multi-line search IDs>", "mode": "batch-agent" }
     - Writes the body into endpoints.txt (overwriting previous entries).
     - Generates un_id (YYYYmmdd_HHMMSS_<slug>), creates ui_service/runs/<run_id>/.
     - Launches RUN_FULL_PIPELINE.py --mode <mode> with subprocess.Popen, redirecting stdout/stderr to <run_id>.log.
     - Responds immediately: { "run_id": "...", "status": "started" }.
  2. GET /runs/{run_id}/status
     - Returns current process state: unning/completed/failed, elapsed time, list of generated output folders (if detected).
  3. GET /runs/{run_id}/logs
     - Streams/tails log file (supports ?offset= for incremental polling).
  4. GET /runs/{run_id}/summary
     - Finds the most recent run folder under SOS_Output for this execution (look for the newest directory created after the process started).
     - Reads data.json, returns headline metrics plus sliced ssessments (with pagination or category filter support to keep payload manageable).
     - Includes a iles array exposing relative paths to ssessment.csv, eport.md, mistral_full_reports.md, etc.

- Process supervision:
  - Keep a run registry in ui_service/state.py mapping un_id to Popen handle, log path, start time, detected output dir.
  - On process exit, capture return code and store final status.

- Security: local-only (no auth) since tool runs on operator machine. All sensitive keys remain in API_KEYS.py or env.

## Frontend Dashboard (SOS_UI_Dashboard)
- Location: SOS_UI_Dashboard/web/
- Stack: Plain HTML + modern JS (no heavy framework to stay portable).
- Main sections:
  1. **Endpoint Input Panel**
     - Textarea (auto-trims blank lines, removes duplicates).
     - Dropdown for pipeline mode (default atch-agent).
     - Run button that POSTs to /runs and switches the view into run-monitor mode.
  2. **Run Monitor**
     - Live status chips (regex, batch, agent) inferred from log keywords.
     - Streaming log window (poll /logs every 2s with offset to append lines).
     - Elapsed time counter.
  3. **Results Explorer**
     - Once /summary reports completed, render metrics (GO/NO-GO counts, doc coverage).
     - Table of assessments with filters:
       - Decision filter (GO / NO-GO / INDETERMINATE).
       - Search box for title/announcement.
       - Columns: decision, title, agency, reasoning, knockout category.
     - Detail drawer/modal when clicking a row:
       - Show all metadata fields.
       - Display model narrative (from nalysis_notes or mistral_full_reports.md section).
       - Provide buttons to open full report in a new tab (link to Markdown file) and download CSV.

- Asset Build:
  - Use ite or simple 
pm tooling for bundling (optional). For simplicity, an ES module + plain CSS with 
pm run build generating files into SOS_UI_Dashboard/dist/.
  - Serve static files through FastAPI’s StaticFiles mount so the UI and API come from one process.

## One-click Launcher
- Provide START_DASHBOARD.bat at repo root:
  - Sets working directory.
  - Activates venv / ensures dependencies (optional message if uvicorn missing).
  - Runs uvicorn ui_service.app:app --reload (or --host 127.0.0.1 --port 8090).
  - Opens default browser to http://localhost:8090.

## Data Handling Notes
- All automation continues writing to endpoints.txt and SOS_Output/ exactly as today.
- UI will *read* data.json and mistral_full_reports.md; no modifications to those files.
- Run folders are detected by comparing directory timestamps against the run’s start time (safe even when multiple runs occur sequentially).

## Risk Mitigation
- No edits to pipeline scripts beyond the optional key fallbacks already in place.
- UI service writes temporary files under ui_service/runs/ only.
- Extensive logging in the wrapper (start time, command, exit codes) to aid debugging without stepping into pipeline internals.
