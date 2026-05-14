"""
Voice AI Server - Windows 11
Hindi + English speech recognition with AI responses
100% Free & Local
"""

import os
import io
import json
import threading
import tempfile
import subprocess
import time

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# ── App Setup ─────────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder="static")
CORS(app)

# ── Global: Whisper model (lazy load) ────────────────────────────────────────
_whisper_model = None
_model_lock = threading.Lock()

def get_whisper_model():
    """Load Whisper model once, reuse every time."""
    global _whisper_model
    with _model_lock:
        if _whisper_model is None:
            print("[Voice AI] Loading Whisper model (first time, please wait)...")
            from faster_whisper import WhisperModel
            # 'base' is fast & good for Hindi+English; change to 'small' for better accuracy
            _whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
            print("[Voice AI] Whisper model loaded ✓")
    return _whisper_model


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/transcribe", methods=["POST"])
def transcribe():
    """
    Accepts audio file (WAV/WebM/MP3) from browser,
    runs Whisper STT, returns transcript.
    """
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]

    # Save to temp file
    suffix = ".webm"
    if audio_file.filename:
        ext = os.path.splitext(audio_file.filename)[-1].lower()
        if ext in [".wav", ".mp3", ".ogg", ".m4a", ".webm"]:
            suffix = ext

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        audio_file.save(tmp.name)
        tmp_path = tmp.name

    try:
        model = get_whisper_model()
        # language=None → auto-detect Hindi or English
        segments, info = model.transcribe(
            tmp_path,
            language=None,          # auto-detect
            task="transcribe",      # keep original language (not translate)
            beam_size=5,
            vad_filter=True,        # remove silence automatically
            vad_parameters=dict(min_silence_duration_ms=500),
        )

        transcript = " ".join(seg.text.strip() for seg in segments)
        detected_lang = info.language

        return jsonify({
            "transcript": transcript,
            "language": detected_lang,
            "success": True
        })

    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


@app.route("/ask", methods=["POST"])
def ask_ai():
    """
    Send transcript text to Ollama (local LLM) and get AI response.
    Falls back to a helpful message if Ollama is not running.
    """
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    user_text = data["text"].strip()
    conversation_history = data.get("history", [])

    try:
        response_text = call_ollama(user_text, conversation_history)
        return jsonify({
            "response": response_text,
            "success": True
        })
    except Exception as e:
        return jsonify({
            "response": f"Ollama se connect nahi ho saka. Error: {str(e)}\n\nOllama install karein: https://ollama.com  Phir terminal mein chalayein: ollama run llama3",
            "success": False
        })


@app.route("/speak", methods=["POST"])
def speak():
    """
    Text-to-Speech using pyttsx3 (Windows SAPI, offline).
    Plays audio directly on the server machine (your laptop).
    """
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data["text"].strip()
    if not text:
        return jsonify({"success": True, "message": "Empty text"})

    try:
        # Run TTS in a separate thread so it doesn't block the request
        tts_thread = threading.Thread(target=_speak_text, args=(text,), daemon=True)
        tts_thread.start()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500


def _speak_text(text: str):
    """Internal: speak text using pyttsx3."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        # Adjust speed (default ~200, lower = slower)
        engine.setProperty("rate", 160)
        engine.setProperty("volume", 1.0)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"[TTS Error] {e}")


@app.route("/status", methods=["GET"])
def status():
    """Check if Ollama is running."""
    ollama_ok = False
    try:
        import urllib.request
        urllib.request.urlopen("http://localhost:11434", timeout=2)
        ollama_ok = True
    except Exception:
        pass

    return jsonify({
        "server": "running",
        "ollama": ollama_ok,
        "whisper_loaded": _whisper_model is not None
    })


# ── Ollama Helper ─────────────────────────────────────────────────────────────

def call_ollama(user_text: str, history: list) -> str:
    """Call local Ollama API with conversation history."""
    import urllib.request
    import json

    # Build messages
    messages = [
        {
            "role": "system",
            "content": (
                "Aap ek helpful AI assistant hain jo Hindi aur English dono mein "
                "baat kar sakte hain. User jo bhi bhasha bole, usi mein jawab dein. "
                "Apne jawab clear aur helpful rakhen. Agar user Hindi mein bole toh "
                "Hindi mein jawab dein, agar English mein bole toh English mein."
            )
        }
    ]

    # Add conversation history (last 10 messages to keep context)
    for msg in history[-10:]:
        messages.append(msg)

    # Add current user message
    messages.append({"role": "user", "content": user_text})

    payload = json.dumps({
        "model": "llama3",
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 500,
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        return result["message"]["content"]


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  🎤  Voice AI Server - Hindi + English")
    print("=" * 55)
    print("  Server:  http://localhost:5050")
    print("  Browser mein yeh link kholein!")
    print("=" * 55)

    # Pre-load whisper model in background
    preload_thread = threading.Thread(target=get_whisper_model, daemon=True)
    preload_thread.start()

    app.run(host="0.0.0.0", port=5050, debug=False, threaded=True)
