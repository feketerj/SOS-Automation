@echo off
echo ============================================================
echo SOS POST-RUN CHECKLIST
echo ============================================================
echo Validates outputs, CSV, schema (if available), and writes audit/metrics.
echo Usage: RUN_POSTRUN_CHECK.bat [SOS_Output\YYYY-MM\Run_*\]
echo ------------------------------------------------------------

python tools/postrun_checklist.py %*

echo.
pause

