@echo off
echo ============================================================
echo SOS ASSESSMENT - NO AI MODE (Regex + Collect Only)
echo ============================================================
echo This runs without any AI calls:
echo   1) Fetch opportunities and documents from HigherGov
echo   2) Apply Regex gate (divert NO-GOs)
echo   3) Prepare batch JSONL for later (GO/INDETERMINATE only)
echo   4) Save metadata + regex knockouts
echo ------------------------------------------------------------
echo Requires: HIGHERGOV_API_KEY in your environment (or default)
echo Outputs : batch_input_*.jsonl and batch_metadata_*.json
echo ============================================================
echo.

REM Change to batch processor directory
cd Mistral_Batch_Processor

REM Run collector (no AI calls)
python BATCH_COLLECTOR.py

REM Return to original directory
cd ..

echo.
echo ============================================================
echo NO-AI COLLECTION COMPLETE
echo Next: You can run RUN_BATCH_ONLY.bat to submit later
echo Or use FULL_BATCH_PROCESSOR after reviewing batch_input_*.jsonl
echo ============================================================
pause

