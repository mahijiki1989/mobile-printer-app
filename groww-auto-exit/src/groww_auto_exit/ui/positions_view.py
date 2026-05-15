"""Positions tab: live table of open positions."""
from __future__ import annotations

from typing import Sequence

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import (
    QHeaderView, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
)

from ..models import Position
from .theme import COLOR_LOSS, COLOR_NEUTRAL, COLOR_PROFIT


_HEADERS = [
    "Symbol", "Exch", "Seg", "Prod", "Qty",
    "Avg", "LTP", "MTM", "Rule", "Action",
]


class PositionsView(QWidget):
    manualExitRequested = Signal(object)  # Position
    editRuleRequested = Signal(str)       # position_key

    def __init__(self) -> None:
        super().__init__()
        self._build()
        self._rules_summary: dict[str, str] = {}

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        self.table = QTableWidget(0, len(_HEADERS))
        self.table.setHorizontalHeaderLabels(_HEADERS)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        h = self.table.horizontalHeader()
        h.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for i in (1, 2, 3, 4):
            h.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(self.table)

    # ----- public slots ---------------------------------------------------

    def setRulesSummary(self, summary: dict[str, str]) -> None:
        self._rules_summary = dict(summary)

    def setPositions(self, positions: Sequence[Position]) -> None:
        self.table.setRowCount(len(positions))
        for r, p in enumerate(positions):
            self._set_text(r, 0, p.symbol)
            self._set_text(r, 1, p.exchange.value)
            self._set_text(r, 2, p.segment.value)
            self._set_text(r, 3, p.product.value)
            self._set_text(r, 4, str(p.quantity))
            self._set_text(r, 5, f"{p.avg_price:.2f}")
            self._set_text(r, 6, f"{p.ltp:.2f}")

            mtm_item = QTableWidgetItem(f"{p.mtm:+.2f}")
            color = COLOR_PROFIT if p.mtm > 0 else (COLOR_LOSS if p.mtm < 0 else COLOR_NEUTRAL)
            mtm_item.setForeground(QBrush(QColor(color)))
            mtm_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(r, 7, mtm_item)

            self._set_text(r, 8, self._rules_summary.get(p.key(), "-"))

            btn = QPushButton("Square off")
            btn.clicked.connect(lambda _=False, pos=p: self.manualExitRequested.emit(pos))
            self.table.setCellWidget(r, 9, btn)

    # ----- helpers --------------------------------------------------------

    def _set_text(self, row: int, col: int, text: str) -> None:
        item = QTableWidgetItem(text)
        if col in (4, 5, 6, 7):
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.table.setItem(row, col, item)
