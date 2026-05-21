"""
Configuration manager for VoiceSetu.
Handles loading, saving, and providing default settings.
Config is stored as JSON in the user's AppData directory.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict


APP_NAME = "VoiceSetu"
APP_VERSION = "1.0.0"

DEFAULT_CONFIG: Dict[str, Any] = {
    "language": "en",
    "speech_language": "en",
    "auto_detect_language": False,
    "theme": "dark",
    "model_size": "tiny",
    "model_path": "",
    "microphone_index": -1,
    "hotkey_ptt": "ctrl+shift+space",
    "hotkey_toggle": "ctrl+shift+d",
    "insertion_mode": "auto",
    "silence_threshold": 1.0,
    "sample_rate": 16000,
    "show_mini_window": True,
    "start_minimized": False,
    "minimize_to_tray": True,
    "auto_start_listening": False,
    "max_history_items": 200,
    "preserve_clipboard": True,
    "compute_type": "int8",
    "beam_size": 1,
    "vad_enabled": True,
    "vad_threshold": 0.3,
}


def get_app_data_dir() -> Path:
    """Get the application data directory for storing config and data."""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base = Path.home() / ".config"
    app_dir = base / APP_NAME
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


def get_models_dir() -> Path:
    """Get the directory where whisper models are stored."""
    models_dir = get_app_data_dir() / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    return models_dir


def get_config_path() -> Path:
    """Get the path to the config file."""
    return get_app_data_dir() / "config.json"


def get_history_path() -> Path:
    """Get the path to the history file."""
    return get_app_data_dir() / "history.json"


def get_resource_path(relative_path: str) -> Path:
    """Get the absolute path to a resource, works for dev and PyInstaller."""
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent.parent
    return base_path / relative_path


class ConfigManager:
    """Manages application configuration with load/save/defaults."""

    def __init__(self):
        self._config: Dict[str, Any] = dict(DEFAULT_CONFIG)
        self._config_path = get_config_path()
        self.load()

    def load(self) -> None:
        """Load configuration from disk. Falls back to defaults if not found."""
        if self._config_path.exists():
            try:
                with open(self._config_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                for key in DEFAULT_CONFIG:
                    if key in saved:
                        self._config[key] = saved[key]
            except (json.JSONDecodeError, IOError, OSError):
                self._config = dict(DEFAULT_CONFIG)
        else:
            self._config = dict(DEFAULT_CONFIG)

    def save(self) -> None:
        """Save current configuration to disk."""
        try:
            self._config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._config_path, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=4, ensure_ascii=False)
        except (IOError, OSError):
            pass

    def get(self, key: str, default: Any = None) -> Any:
        """Get a config value by key."""
        return self._config.get(key, default if default is not None else DEFAULT_CONFIG.get(key))

    def set(self, key: str, value: Any) -> None:
        """Set a config value and save."""
        self._config[key] = value
        self.save()

    def get_all(self) -> Dict[str, Any]:
        """Get a copy of all config values."""
        return dict(self._config)

    def reset(self) -> None:
        """Reset to default configuration."""
        self._config = dict(DEFAULT_CONFIG)
        self.save()

    @property
    def model_size(self) -> str:
        return self._config.get("model_size", "base")

    @property
    def speech_language(self) -> str:
        return self._config.get("speech_language", "en")

    @property
    def ui_language(self) -> str:
        return self._config.get("language", "en")

    @property
    def theme(self) -> str:
        return self._config.get("theme", "dark")

    @property
    def insertion_mode(self) -> str:
        return self._config.get("insertion_mode", "auto")

    @property
    def microphone_index(self) -> int:
        return self._config.get("microphone_index", -1)

    @property
    def hotkey_ptt(self) -> str:
        return self._config.get("hotkey_ptt", "ctrl+shift+space")

    @property
    def hotkey_toggle(self) -> str:
        return self._config.get("hotkey_toggle", "ctrl+shift+d")
