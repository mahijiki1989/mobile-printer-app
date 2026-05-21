# ============================================
# VoiceSetu - COMPLETE Auto Builder v2
# 
# INSTRUCTIONS:
# 1. Windows Security mein VoiceSetu folder exclude karo
# 2. PowerShell (Admin) kholo
# 3. Yeh run karo:
#    Set-ExecutionPolicy Bypass -Scope Process -Force
#    cd "E:\mobile-printer-app-feat-voicesetu-desktop-app\VoiceSetu"
#    .\AUTO_BUILD.ps1
# ============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  VoiceSetu Auto Builder v2" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
$ErrorActionPreference = "Continue"
$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectDir

Write-Host "[INFO] Folder: $projectDir" -ForegroundColor Gray
Write-Host ""

# ---- Check Windows Defender exclusion reminder ----
Write-Host "[IMPORTANT] Kya tumne Windows Defender mein folder exclude kiya?" -ForegroundColor Red
Write-Host "  Agar nahi kiya toh build fail hoga!" -ForegroundColor Red
Write-Host "  Windows Security > Virus Protection > Manage Settings > Exclusions" -ForegroundColor Yellow
Write-Host "  Add Folder: $projectDir" -ForegroundColor Yellow
Write-Host ""
$confirm = Read-Host "Exclusion add kar liya? (y/n)"
if ($confirm -ne "y") {
    Write-Host ""
    Write-Host "Pehle Windows Defender mein exclusion add karo, phir script run karo." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 0
}

# ---- STEP 1: Find Python ----
Write-Host ""
Write-Host "[1/7] Python dhundh rahe hain..." -ForegroundColor Yellow

$pythonCmd = $null
foreach ($p in @("python", "py")) {
    try {
        $result = & $p --version 2>&1
        if ($result -match "Python 3\.\d+") {
            $pythonCmd = $p
            Write-Host "  Found: $result" -ForegroundColor Green
            break
        }
    } catch {}
}

if (-not $pythonCmd) {
    Write-Host "  ERROR: Python nahi mila!" -ForegroundColor Red
    Write-Host "  Download karo: https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe" -ForegroundColor Yellow
    Write-Host "  Install mein 'Add to PATH' tick karo!" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# ---- STEP 2: Create venv ----
Write-Host ""
Write-Host "[2/7] Virtual environment..." -ForegroundColor Yellow

if (Test-Path "venv") {
    Write-Host "  Purana venv delete kar rahe hain..." -ForegroundColor Gray
    Remove-Item -Recurse -Force venv
}

& $pythonCmd -m venv venv
$venvPython = Join-Path $projectDir "venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "  ERROR: Venv nahi bana!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "  Venv ready." -ForegroundColor Green

# ---- STEP 3: Install packages ----
Write-Host ""
Write-Host "[3/7] Packages install ho rahe hain (5-10 min)..." -ForegroundColor Yellow
Write-Host "  Internet connected hona chahiye..." -ForegroundColor Gray

& $venvPython -m pip install --upgrade pip --quiet 2>&1 | Out-Null

$packages = @(
    "customtkinter==5.2.1",
    "faster-whisper==1.0.3",
    "sounddevice==0.4.7",
    "numpy==1.26.4",
    "keyboard==0.13.5",
    "pyperclip==1.8.2",
    "pystray==0.19.5",
    "Pillow==10.4.0",
    "pyinstaller==6.6.0"
)

foreach ($pkg in $packages) {
    Write-Host "  Installing: $pkg" -ForegroundColor Gray
    & $venvPython -m pip install $pkg --quiet 2>&1 | Out-Null
}

Write-Host "  Sab packages install ho gaye!" -ForegroundColor Green

# ---- STEP 4: Generate Icon ----
Write-Host ""
Write-Host "[4/7] Icon generate kar rahe hain..." -ForegroundColor Yellow

& $venvPython generate_icon.py 2>&1 | Out-Null

if (Test-Path "assets\icon.ico") {
    Write-Host "  Icon ready: assets\icon.ico" -ForegroundColor Green
} else {
    Write-Host "  Icon skip (problem nahi hai)" -ForegroundColor Yellow
}

# ---- STEP 5: Clean old build ----
Write-Host ""
Write-Host "[5/7] Purani build files clean kar rahe hain..." -ForegroundColor Yellow

if (Test-Path "dist") { Remove-Item -Recurse -Force dist }
if (Test-Path "build") { Remove-Item -Recurse -Force build }
Write-Host "  Clean done." -ForegroundColor Green

# ---- STEP 6: Build EXE ----
Write-Host ""
Write-Host "[6/7] App build ho rahi hai (2-5 min wait karo)..." -ForegroundColor Yellow
Write-Host "  PyInstaller kaam kar raha hai..." -ForegroundColor Gray

$pyinstaller = Join-Path $projectDir "venv\Scripts\pyinstaller.exe"

# Build WITHOUT icon to avoid Windows Defender issue
& $pyinstaller --noconfirm --clean --name "VoiceSetu" --windowed --noupx `
    --add-data "locales;locales" `
    --add-data "assets;assets" `
    --hidden-import "faster_whisper" `
    --hidden-import "ctranslate2" `
    --hidden-import "huggingface_hub" `
    --hidden-import "tokenizers" `
    --hidden-import "sounddevice" `
    --hidden-import "numpy" `
    --hidden-import "keyboard" `
    --hidden-import "pyperclip" `
    --hidden-import "pystray" `
    --hidden-import "PIL" `
    --hidden-import "PIL.Image" `
    --hidden-import "PIL.ImageDraw" `
    --hidden-import "customtkinter" `
    --hidden-import "pkg_resources.extern" `
    --exclude-module "matplotlib" `
    --exclude-module "scipy" `
    --exclude-module "pandas" `
    --exclude-module "pytest" `
    main.py 2>&1 | ForEach-Object {
        if ($_ -match "error|Error|ERROR|failed|Failed") {
            Write-Host "  $_" -ForegroundColor Red
        }
    }

$exePath = Join-Path $projectDir "dist\VoiceSetu\VoiceSetu.exe"
if (Test-Path $exePath) {
    Write-Host ""
    Write-Host "  ============================================" -ForegroundColor Green
    Write-Host "  BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "  ============================================" -ForegroundColor Green
    Write-Host "  EXE: $exePath" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "  BUILD FAIL!" -ForegroundColor Red
    Write-Host "  Neeche error check karo." -ForegroundColor Red
    Write-Host ""
    Write-Host "  Manual try karo:" -ForegroundColor Yellow
    Write-Host "  venv\Scripts\pyinstaller.exe --noconfirm --name VoiceSetu --windowed --noupx --add-data `"locales;locales`" --add-data `"assets;assets`" main.py" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# ---- STEP 7: Done ----
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  DONE! App ready hai!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  App kahan hai:" -ForegroundColor Cyan
Write-Host "  $exePath" -ForegroundColor White
Write-Host ""
Write-Host "  Double-click karke chalao!" -ForegroundColor Cyan
Write-Host ""
Write-Host "  FIRST RUN: Speech model download hoga (~74MB)" -ForegroundColor Yellow
Write-Host "  Uske baad OFFLINE kaam karega!" -ForegroundColor Yellow
Write-Host ""

# Open folder
Start-Process explorer.exe (Join-Path $projectDir "dist\VoiceSetu")

Read-Host "Press Enter to exit"
