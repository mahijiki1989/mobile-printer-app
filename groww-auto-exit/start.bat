@echo off
REM ============================================================
REM  Groww Auto-Exit  -  launcher
REM ============================================================
REM  Double-click this to start the app after running install.bat
REM ============================================================

setlocal

if not exist .venv\Scripts\python.exe (
    echo [ERROR] .venv not found. Run install.bat first.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
python run.py

REM Keep window open if the app crashes so the user can read the error.
if errorlevel 1 (
    echo.
    echo App exited with an error.
    pause
)
