@echo off
echo ============================================================
echo MISTRAL BATCH PROCESSOR - Auto Process from Downloads
echo ============================================================
echo.
echo This will:
echo 1. Find the latest JSONL file in your Downloads folder
echo 2. Process it automatically
echo 3. Put results in SOS_Output (where they belong!)
echo 4. Clean up working files
echo.
pause

:: Find the latest JSONL file in Downloads
for /f "tokens=*" %%a in ('dir /b /o-d "C:\Users\feket\Downloads\*.jsonl" 2^>nul') do (
    set RESULT_FILE=C:\Users\feket\Downloads\%%a
    goto :found
)

echo No JSONL files found in Downloads folder!
pause
exit

:found
echo.
echo Found: %RESULT_FILE%
echo.

:: Create temp working directory with timestamp
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "timestamp=%dt:~0,8%_%dt:~8,6%"

:: Copy to working location with proper name
echo Copying to working location...
copy "%RESULT_FILE%" "batch_results_%timestamp%.jsonl" >nul

:: Find matching metadata (use most recent)
for /f "tokens=*" %%a in ('dir /b /o-d batch_metadata_*.json 2^>nul') do (
    set METADATA_FILE=%%a
    goto :parse
)

echo Warning: No metadata file found. Results may be incomplete.
set METADATA_FILE=

:parse
echo.
echo Processing results...
python BATCH_RESULTS_PARSER.py

if errorlevel 1 goto error

echo.
echo ============================================================
echo SUCCESS! Results saved to:
echo   SOS_Output\2025-09\BatchRun_[timestamp]_BATCH\
echo ============================================================
echo.
echo Cleaning up temporary files...

:: Clean up working files (keep metadata for reference)
del batch_results_%timestamp%.jsonl 2>nul

echo Done!
pause
exit

:error
echo.
echo ERROR: Failed to process results
pause
exit /b 1