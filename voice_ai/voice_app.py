"""
Voice Transcription App
Windows 11 | Python 3.14 | No Extra Packages
Uses Windows Built-in System.Speech via PowerShell
OFFLINE - Internet ki zaroorat NAHI
"""

import tkinter as tk
from tkinter import scrolledtext
import threading
import subprocess
import time
import os

# ── Colors ─────────────────────────────────────────────────────────────
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
        self.root.geometry("700x520")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        self.is_listening = False
        self.full_text = ""
        self.stop_flag = threading.Event()
        self.process = None
        self.timer_secs = 0
        self.timer_id = None

        self._build_ui()
        self._set_status("ready", "Taiyaar — बोलें button dabayein ya SPACE")

    def _build_ui(self):
        # ─── Top ───
        top = tk.Frame(self.root, bg=BG2, height=48)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Label(top, text="  Voice Transcription", bg=BG2, fg=WHITE,
                 font=("Segoe UI", 13, "bold")).pack(side="left", padx=10, pady=8)
        tk.Label(top, text="Hindi + English | Offline",
                 bg=BG2, fg=DIM, font=("Segoe UI", 9)).pack(side="left")

        # ─── Status ───
        sf = tk.Frame(self.root, bg="#111827", height=26)
        sf.pack(fill="x")
        sf.pack_propagate(False)
        self.dot = tk.Label(sf, text="●", bg="#111827", fg=GREEN, font=("", 10))
        self.dot.pack(side="left", padx=(12, 4))
        self.status = tk.Label(sf, text="...", bg="#111827", fg=GREY,
                               font=("Segoe UI", 9), anchor="w")
        self.status.pack(side="left", fill="x")

        # ─── Live ───
        lf = tk.Frame(self.root, bg="#0d1933", height=32)
        lf.pack(fill="x")
        lf.pack_propagate(False)
        tk.Label(lf, text=" LIVE", bg="#0d1933", fg=BLUE,
                 font=("Segoe UI", 8, "bold")).pack(side="left", padx=(10, 4))
        self.live = tk.Label(lf, text="", bg="#0d1933", fg=GREY,
                             font=("Segoe UI", 10), anchor="w")
        self.live.pack(side="left", fill="x", expand=True)

        # ─── Text ───
        tf = tk.Frame(self.root, bg=BG)
        tf.pack(fill="both", expand=True, padx=12, pady=(8, 4))
        self.textbox = scrolledtext.ScrolledText(
            tf, wrap=tk.WORD, font=("Consolas", 12),
            bg=BG3, fg=WHITE, insertbackground=BLUE,
            relief="flat", bd=0, padx=14, pady=12,
            spacing1=3, spacing3=3, state="disabled"
        )
        self.textbox.pack(fill="both", expand=True)

        # ─── Count ───
        self.count = tk.Label(self.root, text="0 words", bg=BG, fg=DIM,
                              font=("Segoe UI", 9), anchor="e")
        self.count.pack(fill="x", padx=14)

        # ─── Bottom ───
        bot = tk.Frame(self.root, bg=BG2)
        bot.pack(fill="x", side="bottom")

        self.timer_lbl = tk.Label(bot, text="0:00", bg=BG2, fg=DIM,
                                  font=("Consolas", 10))
        self.timer_lbl.pack(side="left", padx=14, pady=12)

        # Clear
        tk.Button(bot, text="  Clear", command=self._clear,
                  bg="#2d1b1b", fg="#f87171", font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, padx=14, pady=7, cursor="hand2",
                  activebackground="#3d2020", activeforeground="#f87171"
                  ).pack(side="left", padx=6, pady=10)

        # Copy
        self.copy_btn = tk.Button(bot, text="  Copy All", command=self._copy,
                                  bg="#1a2d1a", fg="#4ade80",
                                  font=("Segoe UI", 10, "bold"),
                                  relief="flat", bd=0, padx=14, pady=7,
                                  cursor="hand2",
                                  activebackground="#1f381f",
                                  activeforeground="#4ade80")
        self.copy_btn.pack(side="left", padx=0, pady=10)

        # Mic
        self.mic_btn = tk.Button(bot, text="  Bolein", command=self._toggle,
                                 bg=PURPLE, fg="white",
                                 font=("Segoe UI", 12, "bold"),
                                 relief="flat", bd=0, padx=24, pady=9,
                                 cursor="hand2",
                                 activebackground="#6d28d9",
                                 activeforeground="white")
        self.mic_btn.pack(side="right", padx=12, pady=10)

        # Keys
        self.root.bind("<space>", lambda e: self._toggle())
        self.root.bind("<Control-c>", lambda e: self._copy())

    # ── Toggle ────────────────────────────────────────────────────────────
    def _toggle(self):
        if self.is_listening:
            self._stop()
        else:
            self._start()

    def _start(self):
        self.is_listening = True
        self.stop_flag.clear()
        self.mic_btn.config(text="  Rokein", bg=RED, activebackground="#b91c1c")
        self._set_status("listening", "Sun rahe hain... bolte rahein")
        self._start_timer()
        threading.Thread(target=self._listen, daemon=True).start()

    def _stop(self):
        self.is_listening = False
        self.stop_flag.set()
        if self.process:
            try:
                self.process.terminate()
            except:
                pass
        self._stop_timer()
        self.mic_btn.config(text="  Bolein", bg=PURPLE, activebackground="#6d28d9")
        self._set_status("ready", "Ruk gaye — Copy karein ya dobara bolein")
        self.live.config(text="", fg=GREY)

    # ── Listen via PowerShell System.Speech ────────────────────────────────
    def _listen(self):
        """Windows built-in speech recognition - OFFLINE, no packages."""
        
        ps_code = '''
Add-Type -AssemblyName System.Speech
$re = New-Object System.Speech.Recognition.SpeechRecognitionEngine
$gr = New-Object System.Speech.Recognition.DictationGrammar
$re.LoadGrammar($gr)
$re.SetInputToDefaultAudioDevice()
$re.InitialSilenceTimeout = [TimeSpan]::FromSeconds(4)
$re.EndSilenceTimeout = [TimeSpan]::FromSeconds(1.5)
Write-Output "READY"
while($true){
    try{
        $r = $re.Recognize([TimeSpan]::FromSeconds(30))
        if($r -and $r.Text){
            Write-Output ("TEXT:" + $r.Text)
        }else{
            Write-Output "WAIT"
        }
    }catch{
        Write-Output ("ERR:" + $_.Exception.Message)
        break
    }
}
'''
        try:
            self.process = subprocess.Popen(
                ["powershell", "-NoProfile", "-NonInteractive",
                 "-ExecutionPolicy", "Bypass", "-Command", ps_code],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True, encoding="utf-8", errors="replace",
                creationflags=0x08000000  # CREATE_NO_WINDOW
            )

            for line in self.process.stdout:
                if self.stop_flag.is_set():
                    break
                line = line.strip()
                if not line:
                    continue

                if line == "READY":
                    self.root.after(0, lambda: self.live.config(
                        text="Bol sakte hain...", fg=GREEN))

                elif line.startswith("TEXT:"):
                    txt = line[5:].strip()
                    if txt:
                        self.root.after(0, lambda t=txt: self._add(t))

                elif line.startswith("ERR:"):
                    err = line[4:]
                    self.root.after(0, lambda e=err: self._set_status(
                        "error", f"Error: {e}"))
                    break

        except FileNotFoundError:
            self.root.after(0, lambda: self._set_status(
                "error", "PowerShell nahi mila — Windows 11 hai?"))
        except Exception as e:
            self.root.after(0, lambda: self._set_status(
                "error", f"Error: {e}"))
        finally:
            try:
                self.process.terminate()
            except:
                pass
            # Auto restart if still listening
            if self.is_listening and not self.stop_flag.is_set():
                time.sleep(0.5)
                threading.Thread(target=self._listen, daemon=True).start()

    # ── Helpers ────────────────────────────────────────────────────────────
    def _add(self, phrase):
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
            text="Bol sakte hain...", fg=GREY) if self.is_listening else None)

    def _set_status(self, state, text):
        c = {"ready": GREEN, "listening": BLUE, "error": RED, "warn": YELLOW}
        self.dot.config(fg=c.get(state, YELLOW))
        self.status.config(text=text)

    def _copy(self):
        if not self.full_text.strip():
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.full_text)
        self.copy_btn.config(text="  Copied!", fg="#86efac")
        self.root.after(2000, lambda: self.copy_btn.config(
            text="  Copy All", fg="#4ade80"))

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
        if self.process:
            try:
                self.process.terminate()
            except:
                pass
        self.root.destroy()


# ── Main ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    try:
        from ctypes import windll, byref, sizeof, c_int
        hwnd = windll.user32.GetParent(root.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, byref(c_int(1)), sizeof(c_int))
    except:
        pass
    app = VoiceApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
