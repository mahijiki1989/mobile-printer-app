"""
System tray integration for VoiceSetu.
Provides tray icon with context menu for quick access.
Uses pystray for Windows system tray support.
"""

import logging
import threading
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class TrayManager:
    """
    Manages the system tray icon and context menu.
    Runs in a separate thread to avoid blocking the main UI.
    """

    def __init__(
        self,
        on_show: Optional[Callable] = None,
        on_quit: Optional[Callable] = None,
        on_toggle_dictation: Optional[Callable] = None,
    ):
        self._on_show = on_show
        self._on_quit = on_quit
        self._on_toggle_dictation = on_toggle_dictation
        self._icon = None
        self._thread: Optional[threading.Thread] = None
        self._is_running = False

    def start(self) -> None:
        """Start the tray icon in a background thread."""
        if self._is_running:
            return

        self._thread = threading.Thread(target=self._run_tray, daemon=True)
        self._thread.start()
        self._is_running = True

    def _create_icon_image(self):
        """Create a simple icon image for the tray."""
        try:
            from PIL import Image, ImageDraw

            size = 64
            image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)

            # Draw a microphone-like icon
            # Circle background
            draw.ellipse([4, 4, 60, 60], fill=(41, 128, 185), outline=(52, 152, 219), width=2)
            # Mic body (rectangle)
            draw.rounded_rectangle([24, 14, 40, 38], radius=8, fill=(255, 255, 255))
            # Mic stand (arc + line)
            draw.arc([18, 24, 46, 48], start=0, end=180, fill=(255, 255, 255), width=2)
            draw.line([32, 48, 32, 54], fill=(255, 255, 255), width=2)
            draw.line([24, 54, 40, 54], fill=(255, 255, 255), width=2)

            return image
        except ImportError:
            # Fallback: return a simple colored square
            from PIL import Image
            image = Image.new("RGB", (64, 64), (41, 128, 185))
            return image

    def _run_tray(self) -> None:
        """Run the system tray icon."""
        try:
            import pystray
            from pystray import MenuItem, Menu

            icon_image = self._create_icon_image()

            menu = Menu(
                MenuItem("VoiceSetu", self._on_show_click, default=True),
                Menu.SEPARATOR,
                MenuItem("Start/Stop Dictation", self._on_toggle_click),
                Menu.SEPARATOR,
                MenuItem("Quit", self._on_quit_click),
            )

            self._icon = pystray.Icon(
                name="VoiceSetu",
                icon=icon_image,
                title="VoiceSetu - Offline Dictation",
                menu=menu,
            )

            self._icon.run()

        except Exception as e:
            logger.error(f"Tray icon error: {e}")
            self._is_running = False

    def _on_show_click(self, icon=None, item=None) -> None:
        """Handle show/restore click."""
        if self._on_show:
            self._on_show()

    def _on_toggle_click(self, icon=None, item=None) -> None:
        """Handle toggle dictation click."""
        if self._on_toggle_dictation:
            self._on_toggle_dictation()

    def _on_quit_click(self, icon=None, item=None) -> None:
        """Handle quit click."""
        self.stop()
        if self._on_quit:
            self._on_quit()

    def stop(self) -> None:
        """Stop and remove the tray icon."""
        self._is_running = False
        if self._icon:
            try:
                self._icon.stop()
            except Exception:
                pass
            self._icon = None

    def update_tooltip(self, text: str) -> None:
        """Update the tray icon tooltip text."""
        if self._icon:
            try:
                self._icon.title = text
            except Exception:
                pass
