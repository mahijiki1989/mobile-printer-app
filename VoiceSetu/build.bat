@echo off
REM VoiceSetu Build Script for Windows
REM This script builds the app.exe and installer.exe

echo ============================================
echo   VoiceSetu Build Script
echo ============================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo [1/5] Creating virtual environment...
    python -m venv venv
) else (
    echo [1/5] Virtual environment already exists.
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install dependencies
echo [2/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

REM Generate icon if not exists
if not exist "assets\icon.ico" (
    echo [2.5/5] Generating application icon...
    python generate_icon.py
)

REM Build with PyInstaller
echo [3/5] Building application with PyInstaller...
pyinstaller voicesetu.spec --noconfirm --clean
if errorlevel 1 (
    echo ERROR: PyInstaller build failed.
    pause
    exit /b 1
)

echo [4/5] Build complete. Output in dist\VoiceSetu\
echo.

REM Check for Inno Setup
set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if exist %ISCC% (
    echo [5/5] Building installer with Inno Setup...
    if not exist "build\installer" mkdir build\installer
    %ISCC% installer.iss
    if errorlevel 1 (
        echo ERROR: Inno Setup build failed.
        pause
        exit /b 1
    )
    echo.
    echo ============================================
    echo   BUILD SUCCESSFUL!
    echo   App:       dist\VoiceSetu\VoiceSetu.exe
    echo   Installer: build\installer\VoiceSetu_Setup_1.0.0.exe
    echo ============================================
) else (
    echo [5/5] Inno Setup not found at %ISCC%
    echo Skipping installer generation.
    echo Install Inno Setup 6 from https://jrsoftware.org/isdl.php
    echo Then run: %ISCC% installer.iss
    echo.
    echo ============================================
    echo   PARTIAL BUILD SUCCESSFUL!
    echo   App: dist\VoiceSetu\VoiceSetu.exe
    echo ============================================
)

echo.
pause
