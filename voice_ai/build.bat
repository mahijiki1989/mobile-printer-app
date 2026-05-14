@echo off
chcp 65001 >nul
title Voice App - EXE Build

:: Is folder mein jaao
cd /d "%~dp0"

echo.
echo  ========================================
echo    Voice Transcription - EXE Build
echo  ========================================
echo.

:: Python check
echo [1/3] Python check...
python --version
if %errorlevel% neq 0 (
    echo.
    echo  ERROR: Python nahi mila!
    echo  python.org se install karein
    pause
    exit /b 1
)
echo.

:: Sirf PyInstaller chahiye — koi PyAudio, koi SpeechRecognition nahi!
echo [2/3] PyInstaller install...
python -m pip install --upgrade pip --quiet
python -m pip install pyinstaller --quiet
if %errorlevel% neq 0 (
    echo ERROR: pip install fail hua
    pause
    exit /b 1
)
echo  PyInstaller ready!
echo.

:: EXE build
echo [3/3] EXE ban raha hai... (2-3 min wait karein)
echo.

pyinstaller --onefile --windowed --name "VoiceTranscription" voice_app.py

if %errorlevel% neq 0 (
    echo.
    echo  ERROR: Build fail hua — upar error dekho
    pause
    exit /b 1
)

:: Copy to current folder
if exist "dist\VoiceTranscription.exe" (
    copy /y "dist\VoiceTranscription.exe" "VoiceTranscription.exe" >nul
    echo.
    echo  ========================================
    echo   SUCCESS! EXE ban gaya:
    echo   %~dp0VoiceTranscription.exe
    echo.
    echo   Is file ko Desktop pe rakh kar
    echo   double-click se chalayein!
    echo  ========================================
    echo.
    :: Open folder
    explorer "%~dp0"
) else (
    echo  ERROR: EXE nahi mila
)

pause
