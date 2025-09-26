@echo off
echo ============================================================
echo MISTRAL BATCH PROCESSOR - Complete Pipeline
echo ============================================================
echo.
echo This will process all opportunities from endpoints.txt
echo using Mistral's batch API for parallel processing
echo.
pause

echo.
echo ============================================================
echo STEP 1: Collecting opportunities and creating JSONL
echo ============================================================
python BATCH_COLLECTOR.py
if errorlevel 1 goto error

echo.
echo ============================================================
echo STEP 2: Submitting batch to Mistral
echo ============================================================
python BATCH_SUBMITTER.py
if errorlevel 1 goto error

echo.
echo ============================================================
echo BATCH SUBMITTED SUCCESSFULLY!
echo ============================================================
echo.
echo The batch has been submitted to Mistral for processing.
echo This typically takes 5-15 minutes depending on volume.
echo.
echo You can check the status anytime by running:
echo   python BATCH_SUBMITTER.py --status [batch_id]
echo.
echo Once complete, download and parse results with:
echo   python BATCH_SUBMITTER.py --download [batch_id]
echo   python BATCH_RESULTS_PARSER.py
echo.
pause
exit

:error
echo.
echo ERROR: Process failed. Check the error message above.
pause
exit /b 1