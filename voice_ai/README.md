# 🎤 Voice AI — Hindi & English Assistant
### Windows 11 ke liye | 100% Free | Internet ki zaroorat nahi

---

## ✨ Kya karta hai yeh?

| Feature | Detail |
|---------|--------|
| 🎙️ **Aawaz sunega** | Microphone se bolein — Hindi ya English, dono |
| ⏱️ **Lamba sun sakta hai** | Bina kisi time limit ke — jitna chahe bolein |
| 📝 **Text mein likhega** | Jo bola, woh screen par likh dega |
| 🤖 **AI jawab dega** | Local AI (Ollama+LLaMA3) se smart reply |
| 🔊 **Bol bhi sakta hai** | AI ka jawab awaaz mein sun sakte hain |
| 🔒 **Poora offline** | Koi data internet par nahi jata |

---

## 📋 Zaroori Cheezein (Ek Baar)

### 1. Python Install Karein
👉 https://www.python.org/downloads/

> ⚠️ **Zaroori:** Install karte waqt **"Add Python to PATH"** ka checkbox zaroor tick karein!

### 2. Ollama Install Karein (Free AI Engine)
👉 https://ollama.com/download

> Ollama ek free, local AI tool hai. Koi account nahi chahiye.

---

## 🚀 Pehli Baar Setup (Sirf Ek Baar)

1. `voice_ai` folder mein jaayein
2. **`setup.bat`** par double-click karein
3. Wait karein — sab kuch automatic install ho jaayega
4. (~5-10 min lagenge, internet speed pe depend karta hai)

---

## ▶️ Roz Use Karne Ke Liye

1. **`start.bat`** par double-click karein
2. Browser automatically khulega: `http://localhost:5050`
3. **Bas bolein!** 🎤

---

## 🎮 Kaise Use Karein

```
🎤 [बोलें] button dabayein
        ↓
    Bolna shuru karein (Hindi ya English)
        ↓
🛑 [रोकें] button dabayein (recording rukegi)
        ↓
📝 Aapki baat screen par likh jayegi
        ↓
🤖 [AI से पूछें] dabayein — AI jawab dega
        ↓
🔊 [सुनें] dabayein — AI ka jawab awaaz mein sunein
```

### ⌨️ Keyboard Shortcuts
| Key | Kaam |
|-----|------|
| `SPACE` | Recording start / stop |
| `ENTER` | AI se puchein |

---

## 📁 Files Ki Jankari

```
voice_ai/
├── voice_server.py      ← Main Python server (brain)
├── requirements.txt     ← Python packages list
├── setup.bat            ← Pehli baar chalayein
├── start.bat            ← Roz chalayein
└── static/
    ├── index.html       ← UI (browser mein dikhta hai)
    ├── style.css        ← Design / styling
    └── app.js           ← Browser ka logic
```

---

## ❓ Problems & Solutions

### ❌ "Microphone access nahi mila"
> Browser mein `http://localhost:5050` kholein (HTTPS nahi, HTTP).  
> Chrome/Edge mein localhost ke liye microphone automatically allow hota hai.

### ❌ "Ollama se connect nahi ho saka"
> 1. Ollama install hai? → https://ollama.com/download  
> 2. Terminal mein chalayein: `ollama run llama3`  
> 3. Pehli baar 4-5 GB download hoga — wait karein

### ❌ "Python nahi mila" error
> Python install karein: https://www.python.org/downloads/  
> **"Add to PATH"** zaroor tick karein!

### ❌ Server start nahi ho raha
> `voice_ai` folder ke andar se `start.bat` chalayein, bahar se nahi.

### 🐌 "Pehli baar slow hai"
> Bilkul normal hai! Whisper model (~150MB) pehli baar load hone mein  
> 30-60 second lagते hain. Doosri baar se fast hoga.

---

## 🛠️ Technical Details

| Component | Tool | Kyu? |
|-----------|------|------|
| Speech-to-Text | `faster-whisper` (Whisper base model) | Free, offline, Hindi+English support |
| AI Brain | `Ollama + LLaMA3` | Free, local, no data leaves laptop |
| Text-to-Speech | `pyttsx3` (Windows SAPI) | Built-in Windows voices, offline |
| Web Server | `Flask` | Lightweight Python server |
| Frontend | HTML + CSS + JS | Browser mein chalta hai, koi install nahi |

---

## 💡 Tips

- **Saaf jagah mein bolein** — background noise kam ho toh accuracy zyada hogi
- **Lamba bolein** — ek baar mein poora sentence bolein, bich mein ruke nahi
- **Conversation yaad rakhta hai** — AI pichli baatein yaad rakhta hai (10 messages tak)
- **Clear button** — nayi baat shuru karni ho toh 🗑️ Clear dabayein

---

*Made with ❤️ | 100% Free & Local | No data leaves your laptop*
