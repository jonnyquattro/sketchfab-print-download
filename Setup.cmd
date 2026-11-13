@echo off
cd /d "%~dp0"
python -m venv .venv
if errorlevel 1 goto fail
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto fail
pushd vendor\sfrip
call npm.cmd ci --ignore-scripts --no-audit --no-fund
if errorlevel 1 (
    popd
    goto fail
)
popd
echo Setup complete. Run Start Sketchfab Helper.cmd next.
pause
exit /b 0
:fail
echo Setup failed. Check the error above. Python and Node.js must be installed.
pause
exit /b 1
