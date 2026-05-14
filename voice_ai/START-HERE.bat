@echo off
chcp 65001 >nul
title Voice Transcription
cd /d "%~dp0"

echo.
echo  ==========================================
echo    Voice Transcription App
echo    Mic permission ek baar dein — yaad rahega
echo  ==========================================
echo.

:: Python dhundho
set PYCMD=
py --version >nul 2>&1
if %errorlevel% equ 0 ( set PYCMD=py& goto :go )
python --version >nul 2>&1
if %errorlevel% equ 0 ( set PYCMD=python& goto :go )
python3 --version >nul 2>&1
if %errorlevel% equ 0 ( set PYCMD=python3& goto :go )

:: Python nahi mila — seedha Edge mein kholo
echo  Python nahi mila, Edge mein file khol rahe hain...
echo  (Mic permission baar baar maang sakta hai file:// pe)
start msedge "%~dp0VoiceTranscription.html"
goto :end

:go
echo  Server shuru ho raha hai...
echo.
echo  ==========================================
echo   Browser mein kholein: http://localhost:8080
echo   Mic permission SIRF EK BAAR dena hai!
echo.
echo   Band karne ke liye: is window ko band karein
echo  ==========================================
echo.

:: 2 sec baad browser kholo
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:8080/VoiceTranscription.html"

:: Python ka built-in HTTP server — koi pip install nahi
%PYCMD% -m http.server 8080

:end
pause
