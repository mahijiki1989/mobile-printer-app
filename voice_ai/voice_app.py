"""
Voice Transcription App
Windows 11 | Python 3.14 | English (Hindi limited)
ZERO EXTRA PACKAGES — only tkinter + powershell
"""

import tkinter as tk
from tkinter import scrolledtext
import threading
import subprocess
import time

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


class VoiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Transcription")
        self.root.geometry("700x520")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        self.is_listening = False
        self.full_text = ""
        self.stop_flag = threading.Event()
        self.timer_secs = 0
        self.timer_id = None
        self._build_ui()
        self._set_status("ready", "Taiyaar — Bolein button dabayein ya SPACE")

    def _build_ui(self):
        hdr = tk.Frame(self.root, bg=BG2, height=48)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Label(hdr, text="  Voice Transcription", bg=BG2, fg=WHITE,
                 font=("Segoe UI", 13, "bold")).pack(side="left", padx=8, pady=10)
        tk.Label(hdr, text="Windows Speech | No Install",
                 bg=BG2, fg=DIM, font=("Segoe UI", 9)).pack(side="left")

        sf = tk.Frame(self.root, bg="#111827", height=26)
        sf.pack(fill="x"); sf.pack_propagate(False)
        self.dot = tk.Label(sf, text="*", bg="#111827", fg=GREEN, font=("", 10))
        self.dot.pack(side="left", padx=(12, 4))
        self.status = tk.Label(sf, text="...", bg="#111827", fg=GREY,
                               font=("Segoe UI", 9), anchor="w")
        self.status.pack(side="left", fill="x")

        lf = tk.Frame(self.root, bg="#0d1933", height=32)
        lf.pack(fill="x"); lf.pack_propagate(False)
        tk.Label(lf, text=" LIVE ", bg="#0d1933", fg=BLUE,
                 font=("Segoe UI", 8, "bold")).pack(side="left", padx=(8, 2))
        self.live = tk.Label(lf, text="", bg="#0d1933", fg=GREY,
                             font=("Segoe UI", 10), anchor="w")
        self.live.pack(side="left", fill="x", expand=True)

        tf = tk.Frame(self.root, bg=BG)
        tf.pack(fill="both", expand=True, padx=12, pady=(8, 2))
        self.textbox = scrolledtext.ScrolledText(
            tf, wrap=tk.WORD, font=("Consolas", 12),
            bg=BG3, fg=WHITE, insertbackground=BLUE,
            relief="flat", bd=0, padx=14, pady=12,
            spacing1=3, spacing3=3, state="disabled")
        self.textbox.pack(fill="both", expand=True)

        self.count = tk.Label(self.root, text="0 words", bg=BG, fg=DIM,
                              font=("Segoe UI", 9), anchor="e")
        self.count.pack(fill="x", padx=14)

        bot = tk.Frame(self.root, bg=BG2)
        bot.pack(fill="x", side="bottom")
        self.timer_lbl = tk.Label(bot, text="0:00", bg=BG2, fg=DIM,
                                  font=("Consolas", 10))
        self.timer_lbl.pack(side="left", padx=14, pady=12)

        tk.Button(bot, text=" Clear", command=self._clear,
                  bg="#2d1b1b", fg="#f87171", font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, padx=14, pady=7, cursor="hand2",
                  activebackground="#3d2020", activeforeground="#f87171"
                  ).pack(side="left", padx=6, pady=10)

        self.copy_btn = tk.Button(bot, text=" Copy All", command=self._copy,
                                  bg="#1a2d1a", fg="#4ade80",
                                  font=("Segoe UI", 10, "bold"),
                                  relief="flat", bd=0, padx=14, pady=7,
                                  cursor="hand2", activebackground="#1f381f",
                                  activeforeground="#4ade80")
        self.copy_btn.pack(side="left", pady=10)

        self.mic_btn = tk.Button(bot, text="  Bolein", command=self._toggle,
                                 bg=PURP, fg="white",
                                 font=("Segoe UI", 12, "bold"),
                                 relief="flat", bd=0, padx=24, pady=9,
                                 cursor="hand2", activebackground="#6d28d9",
                                 activeforeground="white")
        self.mic_btn.pack(side="right", padx=12, pady=10)

        tk.Label(bot, text="Space=Bolein/Rokein  Ctrl+C=Copy",
                 bg=BG2, fg=DIM, font=("Segoe UI", 8)).pack(side="right", padx=(0,8))

        self.root.bind("<space>", lambda e: self._toggle())
        self.root.bind("<Control-c>", lambda e: self._copy())

    def _toggle(self):
        if self.is_listening:
            self._stop()
        else:
            self._start()

    def _start(self):
        self.is_listening = True
        self.stop_flag.clear()
        self.mic_btn.config(text="  Rokein", bg=RED, activebackground="#b91c1c")
        self._set_status("listening", "Sun raha hoon... bolte rahein")
        self.live.config(text="Bol sakte hain...", fg=GREEN)
        self._start_timer()
        threading.Thread(target=self._listen_loop, daemon=True).start()

    def _stop(self):
        self.is_listening = False
        self.stop_flag.set()
        self._stop_timer()
        self.mic_btn.config(text="  Bolein", bg=PURP, activebackground="#6d28d9")
        self._set_status("ready", "Ruk gaye — Copy karein ya dobara bolein")
        self.live.config(text="", fg=GREY)

    def _listen_loop(self):
        """Continuously recognize speech using PowerShell System.Speech."""
        while not self.stop_flag.is_set():
            self.root.after(0, lambda: self.live.config(text="Bol sakte hain...", fg=GREEN))
            text = self._recognize(8)
            if self.stop_flag.is_set():
                break
            if text:
                self.root.after(0, lambda t=text: self._add_text(t))

    def _recognize(self, duration):
        """Single recognition attempt via PowerShell."""
        ps = f'''
Add-Type -AssemblyName System.Speech
$re = New-Object System.Speech.Recognition.SpeechRecognitionEngine
$gr = New-Object System.Speech.Recognition.DictationGrammar
$re.LoadGrammar($gr)
$re.SetInputToDefaultAudioDevice()
$re.InitialSilenceTimeout = [TimeSpan]::FromSeconds(3)
$re.EndSilenceTimeout = [TimeSpan]::FromSeconds(1.2)
try {{
    $r = $re.Recognize([TimeSpan]::FromSeconds({duration}))
    if ($r -and $r.Text) {{ Write-Output $r.Text }}
}} catch {{}}
'''
        try:
            r = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive",
                 "-ExecutionPolicy", "Bypass", "-Command", ps],
                capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=duration + 10,
                creationflags=0x08000000)
            return r.stdout.strip()
        except:
            return ""

    def _add_text(self, phrase):
        sep = " " if self.full_text and self.full_text[-1] not in ("\n", " ") else ""
        self.full_text += sep + phrase
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert(tk.END, self.full_text)
        self.textbox.see(tk.END)
        self.textbox.configure(state="disabled")
        w = len(self.full_text.split())
        self.count.config(text=f"{w} words  |  {len(self.full_text)} chars")
        self.live.config(text=f'"{phrase}"', fg=GREEN)
        self.root.after(2500, lambda: self.live.config(
            text="Bol sakte hain...", fg=GREEN) if self.is_listening else None)

    def _set_status(self, state, text):
        c = {"ready": GREEN, "listening": BLUE, "error": RED, "warn": YEL}
        self.dot.config(fg=c.get(state, YEL))
        self.status.config(text=text)

    def _copy(self):
        if not self.full_text.strip(): return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.full_text)
        self.copy_btn.config(text=" Copied!", fg="#86efac")
        self.root.after(2000, lambda: self.copy_btn.config(text=" Copy All", fg="#4ade80"))

    def _clear(self):
        self.full_text = ""
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", tk.END)
        self.textbox.configure(state="disabled")
        self.count.config(text="0 words")

    def _start_timer(self):
        self.timer_secs = 0
        self._tick()

    def _tick(self):
        if not self.is_listening: return
        m, s = divmod(self.timer_secs, 60)
        self.timer_lbl.config(text=f"{m}:{s:02d}", fg=RED)
        self.timer_secs += 1
        self.timer_id = self.root.after(1000, self._tick)

    def _stop_timer(self):
        if self.timer_id: self.root.after_cancel(self.timer_id)
        self.timer_lbl.config(text="0:00", fg=DIM)

    def on_close(self):
        self.stop_flag.set()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    try:
        from ctypes import windll, byref, sizeof, c_int
        hwnd = windll.user32.GetParent(root.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, byref(c_int(1)), sizeof(c_int))
    except: pass
    app = VoiceApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
