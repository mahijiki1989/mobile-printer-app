"""Dashboard tab: status badge, account MTM, totals, quick actions."""
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QGridLayout, QGroupBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget,
)

from ..models import StatusBadge
from .theme import BADGE_COLORS, COLOR_LOSS, COLOR_NEUTRAL, COLOR_PROFIT


class DashboardView(QWidget):
    panicRequested = Signal()
    pauseToggled = Signal(bool)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._paused = False
        self._build()

    def _build(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 20, 20, 20)
        outer.setSpacing(16)

        top = QHBoxLayout()

        self.statusBadge = QLabel("MONITORING")
        self.statusBadge.setObjectName("bigBadge")
        self.statusBadge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.statusBadge.setMinimumWidth(180)
        self._set_badge_color(StatusBadge.MONITORING)

        self.connectionLabel = QLabel("Connection: ...")
        self.connectionLabel.setStyleSheet(f"color: {COLOR_NEUTRAL};")

        top.addWidget(self.statusBadge)
        top.addSpacing(20)
        top.addWidget(self.connectionLabel)
        top.addStretch()

        # Stats grid
        stats = QGroupBox("Account")
        grid = QGridLayout(stats)

        self.accountMtmLabel = QLabel("0.00")
        self.accountMtmLabel.setStyleSheet("font-size: 22px; font-weight: 600;")
        self.dailyPnlLabel = QLabel("0.00")
        self.openPosCountLabel = QLabel("0")
        self.armedCountLabel = QLabel("0")
        self.exitsTodayLabel = QLabel("0")

        grid.addWidget(QLabel("Account MTM"),    0, 0)
        grid.addWidget(self.accountMtmLabel,     0, 1)
        grid.addWidget(QLabel("Daily realised"), 0, 2)
        grid.addWidget(self.dailyPnlLabel,       0, 3)

        grid.addWidget(QLabel("Open positions"), 1, 0)
        grid.addWidget(self.openPosCountLabel,   1, 1)
        grid.addWidget(QLabel("Rules armed"),    1, 2)
        grid.addWidget(self.armedCountLabel,     1, 3)
        grid.addWidget(QLabel("Exits today"),    1, 4)
        grid.addWidget(self.exitsTodayLabel,     1, 5)

        # Quick actions
        actions = QGroupBox("Quick actions")
        row = QHBoxLayout(actions)
        self.panicBtn = QPushButton("PANIC EXIT ALL")
        self.panicBtn.setObjectName("panicButton")
        self.panicBtn.setMinimumHeight(40)
        self.panicBtn.clicked.connect(self.panicRequested.emit)

        self.pauseBtn = QPushButton("Pause")
        self.pauseBtn.setMinimumHeight(40)
        self.pauseBtn.clicked.connect(self._toggle_paused)

        row.addWidget(self.panicBtn, 2)
        row.addWidget(self.pauseBtn, 1)
        row.addStretch()

        outer.addLayout(top)
        outer.addWidget(stats)
        outer.addWidget(actions)
        outer.addStretch()

    # ------------------------------- slots from worker
    def setStatusBadge(self, badge: StatusBadge) -> None:
        self.statusBadge.setText(badge.value if hasattr(badge, "value") else str(badge))
        self._set_badge_color(badge)

    def setConnection(self, connected: bool, message: str) -> None:
        dot = "● Connected" if connected else "○ Disconnected"
        color = COLOR_PROFIT if connected else COLOR_LOSS
        self.connectionLabel.setText(f"Connection: {dot}  ({message})")
        self.connectionLabel.setStyleSheet(f"color: {color};")

    def setAccountMtm(self, mtm: float) -> None:
        self.accountMtmLabel.setText(f"{mtm:+,.2f}")
        color = COLOR_PROFIT if mtm > 0 else (COLOR_LOSS if mtm < 0 else COLOR_NEUTRAL)
        self.accountMtmLabel.setStyleSheet(f"font-size: 22px; font-weight: 600; color: {color};")

    def setDailyPnl(self, pnl: float) -> None:
        self.dailyPnlLabel.setText(f"{pnl:+,.2f}")
        color = COLOR_PROFIT if pnl > 0 else (COLOR_LOSS if pnl < 0 else COLOR_NEUTRAL)
        self.dailyPnlLabel.setStyleSheet(f"color: {color};")

    def setOpenPositionsCount(self, n: int) -> None:
        self.openPosCountLabel.setText(str(n))

    def setArmedCount(self, n: int) -> None:
        self.armedCountLabel.setText(str(n))

    def setExitsToday(self, n: int) -> None:
        self.exitsTodayLabel.setText(str(n))

    # ------------------------------- internals
    def _toggle_paused(self) -> None:
        self._paused = not self._paused
        self.pauseBtn.setText("Resume" if self._paused else "Pause")
        self.pauseToggled.emit(self._paused)

    def _set_badge_color(self, badge) -> None:
        key = badge.value if hasattr(badge, "value") else str(badge)
        bg = BADGE_COLORS.get(key, "#444")
        self.statusBadge.setStyleSheet(
            f"background-color: {bg}; color: white; padding: 6px 12px;"
            " border-radius: 12px; font-weight: 700;"
        )
