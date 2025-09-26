@echo off
call .venv\Scripts\activate.bat >nul 2>&1
if errorlevel 1 (
  echo fail
)