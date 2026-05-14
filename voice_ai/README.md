# 🎤 Voice Transcription App — Windows 11

**Boliye aur text aa jaayega — koi browser nahi, koi server nahi**

---

## ⚡ Ek Baar mein Samajh Lo

```
build.bat  →  VoiceTranscription.exe  →  Desktop pe rakh do  →  Double-click  →  Boliye!
```

---

## 📥 Step 1 — ZIP Download Karein

**👉 https://github.com/mahijiki1989/mobile-printer-app/archive/refs/heads/feature/voice-ai.zip**

Extract karo → `voice_ai` folder kholein

---

## 🔨 Step 2 — EXE Banayein (Sirf Ek Baar)

**`build.bat`** pe double-click karein

```
[1/4] Python check...       ✓
[2/4] Packages install...   ✓  (2-3 min)
[3/4] EXE build...          ✓  (3-5 min)
[4/4] EXE copy...           ✓

BUILD SUCCESSFUL!
VoiceTranscription.exe ready hai!
```

> ⚠️ Agar PyAudio install fail ho, terminal mein chalayein:
> ```
> pip install pipwin
> pipwin install pyaudio
> ```
> Phir `build.bat` dobara chalayein.

---

## ▶️ Step 3 — Use Karein (Roz)

1. **`VoiceTranscription.exe`** Desktop pe rakho
2. Double-click karke kholein
3. **🎤 बोलें** button dabayein (ya `Space`)
4. Bolte rahein — **jitna chahein, jitni der**
5. Rukne ke baad **⏹ रोकें** dabayein
6. **📋 Copy All** se copy karein

---

## 🖥️ App Kaisi Dikhti Hai

```
┌─────────────────────────────────────────────┐
│ 🎙️  Voice Transcription   Windows 11 • Free │
│ ● Mic ready — बोलें button dabayein         │
│ LIVE [यहाँ real-time text दिखेगा...]        │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │                                      │   │
│  │  Aapki poori baat yahan              │   │
│  │  likhti jaayegi...                   │   │
│  │                                      │   │
│  └──────────────────────────────────────┘   │
│  42 words  •  236 characters                │
│                                              │
│  0:00  🗑 Clear  📋 Copy All    🎤 बोलें   │
└─────────────────────────────────────────────┘
```

---

## ⌨️ Shortcuts

| Key | Kaam |
|-----|------|
| `Space` | Bolna shuru / rokna |
| `Ctrl+C` | Copy all text |
| `Ctrl+L` | Clear |

---

## ❓ Problems

### ❌ PyAudio install nahi hua
```
pip install pipwin
pipwin install pyaudio
```

### ❌ "Microphone nahi mila"
- Mic connected hai? Device Manager mein check karein
- Dusra mic try karein

### ❌ "Internet connection nahi"
- Google Speech API ke liye internet chahiye
- WiFi/data on karein

### 🐌 Pehli baar slow open hota hai
- Normal hai — antivirus scan karta hai `.exe` ko pehli baar
- Ek baar open hone ke baad fast hoga

### ❌ Windows ne "Unknown Publisher" warning diya
- "More info" click karein → "Run anyway"
- Yeh normal hai unsigned `.exe` ke liye

---

## 📁 Files

```
voice_ai/
├── voice_app.py          ← Main source code
├── build.bat             ← EXE banane ke liye (ek baar)
├── VoiceTranscription.exe← Taiyaar EXE (build ke baad)
└── README.md             ← Yeh file
```

---

*100% Free • Windows 11 • Google Speech API (internet needed) • Hindi + English*
