"""
Main application window for VoiceSetu.
Provides the primary dictation interface with status,
language selection, history view, and controls.
"""

import logging
import threading
import time
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
from typing import Optional

import customtkinter as ctk

from src.core.config import APP_VERSION, ConfigManager
from src.core.history import HistoryManager
from src.core.hotkeys import HotkeyManager
from src.core.localization import Localization
from src.core.text_inserter import TextInserter
from src.core.tray import TrayManager
from src.engine.recorder import AudioRecorder
from src.engine.transcriber import TranscriptionEngine
from src.ui.mini_window import MiniWindow
from src.ui.settings_window import SettingsWindow

logger = logging.getLogger(__name__)


class MainWindow(ctk.CTk):
    """Main application window for VoiceSetu."""

    def __init__(self):
        super().__init__()

        self._config = ConfigManager()
        self._locale = Localization(self._config.ui_language)
        self._history = HistoryManager(max_items=self._config.get("max_history_items", 200))
        self._inserter = TextInserter(
            mode=self._config.insertion_mode,
            preserve_clipboard=self._config.get("preserve_clipboard", True),
        )
        self._recorder = AudioRecorder(
            sample_rate=self._config.get("sample_rate", 16000),
            silence_threshold=self._config.get("silence_threshold", 1.5),
            device_index=self._config.microphone_index,
            vad_enabled=self._config.get("vad_enabled", True),
        )
        self._transcriber = TranscriptionEngine(
            model_size=self._config.model_size,
            compute_type=self._config.get("compute_type", "int8"),
            model_path=self._config.get("model_path", ""),
            beam_size=self._config.get("beam_size", 5),
        )
        self._hotkey_manager = HotkeyManager()
        self._tray_manager: Optional[TrayManager] = None
        self._mini_window: Optional[MiniWindow] = None

        self._is_dictating = False
        self._is_ptt_active = False

        self._setup_window()
        self._create_widgets()
        self._setup_hotkeys()
        self._setup_tray()
        self._load_model_async()
        self._recorder.set_on_silence_detected(self._on_silence_detected)

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_window(self) -> None:
        """Configure the main window."""
        ctk.set_appearance_mode(self._config.theme)
        ctk.set_default_color_theme("blue")

        self.title(f"VoiceSetu - {self._locale.get('tagline')}")
        self.geometry("680x560")
        self.minsize(600, 500)

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - 680) // 2
        y = (screen_h - 560) // 2
        self.geometry(f"680x560+{x}+{y}")

    def _create_widgets(self) -> None:
        """Create all main window widgets."""
        header = ctk.CTkFrame(self, fg_color="transparent", height=60)
        header.pack(fill="x", padx=15, pady=(10, 0))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="VoiceSetu",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(side="left", padx=5)

        ctk.CTkLabel(
            header,
            text=self._locale.get("tagline"),
            font=ctk.CTkFont(size=12),
            text_color=("#666", "#999"),
        ).pack(side="left", padx=(5, 0), pady=(6, 0))

        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right")

        ctk.CTkButton(
            btn_frame,
            text="\u2699",
            width=36,
            height=36,
            corner_radius=8,
            fg_color=("#ddd", "#333"),
            hover_color=("#ccc", "#444"),
            text_color=("#333", "#eee"),
            font=ctk.CTkFont(size=18),
            command=self._open_settings,
        ).pack(side="right", padx=2)

        self._mini_btn = ctk.CTkButton(
            btn_frame,
            text="\u25A0",
            width=36,
            height=36,
            corner_radius=8,
            fg_color=("#ddd", "#333"),
            hover_color=("#ccc", "#444"),
            text_color=("#333", "#eee"),
            font=ctk.CTkFont(size=14),
            command=self._toggle_mini_window,
        )
        self._mini_btn.pack(side="right", padx=2)

        status_frame = ctk.CTkFrame(self, corner_radius=10)
        status_frame.pack(fill="x", padx=15, pady=10)

        self._status_dot = ctk.CTkLabel(
            status_frame,
            text="\u25CF",
            font=ctk.CTkFont(size=20),
            text_color="#666666",
            width=30,
        )
        self._status_dot.pack(side="left", padx=(15, 5), pady=12)

        self._status_label = ctk.CTkLabel(
            status_frame,
            text=self._locale.get("status_idle"),
            font=ctk.CTkFont(size=14),
        )
        self._status_label.pack(side="left", padx=5, pady=12)

        self._lang_label = ctk.CTkLabel(
            status_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=("#888", "#777"),
        )
        self._lang_label.pack(side="right", padx=15, pady=12)

        controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        controls_frame.pack(fill="x", padx=15, pady=5)

        self._dictate_btn = ctk.CTkButton(
            controls_frame,
            text=self._locale.get("btn_start"),
            font=ctk.CTkFont(size=14, weight="bold"),
            height=44,
            corner_radius=10,
            fg_color=("#2980b9", "#2980b9"),
            hover_color=("#3498db", "#3498db"),
            command=self._toggle_dictation,
        )
        self._dictate_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        ctk.CTkLabel(
            controls_frame,
            text=self._locale.get("lbl_language") + ":",
            font=ctk.CTkFont(size=12),
        ).pack(side="left", padx=(10, 5))

        lang_values = ["English", "Hindi", "Auto"]
        current_speech_lang = self._config.get("speech_language", "en")
        lang_map_display = {"en": "English", "hi": "Hindi", "auto": "Auto"}
        self._speech_lang_var = ctk.StringVar(
            value=lang_map_display.get(current_speech_lang, "English")
        )

        self._lang_menu = ctk.CTkOptionMenu(
            controls_frame,
            values=lang_values,
            variable=self._speech_lang_var,
            width=100,
            command=self._on_language_changed,
        )
        self._lang_menu.pack(side="left", padx=5)

        history_header = ctk.CTkFrame(self, fg_color="transparent")
        history_header.pack(fill="x", padx=15, pady=(10, 2))

        ctk.CTkLabel(
            history_header,
            text=self._locale.get("history_title"),
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(side="left")

        ctk.CTkButton(
            history_header,
            text=self._locale.get("btn_export_history"),
            width=100,
            height=28,
            font=ctk.CTkFont(size=11),
            fg_color=("#7f8c8d", "#555"),
            hover_color=("#95a5a6", "#666"),
            command=self._export_history,
        ).pack(side="right", padx=(5, 0))

        ctk.CTkButton(
            history_header,
            text=self._locale.get("btn_clear_history"),
            width=100,
            height=28,
            font=ctk.CTkFont(size=11),
            fg_color=("#c0392b", "#8b0000"),
            hover_color=("#e74c3c", "#a00000"),
            command=self._clear_history,
        ).pack(side="right")

        self._history_frame = ctk.CTkScrollableFrame(
            self,
            corner_radius=8,
            fg_color=("#f5f5f5", "#1a1a2e"),
        )
        self._history_frame.pack(fill="both", expand=True, padx=15, pady=(5, 10))

        self._refresh_history_view()

        footer = ctk.CTkFrame(self, fg_color="transparent", height=30)
        footer.pack(fill="x", padx=15, pady=(0, 8))
        footer.pack_propagate(False)

        ctk.CTkLabel(
            footer,
            text=self._locale.get("about_privacy"),
            font=ctk.CTkFont(size=10),
            text_color=("#27ae60", "#2ecc71"),
        ).pack(side="left")

        ctk.CTkLabel(
            footer,
            text=f"v{APP_VERSION}",
            font=ctk.CTkFont(size=10),
            text_color=("#999", "#666"),
        ).pack(side="right")

    def _set_status(self, status: str, text: str = "") -> None:
        """Update the status indicator."""
        color_map = {
            "idle": "#666666",
            "ready": "#27ae60",
            "listening": "#e74c3c",
            "processing": "#f39c12",
            "inserted": "#2ecc71",
            "error": "#e74c3c",
            "loading": "#f39c12",
        }
        self._status_dot.configure(text_color=color_map.get(status, "#666"))
        display_text = text if text else self._locale.get(f"status_{status}", status)
        self._status_label.configure(text=display_text)

        if self._mini_window:
            mini_status_map = {
                "idle": MiniWindow.STATUS_IDLE,
                "ready": MiniWindow.STATUS_IDLE,
                "listening": MiniWindow.STATUS_LISTENING,
                "processing": MiniWindow.STATUS_PROCESSING,
                "inserted": MiniWindow.STATUS_IDLE,
                "error": MiniWindow.STATUS_IDLE,
                "loading": MiniWindow.STATUS_PROCESSING,
            }
            self._mini_window.set_status(
                mini_status_map.get(status, MiniWindow.STATUS_IDLE),
                display_text,
            )

    def _load_model_async(self) -> None:
        """Load the transcription model in background."""
        self._set_status("loading", self._locale.get("status_model_loading"))

        def on_complete(success):
            if success:
                self.after(0, lambda: self._set_status("ready", self._locale.get("status_ready")))
            else:
                self.after(0, lambda: self._set_status("error", self._locale.get("error_model_load")))

        def on_progress(msg):
            self.after(0, lambda: self._status_label.configure(text=msg))

        self._transcriber.load_model_async(on_complete=on_complete, on_progress=on_progress)

    def _toggle_dictation(self) -> None:
        """Toggle dictation on/off."""
        if self._is_dictating:
            self._stop_dictation()
        else:
            self._start_dictation()

    def _start_dictation(self) -> None:
        """Start recording audio for dictation."""
        if not self._transcriber.is_loaded:
            self._set_status("error", self._locale.get("error_model_load"))
            return

        if self._recorder.start_recording():
            self._is_dictating = True
            self._set_status("listening", self._locale.get("status_listening"))
            self._dictate_btn.configure(
                text=self._locale.get("btn_stop"),
                fg_color=("#c0392b", "#c0392b"),
                hover_color=("#e74c3c", "#e74c3c"),
            )
        else:
            self._set_status("error", self._locale.get("error_recording"))

    def _stop_dictation(self) -> None:
        """Stop recording and process the audio."""
        if not self._is_dictating:
            return

        self._is_dictating = False
        self._dictate_btn.configure(
            text=self._locale.get("btn_start"),
            fg_color=("#2980b9", "#2980b9"),
            hover_color=("#3498db", "#3498db"),
        )

        audio_data = self._recorder.stop_recording()

        if audio_data is None or len(audio_data) < 1600:
            self._set_status("ready", self._locale.get("status_ready"))
            return

        self._set_status("processing", self._locale.get("status_processing"))

        def process():
            try:
                lang_map = {"English": "en", "Hindi": "hi", "Auto": "auto"}
                speech_lang = lang_map.get(self._speech_lang_var.get(), "en")
                auto_detect = self._config.get("auto_detect_language", False) or speech_lang == "auto"

                text, detected_lang, confidence = self._transcriber.transcribe(
                    audio_data,
                    language=speech_lang if not auto_detect else "en",
                    auto_detect=auto_detect,
                )

                if text:
                    self.after(0, lambda: self._on_transcription_complete(text, detected_lang, confidence))
                else:
                    self.after(0, lambda: self._set_status("ready", self._locale.get("status_ready")))

            except Exception as e:
                logger.error(f"Transcription error: {e}")
                self.after(0, lambda: self._set_status("error", self._locale.get("error_transcription")))

        threading.Thread(target=process, daemon=True).start()

    def _on_transcription_complete(self, text: str, language: str, confidence: float) -> None:
        """Handle completed transcription."""
        success = self._inserter.insert_text(text)

        if success:
            self._set_status("inserted", self._locale.get("status_inserted"))
        else:
            self._set_status("ready", self._locale.get("error_insertion"))

        self._history.add(text=text, language=language, confidence=confidence)
        self._refresh_history_view()
        self._lang_label.configure(text=f"[{language}] {confidence:.0%}")

        self.after(2000, lambda: self._set_status("ready", self._locale.get("status_ready")))

    def _on_silence_detected(self) -> None:
        """Called when silence is detected during recording."""
        if self._is_dictating and not self._is_ptt_active:
            self.after(0, self._stop_dictation)

    def _on_language_changed(self, value: str) -> None:
        """Handle speech language change."""
        lang_map = {"English": "en", "Hindi": "hi", "Auto": "auto"}
        self._config.set("speech_language", lang_map.get(value, "en"))

    def _refresh_history_view(self) -> None:
        """Refresh the history list display."""
        for widget in self._history_frame.winfo_children():
            widget.destroy()

        if self._history.count == 0:
            ctk.CTkLabel(
                self._history_frame,
                text=self._locale.get("history_empty"),
                text_color=("#999", "#666"),
                font=ctk.CTkFont(size=12),
            ).pack(pady=30)
            return

        for idx, item in enumerate(self._history.items[:50]):
            self._create_history_item_widget(idx, item)

    def _create_history_item_widget(self, index: int, item) -> None:
        """Create a widget for a single history item."""
        frame = ctk.CTkFrame(
            self._history_frame,
            corner_radius=6,
            fg_color=("#ffffff", "#252545"),
            border_width=1,
            border_color=("#e0e0e0", "#333355"),
        )
        frame.pack(fill="x", pady=2, padx=2)

        top_row = ctk.CTkFrame(frame, fg_color="transparent")
        top_row.pack(fill="x", padx=8, pady=(6, 2))

        ctk.CTkLabel(
            top_row,
            text=f"{item.timestamp}  [{item.language}]",
            font=ctk.CTkFont(size=10),
            text_color=("#888", "#777"),
        ).pack(side="left")

        btn_row = ctk.CTkFrame(top_row, fg_color="transparent")
        btn_row.pack(side="right")

        ctk.CTkButton(
            btn_row,
            text=self._locale.get("btn_copy"),
            width=50,
            height=22,
            font=ctk.CTkFont(size=10),
            fg_color=("#bbb", "#444"),
            hover_color=("#aaa", "#555"),
            command=lambda i=index: self._copy_history_item(i),
        ).pack(side="left", padx=1)

        ctk.CTkButton(
            btn_row,
            text=self._locale.get("btn_reinsert"),
            width=60,
            height=22,
            font=ctk.CTkFont(size=10),
            fg_color=("#2980b9", "#2980b9"),
            hover_color=("#3498db", "#3498db"),
            command=lambda i=index: self._reinsert_history_item(i),
        ).pack(side="left", padx=1)

        ctk.CTkButton(
            btn_row,
            text=self._locale.get("btn_delete"),
            width=50,
            height=22,
            font=ctk.CTkFont(size=10),
            fg_color=("#c0392b", "#8b0000"),
            hover_color=("#e74c3c", "#a00000"),
            command=lambda i=index: self._delete_history_item(i),
        ).pack(side="left", padx=1)

        display_text = item.text if len(item.text) <= 120 else item.text[:120] + "..."
        text_label = ctk.CTkLabel(
            frame,
            text=display_text,
            font=ctk.CTkFont(size=12),
            anchor="w",
            justify="left",
            wraplength=580,
        )
        text_label.pack(fill="x", padx=8, pady=(2, 6))

    def _copy_history_item(self, index: int) -> None:
        """Copy a history item to clipboard."""
        item = self._history.get(index)
        if item:
            self._inserter.copy_to_clipboard(item.text)

    def _reinsert_history_item(self, index: int) -> None:
        """Re-insert a history item into the focused app."""
        item = self._history.get(index)
        if item:
            self.after(300, lambda: self._inserter.insert_text(item.text))

    def _delete_history_item(self, index: int) -> None:
        """Delete a history item."""
        self._history.remove(index)
        self._refresh_history_view()

    def _clear_history(self) -> None:
        """Clear all history after confirmation."""
        if messagebox.askyesno(
            self._locale.get("app_name"),
            self._locale.get("confirm_clear_history"),
        ):
            self._history.clear()
            self._refresh_history_view()

    def _export_history(self) -> None:
        """Export history to a text file."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Export History",
        )
        if filepath:
            if self._history.export_to_txt(filepath):
                messagebox.showinfo("VoiceSetu", self._locale.get("notification_exported"))

    def _open_settings(self) -> None:
        """Open the settings window."""
        SettingsWindow(
            self,
            config=self._config,
            locale=self._locale,
            on_save=self._on_settings_saved,
        )

    def _on_settings_saved(self) -> None:
        """Handle settings being saved - apply changes."""
        new_theme = self._config.theme
        ctk.set_appearance_mode(new_theme)

        new_lang = self._config.ui_language
        if new_lang != self._locale.language:
            self._locale.set_language(new_lang)

        self._inserter.set_mode(self._config.insertion_mode)
        self._inserter.set_preserve_clipboard(self._config.get("preserve_clipboard", True))
        self._recorder.set_device(self._config.microphone_index)
        self._recorder.set_silence_threshold(self._config.get("silence_threshold", 1.5))

        if self._config.model_size != self._transcriber._model_size:
            self._transcriber.change_model(
                model_size=self._config.model_size,
                compute_type=self._config.get("compute_type", "int8"),
            )
            self._load_model_async()

        self._setup_hotkeys()

    def _setup_hotkeys(self) -> None:
        """Register global hotkeys."""
        self._hotkey_manager.update_hotkeys(
            ptt_hotkey=self._config.hotkey_ptt,
            toggle_hotkey=self._config.hotkey_toggle,
            toggle_callback=self._on_toggle_hotkey,
            ptt_start=self._on_ptt_start,
            ptt_stop=self._on_ptt_stop,
        )

    def _on_toggle_hotkey(self) -> None:
        """Handle toggle hotkey press."""
        self.after(0, self._toggle_dictation)

    def _on_ptt_start(self) -> None:
        """Handle push-to-talk press."""
        self._is_ptt_active = True
        self.after(0, self._start_dictation)

    def _on_ptt_stop(self) -> None:
        """Handle push-to-talk release."""
        self._is_ptt_active = False
        self.after(0, self._stop_dictation)

    def _setup_tray(self) -> None:
        """Setup system tray icon."""
        self._tray_manager = TrayManager(
            on_show=self._show_from_tray,
            on_quit=self._quit_app,
            on_toggle_dictation=lambda: self.after(0, self._toggle_dictation),
        )
        self._tray_manager.start()

    def _toggle_mini_window(self) -> None:
        """Toggle the floating mini window."""
        if self._mini_window is None or not self._mini_window.winfo_exists():
            self._mini_window = MiniWindow(
                self,
                on_toggle=self._toggle_dictation,
                on_open_main=self._show_from_tray,
            )
        else:
            self._mini_window.destroy()
            self._mini_window = None

    def _show_from_tray(self) -> None:
        """Show the main window from tray."""
        self.after(0, self.deiconify)
        self.after(0, self.lift)
        self.after(0, self.focus_force)

    def _on_close(self) -> None:
        """Handle window close button."""
        if self._config.get("minimize_to_tray", True):
            self.withdraw()
        else:
            self._quit_app()

    def _quit_app(self) -> None:
        """Fully quit the application."""
        if self._is_dictating:
            self._recorder.stop_recording()

        self._hotkey_manager.unregister_all()

        if self._tray_manager:
            self._tray_manager.stop()

        if self._mini_window and self._mini_window.winfo_exists():
            self._mini_window.destroy()

        self._transcriber.unload_model()
        self.quit()
        self.destroy()
