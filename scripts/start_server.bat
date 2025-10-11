@echo off
REM Change to the folder where this BAT file is located
cd /d "%~dp0"

REM Make a logs folder if it doesn't exist
if not exist logs mkdir logs

REM Get timestamp for log file
for /f "tokens=1-4 delims=/ " %%a in ("%date%") do (
    set date=%%d-%%b-%%c
)
for /f "tokens=1-2 delims=: " %%a in ("%time%") do (
    set time=%%a-%%b
)
set logname=logs\fastapi_%date%_%time%.log

REM Run FastAPI server with uvicorn and log output
py -3.11 -m uvicorn app:app --host 0.0.0.0 --port 5000 >> "%logname%" 2>&1
