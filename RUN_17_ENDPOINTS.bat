@echo off
echo ================================================================================
echo RUNNING FULL BATCH - 17 ENDPOINTS
echo ================================================================================
echo.
set SKIP_AGENT_VERIFICATION=1
cd Mistral_Batch_Processor
echo n | python FULL_BATCH_PROCESSOR.py
echo.
echo ================================================================================
echo BATCH PROCESSING SUBMITTED
echo Check status with: python CHECK_BATCH_STATUS.py
echo ================================================================================
pause