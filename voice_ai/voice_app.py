"""
Voice Transcription App
Windows 11 - Python 3.14 Compatible
NO PyAudio, NO SpeechRecognition library
Uses ONLY: tkinter (built-in) + Windows PowerShell Speech Recognition
"""

import tkinter as tk
from tkinter import scrolledtext
import threading
import subprocess
import sys
import os
import time

# ── Colors ────────────────────────────────────────────────────────────────────
BG       = "#0f1117"
BG2      = "#1a1d2e"
BG3      = "#13151f"
BLUE     = "#4f8ef7"
PURPLE   = "#7c3aed"
RED      = "#ef4444"
GREEN    = "#22c55e"
YELLOW   = "#f59e0b"
WHITE    = "#e8eaf0"
GREY     = "#8892a4"
DIM      = "#4a5568"

class VoiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Transcription")
        self.root.geometry("720x560")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        # State
        self.is_listening  = False
        self.full_text     = ""
        self.listen_thread = None
        self.stop_flag     = threading.Event()
        self.timer_secs    = 0
        self.timer_id      = None

        self._build_ui()
        self._set_status("ready", "✅ Taiyaar — 🎤 बोलें button dabayein ya SPACE")

    # ─────────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Title bar
        top = tk.Frame(self.root, bg=BG2, height=50)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Label(top, text="🎙️  Voice Transcription",
                 bg=BG2, fg=WHITE, font=("Segoe UI", 14, "bold")).pack(side="left", padx=14, pady=10)
        tk.Label(top, text="Windows 11 • Hindi + English",
                 bg=BG2, fg=DIM, font=("Segoe UI", 9)).pack(side="left", padx=4)

        # Status bar
        sbar = tk.Frame(self.root, bg="#111827", height=28)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.dot_lbl = tk.Label(sbar, text="●", bg="#111827", fg=YELLOW,
                                font=("Segoe UI", 10))
        self.dot_lbl.pack(side="left", padx=(12, 4))
        self.status_lbl = tk.Label(sbar, text="...", bg="#111827", fg=GREY,
                                   font=("Segoe UI", 9), anchor="w")
        self.status_lbl.pack(side="left", fill="x")

        # Live bar
        live_bar = tk.Frame(self.root, bg="#0d1933", height=34)
        live_bar.pack(fill="x")
        live_bar.pack_propagate(False)
        tk.Label(live_bar, text="LIVE", bg="#0d1933", fg=BLUE,
                 font=("Segoe UI", 8, "bold")).pack(side="left", padx=(12,5))
        self.live_lbl = tk.Label(live_bar, text="यहाँ bolne par text dikhega...",
                                  bg="#0d1933", fg=GREY,
                                  font=("Segoe UI", 10), anchor="w")
        self.live_lbl.pack(side="left", fill="x", expand=True)

        # Main text area
        txt_frame = tk.Frame(self.root, bg=BG)
        txt_frame.pack(fill="both", expand=True, padx=12, pady=(8,4))
        self.textbox = scrolledtext.ScrolledText(
            txt_frame, wrap=tk.WORD,
            font=("Consolas", 12),
            bg=BG3, fg=WHITE,
            insertbackground=BLUE,
            relief="flat", bd=0,
            padx=14, pady=12,
            spacing1=4, spacing3=4,
            state="disabled"
        )
        self.textbox.pack(fill="both", expand=True)

        # Word count
        self.count_lbl = tk.Label(self.root, text="0 words  •  0 chars",
                                   bg=BG, fg=DIM, font=("Segoe UI", 9), anchor="e")
        self.count_lbl.pack(fill="x", padx=14, pady=(0, 3))

        # Bottom bar
        bot = tk.Frame(self.root, bg=BG2)
        bot.pack(fill="x", side="bottom")

        self.timer_lbl = tk.Label(bot, text="0:00", bg=BG2, fg=DIM,
                                   font=("Consolas", 10))
        self.timer_lbl.pack(side="left", padx=14, pady=14)

        # Clear
        self.clear_btn = tk.Button(bot, text="🗑  Clear", command=self._clear,
                                   bg="#2d1b1b", fg="#f87171",
                                   font=("Segoe UI", 10, "bold"),
                                   relief="flat", bd=0, padx=14, pady=8,
                                   cursor="hand2",
                                   activebackground="#3d2020", activeforeground="#f87171")
        self.clear_btn.pack(side="left", padx=6, pady=10)

        # Copy
        self.copy_btn = tk.Button(bot, text="📋  Copy All", command=self._copy,
                                   bg="#1a2d1a", fg="#4ade80",
                                   font=("Segoe UI", 10, "bold"),
                                   relief="flat", bd=0, padx=14, pady=8,
                                   cursor="hand2",
                                   activebackground="#1f381f", activeforeground="#4ade80")
        self.copy_btn.pack(side="left", padx=0, pady=10)

        # Hint
        tk.Label(bot, text="Space = बोलें/रोकें  |  Ctrl+C = Copy",
                 bg=BG2, fg=DIM, font=("Segoe UI", 8)
                 ).pack(side="right", padx=(0, 110))

        # MIC button
        self.mic_btn = tk.Button(bot, text="🎤  बोलें",
                                  command=self._toggle,
                                  bg=PURPLE, fg="white",
                                  font=("Segoe UI", 12, "bold"),
                                  relief="flat", bd=0,
                                  padx=26, pady=10,
                                  cursor="hand2",
                                  activebackground="#6d28d9", activeforeground="white")
        self.mic_btn.pack(side="right", padx=12, pady=10)

        # Keyboard
        self.root.bind("<space>",   lambda e: self._toggle())
        self.root.bind("<Control-c>", lambda e: self._copy())
        self.root.bind("<Control-l>", lambda e: self._clear())

    # ─────────────────────────────────────────────────────────────────────────
    def _toggle(self):
        if self.is_listening:
            self._stop()
        else:
            self._start()

    def _start(self):
        self.is_listening = True
        self.stop_flag.clear()
        self.mic_btn.config(text="⏹  रोकें", bg=RED, activebackground="#b91c1c")
        self._set_status("listening", "🎙️  सुन रहे हैं... बोलते रहें जितना चाहें")
        self._start_timer()
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()

    def _stop(self):
        self.is_listening = False
        self.stop_flag.set()
        self._stop_timer()
        self.mic_btn.config(text="🎤  बोलें", bg=PURPLE, activebackground="#6d28d9")
        self._set_status("ready", "✅ Ruk gaye — Copy karein ya dobara bolein")
        self.live_lbl.config(text="", fg=GREY)

    # ─────────────────────────────────────────────────────────────────────────
    # Windows PowerShell Speech Recognition — koi extra package nahi!
    # ─────────────────────────────────────────────────────────────────────────
    def _listen_loop(self):
        """
        Windows Speech Recognition (System.Speech) via PowerShell.
        Python 3.14 ke saath 100% compatible.
        Koi PyAudio, koi SpeechRecognition library nahi chahiye.
        OFFLINE — internet ki zaroorat nahi!
        """
        # PowerShell script jo continuously sun ta hai
        ps_script = r"""
Add-Type -AssemblyName System.Speech
$recognizer = New-Object System.Speech.Recognition.SpeechRecognitionEngine

# Hindi + English grammar — free dictation
$grammar = New-Object System.Speech.Recognition.DictationGrammar
$recognizer.LoadGrammar($grammar)

# Default microphone
$recognizer.SetInputToDefaultAudioDevice()

# Timeout settings
$recognizer.InitialSilenceTimeout = [TimeSpan]::FromSeconds(5)
$recognizer.BabbleTimeout = [TimeSpan]::FromSeconds(3)
$recognizer.EndSilenceTimeout = [TimeSpan]::FromSeconds(1.5)

Write-Host "READY"
[Console]::Out.Flush()

while ($true) {
    try {
        $result = $recognizer.Recognize([TimeSpan]::FromSeconds(30))
        if ($result -ne $null -and $result.Text -ne "") {
            Write-Host ("TEXT:" + $result.Text)
            [Console]::Out.Flush()
        } else {
            Write-Host "TIMEOUT"
            [Console]::Out.Flush()
        }
    } catch {
        Write-Host ("ERROR:" + $_.Exception.Message)
        [Console]::Out.Flush()
        break
    }
}
"""
        try:
            proc = subprocess.Popen(
                ["powershell", "-NoProfile", "-NonInteractive",
                 "-ExecutionPolicy", "Bypass", "-Command", ps_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # Wait for READY
            while not self.stop_flag.is_set():
                line = proc.stdout.readline()
                if not line:
                    break
                line = line.strip()
                if line == "READY":
                    self.root.after(0, lambda: self.live_lbl.config(
                        text="🎙️ Bol sakte hain...", fg=GREEN))
                    break
                elif line.startswith("ERROR:"):
                    self.root.after(0, lambda l=line: self._set_status(
                        "error", f"❌ {l[6:]}"))
                    return

            # Main loop — sun ta raho
            while not self.stop_flag.is_set():
                line = proc.stdout.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue

                if line.startswith("TEXT:"):
                    text = line[5:].strip()
                    if text:
                        self.root.after(0, lambda t=text: self._add_text(t))

                elif line == "TIMEOUT":
                    # Normal — koi awaaz nahi aayi, continue
                    continue

                elif line.startswith("ERROR:"):
                    self.root.after(0, lambda l=line: self._set_status(
                        "error", f"❌ {l[6:]}"))
                    break

        except Exception as e:
            self.root.after(0, lambda: self._set_status(
                "error", f"❌ Error: {e}"))
        finally:
            try:
                proc.terminate()
            except Exception:
                pass
            if not self.stop_flag.is_set():
                # Auto restart karo
                if self.is_listening:
                    time.sleep(0.3)
                    self.listen_thread = threading.Thread(
                        target=self._listen_loop, daemon=True)
                    self.listen_thread.start()

    # ─────────────────────────────────────────────────────────────────────────
    def _add_text(self, phrase: str):
        """Main thread mein text add karo."""
        sep = " " if self.full_text and not self.full_text[-1] in ("\n", " ") else ""
        self.full_text += sep + phrase
        self._refresh()
        self.live_lbl.config(text=f"✓ \"{phrase}\"", fg=GREEN)
        self.root.after(2000, lambda: self.live_lbl.config(
            text="🎙️ Bol sakte hain...", fg=GREY))

    def _refresh(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert(tk.END, self.full_text)
        self.textbox.see(tk.END)
        self.textbox.configure(state="disabled")
        w = len(self.full_text.split()) if self.full_text.strip() else 0
        c = len(self.full_text)
        self.count_lbl.config(text=f"{w} words  •  {c} chars")

    def _set_status(self, state, text):
        colors = {"ready": GREEN, "listening": BLUE, "error": RED, "warn": YELLOW}
        self.dot_lbl.config(fg=colors.get(state, YELLOW))
        self.status_lbl.config(text=text)

    def _copy(self):
        if not self.full_text.strip():
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.full_text)
        self.copy_btn.config(text="✅  Copied!", fg="#86efac")
        self.root.after(2000, lambda: self.copy_btn.config(
            text="📋  Copy All", fg="#4ade80"))

    def _clear(self):
        self.full_text = ""
        self._refresh()
        self.live_lbl.config(text="", fg=GREY)

    # Timer
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
        self.root.destroy()


# ─────────────────────────────────────────────────────────────────────────────
def main():
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


if __name__ == "__main__":
    main()
