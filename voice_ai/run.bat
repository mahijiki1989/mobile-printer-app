@echo off
chcp 65001 >nul
title Voice Transcription App
cd /d "%~dp0"

echo.
echo  ============================================
echo    Voice Transcription App - Starting...
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
echo  python.org/downloads se install karein
echo  Install karte waqt "Add Python to PATH" ZAROOR tick karein!
pause
exit /b 1

:found_py
echo  Python mila: %PYCMD%
%PYCMD% --version
echo.

:: ── Required packages install ────────────────────────────────────────────────
echo  Packages check/install ho rahe hain...
echo  (pehli baar 1-2 minute lag sakte hain)
echo.

%PYCMD% -m pip install sounddevice numpy --quiet --disable-pip-version-check

if %errorlevel% neq 0 (
    echo.
    echo  ERROR: Packages install nahi hue!
    echo  Internet connection check karein.
    pause
    exit /b 1
)

echo  Packages ready!
echo.

:: ── App chalao ────────────────────────────────────────────────────────────────
echo  App shuru ho rahi hai...
echo  (window band karne ke liye X button dabayein)
echo.

%PYCMD% voice_app.py

if %errorlevel% neq 0 (
    echo.
    echo  App band ho gayi ya error aaya.
    pause
)
