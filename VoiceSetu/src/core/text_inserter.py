"""
Text insertion module for VoiceSetu.
Inserts transcribed text into the currently focused application.

Strategy order:
1. Clipboard paste (Ctrl+V) - fastest and most reliable
2. Simulated typing - fallback for apps that block paste
3. Copy-only - last resort, just places text on clipboard

Preserves original clipboard content when possible.
"""

import ctypes
import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)


def _get_clipboard_text() -> Optional[str]:
    """Get current clipboard text content (Windows API)."""
    try:
        import pyperclip
        return pyperclip.paste()
    except Exception:
        return None


def _set_clipboard_text(text: str) -> bool:
    """Set clipboard text content."""
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except Exception as e:
        logger.error(f"Failed to set clipboard: {e}")
        return False


def _simulate_paste() -> bool:
    """Simulate Ctrl+V keystroke to paste from clipboard."""
    try:
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32

        VK_CONTROL = 0x11
        VK_V = 0x56
        KEYEVENTF_KEYUP = 0x0002

        user32.keybd_event(VK_CONTROL, 0, 0, 0)
        time.sleep(0.02)
        user32.keybd_event(VK_V, 0, 0, 0)
        time.sleep(0.02)
        user32.keybd_event(VK_V, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(0.02)
        user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(0.05)

        return True
    except Exception as e:
        logger.error(f"Paste simulation failed: {e}")
        return False


def _simulate_typing(text: str) -> bool:
    """Simulate keyboard typing character by character."""
    try:
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32

        for char in text:
            code_point = ord(char)
            # Use SendInput with UNICODE flag for proper character support
            # This handles Hindi/Unicode characters correctly
            INPUT_KEYBOARD = 1
            KEYEVENTF_UNICODE = 0x0004
            KEYEVENTF_KEYUP = 0x0002

            class KEYBDINPUT(ctypes.Structure):
                _fields_ = [
                    ("wVk", ctypes.c_ushort),
                    ("wScan", ctypes.c_ushort),
                    ("dwFlags", ctypes.c_ulong),
                    ("time", ctypes.c_ulong),
                    ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
                ]

            class INPUT(ctypes.Structure):
                class _INPUT(ctypes.Union):
                    _fields_ = [("ki", KEYBDINPUT)]
                _fields_ = [
                    ("type", ctypes.c_ulong),
                    ("ii", _INPUT),
                ]

            # Key down
            inp_down = INPUT()
            inp_down.type = INPUT_KEYBOARD
            inp_down.ii.ki.wVk = 0
            inp_down.ii.ki.wScan = code_point
            inp_down.ii.ki.dwFlags = KEYEVENTF_UNICODE
            inp_down.ii.ki.time = 0
            inp_down.ii.ki.dwExtraInfo = None

            # Key up
            inp_up = INPUT()
            inp_up.type = INPUT_KEYBOARD
            inp_up.ii.ki.wVk = 0
            inp_up.ii.ki.wScan = code_point
            inp_up.ii.ki.dwFlags = KEYEVENTF_UNICODE | KEYEVENTF_KEYUP
            inp_up.ii.ki.time = 0
            inp_up.ii.ki.dwExtraInfo = None

            user32.SendInput(1, ctypes.byref(inp_down), ctypes.sizeof(INPUT))
            user32.SendInput(1, ctypes.byref(inp_up), ctypes.sizeof(INPUT))
            time.sleep(0.01)

        return True
    except Exception as e:
        logger.error(f"Typing simulation failed: {e}")
        return False


class TextInserter:
    """
    Handles inserting transcribed text into the active application.
    Supports multiple insertion strategies with automatic fallback.
    """

    MODE_AUTO = "auto"
    MODE_CLIPBOARD = "clipboard"
    MODE_TYPING = "typing"

    def __init__(self, mode: str = "auto", preserve_clipboard: bool = True):
        self._mode = mode
        self._preserve_clipboard = preserve_clipboard

    def set_mode(self, mode: str) -> None:
        """Set the insertion mode."""
        self._mode = mode

    def set_preserve_clipboard(self, preserve: bool) -> None:
        """Set whether to preserve clipboard content."""
        self._preserve_clipboard = preserve

    def insert_text(self, text: str) -> bool:
        """
        Insert text into the currently focused application.

        Returns True if text was successfully inserted, False if only copied.
        """
        if not text:
            return False

        if self._mode == self.MODE_CLIPBOARD:
            return self._insert_via_clipboard(text)
        elif self._mode == self.MODE_TYPING:
            return self._insert_via_typing(text)
        else:
            return self._insert_auto(text)

    def _insert_auto(self, text: str) -> bool:
        """
        Auto mode: try clipboard paste first, fall back to typing.
        """
        # Try clipboard paste first (fastest)
        if self._insert_via_clipboard(text):
            return True

        # Fall back to simulated typing
        logger.info("Clipboard paste failed, falling back to typing")
        if self._insert_via_typing(text):
            return True

        # Last resort: just copy to clipboard
        logger.info("Typing failed, copying to clipboard only")
        _set_clipboard_text(text)
        return False

    def _insert_via_clipboard(self, text: str) -> bool:
        """Insert text using clipboard paste (Ctrl+V)."""
        original_clipboard = None

        if self._preserve_clipboard:
            original_clipboard = _get_clipboard_text()

        if not _set_clipboard_text(text):
            return False

        time.sleep(0.05)

        success = _simulate_paste()

        if self._preserve_clipboard and original_clipboard is not None:
            time.sleep(0.1)
            _set_clipboard_text(original_clipboard)

        return success

    def _insert_via_typing(self, text: str) -> bool:
        """Insert text using simulated typing."""
        return _simulate_typing(text)

    def copy_to_clipboard(self, text: str) -> bool:
        """Simply copy text to clipboard without inserting."""
        return _set_clipboard_text(text)
