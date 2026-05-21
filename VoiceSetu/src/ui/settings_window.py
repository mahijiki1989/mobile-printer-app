"""
Settings window for VoiceSetu.
Provides tabs for General, Audio, Models, Hotkeys, and About.
All changes are persisted via ConfigManager.
"""

import logging
from typing import Callable, List, Optional, Tuple

import customtkinter as ctk

from src.core.config import APP_VERSION, ConfigManager
from src.core.localization import Localization
from src.engine.recorder import AudioRecorder

logger = logging.getLogger(__name__)


class SettingsWindow(ctk.CTkToplevel):
    """Settings window with tabbed interface."""

    def __init__(
        self,
        parent,
        config: ConfigManager,
        locale: Localization,
        on_save: Optional[Callable] = None,
    ):
        super().__init__(parent)

        self._config = config
        self._locale = locale
        self._on_save = on_save

        self._setup_window()
        self._create_widgets()
        self._load_current_settings()

        self.grab_set()
        self.focus_set()

    def _setup_window(self) -> None:
        """Configure the settings window."""
        self.title(self._locale.get("settings_title"))
        self.geometry("550x480")
        self.resizable(False, False)
        self.transient(self.master)

        x = self.master.winfo_x() + 50
        y = self.master.winfo_y() + 50
        self.geometry(f"550x480+{x}+{y}")

    def _create_widgets(self) -> None:
        """Create the tabbed settings interface."""
        self._tabview = ctk.CTkTabview(self, width=520, height=400)
        self._tabview.pack(padx=15, pady=(15, 5), fill="both", expand=True)

        self._tab_general = self._tabview.add(self._locale.get("settings_general"))
        self._tab_audio = self._tabview.add(self._locale.get("settings_audio"))
        self._tab_models = self._tabview.add(self._locale.get("settings_models"))
        self._tab_hotkeys = self._tabview.add(self._locale.get("settings_hotkeys"))
        self._tab_about = self._tabview.add(self._locale.get("settings_about"))

        self._build_general_tab()
        self._build_audio_tab()
        self._build_models_tab()
        self._build_hotkeys_tab()
        self._build_about_tab()

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(5, 15), fill="x", padx=15)

        ctk.CTkButton(
            btn_frame,
            text=self._locale.get("btn_save"),
            command=self._save_settings,
            width=100,
            fg_color=("#2980b9", "#2980b9"),
            hover_color=("#3498db", "#3498db"),
        ).pack(side="right", padx=(5, 0))

        ctk.CTkButton(
            btn_frame,
            text=self._locale.get("btn_cancel"),
            command=self.destroy,
            width=100,
            fg_color=("#7f8c8d", "#555"),
            hover_color=("#95a5a6", "#666"),
        ).pack(side="right")

    def _build_general_tab(self) -> None:
        """Build the General settings tab."""
        frame = self._tab_general

        ctk.CTkLabel(frame, text=self._locale.get("lbl_language"), anchor="w").pack(
            fill="x", padx=10, pady=(10, 2)
        )
        self._ui_lang_var = ctk.StringVar(value=self._config.get("language", "en"))
        ctk.CTkOptionMenu(
            frame,
            values=["en", "hi"],
            variable=self._ui_lang_var,
            width=200,
        ).pack(padx=10, anchor="w")

        ctk.CTkLabel(frame, text=self._locale.get("lbl_theme"), anchor="w").pack(
            fill="x", padx=10, pady=(15, 2)
        )
        self._theme_var = ctk.StringVar(value=self._config.get("theme", "dark"))
        ctk.CTkOptionMenu(
            frame,
            values=["dark", "light"],
            variable=self._theme_var,
            width=200,
        ).pack(padx=10, anchor="w")

        ctk.CTkLabel(frame, text=self._locale.get("lbl_insertion_mode"), anchor="w").pack(
            fill="x", padx=10, pady=(15, 2)
        )
        self._insertion_var = ctk.StringVar(value=self._config.get("insertion_mode", "auto"))
        ctk.CTkOptionMenu(
            frame,
            values=["auto", "clipboard", "typing"],
            variable=self._insertion_var,
            width=200,
        ).pack(padx=10, anchor="w")

        self._minimize_tray_var = ctk.BooleanVar(
            value=self._config.get("minimize_to_tray", True)
        )
        ctk.CTkCheckBox(
            frame,
            text="Minimize to system tray",
            variable=self._minimize_tray_var,
        ).pack(padx=10, pady=(15, 5), anchor="w")

        self._preserve_clip_var = ctk.BooleanVar(
            value=self._config.get("preserve_clipboard", True)
        )
        ctk.CTkCheckBox(
            frame,
            text="Preserve clipboard content",
            variable=self._preserve_clip_var,
        ).pack(padx=10, pady=5, anchor="w")

    def _build_audio_tab(self) -> None:
        """Build the Audio settings tab."""
        frame = self._tab_audio

        ctk.CTkLabel(frame, text=self._locale.get("lbl_microphone"), anchor="w").pack(
            fill="x", padx=10, pady=(10, 2)
        )

        mics = AudioRecorder.get_microphones()
        mic_names = [f"{idx}: {name}" for idx, name in mics] if mics else ["Default"]
        self._mic_var = ctk.StringVar(value=mic_names[0] if mic_names else "Default")

        current_idx = self._config.get("microphone_index", -1)
        for idx, name in mics:
            if idx == current_idx:
                self._mic_var.set(f"{idx}: {name}")
                break

        ctk.CTkOptionMenu(
            frame,
            values=mic_names,
            variable=self._mic_var,
            width=350,
        ).pack(padx=10, anchor="w")

        ctk.CTkLabel(
            frame, text=self._locale.get("lbl_silence_threshold"), anchor="w"
        ).pack(fill="x", padx=10, pady=(15, 2))

        self._silence_var = ctk.DoubleVar(
            value=self._config.get("silence_threshold", 1.5)
        )
        silence_frame = ctk.CTkFrame(frame, fg_color="transparent")
        silence_frame.pack(fill="x", padx=10)

        self._silence_slider = ctk.CTkSlider(
            silence_frame,
            from_=0.5,
            to=5.0,
            number_of_steps=9,
            variable=self._silence_var,
            width=250,
        )
        self._silence_slider.pack(side="left")

        self._silence_label = ctk.CTkLabel(
            silence_frame, text=f"{self._silence_var.get():.1f}s", width=50
        )
        self._silence_label.pack(side="left", padx=10)
        self._silence_var.trace_add(
            "write", lambda *_: self._silence_label.configure(
                text=f"{self._silence_var.get():.1f}s"
            )
        )

        self._vad_var = ctk.BooleanVar(value=self._config.get("vad_enabled", True))
        ctk.CTkCheckBox(
            frame,
            text="Enable Voice Activity Detection (VAD)",
            variable=self._vad_var,
        ).pack(padx=10, pady=(15, 5), anchor="w")

    def _build_models_tab(self) -> None:
        """Build the Models settings tab."""
        frame = self._tab_models

        ctk.CTkLabel(frame, text=self._locale.get("lbl_model"), anchor="w").pack(
            fill="x", padx=10, pady=(10, 2)
        )

        model_options = ["tiny", "base", "small", "medium", "large-v2"]
        self._model_var = ctk.StringVar(value=self._config.get("model_size", "base"))
        ctk.CTkOptionMenu(
            frame,
            values=model_options,
            variable=self._model_var,
            width=200,
        ).pack(padx=10, anchor="w")

        info_text = (
            "Model sizes and approximate performance:\n"
            "  tiny   - ~39MB, fastest, lower accuracy\n"
            "  base   - ~74MB, fast, good accuracy (recommended)\n"
            "  small  - ~244MB, balanced speed/accuracy\n"
            "  medium - ~769MB, slower, better accuracy\n"
            "  large  - ~1.5GB, slowest, best accuracy\n\n"
            "Smaller models work better on older hardware.\n"
            "Models download automatically on first use."
        )
        ctk.CTkLabel(
            frame,
            text=info_text,
            anchor="w",
            justify="left",
            font=ctk.CTkFont(size=11),
            text_color=("#555", "#aaa"),
        ).pack(fill="x", padx=10, pady=(15, 5))

        ctk.CTkLabel(frame, text="Compute Type:", anchor="w").pack(
            fill="x", padx=10, pady=(10, 2)
        )
        self._compute_var = ctk.StringVar(value=self._config.get("compute_type", "int8"))
        ctk.CTkOptionMenu(
            frame,
            values=["int8", "float32"],
            variable=self._compute_var,
            width=200,
        ).pack(padx=10, anchor="w")

        ctk.CTkLabel(
            frame, text=self._locale.get("lbl_auto_detect"), anchor="w"
        ).pack(fill="x", padx=10, pady=(15, 2))
        self._auto_detect_var = ctk.BooleanVar(
            value=self._config.get("auto_detect_language", False)
        )
        ctk.CTkCheckBox(
            frame,
            text=self._locale.get("lbl_auto_detect"),
            variable=self._auto_detect_var,
        ).pack(padx=10, anchor="w")

    def _build_hotkeys_tab(self) -> None:
        """Build the Hotkeys settings tab."""
        frame = self._tab_hotkeys

        ctk.CTkLabel(frame, text=self._locale.get("lbl_hotkey_ptt"), anchor="w").pack(
            fill="x", padx=10, pady=(10, 2)
        )
        self._ptt_var = ctk.StringVar(
            value=self._config.get("hotkey_ptt", "ctrl+shift+space")
        )
        ctk.CTkEntry(frame, textvariable=self._ptt_var, width=250).pack(
            padx=10, anchor="w"
        )

        ctk.CTkLabel(frame, text=self._locale.get("lbl_hotkey_toggle"), anchor="w").pack(
            fill="x", padx=10, pady=(15, 2)
        )
        self._toggle_var = ctk.StringVar(
            value=self._config.get("hotkey_toggle", "ctrl+shift+d")
        )
        ctk.CTkEntry(frame, textvariable=self._toggle_var, width=250).pack(
            padx=10, anchor="w"
        )

        ctk.CTkLabel(
            frame,
            text=(
                "Hotkey format examples:\n"
                "  ctrl+shift+space\n"
                "  ctrl+shift+d\n"
                "  ctrl+alt+r\n\n"
                "Push-to-Talk: Hold to record, release to stop.\n"
                "Toggle: Press once to start, press again to stop."
            ),
            anchor="w",
            justify="left",
            font=ctk.CTkFont(size=11),
            text_color=("#555", "#aaa"),
        ).pack(fill="x", padx=10, pady=(15, 5))

    def _build_about_tab(self) -> None:
        """Build the About tab."""
        frame = self._tab_about

        ctk.CTkLabel(
            frame,
            text="VoiceSetu",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            frame,
            text=f"{self._locale.get('about_version')}: {APP_VERSION}",
            font=ctk.CTkFont(size=12),
        ).pack(pady=2)

        ctk.CTkLabel(
            frame,
            text=self._locale.get("about_description"),
            wraplength=450,
            justify="center",
            font=ctk.CTkFont(size=11),
            text_color=("#555", "#aaa"),
        ).pack(pady=(15, 10), padx=20)

        ctk.CTkLabel(
            frame,
            text=self._locale.get("about_privacy"),
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#27ae60", "#2ecc71"),
        ).pack(pady=10)

    def _load_current_settings(self) -> None:
        """Load current settings into the form fields."""
        pass

    def _save_settings(self) -> None:
        """Save all settings from the form."""
        self._config.set("language", self._ui_lang_var.get())
        self._config.set("theme", self._theme_var.get())
        self._config.set("insertion_mode", self._insertion_var.get())
        self._config.set("minimize_to_tray", self._minimize_tray_var.get())
        self._config.set("preserve_clipboard", self._preserve_clip_var.get())
        self._config.set("silence_threshold", self._silence_var.get())
        self._config.set("vad_enabled", self._vad_var.get())
        self._config.set("model_size", self._model_var.get())
        self._config.set("compute_type", self._compute_var.get())
        self._config.set("auto_detect_language", self._auto_detect_var.get())
        self._config.set("hotkey_ptt", self._ptt_var.get())
        self._config.set("hotkey_toggle", self._toggle_var.get())

        mic_str = self._mic_var.get()
        if mic_str and ":" in mic_str:
            try:
                mic_idx = int(mic_str.split(":")[0])
                self._config.set("microphone_index", mic_idx)
            except ValueError:
                self._config.set("microphone_index", -1)
        else:
            self._config.set("microphone_index", -1)

        self._config.save()

        if self._on_save:
            self._on_save()

        self.destroy()
