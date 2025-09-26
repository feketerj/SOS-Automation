@echo off
title SOS Assessment Tool
echo ========================================
echo Starting SOS Assessment Tool UI...
echo ========================================
echo.

cd /d "C:\Users\feket\OneDrive\Desktop\excelsior\r_staff\r_3\Deployed_Code_Op_Locations\SOS-Assessment-Automation-Tool"

echo Launching Streamlit interface...
echo.
echo Opening Chrome browser...
start chrome http://localhost:8501
echo.
echo Starting server...
echo Press Ctrl+C in this window to stop the server
echo ========================================
echo.

C:\Users\feket\Miniconda3\python.exe -m streamlit run ui_service/app.py

pause