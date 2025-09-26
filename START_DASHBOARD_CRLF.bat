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

REM Create a dedicated virtual environment if it does not exist
if not exist .venv (
  echo [SETUP] Creating virtual environment (.venv)...
  python -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment.
    goto :EOF
  )
)

REM Use the virtual environment's Python
set "PY_EXE=.venv\Scripts\python.exe"
if not exist "%PY_EXE%" (
  echo [ERROR] Virtual environment is missing python.exe
  goto :EOF
)

REM Activate environment for this session
call .venv\Scripts\activate.bat >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Failed to activate virtual environment.
  goto :EOF
)

REM Install or update required packages quietly
set "REQ_FILE=ui_service\requirements.txt"
if not exist "%REQ_FILE%" (
  echo streamlit> "%REQ_FILE%"
)

echo [SETUP] Installing dashboard dependencies (once per environment)...
"%PY_EXE%" -m pip install --upgrade --quiet --disable-pip-version-check pip
"%PY_EXE%" -m pip install --quiet --disable-pip-version-check -r "%REQ_FILE%"
if errorlevel 1 (
  echo [ERROR] Dependency installation failed.
  goto :EOF
)

echo.
echo ================================================
echo SOS Pipeline Control Panel
echo Launching at http://127.0.0.1:8501
echo Close this window to stop the dashboard.
echo ================================================
echo.

start "" http://127.0.0.1:8501
"%PY_EXE%" -m streamlit run ui_service\app.py --server.port 8501 --server.headless true

endlocal

