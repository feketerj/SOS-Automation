@echo off
echo ============================================================
echo SOS ASSESSMENT - BATCH + AGENT VERIFICATION MODE
echo ============================================================
echo Pipeline: Regex (FREE) -^> Batch (50%% off) -^> Agent (selective)
echo Cost: BALANCED - Good savings with accuracy check
echo Accuracy: EXCELLENT - Agent verifies GOs/INDETERMINATEs
echo ============================================================
echo.

REM Clear any skip flag to ensure agent verification runs
set SKIP_AGENT_VERIFICATION=

REM Change to batch processor directory
cd Mistral_Batch_Processor

REM Run batch processor with full pipeline
python FULL_BATCH_PROCESSOR.py

REM Return to original directory
cd ..

echo.
echo ============================================================
echo BATCH + AGENT VERIFICATION COMPLETE
echo Results in: SOS_Output\2025-09\Run_[timestamp]_BATCH\
echo ============================================================
pause