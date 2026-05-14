@echo off
chcp 65001 >nul
title Voice App — EXE Build

echo.
echo  ================================================
echo    Voice Transcription App — EXE Build Script
echo    Yeh .exe banayega jo directly chalega
echo  ================================================
echo.

:: voice_ai folder mein jaao
cd /d "%~dp0"

:: ── Python check ─────────────────────────────────────────────────────────────
echo [1/4] Python check...
python --version
if %errorlevel% neq 0 (
    echo.
    echo  ERROR: Python nahi mila!
    echo  python.org se install karein — "Add to PATH" tick karein
    pause
    exit /b 1
)
echo.

:: ── Packages install ──────────────────────────────────────────────────────────
echo [2/4] Required packages install ho rahe hain...
echo  (pehli baar 2-3 minute lag sakte hain)
echo.
python -m pip install --upgrade pip
python -m pip install SpeechRecognition pyaudio pyinstaller
if %errorlevel% neq 0 (
    echo.
    echo  ERROR: Packages install nahi hue.
    echo.
    echo  PyAudio install fail hone par manually try karein:
    echo    pip install pipwin
    echo    pipwin install pyaudio
    echo.
    pause
    exit /b 1
)
echo.
echo  Packages ready!
echo.

:: ── PyInstaller se EXE build ──────────────────────────────────────────────────
echo [3/4] EXE build ho raha hai...
echo  (3-5 minute lagenge — please wait)
echo.

pyinstaller ^
    --onefile ^
    --windowed ^
    --name "VoiceTranscription" ^
    --hidden-import=speech_recognition ^
    --hidden-import=pyaudio ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.scrolledtext ^
    --collect-all speech_recognition ^
    voice_app.py

if %errorlevel% neq 0 (
    echo.
    echo  ERROR: EXE build fail ho gaya!
    echo  Upar ka error message dekho.
    pause
    exit /b 1
)

:: ── Copy to current folder ────────────────────────────────────────────────────
echo.
echo [4/4] EXE copy kar rahe hain...

if exist "dist\VoiceTranscription.exe" (
    copy /y "dist\VoiceTranscription.exe" "VoiceTranscription.exe"
    echo.
    echo  ================================================
    echo    BUILD SUCCESSFUL!
    echo.
    echo    VoiceTranscription.exe is folder mein hai:
    echo    %~dp0VoiceTranscription.exe
    echo.
    echo    Is file ko Desktop pe rakh do aur
    echo    double-click karke chalao!
    echo  ================================================
) else (
    echo.
    echo  ERROR: dist\VoiceTranscription.exe nahi mila.
    pause
    exit /b 1
)

echo.
pause
