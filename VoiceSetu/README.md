# VoiceSetu - Offline Voice to Text for Windows

**VoiceSetu** is a fully offline desktop dictation application for Windows 10/11 that converts speech to text in **Hindi** and **English**. All speech recognition happens locally on your machine — no audio data is ever sent to any cloud service or external server.

---

## Privacy Statement

> **100% Offline. No data leaves your computer.**
> VoiceSetu uses local AI models (faster-whisper) running entirely on your CPU.
> There is no cloud API, no login, no subscription, no telemetry.

---

## Features

- **Offline Speech Recognition** — Hindi and English using faster-whisper
- **Global Hotkeys** — Push-to-talk and toggle dictation from any app
- **Text Insertion** — Automatically types/pastes recognized text into focused app
- **Floating Mini Window** — Always-on-top status indicator
- **System Tray** — Runs in background with tray icon
- **History** — Browse, copy, re-insert, edit, delete past transcriptions
- **Export** — Save history to .txt file
- **Dark/Light Theme** — Modern CustomTkinter UI
- **Bilingual UI** — Full Hindi and English interface
- **Multiple Models** — Choose speed vs accuracy (tiny → large)
- **Silence Detection** — Auto-stops recording after silence
- **Microphone Selection** — Choose your preferred input device

---

## System Requirements

- Windows 10/11 (64-bit)
- 4GB+ RAM (8GB recommended for medium/large models)
- Microphone
- ~200MB disk space (base model), up to 2GB for large models
- No internet required after initial model download

---

## Quick Start (For Users)

1. Run the installer: `VoiceSetu_Setup_1.0.0.exe`
2. Launch VoiceSetu from Desktop or Start Menu
3. Wait for the model to load (first launch downloads the base model, requires internet once)
4. Press **Ctrl+Shift+D** to toggle dictation, or **Ctrl+Shift+Space** to push-to-talk
5. Speak into your microphone
6. Text appears in the active application

---

## Build Instructions (For Developers)

### Prerequisites

- Python 3.10 or 3.11 (64-bit) — [python.org](https://www.python.org/downloads/)
- Inno Setup 6 — [jrsoftware.org](https://jrsoftware.org/isdl.php) (for installer)
- Git (optional)

### Step-by-Step Build

```cmd
REM 1. Open Command Prompt in the VoiceSetu project folder

REM 2. Create virtual environment
python -m venv venv

REM 3. Activate virtual environment
venv\Scripts\activate

REM 4. Install dependencies
pip install -r requirements.txt

REM 5. Generate application icon
python generate_icon.py

REM 6. Build the application with PyInstaller
pyinstaller voicesetu.spec --noconfirm --clean

REM 7. Test the built app
dist\VoiceSetu\VoiceSetu.exe

REM 8. Build the installer with Inno Setup
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss

REM 9. Installer output
REM    build\installer\VoiceSetu_Setup_1.0.0.exe
```

### Or use the automated build script:

```cmd
build.bat
```

---

## Model Download

On first launch, VoiceSetu downloads the speech model from Hugging Face (open source). After that, no internet is needed.

Models are cached in: `%APPDATA%\VoiceSetu\models\`

### Model Sizes

| Model | Size | Speed | Accuracy | RAM Usage |
|-------|------|-------|----------|-----------|
| tiny | ~39MB | Fastest | Lower | ~1GB |
| base | ~74MB | Fast | Good | ~1.5GB |
| small | ~244MB | Balanced | Better | ~2.5GB |
| medium | ~769MB | Slower | High | ~4GB |
| large-v2 | ~1.5GB | Slowest | Best | ~6GB |

**Recommended:** `base` for most users. Use `small` if you need better Hindi accuracy.

---

## Hotkeys

| Hotkey | Action |
|--------|--------|
| Ctrl+Shift+D | Toggle dictation (press to start, press again to stop) |
| Ctrl+Shift+Space | Push-to-talk (hold to record, release to process) |

Hotkeys can be customized in Settings → Hotkeys.

---

## Text Insertion Modes

1. **Auto** (default) — Tries clipboard paste first, falls back to simulated typing
2. **Clipboard** — Always uses Ctrl+V paste
3. **Typing** — Simulates keyboard input character by character

The auto mode works with most applications. Use typing mode for apps that block paste.

---

## Why onedir Instead of onefile?

PyInstaller `onedir` mode is used instead of `onefile` because:
- faster-whisper requires native DLLs (CTranslate2) that need to remain as separate files
- `onefile` extracts everything to a temp folder on each launch, causing slow startup
- `onedir` starts instantly and plays well with Inno Setup installer packaging
- The Inno Setup installer bundles the entire directory into a single .exe installer anyway

---

## Project Structure

```
VoiceSetu/
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── voicesetu.spec           # PyInstaller build spec
├── installer.iss            # Inno Setup installer script
├── build.bat                # Automated build script
├── generate_icon.py         # Icon generator utility
├── README.md                # This file
├── assets/
│   ├── icon.ico             # Application icon (generated)
│   └── icon.png             # PNG version
├── locales/
│   ├── en.json              # English UI strings
│   └── hi.json              # Hindi UI strings
└── src/
    ├── __init__.py
    ├── core/
    │   ├── __init__.py
    │   ├── config.py        # Configuration manager
    │   ├── history.py       # Transcription history
    │   ├── hotkeys.py       # Global hotkey manager
    │   ├── localization.py  # Localization system
    │   ├── text_inserter.py # Text insertion into apps
    │   └── tray.py          # System tray integration
    ├── engine/
    │   ├── __init__.py
    │   ├── recorder.py      # Audio recording
    │   └── transcriber.py   # Speech-to-text engine
    └── ui/
        ├── __init__.py
        ├── main_window.py   # Main application window
        ├── mini_window.py   # Floating mini window
        └── settings_window.py # Settings dialog
```

---

## Configuration

Settings are stored in: `%APPDATA%\VoiceSetu\config.json`

History is stored in: `%APPDATA%\VoiceSetu\history.json`

Logs are stored in: `%APPDATA%\VoiceSetu\logs\voicesetu.log`

---

## Troubleshooting

### "Model not loading"
- Ensure you have internet for the first model download
- Check `%APPDATA%\VoiceSetu\logs\voicesetu.log` for errors
- Try a smaller model (tiny) in Settings → Models
- Ensure at least 2GB free RAM

### "No microphone detected"
- Check Windows Sound Settings → Input devices
- Ensure microphone permissions are granted
- Try selecting a specific mic in Settings → Audio

### "Text not inserting into my app"
- Try switching insertion mode in Settings → General
- Some apps (like games) may block simulated input
- Use "Clipboard Paste" mode and manually Ctrl+V

### "Hotkeys not working"
- Run VoiceSetu as Administrator for global hotkeys
- Check if another app is using the same hotkey combination
- Change hotkeys in Settings → Hotkeys

### "Hindi transcription is inaccurate"
- Use the `small` or `medium` model for better Hindi accuracy
- Speak clearly and at a normal pace
- Ensure minimal background noise

### Build errors
- Use Python 3.10 or 3.11 (not 3.12+ due to ctranslate2 compatibility)
- Ensure Visual C++ Redistributable is installed
- Run `pip install --upgrade pip` before installing requirements

---

## Known Limitations

1. First launch requires internet to download the speech model (~74MB for base)
2. Large models require significant RAM (4-6GB)
3. Hindi accuracy depends on model size — use `small` or larger for production Hindi use
4. Some full-screen applications may not accept simulated input
5. Push-to-talk hotkey release detection may be slightly delayed in some scenarios
6. No GPU acceleration on the default build (uses CPU with int8 quantization for speed)

---

## License

This project is provided as-is for personal and educational use.
All speech processing is done locally. No third-party services are used.

---

## Final Requirement Checklist

| Requirement | Status |
|-------------|--------|
| No paid API | ✅ Uses open-source faster-whisper |
| No cloud API | ✅ All processing local |
| No login | ✅ No authentication required |
| No subscription | ✅ Free forever |
| No telemetry | ✅ No data sent anywhere |
| Works offline | ✅ After initial model download |
| Hindi support | ✅ Full Hindi transcription |
| English support | ✅ Full English transcription |
| Buildable app.exe | ✅ PyInstaller onedir |
| Buildable installer.exe | ✅ Inno Setup |
| Global push-to-talk | ✅ Ctrl+Shift+Space |
| Toggle hotkey | ✅ Ctrl+Shift+D |
| Hindi UI | ✅ Full localization |
| English UI | ✅ Full localization |
| Floating mini window | ✅ Draggable, always-on-top |
| Settings window | ✅ Tabbed interface |
| Dark/Light mode | ✅ CustomTkinter themes |
| Microphone selector | ✅ In settings |
| Model selector | ✅ tiny/base/small/medium/large |
| Status indicator | ✅ Idle/Listening/Processing/Inserted |
| History | ✅ With copy/reinsert/edit/delete |
| Export history | ✅ To .txt file |
| Text insertion | ✅ Paste + Typing + Fallback |
| Clipboard preservation | ✅ Configurable |
| Silence detection | ✅ Configurable threshold |
| System tray | ✅ With context menu |
| Privacy | ✅ Stated in UI and README |
