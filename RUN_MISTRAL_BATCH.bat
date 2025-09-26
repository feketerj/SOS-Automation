@echo off
echo ========================================================================
echo                     MISTRAL BATCH PROCESSOR
echo ========================================================================
echo.
echo This will process all search IDs in endpoints.txt using:
echo   1. Regex filtering (knocks out obvious NO-GOs locally)
echo   2. Mistral batch API (processes remaining opportunities)
echo   3. CSV output matching production format
echo.
echo ========================================================================
echo.

REM Change to Mistral_Batch_Processor directory
cd Mistral_Batch_Processor

echo Starting batch processing pipeline...
echo.

REM Run the full batch processor
python FULL_BATCH_PROCESSOR.py

echo.
echo ========================================================================
echo Batch processing initiated!
echo Results will be saved to SOS_Output folder when complete.
echo ========================================================================
echo.

pause