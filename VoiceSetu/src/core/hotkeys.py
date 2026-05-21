"""
Global hotkey manager for VoiceSetu.
Registers system-wide hotkeys for push-to-talk and toggle dictation.
Uses the keyboard library for global hotkey detection.
"""

import logging
import threading
from typing import Callable, Dict, Optional

logger = logging.getLogger(__name__)


class HotkeyManager:
    """
    Manages global hotkeys for the application.
    Supports push-to-talk (hold) and toggle (press once) modes.
    """

    def __init__(self):
        self._hotkeys: Dict[str, int] = {}
        self._callbacks: Dict[str, Callable] = {}
        self._ptt_callback_start: Optional[Callable] = None
        self._ptt_callback_stop: Optional[Callable] = None
        self._ptt_hotkey: str = ""
        self._toggle_hotkey: str = ""
        self._is_active = False
        self._lock = threading.Lock()

    def register_toggle_hotkey(self, hotkey: str, callback: Callable) -> bool:
        """
        Register a global toggle hotkey (press to start, press again to stop).

        Args:
            hotkey: Key combination string (e.g., 'ctrl+shift+d')
            callback: Function to call when hotkey is pressed
        """
        try:
            import keyboard

            if self._toggle_hotkey and self._toggle_hotkey in self._hotkeys:
                try:
                    keyboard.remove_hotkey(self._hotkeys[self._toggle_hotkey])
                except (ValueError, KeyError):
                    pass

            hook_id = keyboard.add_hotkey(
                hotkey,
                callback,
                suppress=False,
                trigger_on_release=False,
            )
            self._hotkeys[hotkey] = hook_id
            self._callbacks[hotkey] = callback
            self._toggle_hotkey = hotkey
            logger.info(f"Toggle hotkey registered: {hotkey}")
            return True

        except Exception as e:
            logger.error(f"Failed to register toggle hotkey '{hotkey}': {e}")
            return False

    def register_ptt_hotkey(
        self,
        hotkey: str,
        on_press: Callable,
        on_release: Callable,
    ) -> bool:
        """
        Register a push-to-talk hotkey (hold to record, release to stop).

        Args:
            hotkey: Key combination string (e.g., 'ctrl+shift+space')
            on_press: Function to call when hotkey is pressed
            on_release: Function to call when hotkey is released
        """
        try:
            import keyboard

            if self._ptt_hotkey and self._ptt_hotkey in self._hotkeys:
                try:
                    keyboard.remove_hotkey(self._hotkeys[self._ptt_hotkey])
                except (ValueError, KeyError):
                    pass

            self._ptt_callback_start = on_press
            self._ptt_callback_stop = on_release
            self._ptt_hotkey = hotkey

            hook_id = keyboard.add_hotkey(
                hotkey,
                self._on_ptt_press,
                suppress=False,
                trigger_on_release=False,
            )
            self._hotkeys[hotkey] = hook_id

            keyboard.on_release_key(
                hotkey.split("+")[-1],
                self._on_ptt_release_check,
                suppress=False,
            )

            logger.info(f"PTT hotkey registered: {hotkey}")
            return True

        except Exception as e:
            logger.error(f"Failed to register PTT hotkey '{hotkey}': {e}")
            return False

    def _on_ptt_press(self) -> None:
        """Handle push-to-talk key press."""
        with self._lock:
            if not self._is_active:
                self._is_active = True
                if self._ptt_callback_start:
                    self._ptt_callback_start()

    def _on_ptt_release_check(self, event=None) -> None:
        """Handle push-to-talk key release."""
        with self._lock:
            if self._is_active:
                self._is_active = False
                if self._ptt_callback_stop:
                    self._ptt_callback_stop()

    def unregister_all(self) -> None:
        """Unregister all hotkeys."""
        try:
            import keyboard

            for hotkey, hook_id in self._hotkeys.items():
                try:
                    keyboard.remove_hotkey(hook_id)
                except (ValueError, KeyError):
                    pass

            self._hotkeys.clear()
            self._callbacks.clear()
            self._ptt_hotkey = ""
            self._toggle_hotkey = ""
            logger.info("All hotkeys unregistered")

        except Exception as e:
            logger.error(f"Error unregistering hotkeys: {e}")

    def update_hotkeys(
        self,
        ptt_hotkey: str,
        toggle_hotkey: str,
        toggle_callback: Callable,
        ptt_start: Callable,
        ptt_stop: Callable,
    ) -> None:
        """Update all hotkeys with new key combinations."""
        self.unregister_all()
        self.register_toggle_hotkey(toggle_hotkey, toggle_callback)
        self.register_ptt_hotkey(ptt_hotkey, ptt_start, ptt_stop)
