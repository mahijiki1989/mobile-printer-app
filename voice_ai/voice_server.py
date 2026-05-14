"""
Voice AI Server — voice_server.py
Windows 11 Built-in Only — Python 3.14 Compatible

Kya karta hai:
  /          → index.html serve karta hai (browser UI)
  /ask       → AI jaisi smart responses deta hai (pure Python)
  /speak     → Windows PowerShell SAPI TTS (pyttsx3 ki zaroorat nahi!)
  /status    → health check

Zaroorat:  Python 3.14  +  flask  +  flask-cors
           (sirf 2 packages! — TTS Windows PowerShell se hoga)
"""

import os
import re
import subprocess
import threading
import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# ── App ───────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=os.path.join(BASE_DIR, "static"))
CORS(app)

# ── TTS via Windows PowerShell SAPI — pyttsx3 ki zaroorat nahi ───────────────
_tts_lock    = threading.Lock()
_tts_process = None   # current speaking process

def speak_via_powershell(text: str):
    """
    Windows built-in SAPI TTS using PowerShell.
    Python 3.14 ke saath 100% compatible.
    Koi extra package nahi chahiye.
    """
    global _tts_process
    # Pehle chalu awaaz band karo
    with _tts_lock:
        if _tts_process and _tts_process.poll() is None:
            _tts_process.terminate()

    # Special characters escape karo PowerShell ke liye
    safe_text = text.replace("'", "\\'").replace('"', '\\"').replace("`", "``")

    ps_script = (
        "Add-Type -AssemblyName System.Speech; "
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "$s.Rate = -1; "          # -10 (slow) to 10 (fast), -1 = thoda slow
        "$s.Volume = 100; "
        f"$s.Speak('{safe_text}');"
    )

    with _tts_lock:
        _tts_process = subprocess.Popen(
            ["powershell", "-WindowStyle", "Hidden", "-Command", ps_script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
        )

def stop_speaking():
    """Chalu TTS band karo."""
    global _tts_process
    with _tts_lock:
        if _tts_process and _tts_process.poll() is None:
            _tts_process.terminate()
            _tts_process = None

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)


@app.route("/ask", methods=["POST"])
def ask():
    """
    Simple rule-based AI responses — Windows built-in Python only.
    No model, no API key, no internet needed for this part.
    Browser ka Web Speech API speech-to-text handle karta hai,
    yeh sirf text response deta hai.
    """
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    history = data.get("history") or []

    if not text:
        return jsonify({"response": "Kuch bola nahi gaya.", "success": False})

    response = generate_response(text, history)
    return jsonify({"response": response, "success": True})


@app.route("/speak", methods=["POST"])
def speak():
    """
    Windows PowerShell SAPI TTS — pyttsx3 ki zaroorat nahi.
    Python 3.14 ke saath 100% kaam karta hai.
    Laptop ke speakers par seedha bolega.
    """
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"success": True})

    threading.Thread(
        target=speak_via_powershell,
        args=(text,),
        daemon=True
    ).start()
    return jsonify({"success": True})


@app.route("/speak/stop", methods=["POST"])
def speak_stop():
    """Chalu TTS band karo."""
    stop_speaking()
    return jsonify({"success": True})


@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "server": "running",
        "python": "3.14+",
        "tts": "windows-powershell-sapi",
        "stt": "web-speech-api",
        "packages_needed": ["flask", "flask-cors"]
    })


# ── Response Generator (Pure Python — No Model) ───────────────────────────────

# Simple knowledge base — expandable
GREETINGS = {"नमस्ते", "hello", "hi", "hey", "helo", "namaste", "namaskar",
             "namasté", "नमस्कार", "हैलो", "हाय"}

TIME_WORDS = {"time", "समय", "baje", "kitne baje", "कितने बजे", "what time"}
DATE_WORDS = {"date", "तारीख", "aaj", "आज", "today", "din", "दिन", "kya din"}

WEATHER_WORDS = {"weather", "mausam", "मौसम", "garmi", "गर्मी", "sardi", "सर्दी"}

THANKS_WORDS = {"thanks", "thank you", "shukriya", "शुक्रिया", "dhanyavaad",
                "धन्यवाद", "thx", "ty"}

BYE_WORDS = {"bye", "goodbye", "alvida", "अलविदा", "baad mein milte hain",
             "ok bye", "band karo"}

HELP_WORDS = {"help", "madad", "मदद", "kya kar sakte", "क्या कर सकते",
              "kya karte", "commands"}

JOKES_WORDS = {"joke", "mazak", "मज़ाक", "hasao", "hasana", "funny", "comedy"}

JOKES_HI = [
    "एक आदमी doctor के पास गया।\nDoctor: क्या हुआ?\nआदमी: मुझे लगता है मैं अदृश्य हूँ।\nDoctor: अगला patient आ जाए! 😂",
    "Teacher: बताओ पानी कहाँ से आता है?\nStudent: नल से!\nTeacher: नल से पहले?\nStudent: टंकी से!\nTeacher: (सिर पकड़ लेते हैं) 😄",
    "मेरी memory इतनी कमज़ोर है...\nकि मैंने कल gym join किया\nआज याद ही नहीं रहा! 💪😂",
]

JOKES_EN = [
    "Why don't scientists trust atoms?\nBecause they make up everything! 😂",
    "I told my computer I needed a break.\nNow it won't stop sending me Kit-Kat ads. 😄",
    "Why did the programmer quit his job?\nBecause he didn't get arrays (a raise)! 😂",
]

_joke_idx_hi = 0
_joke_idx_en = 0

CAPABILITIES = """मैं यह कर सकता हूँ:
• 🕐 **समय और तारीख** बताना
• 😄 **Jokes** सुनाना  
• 💬 **हिंदी और English** में बात करना
• 🔢 **गणित** के सवाल हल करना
• 📝 **आपकी बात** repeat करना
• 🔊 **जवाब बोलकर** सुनाना

बस बोलिए — मैं हाज़िर हूँ! 😊"""

MATH_PATTERN = re.compile(
    r'(\d+\.?\d*)\s*([\+\-\×\*\/÷x]|plus|minus|times|divided by|गुणा|जमा|घटा|भाग)\s*(\d+\.?\d*)',
    re.IGNORECASE
)


def generate_response(text: str, history: list) -> str:
    """Rule-based response engine — expandable, no model needed."""
    global _joke_idx_hi, _joke_idx_en

    t_lower = text.lower().strip()
    words   = set(re.split(r'[\s,।?!।]+', t_lower))

    # ── Greeting ──────────────────────────────────────────────────────────────
    if words & GREETINGS:
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            greeting = "सुप्रभात! Good Morning! ☀️"
        elif 12 <= hour < 17:
            greeting = "नमस्ते! Good Afternoon! 🌤️"
        elif 17 <= hour < 21:
            greeting = "शुभ संध्या! Good Evening! 🌇"
        else:
            greeting = "नमस्ते! Good Night! 🌙"
        return f"{greeting}\n\nमैं आपका Voice AI हूँ। आप मुझसे कुछ भी पूछ सकते हैं!\nHelp के लिए 'help' बोलें।"

    # ── Time ──────────────────────────────────────────────────────────────────
    if any(w in t_lower for w in TIME_WORDS):
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"अभी समय है: **{time_str}** 🕐\n({now.strftime('%H:%M')} बजे)"

    # ── Date ──────────────────────────────────────────────────────────────────
    if any(w in t_lower for w in DATE_WORDS):
        now = datetime.datetime.now()
        days_hi = ["सोमवार","मंगलवार","बुधवार","गुरुवार","शुक्रवार","शनिवार","रविवार"]
        months_hi = ["जनवरी","फ़रवरी","मार्च","अप्रैल","मई","जून",
                     "जुलाई","अगस्त","सितंबर","अक्टूबर","नवंबर","दिसंबर"]
        day_name  = days_hi[now.weekday()]
        month_name= months_hi[now.month - 1]
        return (
            f"आज की तारीख: **{now.day} {month_name} {now.year}**\n"
            f"दिन: {day_name} ({now.strftime('%A')})"
        )

    # ── Weather ───────────────────────────────────────────────────────────────
    if any(w in t_lower for w in WEATHER_WORDS):
        return (
            "मुझे internet access नहीं है, इसलिए live मौसम नहीं बता सकता। 🌤️\n\n"
            "मौसम के लिए:\n"
            "• Edge में **weather.com** खोलें\n"
            "• या Windows taskbar में weather widget देखें"
        )

    # ── Thanks ────────────────────────────────────────────────────────────────
    if words & THANKS_WORDS:
        return "आपका स्वागत है! 😊\nकोई भी काम हो, बस बोलिए।"

    # ── Bye ───────────────────────────────────────────────────────────────────
    if words & BYE_WORDS:
        return "अलविदा! फिर मिलेंगे। 👋\nखिड़की बंद कर सकते हैं।"

    # ── Help ──────────────────────────────────────────────────────────────────
    if words & HELP_WORDS:
        return CAPABILITIES

    # ── Jokes ─────────────────────────────────────────────────────────────────
    if words & JOKES_WORDS:
        # Detect language from text
        hindi_chars = sum(1 for c in text if '\u0900' <= c <= '\u097f')
        if hindi_chars > 2:
            joke = JOKES_HI[_joke_idx_hi % len(JOKES_HI)]
            _joke_idx_hi += 1
        else:
            joke = JOKES_EN[_joke_idx_en % len(JOKES_EN)]
            _joke_idx_en += 1
        return joke

    # ── Math ──────────────────────────────────────────────────────────────────
    match = MATH_PATTERN.search(t_lower)
    if match:
        try:
            a   = float(match.group(1))
            op  = match.group(2).strip().lower()
            b   = float(match.group(3))
            op_map = {
                '+': a + b, 'plus': a + b, 'जमा': a + b,
                '-': a - b, 'minus': a - b, 'घटा': a - b,
                '*': a * b, '×': a * b, 'x': a * b, 'times': a * b, 'गुणा': a * b,
                '/': None,  '÷': None, 'divided by': None, 'भाग': None,
            }
            if op in ('/', '÷', 'divided by', 'भाग'):
                if b == 0:
                    return "शून्य से भाग नहीं होता! 😅"
                result = a / b
            else:
                result = op_map.get(op)
                if result is None:
                    return "यह operator समझ नहीं आया।"

            # Clean output: remove trailing .0 if integer
            result_str = str(int(result)) if result == int(result) else f"{result:.4f}".rstrip('0').rstrip('.')
            return f"{match.group(1)} {match.group(2)} {match.group(3)} = **{result_str}** 🔢"
        except Exception:
            pass

    # ── Name questions ────────────────────────────────────────────────────────
    if any(w in t_lower for w in ["naam", "name", "नाम", "kaun", "कौन", "who are you", "tum kaun"]):
        return "मेरा नाम **Voice AI** है। 🤖\nमैं आपका Windows 11 built-in assistant हूँ।\nकोई install नहीं — सब browser में ही चलता है!"

    # ── How are you ───────────────────────────────────────────────────────────
    if any(w in t_lower for w in ["kaisa", "kaisi", "कैसे", "how are you", "theek", "ठीक"]):
        return "मैं बिल्कुल ठीक हूँ, शुक्रिया! 😊\nआप कैसे हैं? कुछ पूछना हो तो बोलिए।"

    # ── Repeat / echo ─────────────────────────────────────────────────────────
    if any(w in t_lower for w in ["repeat", "dobara", "दोबारा", "phir", "फिर बोलो"]):
        # Find last user message from history
        for msg in reversed(history):
            if msg.get("role") == "user":
                return f"आपने कहा था:\n\"{msg['content']}\""
        return "आपने अभी तक कुछ नहीं कहा। पहले कुछ बोलिए!"

    # ── Fallback — Echo + hint ────────────────────────────────────────────────
    hindi_chars = sum(1 for c in text if '\u0900' <= c <= '\u097f')
    if hindi_chars > 3:
        return (
            f"आपने कहा: \"{text}\"\n\n"
            "मैं अभी सीमित हूँ — बड़ा AI (जैसे ChatGPT) नहीं हूँ।\n"
            "लेकिन मैं यह कर सकता हूँ:\n"
            "• समय/तारीख बताना\n"
            "• Jokes सुनाना\n"
            "• Maths हल करना\n"
            "'Help' बोलें — पूरी list देखें!"
        )
    else:
        return (
            f"You said: \"{text}\"\n\n"
            "I'm a simple built-in assistant (no big AI model).\n"
            "I can: tell time/date, crack jokes, solve math.\n"
            "Say 'help' to see what I can do!"
        )


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = 5050
    print("=" * 54)
    print("  🎤  Voice AI Server — Windows 11 Built-in")
    print("=" * 54)
    print(f"  🌐  Browser mein kholein:  http://localhost:{port}")
    print("  🛑  Band karne ke liye:    Ctrl + C")
    print("=" * 54)
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
