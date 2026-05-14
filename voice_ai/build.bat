@echo off
chcp 65001 >nul
title Voice App - EXE Build
cd /d "%~dp0"

echo.
echo  ============================================
echo    Voice Transcription - EXE Build
echo  ============================================
echo.

:: ── Python dhundho ────────────────────────────────────────────────────────────
set PYCMD=

py --version >nul 2>&1
if %errorlevel% equ 0 ( set PYCMD=py & goto :found_py )

python --version >nul 2>&1
if %errorlevel% equ 0 ( set PYCMD=python & goto :found_py )

python3 --version >nul 2>&1
if %errorlevel% equ 0 ( set PYCMD=python3 & goto :found_py )

echo  ERROR: Python nahi mila!
pause
exit /b 1

:found_py
echo  Python: %PYCMD%
%PYCMD% --version
echo.

:: ── Packages install ─────────────────────────────────────────────────────────
echo [1/2] Packages install...
%PYCMD% -m pip install sounddevice numpy pyinstaller --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo  ERROR: Install fail
    pause
    exit /b 1
)
echo  Done!
echo.

:: ── EXE build ────────────────────────────────────────────────────────────────
echo [2/2] EXE build ho raha hai... (2-3 min wait karein)
echo.

%PYCMD% -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name "VoiceTranscription" ^
    --hidden-import=sounddevice ^
    --hidden-import=numpy ^
    --collect-all sounddevice ^
    voice_app.py

if %errorlevel% neq 0 (
    echo  ERROR: Build fail
    pause
    exit /b 1
)

if exist "dist\VoiceTranscription.exe" (
    copy /y "dist\VoiceTranscription.exe" "VoiceTranscription.exe" >nul
    echo.
    echo  ============================================
    echo   SUCCESS! VoiceTranscription.exe ban gaya!
    echo   Desktop pe rakhein aur double-click karein
    echo  ============================================
    explorer "%~dp0"
) else (
    echo  ERROR: EXE nahi bana
)

echo.
pause
