@echo off
chcp 65001 >nul
title Voice Transcription

cd /d "%~dp0"

:: Try "py" first (Windows Launcher - most common)
py --version >nul 2>&1
if %errorlevel% equ 0 (
    py voice_app.py
    goto :done
)

:: Try "python" 
python --version >nul 2>&1
if %errorlevel% equ 0 (
    python voice_app.py
    goto :done
)

:: Try "python3"
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    python3 voice_app.py
    goto :done
)

:: Nothing found
echo.
echo  ======================================
echo  Python nahi mila!
echo.
echo  Yeh try karein:
echo  1. Start Menu mein "Python" search karein
echo  2. Agar dikhe toh:
echo     Settings - Apps - App execution aliases
echo     mein python.exe ON karein
echo  3. Ya phir Command Prompt mein type karein:
echo     py voice_app.py
echo  ======================================
echo.
pause

:done
