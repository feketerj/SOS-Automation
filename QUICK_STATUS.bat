@echo off
echo ================================================================================
echo BATCH PROCESSING STATUS
echo ================================================================================
echo.
echo Stage 1: FETCHING (8-17 mins) - Downloading from HigherGov API
echo Stage 2: FILTERING (instant) - Applying regex patterns
echo Stage 3: BATCHING (1-2 mins) - Creating Mistral batch file
echo Stage 4: SUBMITTING (instant) - Sending to Mistral API
echo.
echo Current Stage: FETCHING OPPORTUNITIES
echo Estimated Total Time: 10-20 minutes
echo.
echo Checking for output files...
cd Mistral_Batch_Processor
dir batch_*.jsonl 2>nul | find ".jsonl" && echo BATCH FILE CREATED! || echo Still processing...
echo.
pause