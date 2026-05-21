# ============================================
# VoiceSetu - One Click Auto Builder
# Just right-click this file -> "Run with PowerShell"
# OR open PowerShell and run: .\AUTO_BUILD.ps1
# ============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  VoiceSetu Auto Builder" -ForegroundColor Cyan
Write-Host "  Yeh script sab kuch automatic karega" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set execution policy for this session
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

$ErrorActionPreference = "Stop"
$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Set-Location $projectDir
Write-Host "[INFO] Working directory: $projectDir" -ForegroundColor Gray

# ---- STEP 1: Check Python ----
Write-Host ""
Write-Host "[1/8] Python check kar rahe hain..." -ForegroundColor Yellow

$pythonCmd = $null
$pythonPaths = @("python", "python3", "py -3.11", "py -3.10", "py")

foreach ($p in $pythonPaths) {
    try {
        $ver = & $p.Split(" ")[0] $p.Split(" ")[1..99] --version 2>&1
        if ($ver -match "Python 3\.(1[0-1])") {
            $pythonCmd = $p
            Write-Host "  Python found: $ver" -ForegroundColor Green
            break
        }
    } catch {}
}

if (-not $pythonCmd) {
    # Try to find python in common locations
    $commonPaths = @(
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
        "C:\Python311\python.exe",
        "C:\Python310\python.exe"
    )
    foreach ($cp in $commonPaths) {
        if (Test-Path $cp) {
            $pythonCmd = $cp
            Write-Host "  Python found at: $cp" -ForegroundColor Green
            break
        }
    }
}

if (-not $pythonCmd) {
    Write-Host ""
    Write-Host "  ERROR: Python 3.10 or 3.11 nahi mila!" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Python download karo: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "  Install karte waqt 'Add Python to PATH' checkbox tick karo!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Python install karne ke baad yeh script dobara run karo." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# ---- STEP 2: Create venv ----
Write-Host ""
Write-Host "[2/8] Virtual environment bana rahe hain..." -ForegroundColor Yellow

if (-not (Test-Path "venv")) {
    & $pythonCmd.Split(" ")[0] $pythonCmd.Split(" ")[1..99] -m venv venv
    Write-Host "  Venv created." -ForegroundColor Green
} else {
    Write-Host "  Venv already exists." -ForegroundColor Green
}

# ---- STEP 3: Activate venv ----
Write-Host ""
Write-Host "[3/8] Venv activate kar rahe hain..." -ForegroundColor Yellow

$venvPython = Join-Path $projectDir "venv\Scripts\python.exe"
$venvPip = Join-Path $projectDir "venv\Scripts\pip.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "  ERROR: Venv Python not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "  Activated: $venvPython" -ForegroundColor Green

# ---- STEP 4: Install dependencies ----
Write-Host ""
Write-Host "[4/8] Dependencies install kar rahe hain (5-10 min lag sakta hai)..." -ForegroundColor Yellow

& $venvPip install --upgrade pip 2>&1 | Out-Null
& $venvPip install -r requirements.txt 2>&1 | ForEach-Object {
    if ($_ -match "Successfully installed") {
        Write-Host "  $_" -ForegroundColor Green
    }
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "  Retrying with individual packages..." -ForegroundColor Yellow
    $packages = @(
        "customtkinter==5.2.1",
        "faster-whisper==1.0.3",
        "sounddevice==0.4.7",
        "numpy==1.26.4",
        "keyboard==0.13.5",
        "pyperclip==1.8.2",
        "pystray==0.19.5",
        "Pillow==10.4.0",
        "PyInstaller==6.6.0"
    )
    foreach ($pkg in $packages) {
        Write-Host "  Installing $pkg..." -ForegroundColor Gray
        & $venvPip install $pkg 2>&1 | Out-Null
    }
}

Write-Host "  Dependencies installed!" -ForegroundColor Green

# ---- STEP 5: Generate icon ----
Write-Host ""
Write-Host "[5/8] App icon generate kar rahe hain..." -ForegroundColor Yellow

& $venvPython generate_icon.py 2>&1 | Out-Null

if (Test-Path "assets\icon.ico") {
    Write-Host "  Icon generated: assets\icon.ico" -ForegroundColor Green
} else {
    Write-Host "  Icon generation skipped (non-critical)" -ForegroundColor Yellow
}

# ---- STEP 6: Build with PyInstaller ----
Write-Host ""
Write-Host "[6/8] PyInstaller se app build kar rahe hain (2-5 min)..." -ForegroundColor Yellow

$pyinstaller = Join-Path $projectDir "venv\Scripts\pyinstaller.exe"

& $pyinstaller voicesetu.spec --noconfirm --clean 2>&1 | ForEach-Object {
    if ($_ -match "Building") {
        Write-Host "  $_" -ForegroundColor Gray
    }
}

$exePath = Join-Path $projectDir "dist\VoiceSetu\VoiceSetu.exe"
if (Test-Path $exePath) {
    Write-Host "  BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "  App: $exePath" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Build failed! Check errors above." -ForegroundColor Red
    Write-Host "  Log check karo: build\VoiceSetu\warn-VoiceSetu.txt" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# ---- STEP 7: Build installer (if Inno Setup available) ----
Write-Host ""
Write-Host "[7/8] Installer build kar rahe hain..." -ForegroundColor Yellow

$isccPaths = @(
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    "C:\Program Files\Inno Setup 6\ISCC.exe",
    "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe"
)

$iscc = $null
foreach ($path in $isccPaths) {
    if (Test-Path $path) {
        $iscc = $path
        break
    }
}

$installerPath = $null
if ($iscc) {
    if (-not (Test-Path "build\installer")) {
        New-Item -ItemType Directory -Path "build\installer" -Force | Out-Null
    }
    & $iscc installer.iss 2>&1 | Out-Null
    $installerPath = Join-Path $projectDir "build\installer\VoiceSetu_Setup_1.0.0.exe"
    if (Test-Path $installerPath) {
        Write-Host "  Installer created: $installerPath" -ForegroundColor Green
    } else {
        Write-Host "  Installer build failed (non-critical)" -ForegroundColor Yellow
    }
} else {
    Write-Host "  Inno Setup nahi mila. Installer skip." -ForegroundColor Yellow
    Write-Host "  Download: https://jrsoftware.org/isdl.php" -ForegroundColor Gray
    Write-Host "  Install karke script dobara run karo for installer." -ForegroundColor Gray
}

# ---- STEP 8: Done! ----
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  BUILD COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  App EXE: dist\VoiceSetu\VoiceSetu.exe" -ForegroundColor White

if ($installerPath -and (Test-Path $installerPath)) {
    Write-Host "  Installer: build\installer\VoiceSetu_Setup_1.0.0.exe" -ForegroundColor White
}

Write-Host ""
Write-Host "  App chalane ke liye:" -ForegroundColor Cyan
Write-Host "    dist\VoiceSetu\VoiceSetu.exe double-click karo" -ForegroundColor White
Write-Host ""
Write-Host "  NOTE: Pehli baar speech model download hoga (~74MB)" -ForegroundColor Yellow
Write-Host "        Uske baad 100% offline kaam karega!" -ForegroundColor Yellow
Write-Host ""

# Open the dist folder
Start-Process explorer.exe "dist\VoiceSetu"

Read-Host "Press Enter to exit"
