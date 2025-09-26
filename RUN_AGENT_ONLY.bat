@echo off
echo ============================================================
echo SOS ASSESSMENT - AGENT ONLY MODE
echo ============================================================
echo Pipeline: Regex (FREE) -^> Agent (full price)
echo Cost: HIGHER - But most accurate
echo Accuracy: BEST - Production agent with full training
echo ============================================================
echo.

REM Run regular batch runner which uses agent
python BATCH_RUN.py

echo.
echo ============================================================
echo AGENT PROCESSING COMPLETE
echo Results in: SOS_Output\2025-09\Run_[timestamp]\
echo ============================================================
pause