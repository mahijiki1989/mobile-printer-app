@echo off
chcp 65001 >nul
title Voice AI - Starting...

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║         🎤  Voice AI - Starting Up                  ║
echo ║         Hindi + English Voice Assistant             ║
echo ╚══════════════════════════════════════════════════════╝
echo.

:: Check if we're in the right directory
if not exist "voice_server.py" (
    echo  ❌ voice_server.py nahi mila!
    echo  voice_ai folder mein se start.bat chalayein.
    pause
    exit /b 1
)

:: Start Ollama in background (if installed)
echo [1/2] Ollama start kar rahe hain...
ollama --version >nul 2>&1
if %errorlevel% equ 0 (
    start /min "Ollama Server" ollama serve
    timeout /t 3 /nobreak >nul
    echo  ✓ Ollama server start ho gaya!
) else (
    echo  ⚠️  Ollama nahi mila - AI response kaam nahi karega.
    echo     Sirf Speech-to-Text (transcription) kaam karega.
)

:: Start Voice AI Python server
echo.
echo [2/2] Voice AI server start ho raha hai...
echo.
echo ══════════════════════════════════════════════════════
echo  🌐  Browser mein yeh link kholein:
echo      http://localhost:5050
echo.
echo  ⌨️  SPACE  = Recording start/stop
echo  ⌨️  ENTER  = AI se puchein
echo.
echo  Band karne ke liye: Ctrl+C dabayein
echo ══════════════════════════════════════════════════════
echo.

:: Open browser automatically after 3 seconds
start "" timeout /t 3 /nobreak >nul
start http://localhost:5050

:: Run server
python voice_server.py

echo.
echo  Server band ho gaya. Phir chalane ke liye start.bat chalayein.
pause
