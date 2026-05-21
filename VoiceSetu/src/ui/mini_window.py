"""
Floating mini window for VoiceSetu.
A small always-on-top widget showing microphone status.
Can be dragged around the screen.
"""

import logging
from typing import Callable, Optional

import customtkinter as ctk

logger = logging.getLogger(__name__)


class MiniWindow(ctk.CTkToplevel):
    """
    Small floating window that shows recording status.
    Always on top, draggable, with a mic indicator.
    """

    STATUS_IDLE = "idle"
    STATUS_LISTENING = "listening"
    STATUS_PROCESSING = "processing"

    def __init__(
        self,
        parent,
        on_toggle: Optional[Callable] = None,
        on_open_main: Optional[Callable] = None,
    ):
        super().__init__(parent)

        self._on_toggle = on_toggle
        self._on_open_main = on_open_main
        self._status = self.STATUS_IDLE
        self._drag_start_x = 0
        self._drag_start_y = 0

        self._setup_window()
        self._create_widgets()

    def _setup_window(self) -> None:
        """Configure the floating window properties."""
        self.title("VoiceSetu")
        self.geometry("120x50")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.92)
        self.configure(fg_color=("#e8e8e8", "#1a1a2e"))

        screen_width = self.winfo_screenwidth()
        x_pos = screen_width - 160
        y_pos = 50
        self.geometry(f"120x50+{x_pos}+{y_pos}")

        self.bind("<Button-1>", self._start_drag)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<Double-Button-1>", self._on_double_click)

    def _create_widgets(self) -> None:
        """Create the mini window widgets."""
        self._frame = ctk.CTkFrame(
            self,
            corner_radius=12,
            fg_color=("#e8e8e8", "#1a1a2e"),
            border_width=1,
            border_color=("#cccccc", "#333355"),
        )
        self._frame.pack(fill="both", expand=True, padx=2, pady=2)
        self._frame.bind("<Button-1>", self._start_drag)
        self._frame.bind("<B1-Motion>", self._on_drag)
        self._frame.bind("<Double-Button-1>", self._on_double_click)

        self._inner = ctk.CTkFrame(self._frame, fg_color="transparent")
        self._inner.pack(fill="both", expand=True, padx=5, pady=5)
        self._inner.bind("<Button-1>", self._start_drag)
        self._inner.bind("<B1-Motion>", self._on_drag)

        self._status_dot = ctk.CTkLabel(
            self._inner,
            text="\u25CF",
            font=ctk.CTkFont(size=18),
            text_color="#666666",
            width=20,
        )
        self._status_dot.pack(side="left", padx=(2, 4))
        self._status_dot.bind("<Button-1>", self._start_drag)
        self._status_dot.bind("<B1-Motion>", self._on_drag)

        self._mic_btn = ctk.CTkButton(
            self._inner,
            text="\U0001F3A4",
            font=ctk.CTkFont(size=16),
            width=36,
            height=30,
            corner_radius=8,
            fg_color=("#d0d0d0", "#2d2d4e"),
            hover_color=("#bbb", "#3d3d6e"),
            text_color=("#333", "#eee"),
            command=self._on_mic_click,
        )
        self._mic_btn.pack(side="left", padx=2)

        self._status_label = ctk.CTkLabel(
            self._inner,
            text="Idle",
            font=ctk.CTkFont(size=10),
            text_color=("#555", "#aaa"),
        )
        self._status_label.pack(side="left", padx=(4, 2))
        self._status_label.bind("<Button-1>", self._start_drag)
        self._status_label.bind("<B1-Motion>", self._on_drag)

    def set_status(self, status: str, label_text: str = "") -> None:
        """Update the visual status indicator."""
        self._status = status

        color_map = {
            self.STATUS_IDLE: "#666666",
            self.STATUS_LISTENING: "#e74c3c",
            self.STATUS_PROCESSING: "#f39c12",
        }

        dot_color = color_map.get(status, "#666666")
        self._status_dot.configure(text_color=dot_color)

        if label_text:
            self._status_label.configure(text=label_text)
        else:
            status_text = {
                self.STATUS_IDLE: "Idle",
                self.STATUS_LISTENING: "Rec",
                self.STATUS_PROCESSING: "...",
            }
            self._status_label.configure(text=status_text.get(status, ""))

        if status == self.STATUS_LISTENING:
            self._mic_btn.configure(fg_color=("#ff6b6b", "#e74c3c"))
        else:
            self._mic_btn.configure(fg_color=("#d0d0d0", "#2d2d4e"))

    def _on_mic_click(self) -> None:
        """Handle mic button click to toggle recording."""
        if self._on_toggle:
            self._on_toggle()

    def _on_double_click(self, event=None) -> None:
        """Handle double click to open main window."""
        if self._on_open_main:
            self._on_open_main()

    def _start_drag(self, event) -> None:
        """Record the starting position for drag."""
        self._drag_start_x = event.x_root - self.winfo_x()
        self._drag_start_y = event.y_root - self.winfo_y()

    def _on_drag(self, event) -> None:
        """Handle window dragging."""
        x = event.x_root - self._drag_start_x
        y = event.y_root - self._drag_start_y
        self.geometry(f"+{x}+{y}")

    def show(self) -> None:
        """Show the mini window."""
        self.deiconify()

    def hide(self) -> None:
        """Hide the mini window."""
        self.withdraw()
