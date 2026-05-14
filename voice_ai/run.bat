@echo off
chcp 65001 >nul
title Voice Transcription

cd /d "%~dp0"

echo.
echo  Voice Transcription App shuru ho rahi hai...
echo.

python voice_app.py

if %errorlevel% neq 0 (
    echo.
    echo  ERROR aaya. Python installed hai?
    echo  python.org se install karein — "Add to PATH" tick karein
    pause
)
