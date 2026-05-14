@echo off
chcp 65001 >nul
title Voice AI - Setup (Windows 11)

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║         Voice AI Setup - Windows 11                 ║
echo ║         Hindi + English Voice Assistant             ║
echo ╚══════════════════════════════════════════════════════╝
echo.

:: ── Step 1: Python Check ──────────────────────────────────────────────────────
echo [1/5] Python check kar rahe hain...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  ❌ Python nahi mila!
    echo  Python download karein: https://www.python.org/downloads/
    echo  Install karte waqt "Add Python to PATH" zaroor tick karein!
    echo.
    pause
    exit /b 1
)
echo  ✓ Python mil gaya!

:: ── Step 2: pip upgrade ───────────────────────────────────────────────────────
echo.
echo [2/5] pip upgrade kar rahe hain...
python -m pip install --upgrade pip --quiet
echo  ✓ pip updated!

:: ── Step 3: Install Python packages ──────────────────────────────────────────
echo.
echo [3/5] Python packages install ho rahe hain...
echo  (pehli baar mein 2-3 minute lag sakte hain, wait karein)
echo.
pip install flask flask-cors faster-whisper pyttsx3
if %errorlevel% neq 0 (
    echo.
    echo  ❌ Package install mein problem aayi!
    echo  Internet connection check karein aur dobara chalayein.
    pause
    exit /b 1
)
echo.
echo  ✓ Saare packages install ho gaye!

:: ── Step 4: Ollama Check ──────────────────────────────────────────────────────
echo.
echo [4/5] Ollama check kar rahe hain...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  ⚠️  Ollama nahi mila!
    echo.
    echo  Ollama install karne ke liye:
    echo  1. Yeh link kholein: https://ollama.com/download
    echo  2. Windows installer download karein aur install karein
    echo  3. Install ke baad yeh setup dobara chalayein
    echo.
    echo  [Skip karein aur abhi sirf Speech-to-Text use karein? Y/N]
    set /p skip_ollama="Aapka jawab: "
    if /i "%skip_ollama%"=="Y" (
        echo  ℹ️  Ollama baad mein install kar sakte hain.
        goto :whisper_download
    ) else (
        start https://ollama.com/download
        echo  Browser mein Ollama ka download page khul gaya.
        echo  Install karke dobara setup.bat chalayein.
        pause
        exit /b 0
    )
) else (
    echo  ✓ Ollama mil gaya!
)

:: ── Step 4b: Download llama3 model ───────────────────────────────────────────
echo.
echo  Llama3 model check kar rahe hain...
echo  (Pehli baar 4-5 GB download hoga - ek baar hi hoga)
echo.
ollama pull llama3
if %errorlevel% neq 0 (
    echo  ⚠️  llama3 download nahi hua. Baad mein manually chalayein: ollama pull llama3
) else (
    echo  ✓ llama3 model ready!
)

:whisper_download
:: ── Step 5: Whisper model pre-download ───────────────────────────────────────
echo.
echo [5/5] Whisper model pre-download kar rahe hain...
echo  (~150MB, ek baar hi hoga)
echo.
python -c "from faster_whisper import WhisperModel; WhisperModel('base', device='cpu', compute_type='int8'); print('Whisper model ready!')"
if %errorlevel% neq 0 (
    echo  ⚠️  Whisper model abhi download nahi hua - pehli baar server start pe hoga.
) else (
    echo  ✓ Whisper model ready!
)

:: ── Done ──────────────────────────────────────────────────────────────────────
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║   ✅  Setup Complete! Ab start.bat chalayein        ║
echo ╚══════════════════════════════════════════════════════╝
echo.
pause
