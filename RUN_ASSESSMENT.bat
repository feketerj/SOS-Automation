@echo off
REM ========================================
REM SOS ASSESSMENT RUNNER - JUST WORKS
REM ========================================

echo ========================================
echo SOS ASSESSMENT AUTOMATION TOOL
echo ========================================
echo.

REM Check if search ID provided
if "%1"=="" (
    echo USAGE: RUN_ASSESSMENT.bat SEARCH_ID
    echo.
    echo EXAMPLE: RUN_ASSESSMENT.bat f5KQeEYWpQ4FtgSOPd6Sm
    echo.
    pause
    exit /b
)

echo Running assessment for: %1
echo.

REM Run the locked production runner
python LOCKED_PRODUCTION_RUNNER.py %1

echo.
echo ========================================
echo ASSESSMENT COMPLETE
echo Check SOS_Output folder for results
echo ========================================
pause