@echo off
echo ============================================================
echo DOWNLOADING AND PARSING BATCH RESULTS
echo ============================================================
echo.

:: Find the most recent batch_info file to get the batch ID
for /f "tokens=*" %%a in ('dir /b /o-d batch_info_*.json 2^>nul') do (
    set BATCH_FILE=%%a
    goto :found
)

echo No batch submissions found!
pause
exit

:found
:: Extract batch ID from filename
for /f "tokens=2 delims=_" %%b in ("%BATCH_FILE%") do set BATCH_ID=%%b
set BATCH_ID=%BATCH_ID:.json=%

echo Found batch: %BATCH_ID%
echo.

echo Step 1: Downloading results...
echo ============================================================
python BATCH_SUBMITTER.py --download %BATCH_ID%
if errorlevel 1 goto error

echo.
echo Step 2: Parsing results and creating CSV...
echo ============================================================
python BATCH_RESULTS_PARSER.py
if errorlevel 1 goto error

echo.
echo ============================================================
echo SUCCESS! Results are saved in:
echo   - SOS_Output\[current month]\BatchRun_[timestamp]_BATCH\
echo   - Local copy in this folder
echo ============================================================
pause
exit

:error
echo.
echo ERROR: Process failed. Check the error message above.
pause
exit /b 1