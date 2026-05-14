@echo off
cd /d "%~dp0"
start "" msedge "%~dp0VoiceTranscription.html"
if %errorlevel% neq 0 start "" "%~dp0VoiceTranscription.html"
