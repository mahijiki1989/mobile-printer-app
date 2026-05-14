@echo off
chcp 65001 >nul
title Voice AI — Windows 11

echo.
echo  ================================================
echo    Voice AI - Windows 11
echo    Hindi + English Voice Assistant
echo  ================================================
echo.

:: Folder mein jaao jahan start.bat hai
cd /d "%~dp0"
echo  Folder: %~dp0
echo.

:: ── Python check ──────────────────────────────────────────────────────────
echo  [1/3] Python check...
python --version
if %errorlevel% neq 0 (
    echo.
    echo  ERROR: Python nahi mila!
    echo  python.org se install karein aur "Add to PATH" tick karein
    pause
    exit /b 1
)
echo.

:: ── pip upgrade + install ─────────────────────────────────────────────────
echo  [2/3] Flask install ho raha hai...
python -m pip install --upgrade pip
python -m pip install flask flask-cors
if %errorlevel% neq 0 (
    echo.
    echo  ERROR: flask install nahi hua!
    echo  Internet connection check karein.
    pause
    exit /b 1
)
echo.
echo  Flask ready!
echo.

:: ── Server start ──────────────────────────────────────────────────────────
echo  [3/3] Server start ho raha hai...
echo.
echo  ================================================
echo   Browser mein kholein:  http://localhost:5050
echo.
echo   SPACE  = bolna shuru / rokna
echo   ENTER  = AI se puchein
echo   S      = jawab sunein
echo.
echo   Band karne ke liye: is window ko band karein
echo   ya Ctrl+C dabayein
echo  ================================================
echo.

:: 3 second baad browser kholo
start "" cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5050"

:: Server run karo
python voice_server.py

echo.
echo  Server band ho gaya. Dubara chalane ke liye start.bat dabayein.
pause
