@echo off
REM ============================================================
REM  Groww Auto-Exit  -  one-click installer for Windows
REM ============================================================
REM  What this does:
REM   1. Checks Python 3.11 is installed
REM   2. Creates a virtualenv in .venv\
REM   3. Installs all dependencies from requirements.txt
REM
REM  Run this ONCE after extracting the ZIP.
REM ============================================================

setlocal

echo.
echo ============================================================
echo   Groww Auto-Exit - Installer
echo ============================================================
echo.

REM --- check Python 3.11 ---
where py >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python launcher 'py' not found.
    echo Please install Python 3.11 from https://www.python.org/downloads/
    echo Make sure "Add Python to PATH" is checked.
    pause
    exit /b 1
)

py -3.11 --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.11 is not installed.
    echo Please install Python 3.11 from https://www.python.org/downloads/
    echo Make sure "Add Python to PATH" is checked.
    pause
    exit /b 1
)

echo [1/3] Found Python 3.11 - OK
echo.

REM --- create venv ---
if exist .venv (
    echo [2/3] Virtualenv already exists, reusing.
) else (
    echo [2/3] Creating virtualenv in .venv\ ...
    py -3.11 -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtualenv.
        pause
        exit /b 1
    )
)
echo.

REM --- install dependencies ---
echo [3/3] Installing dependencies (this can take a few minutes)...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo.

REM --- copy .env if not present ---
if not exist .env (
    echo Creating .env from .env.example ...
    copy .env.example .env >nul
    echo.
    echo IMPORTANT: open .env in Notepad and paste your Groww credentials.
    echo.
)

echo ============================================================
echo   Install complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Edit .env and paste your GROWW_ACCESS_TOKEN
echo      (or GROWW_API_KEY + GROWW_API_SECRET)
echo   2. Double-click start.bat to launch the app.
echo.
pause
