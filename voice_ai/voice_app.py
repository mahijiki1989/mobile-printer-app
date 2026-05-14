"""
Voice Transcription App
Windows 11 | Python 3.14 | Hindi + English
Uses: sounddevice (mic) + Google Speech REST API (free)
"""

import tkinter as tk
from tkinter import scrolledtext
import threading
import json
import urllib.request
import urllib.error
import struct
import wave
import io
import time
import os
import sys
import subprocess

# ── Auto-install missing packages ─────────────────────────────────────────────
def ensure(pkg, import_name=None):
    name = import_name or pkg
    try:
        __import__(name)
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

ensure("sounddevice")
ensure("numpy")

import sounddevice as sd
import numpy as np

# ── Colors ─────────────────────────────────────────────────────────────────────
BG    = "#0f1117"
BG2   = "#1a1d2e"
BG3   = "#13151f"
BLUE  = "#4f8ef7"
PURP  = "#7c3aed"
RED   = "#ef4444"
GREEN = "#22c55e"
YEL   = "#f59e0b"
WHITE = "#e8eaf0"
GREY  = "#8892a4"
DIM   = "#4a5568"

# ── Config ─────────────────────────────────────────────────────────────────────
SAMPLE_RATE  = 16000   # 16kHz — Google prefers this
CHANNELS     = 1
CHUNK_SEC    = 5       # har 5 second ka chunk Google ko bhejenge
SILENCE_THRESH = 0.01  # silence detection threshold


class VoiceApp:
    def __init__(self, root):
        self.root       = root
        self.root.title("Voice Transcription")
        self.root.geometry("700x520")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        self.is_listening  = False
        self.full_text     = ""
        self.stop_flag     = threading.Event()
        self.timer_secs    = 0
        self.timer_id      = None
        self.audio_frames  = []   # raw recorded audio
        self.stream        = None

        self._build_ui()
        self._set_status("ready", "Taiyaar — Bolein button dabayein ya SPACE")

    # ── UI ─────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Header
        hdr = tk.Frame(self.root, bg=BG2, height=48)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Label(hdr, text="  Voice Transcription",
                 bg=BG2, fg=WHITE, font=("Segoe UI", 13, "bold")
                 ).pack(side="left", padx=8, pady=10)
        tk.Label(hdr, text="Hindi + English  |  Google Speech",
                 bg=BG2, fg=DIM, font=("Segoe UI", 9)
                 ).pack(side="left")

        # Status
        sf = tk.Frame(self.root, bg="#111827", height=26)
        sf.pack(fill="x"); sf.pack_propagate(False)
        self.dot = tk.Label(sf, text="●", bg="#111827", fg=GREEN, font=("", 10))
        self.dot.pack(side="left", padx=(12, 4))
        self.status = tk.Label(sf, text="...", bg="#111827", fg=GREY,
                               font=("Segoe UI", 9), anchor="w")
        self.status.pack(side="left", fill="x")

        # Live bar
        lf = tk.Frame(self.root, bg="#0d1933", height=32)
        lf.pack(fill="x"); lf.pack_propagate(False)
        tk.Label(lf, text=" LIVE ", bg="#0d1933", fg=BLUE,
                 font=("Segoe UI", 8, "bold")).pack(side="left", padx=(8, 2))
        self.live = tk.Label(lf, text="Mic button dabayein...",
                             bg="#0d1933", fg=GREY,
                             font=("Segoe UI", 10), anchor="w")
        self.live.pack(side="left", fill="x", expand=True)

        # Main text
        tf = tk.Frame(self.root, bg=BG)
        tf.pack(fill="both", expand=True, padx=12, pady=(8, 2))
        self.textbox = scrolledtext.ScrolledText(
            tf, wrap=tk.WORD, font=("Consolas", 12),
            bg=BG3, fg=WHITE, insertbackground=BLUE,
            relief="flat", bd=0, padx=14, pady=12,
            spacing1=3, spacing3=3, state="disabled"
        )
        self.textbox.pack(fill="both", expand=True)

        # Count
        self.count = tk.Label(self.root, text="0 words",
                              bg=BG, fg=DIM, font=("Segoe UI", 9), anchor="e")
        self.count.pack(fill="x", padx=14)

        # Bottom bar
        bot = tk.Frame(self.root, bg=BG2)
        bot.pack(fill="x", side="bottom")

        self.timer_lbl = tk.Label(bot, text="0:00", bg=BG2, fg=DIM,
                                  font=("Consolas", 10))
        self.timer_lbl.pack(side="left", padx=14, pady=12)

        tk.Button(bot, text=" Clear", command=self._clear,
                  bg="#2d1b1b", fg="#f87171",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, padx=14, pady=7, cursor="hand2",
                  activebackground="#3d2020", activeforeground="#f87171"
                  ).pack(side="left", padx=6, pady=10)

        self.copy_btn = tk.Button(bot, text=" Copy All", command=self._copy,
                                  bg="#1a2d1a", fg="#4ade80",
                                  font=("Segoe UI", 10, "bold"),
                                  relief="flat", bd=0, padx=14, pady=7,
                                  cursor="hand2",
                                  activebackground="#1f381f",
                                  activeforeground="#4ade80")
        self.copy_btn.pack(side="left", pady=10)

        self.mic_btn = tk.Button(bot, text="  Bolein",
                                 command=self._toggle,
                                 bg=PURP, fg="white",
                                 font=("Segoe UI", 12, "bold"),
                                 relief="flat", bd=0, padx=24, pady=9,
                                 cursor="hand2",
                                 activebackground="#6d28d9",
                                 activeforeground="white")
        self.mic_btn.pack(side="right", padx=12, pady=10)

        tk.Label(bot, text="Space=Bolein/Rokein  Ctrl+C=Copy",
                 bg=BG2, fg=DIM, font=("Segoe UI", 8)
                 ).pack(side="right", padx=(0, 8))

        self.root.bind("<space>",     lambda e: self._toggle())
        self.root.bind("<Control-c>", lambda e: self._copy())

    # ── Toggle mic ─────────────────────────────────────────────────────────────
    def _toggle(self):
        if self.is_listening:
            self._stop()
        else:
            self._start()

    def _start(self):
        self.is_listening = True
        self.stop_flag.clear()
        self.audio_frames = []
        self.mic_btn.config(text="  Rokein", bg=RED, activebackground="#b91c1c")
        self._set_status("listening", "Sun raha hoon... bolte rahein jitna chahein")
        self.live.config(text="Shuru ho raha hai...", fg=YEL)
        self._start_timer()
        threading.Thread(target=self._record_loop, daemon=True).start()

    def _stop(self):
        self.is_listening = False
        self.stop_flag.set()
        self._stop_timer()
        self.mic_btn.config(text="  Bolein", bg=PURP, activebackground="#6d28d9")
        self._set_status("ready", "Ruk gaye — Copy karein ya dobara bolein")
        self.live.config(text="", fg=GREY)

    # ── Record + Recognize Loop ────────────────────────────────────────────────
    def _record_loop(self):
        """
        Continuously record audio in chunks of CHUNK_SEC seconds.
        Send each chunk to Google Speech API.
        Append results to transcript.
        """
        self.root.after(0, lambda: self.live.config(
            text="Bol sakte hain...", fg=GREEN))
        self.root.after(0, lambda: self._set_status(
            "listening", "Sun raha hoon... bolte rahein jitna chahein"))

        while not self.stop_flag.is_set():
            # Record CHUNK_SEC seconds of audio
            try:
                audio_data = sd.rec(
                    int(CHUNK_SEC * SAMPLE_RATE),
                    samplerate=SAMPLE_RATE,
                    channels=CHANNELS,
                    dtype="int16",
                    blocking=True
                )
            except Exception as e:
                self.root.after(0, lambda err=str(e): self._set_status(
                    "error", f"Mic error: {err}"))
                time.sleep(1)
                continue

            if self.stop_flag.is_set():
                break

            # Check if there's actual sound (not silence)
            audio_np = audio_data.flatten().astype(np.float32) / 32768.0
            volume = float(np.abs(audio_np).mean())

            if volume < SILENCE_THRESH:
                # Silence — skip, don't send to API
                continue

            # Show "recognizing" state
            self.root.after(0, lambda: self.live.config(
                text="Samajh raha hoon...", fg=YEL))

            # Convert to WAV bytes
            wav_bytes = self._numpy_to_wav(audio_data)

            # Send to Google Speech API (free, no key needed for short audio)
            threading.Thread(
                target=self._recognize,
                args=(wav_bytes,),
                daemon=True
            ).start()

        self.root.after(0, lambda: self.live.config(text="", fg=GREY))

    # ── Google Speech API ──────────────────────────────────────────────────────
    def _recognize(self, wav_bytes: bytes):
        """Send WAV audio to Google Speech API and get transcript."""
        url = (
            "https://www.google.com/speech-api/v2/recognize"
            "?output=json&lang=hi-IN&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
            "&maxAlternatives=1&profanityFilter=false"
        )

        req = urllib.request.Request(
            url,
            data=wav_bytes,
            headers={
                "Content-Type": "audio/l16; rate=16000",
                "User-Agent": "Mozilla/5.0"
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw = resp.read().decode("utf-8")

            # Parse response — each line is a JSON object
            text_parts = []
            for line in raw.strip().splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    results = data.get("result", [])
                    for r in results:
                        alts = r.get("alternative", [])
                        if alts:
                            txt = alts[0].get("transcript", "").strip()
                            if txt:
                                text_parts.append(txt)
                except json.JSONDecodeError:
                    continue

            if text_parts:
                final = " ".join(text_parts)
                self.root.after(0, lambda t=final: self._add_text(t))
            else:
                # No result — restore live label
                self.root.after(0, lambda: self.live.config(
                    text="Bol sakte hain...", fg=GREEN)
                    if self.is_listening else None)

        except urllib.error.URLError as e:
            self.root.after(0, lambda: self._set_status(
                "error", "Internet nahi hai! WiFi on karein."))
        except Exception as e:
            # Silently continue on other errors
            self.root.after(0, lambda: self.live.config(
                text="Bol sakte hain...", fg=GREEN)
                if self.is_listening else None)

    # ── Audio conversion ───────────────────────────────────────────────────────
    def _numpy_to_wav(self, audio_np: np.ndarray) -> bytes:
        """Convert numpy int16 array to WAV bytes."""
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)   # int16 = 2 bytes
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(audio_np.tobytes())
        return buf.getvalue()

    # ── Helpers ────────────────────────────────────────────────────────────────
    def _add_text(self, phrase: str):
        sep = " " if self.full_text and self.full_text[-1] not in ("\n", " ") else ""
        self.full_text += sep + phrase

        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert(tk.END, self.full_text)
        self.textbox.see(tk.END)
        self.textbox.configure(state="disabled")

        words = len(self.full_text.split())
        self.count.config(text=f"{words} words  |  {len(self.full_text)} chars")

        self.live.config(text=f'"{phrase}"', fg=GREEN)
        self.root.after(2500, lambda: self.live.config(
            text="Bol sakte hain...", fg=GREEN) if self.is_listening else None)

    def _set_status(self, state, text):
        colors = {"ready": GREEN, "listening": BLUE,
                  "error": RED, "warn": YEL}
        self.dot.config(fg=colors.get(state, YEL))
        self.status.config(text=text)

    def _copy(self):
        if not self.full_text.strip():
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.full_text)
        self.copy_btn.config(text=" Copied!", fg="#86efac")
        self.root.after(2000, lambda: self.copy_btn.config(
            text=" Copy All", fg="#4ade80"))

    def _clear(self):
        self.full_text = ""
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", tk.END)
        self.textbox.configure(state="disabled")
        self.count.config(text="0 words")
        self.live.config(text="", fg=GREY)

    def _start_timer(self):
        self.timer_secs = 0
        self._tick()

    def _tick(self):
        if not self.is_listening:
            return
        m, s = divmod(self.timer_secs, 60)
        self.timer_lbl.config(text=f"{m}:{s:02d}", fg=RED)
        self.timer_secs += 1
        self.timer_id = self.root.after(1000, self._tick)

    def _stop_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.timer_lbl.config(text="0:00", fg=DIM)

    def on_close(self):
        self.stop_flag.set()
        self.is_listening = False
        try:
            sd.stop()
        except:
            pass
        self.root.destroy()


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()

    # Windows 11 dark title bar
    try:
        from ctypes import windll, byref, sizeof, c_int
        hwnd = windll.user32.GetParent(root.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(
            hwnd, 20, byref(c_int(1)), sizeof(c_int))
    except Exception:
        pass

    app = VoiceApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
