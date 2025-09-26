@echo off
REM Daily health check - Run this each morning
echo ========================================
echo DAILY PIPELINE CHECK
echo ========================================
echo.

REM Run health check
python PIPELINE_HEALTH_CHECK.py

if %errorlevel% neq 0 (
    echo.
    echo [ALERT] PIPELINE ISSUES DETECTED!
    echo Check the health report for details.
    pause
    exit /b 1
)

echo.
echo [OK] Pipeline is healthy and ready to use
echo.
echo Run assessments with:
echo   python LOCKED_PRODUCTION_RUNNER.py [SEARCH_ID]
echo.
pause