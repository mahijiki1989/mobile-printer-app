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

for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo  ✓ Python %PYVER% mila!
echo.

:: ── pip packages (sirf 2 — pehli baar ~5 seconds) ────────────────────────
echo  [1/2] flask + flask-cors install check...
pip install flask flask-cors --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo  ❌ Install nahi hua — internet check karein.
    pause
    exit /b 1
)
echo  ✓ Packages ready!
echo.

:: ── Start server ──────────────────────────────────────────────────────────
echo  [2/2] Server start ho raha hai...
echo.
echo  ══════════════════════════════════════════════
echo   🌐  Browser mein kholein:
echo       http://localhost:5050
echo.
echo   🎤  STT:  Browser Web Speech API (built-in)
echo   🔊  TTS:  Windows PowerShell SAPI (built-in)
echo   🤖  AI:   Python rule-based engine
echo.
echo   ⌨️  SPACE   = bolna shuru / rokna
echo   ⌨️  ENTER   = AI se puchein
echo   ⌨️  S       = jawab sunein
echo.
echo   🛑  Band karne ke liye:  Ctrl + C
echo  ══════════════════════════════════════════════
echo.

:: Browser 2 second baad kholo
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:5050"

:: Server chalao
python "%~dp0voice_server.py"

echo.
echo  Server band ho gaya.
pause
