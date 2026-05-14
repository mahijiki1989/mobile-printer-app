# 🎤 Voice AI — Windows 11 Built-in
### Hindi + English | 100% Free | Kuch bhi Install Nahi

---

## ✨ Yeh Kya Hai?

Aapke Windows 11 laptop ke liye ek Voice Assistant — jo **sirf browser aur Python** se chalta hai.

| Kaam | Kaise |
|------|-------|
| 🎤 Aawaz sunega | Browser ka built-in **Web Speech API** |
| 📝 Text likhega | Automatic — real-time screen par |
| 🤖 Jawab dega | Python ka simple AI engine |
| 🔊 Bol ke sunayega | Windows ka built-in **SAPI TTS** |
| 🔒 Data safe | Koi data internet par nahi jata |

> **Koi Ollama nahi, koi model download nahi, koi API key nahi!**

---

## 📋 Sirf Ek Cheez Chahiye

### Python 3.8+ (Python 3.14 ✅ fully supported)
Agar pehle se installed hai → **seedha `start.bat` chalayein!**

Nahi hai toh: 👉 **https://www.python.org/downloads/**

> ⚠️ Install karte waqt **"Add Python to PATH"** ka tick **zaroor** lagayein!

---

## ▶️ Chalane Ka Tarika

```
1.  voice_ai  folder mein jaayein
2.  start.bat  par double-click karein
3.  Browser apne aap khuleg: http://localhost:5050
4.  🎤 Boliye!
```

**Bas itna hi!** (pehli baar 3 packages ~10 seconds mein install honge)

---

## 🎮 Kaise Use Karein

```
Step 1:  🎤 [बोलें] button dabayein
Step 2:  Bolna shuru karein — Hindi ya English
Step 3:  Aapki baat screen par live likhti jayegi
Step 4:  [रोकें] dabayein — baat poori ho gayi
Step 5:  🤖 [AI से पूछें] dabayein — jawab aayega
Step 6:  🔊 [सुनें] dabayein — jawab awaaz mein sunein
```

### ⌨️ Keyboard Shortcuts

| Key | Kaam |
|-----|------|
| `SPACE` | Recording shuru karo / roko |
| `ENTER` | AI se jawab maango |
| `S` | Jawab awaaz mein sunein |

---

## 🤖 AI Kya Kya Kar Sakta Hai?

| Bolo | Jawab milega |
|------|-------------|
| "Namaste" / "नमस्ते" | Good Morning/Evening greeting |
| "Kitne baje hain?" | Abhi ka time |
| "Aaj ki date kya hai?" | Aaj ki date aur din |
| "Koi joke sunao" | Hindi ya English joke |
| "15 times 8 kya hai?" | 120 ✓ |
| "25 plus 37?" | 62 ✓ |
| "Help" | Poori capabilities list |
| "Bye" / "Alvida" | Farewell |

---

## ❓ Problems aur Solutions

### ❌ "Microphone blocked" error
> Browser address bar mein **🔒 lock icon** click karein  
> → **Microphone = Allow** karein → Page refresh karein

### ❌ "Web Speech API supported nahi"
> **Microsoft Edge** ya **Google Chrome** mein kholein  
> Firefox support nahi karta

### ❌ Server start nahi hua
> `voice_ai` **folder ke andar se** `start.bat` chalayein  
> Bahar se chalane par path error aata hai

### ❌ Python nahi mila
> https://www.python.org/downloads/ se install karein  
> **"Add Python to PATH"** tick karna mat bhulen!

### 🔇 Awaaz nahi aa rahi
> Browser mein `http://localhost:5050` kholein  
> (HTTPS nahi, HTTP — localhost pe TLS nahi chahiye)

---

## 📁 Files

```
voice_ai/
├── start.bat          ← ▶ Yahi chalana hai (double-click)
├── voice_server.py    ← Python server (brain)
├── requirements.txt   ← 2 packages ki list
├── README.md          ← Yeh file
└── static/
    ├── index.html     ← Browser UI
    ├── style.css      ← Design
    └── app.js         ← Voice recording + TTS logic
```

---

## 🛠️ Technical

| Part | Technology | Kyu? |
|------|-----------|------|
| Speech-to-Text | `Web Speech API` (browser built-in) | Windows 11 mein pehle se hai |
| AI Response | Python rule-based engine | Koi model nahi, zero install |
| Text-to-Speech | `PowerShell SAPI` (Windows built-in) | Python 3.14 compatible, pyttsx3 nahi |
| Server | `Flask` (Python) | Sirf **2 packages** |

---

*Made for Windows 11 | 100% Free | No Ollama | No Whisper | No API Key*
