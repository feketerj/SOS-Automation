@echo off
echo ============================================================
echo SOS OUTPUT ARCHIVER
echo ============================================================
echo Moves Run_* folders older than N days into _ARCHIVE_...
echo Usage: RUN_ARCHIVE_OUTPUTS.bat [--days 30]
echo ------------------------------------------------------------

python tools/archive_outputs.py %*

echo.
pause

