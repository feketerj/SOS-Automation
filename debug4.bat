@echo off
set "REQ_FILE=ui_service\requirements.txt"
if not exist "%REQ_FILE%" (
  echo streamlit> "%REQ_FILE%"
)