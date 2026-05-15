"""Activity log tab: append-only event view + CSV export."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFileDialog, QHBoxLayout, QHeaderView, QPushButton, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget,
)

from ..models import AuditEvent


_HEADERS = ["Time", "Event", "Position", "Order", "Message"]


class ActivityView(QWidget):
    exportRequested = Signal(str)  # destination path

    def __init__(self) -> None:
        super().__init__()
        self._build()

    def _build(self) -> None:
        layout = QVBoxLayout(self)

        top = QHBoxLayout()
        self.exportBtn = QPushButton("Export CSV...")
        self.exportBtn.clicked.connect(self._choose_path)
        top.addStretch()
        top.addWidget(self.exportBtn)
        layout.addLayout(top)

        self.table = QTableWidget(0, len(_HEADERS))
        self.table.setHorizontalHeaderLabels(_HEADERS)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

    # ----- public slots ---------------------------------------------------

    def appendEvent(self, ev: AuditEvent) -> None:
        row = 0
        self.table.insertRow(row)
        ts = datetime.fromtimestamp(ev.ts).strftime("%H:%M:%S")
        for col, val in enumerate([
            ts,
            ev.event_type.value,
            ev.position_key or "",
            ev.order_id or "",
            ev.message,
        ]):
            self.table.setItem(row, col, QTableWidgetItem(str(val)))
        # Cap at 1000 rows for memory.
        if self.table.rowCount() > 1000:
            self.table.removeRow(self.table.rowCount() - 1)

    def setEvents(self, events: list[AuditEvent]) -> None:
        self.table.setRowCount(0)
        for ev in events:
            self.appendEvent(ev)

    # ----- internals ------------------------------------------------------

    def _choose_path(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Export activity log",
            f"groww_auto_exit_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV (*.csv)",
        )
        if path:
            self.exportRequested.emit(path)
