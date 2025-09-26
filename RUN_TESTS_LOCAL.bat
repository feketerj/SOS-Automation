@echo off
echo ============================================================
echo SOS LOCAL TESTS (pytest)
echo ============================================================
echo Running curated tests in the tests/ folder (no network).
echo ------------------------------------------------------------

pytest -q tests
if %ERRORLEVEL% NEQ 0 (
  echo.
  echo [WARN] pytest returned a non-zero exit code. Ensure pytest is installed:
  echo        pip install -r requirements.txt
)

echo.
pause

