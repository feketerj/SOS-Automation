@echo off
echo ============================================================
echo SOS SMOKE RUN (No Batch/Agent Submission)
echo ============================================================
echo This preflight check:
echo   1) Runs setup checks
echo   2) Fetches 1 page from the first search ID
echo   3) Applies Regex gate
echo   4) Writes batch_input_*_SMOKE.jsonl and metadata
echo   5) Optionally validates handoff files
echo ------------------------------------------------------------
echo Usage: RUN_SMOKE.bat [--validate]
echo ============================================================
echo.

python tools/smoke_run.py %*

echo.
pause

