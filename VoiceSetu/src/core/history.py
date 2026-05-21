"""
History manager for VoiceSetu.
Stores transcription results with timestamps and metadata.
Persists to JSON file in AppData.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from src.core.config import get_history_path

logger = logging.getLogger(__name__)


class HistoryItem:
    """Represents a single transcription history entry."""

    def __init__(
        self,
        text: str,
        language: str,
        timestamp: Optional[str] = None,
        confidence: float = 0.0,
    ):
        self.text = text
        self.language = language
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.confidence = confidence

    def to_dict(self) -> Dict:
        return {
            "text": self.text,
            "language": self.language,
            "timestamp": self.timestamp,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "HistoryItem":
        return cls(
            text=data.get("text", ""),
            language=data.get("language", "en"),
            timestamp=data.get("timestamp"),
            confidence=data.get("confidence", 0.0),
        )


class HistoryManager:
    """
    Manages transcription history with persistence.
    Stores items in memory and syncs to disk.
    """

    def __init__(self, max_items: int = 200):
        self._items: List[HistoryItem] = []
        self._max_items = max_items
        self._history_path = get_history_path()
        self.load()

    @property
    def items(self) -> List[HistoryItem]:
        return list(self._items)

    @property
    def count(self) -> int:
        return len(self._items)

    def add(self, text: str, language: str, confidence: float = 0.0) -> HistoryItem:
        """Add a new transcription to history."""
        item = HistoryItem(text=text, language=language, confidence=confidence)
        self._items.insert(0, item)

        if len(self._items) > self._max_items:
            self._items = self._items[: self._max_items]

        self.save()
        return item

    def remove(self, index: int) -> bool:
        """Remove item at index."""
        if 0 <= index < len(self._items):
            self._items.pop(index)
            self.save()
            return True
        return False

    def edit(self, index: int, new_text: str) -> bool:
        """Edit the text of an item at index."""
        if 0 <= index < len(self._items):
            self._items[index].text = new_text
            self.save()
            return True
        return False

    def get(self, index: int) -> Optional[HistoryItem]:
        """Get item at index."""
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def clear(self) -> None:
        """Clear all history."""
        self._items.clear()
        self.save()

    def load(self) -> None:
        """Load history from disk."""
        if self._history_path.exists():
            try:
                with open(self._history_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._items = [HistoryItem.from_dict(item) for item in data]
            except (json.JSONDecodeError, IOError, OSError) as e:
                logger.error(f"Failed to load history: {e}")
                self._items = []
        else:
            self._items = []

    def save(self) -> None:
        """Save history to disk."""
        try:
            self._history_path.parent.mkdir(parents=True, exist_ok=True)
            data = [item.to_dict() for item in self._items]
            with open(self._history_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except (IOError, OSError) as e:
            logger.error(f"Failed to save history: {e}")

    def export_to_txt(self, filepath: str) -> bool:
        """Export history to a text file."""
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("VoiceSetu - Transcription History\n")
                f.write("=" * 50 + "\n\n")
                for item in self._items:
                    f.write(f"[{item.timestamp}] ({item.language})\n")
                    f.write(f"{item.text}\n")
                    f.write("-" * 30 + "\n")
            return True
        except (IOError, OSError) as e:
            logger.error(f"Failed to export history: {e}")
            return False
