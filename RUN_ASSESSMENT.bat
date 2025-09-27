@echo off
REM ==============================================================================
REM THE ONE AND ONLY WAY TO RUN ASSESSMENTS
REM ==============================================================================
REM
REM This runs the SOS Assessment Pipeline:
REM   1. Reads endpoints.txt
REM   2. Fetches opportunities from HigherGov
REM   3. Applies regex filtering
REM   4. Saves results to SOS_Output
REM
REM Usage:
REM   1. Edit endpoints.txt (add search IDs, one per line)
REM   2. Double-click this file or run: RUN_ASSESSMENT.bat
REM
REM ==============================================================================

echo.
echo ======================================================================
echo                     SOS ASSESSMENT AUTOMATION
echo ======================================================================
echo.

REM Check for endpoints.txt
if not exist endpoints.txt (
    echo ERROR: endpoints.txt not found!
    echo.
    echo Please create endpoints.txt with your search IDs.
    echo Example:
    echo   AR1yyM0PV54_Ila0ZV6J6
    echo   BR2xxN1QW65_Jmb1YW7K7
    echo.
    pause
    exit /b 1
)

REM Run the assessment
echo Starting assessment pipeline...
echo.
python RUN_ASSESSMENT.py

if errorlevel 1 (
    echo.
    echo ERROR: Assessment failed!
    echo Check that Python is installed and API keys are set.
    echo.
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo                         ASSESSMENT COMPLETE
echo ======================================================================
echo.
echo Results saved to SOS_Output folder.
echo.
pause