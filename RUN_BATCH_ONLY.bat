@echo off
echo ============================================================
echo SOS ASSESSMENT - BATCH ONLY MODE
echo ============================================================
echo Pipeline: Regex (FREE) -^> Batch (50%% off)
echo Cost: CHEAPEST - Maximum savings
echo ============================================================
echo.

REM Set environment variable to skip agent verification
set SKIP_AGENT_VERIFICATION=1

REM Change to batch processor directory
cd Mistral_Batch_Processor

REM Run batch processor
python FULL_BATCH_PROCESSOR.py

REM Return to original directory
cd ..

echo.
echo ============================================================
echo BATCH PROCESSING COMPLETE
echo Results in: SOS_Output\2025-09\Run_[timestamp]_BATCH\
echo ============================================================
pause