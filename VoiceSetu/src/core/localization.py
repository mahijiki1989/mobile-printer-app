"""
Localization manager for VoiceSetu.
Loads language strings from JSON locale files.
Supports English and Hindi with fallback to English.
"""

import json
from pathlib import Path
from typing import Dict, Optional

from src.core.config import get_resource_path


class Localization:
    """Handles loading and retrieving localized strings."""

    SUPPORTED_LANGUAGES = {"en": "English", "hi": "हिंदी"}

    def __init__(self, language: str = "en"):
        self._language = language
        self._strings: Dict[str, str] = {}
        self._fallback_strings: Dict[str, str] = {}
        self._load_fallback()
        self._load_language(language)

    def _get_locale_path(self, lang: str) -> Path:
        """Get the path to a locale JSON file."""
        return get_resource_path(f"locales/{lang}.json")

    def _load_fallback(self) -> None:
        """Load English as fallback."""
        path = self._get_locale_path("en")
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self._fallback_strings = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._fallback_strings = {}

    def _load_language(self, lang: str) -> None:
        """Load a specific language file."""
        path = self._get_locale_path(lang)
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self._strings = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._strings = dict(self._fallback_strings)
        else:
            self._strings = dict(self._fallback_strings)

    def set_language(self, language: str) -> None:
        """Switch the active language."""
        self._language = language
        self._load_language(language)

    def get(self, key: str, default: Optional[str] = None) -> str:
        """Get a localized string by key. Falls back to English, then key name."""
        value = self._strings.get(key)
        if value is not None:
            return value
        value = self._fallback_strings.get(key)
        if value is not None:
            return value
        return default if default is not None else key

    @property
    def language(self) -> str:
        return self._language

    def __getitem__(self, key: str) -> str:
        return self.get(key)
