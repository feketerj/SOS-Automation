@echo off
echo ============================================================
echo CHECKING BATCH STATUS
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
:: Extract batch ID from filename (batch_info_[BATCH_ID].json)
for /f "tokens=2 delims=_" %%b in ("%BATCH_FILE%") do set BATCH_ID=%%b
:: Remove .json extension
set BATCH_ID=%BATCH_ID:.json=%

echo Found batch: %BATCH_ID%
echo.
python BATCH_SUBMITTER.py --status %BATCH_ID%

echo.
echo ============================================================
echo If status is "completed", run DOWNLOAD_AND_PARSE.bat
echo ============================================================
pause