@echo off
echo ============================================================
echo MISTRAL BATCH PROCESSOR - Complete Pipeline
echo ============================================================
echo.
echo This will:
echo 1. Collect all opportunities from endpoints.txt
echo 2. Create JSONL batch file
echo 3. Show instructions for Mistral batch submission
echo.
pause

echo.
echo Step 1: Collecting opportunities...
echo ============================================================
python BATCH_COLLECTOR.py
if errorlevel 1 goto error

echo.
echo ============================================================
echo COLLECTION COMPLETE!
echo.
echo Next steps:
echo 1. Submit the batch_input_*.jsonl file to Mistral
echo 2. Wait for processing to complete
echo 3. Download results and run parser
echo.
echo For detailed instructions, see README.md
echo ============================================================
pause
exit

:error
echo.
echo ERROR: Failed to collect opportunities
pause
exit /b 1