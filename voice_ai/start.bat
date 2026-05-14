@echo off
chcp 65001 >nul
title Voice AI — Windows 11

echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║    🎤  Voice AI — Windows 11 Built-in       ║
echo  ║    Hindi + English  •  No Install Needed    ║
echo  ╚══════════════════════════════════════════════╝
echo.

:: ── Python check ──────────────────────────────────────────────────────────
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  ❌ Python nahi mila!
    echo.
    echo  Python install karein:  https://www.python.org/downloads/
    echo  Install ke waqt "Add Python to PATH" zaroor tick karein!
    echo.
    pause
    exit /b 1
)

:: ── pip packages (sirf pehli baar ~10 seconds) ───────────────────────────
echo  [1/2] Packages check/install kar rahe hain...
pip install flask flask-cors pyttsx3 --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo  ❌ Packages install nahi hue — internet check karein.
    pause
    exit /b 1
)
echo  ✓ Packages ready!
echo.

:: ── Start server + open browser ──────────────────────────────────────────
echo  [2/2] Server start ho raha hai...
echo.
echo  ══════════════════════════════════════════════
echo   🌐  Browser mein kholein:
echo       http://localhost:5050
echo.
echo   ⌨️  SPACE   = bolna shuru / rokna
echo   ⌨️  ENTER   = AI se puchein
echo   ⌨️  S       = jawab sunein
echo.
echo   🛑  Band karne ke liye:  Ctrl + C
echo  ══════════════════════════════════════════════
echo.

:: Open browser after short delay
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:5050"

:: Run server (blocking)
python "%~dp0voice_server.py"

echo.
echo  Server band ho gaya.
pause
