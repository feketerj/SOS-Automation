@echo off
setlocal ENABLEEXTENSIONS

set "PY_EXE=.venv\Scripts\python.exe"
if not exist "%PY_EXE%" (
  echo missing
)