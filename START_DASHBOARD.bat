@echo off
setlocal ENABLEEXTENSIONS

REM Navigate to project root
cd /d "%~dp0"

REM Ensure Python is available
where python >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python is not installed or not on PATH.
  echo Install Python 3.11+ and re-run this launcher.
  goto :EOF
)

python launch_dashboard.py
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" (
  echo.
  echo [WARN] Launcher exited with error code %EXIT_CODE%.
)

endlocal & exit /b %EXIT_CODE%