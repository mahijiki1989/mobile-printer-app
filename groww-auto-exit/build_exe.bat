@echo off
REM ============================================================
REM  Groww Auto-Exit  -  build a standalone Windows .exe
REM ============================================================
REM  Run this AFTER install.bat. Output goes to dist\GrowwAutoExit\
REM ============================================================

setlocal

if not exist .venv\Scripts\python.exe (
    echo [ERROR] .venv not found. Run install.bat first.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
python build_windows.py
if errorlevel 1 (
    echo.
    echo Build failed. See errors above.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Build complete!
echo ============================================================
echo.
echo Your exe is at: dist\GrowwAutoExit\GrowwAutoExit.exe
echo Distribute the entire dist\GrowwAutoExit\ folder.
echo.
pause
