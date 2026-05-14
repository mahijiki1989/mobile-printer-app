@echo off
chcp 65001 >nul
title Voice App - EXE Build

cd /d "%~dp0"

echo.
echo  ========================================
echo    Voice Transcription - EXE Build
echo  ========================================
echo.

:: Find Python (try py, python, python3)
set PYCMD=
py --version >nul 2>&1 && set PYCMD=py
if "%PYCMD%"=="" (python --version >nul 2>&1 && set PYCMD=python)
if "%PYCMD%"=="" (python3 --version >nul 2>&1 && set PYCMD=python3)

if "%PYCMD%"=="" (
    echo  ERROR: Python nahi mila!
    echo  python.org se install karein
    pause
    exit /b 1
)

echo  Python: %PYCMD%
%PYCMD% --version
echo.

:: Install pyinstaller
echo [1/2] PyInstaller install...
%PYCMD% -m pip install pyinstaller --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo ERROR: pip install fail
    pause
    exit /b 1
)
echo  Done!
echo.

:: Build EXE
echo [2/2] EXE build ho raha hai... (2-3 min)
echo.

%PYCMD% -m PyInstaller --onefile --windowed --name "VoiceTranscription" voice_app.py

if %errorlevel% neq 0 (
    echo.
    echo  ERROR: Build fail — upar error dekho
    pause
    exit /b 1
)

if exist "dist\VoiceTranscription.exe" (
    copy /y "dist\VoiceTranscription.exe" "VoiceTranscription.exe" >nul
    echo.
    echo  ========================================
    echo   SUCCESS!
    echo   VoiceTranscription.exe ban gaya!
    echo   Desktop pe rakhein aur double-click karein
    echo  ========================================
    explorer "%~dp0"
) else (
    echo  ERROR: EXE nahi bana
)

echo.
pause
