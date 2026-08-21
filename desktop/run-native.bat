@echo off
setlocal
cd /d "%~dp0\.."
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 desktop\run_native.py %*
) else (
  python desktop\run_native.py %*
)
if errorlevel 1 pause
