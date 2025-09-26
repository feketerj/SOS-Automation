@echo off
echo ========================================
echo REPO CLEANUP - Reducing 3GB to under 100MB
echo ========================================
echo.

REM Check current size
echo Current repository size:
powershell -Command "(Get-ChildItem -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB"
echo GB
echo.

echo WARNING: This will delete:
echo - .venv folder (11,000+ files)
echo - All __pycache__ folders
echo - All .pyc files
echo - .history folder
echo - Archive folders from September
echo - Old batch outputs
echo - Old test outputs
echo.
pause

echo.
echo [1/7] Removing Python virtual environment...
if exist .venv (
    rmdir /s /q .venv
    echo    Deleted .venv
) else (
    echo    .venv not found
)

echo.
echo [2/7] Removing Python cache files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
echo    Cleaned Python cache

echo.
echo [3/7] Removing VS Code history...
if exist .history (
    rmdir /s /q .history
    echo    Deleted .history
) else (
    echo    .history not found
)

echo.
echo [4/7] Removing old archive folders...
if exist _ARCHIVE_2025_09_03 (
    rmdir /s /q _ARCHIVE_2025_09_03
    echo    Deleted _ARCHIVE_2025_09_03
)
if exist _ARCHIVE_2025_09_04 (
    rmdir /s /q _ARCHIVE_2025_09_04
    echo    Deleted _ARCHIVE_2025_09_04
)
if exist _ARCHIVE_OLD_FILES_2025_09_09 (
    rmdir /s /q _ARCHIVE_OLD_FILES_2025_09_09
    echo    Deleted _ARCHIVE_OLD_FILES_2025_09_09
)
if exist _BACKUP_BEFORE_CLEANUP_2025_09_25 (
    rmdir /s /q _BACKUP_BEFORE_CLEANUP_2025_09_25
    echo    Deleted _BACKUP_BEFORE_CLEANUP_2025_09_25
)

echo.
echo [5/7] Removing old batch files...
del /q batch_output_*.jsonl 2>nul
del /q batch_results_*.jsonl 2>nul
del /q batch_summary_*.txt 2>nul
del /q checkpoint_*.txt 2>nul
del /q batch_errors.jsonl 2>nul
del /q batch_format_verification.json 2>nul
del /q test_batch_output.json 2>nul
echo    Cleaned batch artifacts

echo.
echo [6/7] Removing test and temporary files...
if exist tests_archive rmdir /s /q tests_archive
if exist backups rmdir /s /q backups
if exist SOS_Output_TEST rmdir /s /q SOS_Output_TEST
if exist Gov-Test-Docs rmdir /s /q Gov-Test-Docs
if exist Master_Analytics rmdir /s /q Master_Analytics
if exist Reports rmdir /s /q Reports
del /q *.backup 2>nul
del /q script_output.txt 2>nul
del /q pipeline_output.log 2>nul
del /q nul 2>nul
del /q debug1.bat debug2.bat debug3.bat debug4.bat 2>nul
del /q paren_test.bat test.bat 2>nul
echo    Cleaned test/temp files

echo.
echo [7/7] Cleaning Mistral batch processor artifacts...
cd Mistral_Batch_Processor
del /q batch_input_*.jsonl 2>nul
del /q batch_output_*.jsonl 2>nul
del /q batch_results_*.jsonl 2>nul
del /q batch_metadata_*.json 2>nul
del /q batch_info_*.json 2>nul
if exist SOS_Output rmdir /s /q SOS_Output
cd ..
echo    Cleaned Mistral artifacts

echo.
echo ========================================
echo CLEANUP COMPLETE!
echo ========================================
echo.
echo New repository size:
powershell -Command "(Get-ChildItem -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB"
echo MB
echo.
echo Next steps:
echo 1. Run 'python -m venv .venv' to recreate virtual environment
echo 2. Run 'pip install -r requirements.txt' to reinstall dependencies
echo 3. Test with RUN_SMOKE.bat to verify pipeline works
echo.
pause