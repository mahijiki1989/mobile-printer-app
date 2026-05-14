@echo off
chcp 65001 >nul
title Voice Transcription App
cd /d "%~dp0"

echo.
echo  ============================================
echo    Voice Transcription App
echo  ============================================
echo.

:: Python dhundho
set PYCMD=
py --version >nul 2>&1
if %errorlevel% equ 0 ( set PYCMD=py& goto :found )
python --version >nul 2>&1
if %errorlevel% equ 0 ( set PYCMD=python& goto :found )
python3 --version >nul 2>&1
if %errorlevel% equ 0 ( set PYCMD=python3& goto :found )

echo  Python nahi mila!
pause
exit /b 1

:found
echo  Python: %PYCMD%
%PYCMD% --version
echo.
echo  App shuru ho rahi hai...
echo.

%PYCMD% "%~dp0voice_app.py"

if %errorlevel% neq 0 (
    echo.
    echo  ERROR aaya — upar message dekho.
    pause
)
