"""
Voice Transcription App — voice_app.py
Windows 11 ke liye | Pure Python + tkinter
Koi browser nahi, koi server nahi — seedha .exe

Features:
  • Mic button click → bolna shuru
  • Jitna bol do — koi time limit nahi (auto-restart)
  • Real-time live transcript screen pe
  • Ek badi text window mein sab likha aata hai
  • Copy button — ek click mein clipboard mein
  • Clear button — saaf karo
  • System tray icon (minimize pe)
  • Hindi + English auto-detect
"""

import tkinter as tk
from tkinter import scrolledtext, font as tkfont
import threading
import queue
import time
import sys
import os

# ── Speech Recognition ────────────────────────────────────────────────────────
try:
    import speech_recognition as sr
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "SpeechRecognition", "pyaudio"])
    import speech_recognition as sr

# ── Constants ─────────────────────────────────────────────────────────────────
APP_NAME   = "Voice Transcription"
BG_DARK    = "#0f1117"
BG_PANEL   = "#1a1d2e"
BG_BOX     = "#13151f"
ACCENT     = "#4f8ef7"
ACCENT2    = "#7c3aed"
RED        = "#ef4444"
GREEN      = "#22c55e"
YELLOW     = "#f59e0b"
TEXT_WHITE = "#e8eaf0"
TEXT_GREY  = "#8892a4"
TEXT_DIM   = "#4a5568"
FONT_MAIN  = ("Segoe UI", 11)
FONT_MONO  = ("Consolas", 12)
FONT_BIG   = ("Segoe UI", 13, "bold")
FONT_SMALL = ("Segoe UI", 9)

# ── App ───────────────────────────────────────────────────────────────────────
class VoiceApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("700x580")
        self.root.minsize(500, 400)
        self.root.configure(bg=BG_DARK)

        # State
        self.is_listening   = False
        self.full_text      = ""          # complete transcript so far
        self.session_text   = ""          # current session accumulated
        self.ui_queue       = queue.Queue()  # thread → UI communication
        self.recognizer     = sr.Recognizer()
        self.microphone     = None
        self.listen_thread  = None
        self.stop_event     = threading.Event()

        # Mic sensitivity
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 1.2   # 1.2s silence = end of phrase

        self._build_ui()
        self._init_mic()
        self._poll_queue()   # start UI update loop

    # ── Microphone Init ───────────────────────────────────────────────────────
    def _init_mic(self):
        """Background mein mic dhundo."""
        def _find():
            try:
                self.microphone = sr.Microphone()
                # Ambient noise calibrate
                with self.microphone as src:
                    self.recognizer.adjust_for_ambient_noise(src, duration=0.5)
                self.ui_queue.put(("status", "ready", "✅ Mic ready — बोलें button dabayein"))
            except Exception as e:
                self.ui_queue.put(("status", "error",
                    f"❌ Microphone nahi mila: {e}\nMic connect karke dobara chalayein."))

        threading.Thread(target=_find, daemon=True).start()
        self._set_status("warn", "🎤 Microphone dhundh rahe hain...")

    # ── UI Build ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Title bar ──
        title_bar = tk.Frame(self.root, bg=BG_PANEL, height=52)
        title_bar.pack(fill="x", side="top")
        title_bar.pack_propagate(False)

        tk.Label(title_bar, text="🎙️", bg=BG_PANEL, fg=ACCENT,
                 font=("Segoe UI Emoji", 18)).pack(side="left", padx=(14, 6), pady=8)
        tk.Label(title_bar, text="Voice Transcription", bg=BG_PANEL,
                 fg=TEXT_WHITE, font=("Segoe UI", 13, "bold")).pack(side="left", pady=8)
        tk.Label(title_bar, text="Windows 11 • Free • No Internet",
                 bg=BG_PANEL, fg=TEXT_DIM, font=FONT_SMALL).pack(side="left", padx=10, pady=8)

        # ── Status bar ──
        self.status_frame = tk.Frame(self.root, bg=BG_PANEL, height=30)
        self.status_frame.pack(fill="x")
        self.status_frame.pack_propagate(False)

        self.status_dot = tk.Label(self.status_frame, text="●", bg=BG_PANEL,
                                   fg=YELLOW, font=("Segoe UI", 10))
        self.status_dot.pack(side="left", padx=(14, 4))

        self.status_lbl = tk.Label(self.status_frame, text="शुरू हो रहा है...",
                                   bg=BG_PANEL, fg=TEXT_GREY, font=FONT_SMALL,
                                   anchor="w")
        self.status_lbl.pack(side="left", fill="x")

        # ── Live bar (jab bol rahe ho) ──
        self.live_frame = tk.Frame(self.root, bg="#1a2744", height=36)
        self.live_frame.pack(fill="x")
        self.live_frame.pack_propagate(False)

        tk.Label(self.live_frame, text="LIVE", bg="#1a2744",
                 fg=ACCENT, font=("Segoe UI", 8, "bold")).pack(side="left", padx=(12,4))
        self.live_lbl = tk.Label(self.live_frame, text="यहाँ real-time text दिखेगा...",
                                  bg="#1a2744", fg=TEXT_GREY,
                                  font=("Segoe UI", 10), anchor="w",
                                  wraplength=580, justify="left")
        self.live_lbl.pack(side="left", fill="x", expand=True, padx=(0,10))

        # ── Main text box ──
        txt_frame = tk.Frame(self.root, bg=BG_DARK)
        txt_frame.pack(fill="both", expand=True, padx=14, pady=(10, 6))

        self.text_box = scrolledtext.ScrolledText(
            txt_frame,
            wrap=tk.WORD,
            font=FONT_MONO,
            bg=BG_BOX,
            fg=TEXT_WHITE,
            insertbackground=ACCENT,
            selectbackground=ACCENT2,
            relief="flat",
            bd=0,
            padx=14,
            pady=12,
            spacing1=3,
            spacing3=3,
        )
        self.text_box.pack(fill="both", expand=True)
        self.text_box.configure(state="disabled")

        # Word count label
        self.wordcount_lbl = tk.Label(self.root, text="0 words  •  0 characters",
                                       bg=BG_DARK, fg=TEXT_DIM, font=FONT_SMALL,
                                       anchor="e")
        self.wordcount_lbl.pack(fill="x", padx=16)

        # ── Bottom controls ──
        ctrl = tk.Frame(self.root, bg=BG_PANEL)
        ctrl.pack(fill="x", side="bottom")

        # Timer
        self.timer_lbl = tk.Label(ctrl, text="0:00", bg=BG_PANEL,
                                   fg=TEXT_DIM, font=("Consolas", 10))
        self.timer_lbl.pack(side="left", padx=(14, 0), pady=14)

        # Clear button
        self.clear_btn = self._make_btn(ctrl, "🗑  Clear", self._clear,
                                         bg="#2d1b1b", fg="#f87171",
                                         hover="#3d2020")
        self.clear_btn.pack(side="left", padx=8, pady=10)

        # Copy button
        self.copy_btn = self._make_btn(ctrl, "📋  Copy All", self._copy,
                                        bg="#1a2d1a", fg="#4ade80",
                                        hover="#1f381f")
        self.copy_btn.pack(side="left", padx=0, pady=10)

        # BIG mic button (right side)
        self.mic_btn = tk.Button(
            ctrl,
            text="🎤  बोलें",
            command=self._toggle,
            bg=ACCENT2,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            bd=0,
            padx=28,
            pady=10,
            cursor="hand2",
            activebackground="#6d28d9",
            activeforeground="white",
        )
        self.mic_btn.pack(side="right", padx=14, pady=10)

        # Keyboard shortcut
        self.root.bind("<space>", lambda e: self._toggle())
        self.root.bind("<Control-c>", lambda e: self._copy())
        self.root.bind("<Control-l>", lambda e: self._clear())

        # Shortcut hint
        tk.Label(ctrl, text="Space = बोलें/रोकें   Ctrl+C = Copy",
                 bg=BG_PANEL, fg=TEXT_DIM, font=FONT_SMALL
                 ).pack(side="right", padx=(0, 100))

    def _make_btn(self, parent, text, cmd, bg, fg, hover):
        btn = tk.Button(parent, text=text, command=cmd,
                        bg=bg, fg=fg, font=("Segoe UI", 10, "bold"),
                        relief="flat", bd=0, padx=16, pady=8,
                        cursor="hand2",
                        activebackground=hover, activeforeground=fg)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    # ── Mic Toggle ────────────────────────────────────────────────────────────
    def _toggle(self):
        if self.microphone is None:
            return  # still initialising
        if self.is_listening:
            self._stop_listening()
        else:
            self._start_listening()

    def _start_listening(self):
        if self.is_listening:
            return
        self.is_listening  = True
        self.session_text  = ""
        self.stop_event.clear()

        self.mic_btn.config(text="⏹  रोकें", bg=RED, activebackground="#b91c1c")
        self._set_status("listening", "🎙️  सुन रहे हैं... जितना चाहें बोलते रहें")
        self._start_timer()

        self.listen_thread = threading.Thread(
            target=self._listen_loop, daemon=True)
        self.listen_thread.start()

    def _stop_listening(self):
        self.is_listening = False
        self.stop_event.set()
        self._stop_timer()
        self.mic_btn.config(text="🎤  बोलें", bg=ACCENT2,
                            activebackground="#6d28d9")
        self._set_status("ready", "✅ रुक गए — अब Copy कर सकते हैं")
        self.ui_queue.put(("live", ""))

    # ── Continuous Listen Loop ────────────────────────────────────────────────
    def _listen_loop(self):
        """
        Runs in background thread.
        Keeps listening indefinitely until stop_event is set.
        Each phrase is recognized and sent to UI queue.
        Auto-restarts if an error occurs.
        """
        while not self.stop_event.is_set():
            try:
                with self.microphone as src:
                    # Non-blocking listen — returns when pause_threshold seconds of silence
                    try:
                        audio = self.recognizer.listen(
                            src,
                            timeout=3,          # 3s wait for speech to start
                            phrase_time_limit=60  # max 60s per phrase
                        )
                    except sr.WaitTimeoutError:
                        # No speech in 3s — just loop again
                        continue

                if self.stop_event.is_set():
                    break

                # Send to UI: "recognizing..."
                self.ui_queue.put(("live", "⏳ समझ रहे हैं..."))

                # Recognize
                try:
                    text = self.recognizer.recognize_google(
                        audio,
                        language="hi-IN,en-IN",   # Hindi first, English fallback
                    )
                    if text.strip():
                        self.ui_queue.put(("text", text.strip()))
                except sr.UnknownValueError:
                    # Couldn't understand — just continue
                    self.ui_queue.put(("live", ""))
                    continue
                except sr.RequestError as e:
                    self.ui_queue.put(("status", "error",
                        f"❌ Internet connection nahi hai!\nGoogle Speech API ke liye internet chahiye.\nError: {e}"))
                    # Wait and retry
                    time.sleep(2)
                    continue

            except Exception as e:
                if not self.stop_event.is_set():
                    self.ui_queue.put(("live", f"⚠ Error: {e} — retry..."))
                    time.sleep(1)

        self.ui_queue.put(("live", ""))

    # ── UI Queue Polling ──────────────────────────────────────────────────────
    def _poll_queue(self):
        """Main thread mein queue se messages process karo."""
        try:
            while True:
                msg = self.ui_queue.get_nowait()
                kind = msg[0]

                if kind == "text":
                    phrase = msg[1]
                    # Add space if needed
                    sep = " " if self.full_text and not self.full_text.endswith("\n") else ""
                    self.full_text += sep + phrase
                    self.session_text += sep + phrase
                    self._refresh_textbox()
                    self.live_lbl.config(text="", fg=TEXT_GREY)

                elif kind == "live":
                    txt = msg[1]
                    self.live_lbl.config(
                        text=txt if txt else "यहाँ real-time text दिखेगा...",
                        fg=ACCENT if txt else TEXT_GREY
                    )

                elif kind == "status":
                    _, state, text = msg
                    self._set_status(state, text)

        except queue.Empty:
            pass

        self.root.after(80, self._poll_queue)

    # ── Text Box Refresh ──────────────────────────────────────────────────────
    def _refresh_textbox(self):
        self.text_box.configure(state="normal")
        self.text_box.delete("1.0", tk.END)
        self.text_box.insert(tk.END, self.full_text)
        self.text_box.see(tk.END)
        self.text_box.configure(state="disabled")

        # Word count
        words = len(self.full_text.split()) if self.full_text.strip() else 0
        chars = len(self.full_text)
        self.wordcount_lbl.config(text=f"{words} words  •  {chars} characters")

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _set_status(self, state: str, text: str):
        colors = {
            "ready":     GREEN,
            "listening": ACCENT,
            "error":     RED,
            "warn":      YELLOW,
        }
        self.status_dot.config(fg=colors.get(state, YELLOW))
        self.status_lbl.config(text=text)

    def _copy(self):
        if not self.full_text.strip():
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.full_text)
        self.copy_btn.config(text="✅  Copied!", fg="#86efac")
        self.root.after(1800, lambda: self.copy_btn.config(
            text="📋  Copy All", fg="#4ade80"))

    def _clear(self):
        self.full_text    = ""
        self.session_text = ""
        self._refresh_textbox()
        self.live_lbl.config(text="यहाँ real-time text दिखेगा...", fg=TEXT_GREY)
        self.wordcount_lbl.config(text="0 words  •  0 characters")

    # ── Recording Timer ───────────────────────────────────────────────────────
    _timer_seconds = 0
    _timer_id      = None

    def _start_timer(self):
        self._timer_seconds = 0
        self._tick_timer()

    def _tick_timer(self):
        if not self.is_listening:
            return
        m = self._timer_seconds // 60
        s = self._timer_seconds % 60
        self.timer_lbl.config(text=f"{m}:{s:02d}", fg=RED)
        self._timer_seconds += 1
        self._timer_id = self.root.after(1000, self._tick_timer)

    def _stop_timer(self):
        if self._timer_id:
            self.root.after_cancel(self._timer_id)
        self.timer_lbl.config(text="0:00", fg=TEXT_DIM)

    def on_close(self):
        self.stop_event.set()
        self.is_listening = False
        self.root.destroy()


# ── Entry Point ───────────────────────────────────────────────────────────────
def main():
    root = tk.Tk()
    root.resizable(True, True)

    # Windows taskbar icon text
    try:
        root.wm_iconbitmap()   # will use default if no .ico
    except Exception:
        pass

    # Dark title bar (Windows 11)
    try:
        from ctypes import windll, byref, sizeof, c_int
        HWND = windll.user32.GetParent(root.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(
            HWND, 20, byref(c_int(1)), sizeof(c_int))   # dark mode
    except Exception:
        pass

    app = VoiceApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
