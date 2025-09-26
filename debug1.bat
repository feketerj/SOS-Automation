@echo off
setlocal ENABLEEXTENSIONS

REM Navigate to project root
cd /d "%~dp0"

REM Ensure Python is available
where python >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python is not installed or not on PATH.
  goto :EOF
)