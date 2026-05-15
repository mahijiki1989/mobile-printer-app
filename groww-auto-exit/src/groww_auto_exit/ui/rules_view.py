"""Rules tab: per-position rule editor + global default."""
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDoubleSpinBox, QFormLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit, QPushButton, QSpinBox,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
)

from ..models import ExitMode, ExitRule, Position, RuleMode


_HEADERS = ["Position", "Target +INR", "Stop -INR", "Trail Lock", "Trail Giveback", "Mode", "Enabled"]


class _RuleEditor(QGroupBox):
    """Form for editing a single ExitRule (used by both per-position and default)."""

    ruleSaved = Signal(str, object)   # position_key (or "DEFAULT"), ExitRule
    ruleCleared = Signal(str)         # position_key

    def __init__(self, title: str = "Rule") -> None:
        super().__init__(title)
        self._key: str = "DEFAULT"
        self._build()

    def _build(self) -> None:
        form = QFormLayout(self)

        self.targetSpin = QDoubleSpinBox()
        self.targetSpin.setRange(0.0, 10_000_000.0)
        self.targetSpin.setDecimals(2)
        self.targetSpin.setSingleStep(50.0)

        self.stopSpin = QDoubleSpinBox()
        self.stopSpin.setRange(-10_000_000.0, 0.0)
        self.stopSpin.setDecimals(2)
        self.stopSpin.setSingleStep(50.0)

        self.trailLockSpin = QDoubleSpinBox()
        self.trailLockSpin.setRange(0.0, 10_000_000.0)
        self.trailLockSpin.setDecimals(2)
        self.trailLockSpin.setSingleStep(50.0)

        self.trailGivebackSpin = QDoubleSpinBox()
        self.trailGivebackSpin.setRange(0.0, 10_000_000.0)
        self.trailGivebackSpin.setDecimals(2)
        self.trailGivebackSpin.setSingleStep(25.0)

        self.modeCombo = QComboBox()
        self.modeCombo.addItem("ONE_SHOT", ExitMode.ONE_SHOT)
        self.modeCombo.addItem("PARTIAL", ExitMode.PARTIAL)

        self.partialSpin = QSpinBox()
        self.partialSpin.setRange(0, 1_000_000)
        self.partialSpin.setEnabled(False)
        self.modeCombo.currentIndexChanged.connect(
            lambda _: self.partialSpin.setEnabled(self.modeCombo.currentData() == ExitMode.PARTIAL)
        )

        self.enabledCheck = QCheckBox("Rule enabled")
        self.enabledCheck.setChecked(True)

        form.addRow("Target (profit) INR", self.targetSpin)
        form.addRow("Stop (loss) INR (negative)", self.stopSpin)
        form.addRow("Trail lock at INR", self.trailLockSpin)
        form.addRow("Trail giveback INR", self.trailGivebackSpin)
        form.addRow("Exit mode", self.modeCombo)
        form.addRow("Partial qty", self.partialSpin)
        form.addRow(self.enabledCheck)

        row = QHBoxLayout()
        self.saveBtn = QPushButton("Save")
        self.clearBtn = QPushButton("Clear")
        row.addWidget(self.saveBtn)
        row.addWidget(self.clearBtn)
        form.addRow(row)

        self.saveBtn.clicked.connect(self._on_save)
        self.clearBtn.clicked.connect(lambda: self.ruleCleared.emit(self._key))

    # ----- public
    def setTarget(self, key: str, rule: Optional[ExitRule]) -> None:
        self._key = key
        if rule is None:
            self.targetSpin.setValue(0)
            self.stopSpin.setValue(0)
            self.trailLockSpin.setValue(0)
            self.trailGivebackSpin.setValue(0)
            self.modeCombo.setCurrentIndex(0)
            self.partialSpin.setValue(0)
            self.enabledCheck.setChecked(True)
            return
        self.targetSpin.setValue(rule.target_inr or 0.0)
        self.stopSpin.setValue(rule.stop_inr or 0.0)
        self.trailLockSpin.setValue(rule.trail_lock_inr or 0.0)
        self.trailGivebackSpin.setValue(rule.trail_giveback_inr or 0.0)
        idx = self.modeCombo.findData(rule.exit_mode)
        self.modeCombo.setCurrentIndex(max(0, idx))
        self.partialSpin.setValue(rule.partial_qty or 0)
        self.enabledCheck.setChecked(rule.enabled)

    def _on_save(self) -> None:
        try:
            rule = ExitRule(
                rule_mode=RuleMode.PER_POSITION if self._key != "DEFAULT" else RuleMode.PER_POSITION,
                target_inr=self.targetSpin.value() or None,
                stop_inr=self.stopSpin.value() or None,
                trail_lock_inr=self.trailLockSpin.value() or None,
                trail_giveback_inr=self.trailGivebackSpin.value() or None,
                exit_mode=self.modeCombo.currentData(),
                partial_qty=self.partialSpin.value() or None,
                enabled=self.enabledCheck.isChecked(),
            )
        except ValueError as e:
            self._error(str(e))
            return
        self.ruleSaved.emit(self._key, rule)

    def _error(self, msg: str) -> None:
        # tiny inline error so we don't pull in QMessageBox here
        self.setTitle(f"Rule  -  ERROR: {msg}")


class RulesView(QWidget):
    ruleSaved = Signal(str, object)         # position_key, ExitRule
    ruleCleared = Signal(str)               # position_key
    defaultRuleChanged = Signal(object)     # ExitRule

    def __init__(self) -> None:
        super().__init__()
        self._positions: list[Position] = []
        self._rules: dict[str, ExitRule] = {}
        self._build()

    def _build(self) -> None:
        outer = QHBoxLayout(self)

        # left: table of current rules
        left = QVBoxLayout()
        left.addWidget(QLabel("Per-position rules"))
        self.table = QTableWidget(0, len(_HEADERS))
        self.table.setHorizontalHeaderLabels(_HEADERS)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.itemSelectionChanged.connect(self._on_select)
        left.addWidget(self.table, 1)

        # right: editors
        right = QVBoxLayout()

        self.editor = _RuleEditor("Edit rule for selected position")
        self.editor.ruleSaved.connect(self._on_rule_saved)
        self.editor.ruleCleared.connect(self.ruleCleared.emit)
        right.addWidget(self.editor)

        self.defaultEditor = _RuleEditor("Default rule for new positions")
        self.defaultEditor._key = "DEFAULT"
        self.defaultEditor.ruleSaved.connect(lambda _key, rule: self.defaultRuleChanged.emit(rule))
        right.addWidget(self.defaultEditor)

        outer.addLayout(left, 2)
        outer.addLayout(right, 1)

    # ---- public slots
    def setPositions(self, positions: list[Position]) -> None:
        self._positions = list(positions)
        self._refresh()

    def setRules(self, rules: dict[str, ExitRule]) -> None:
        self._rules = dict(rules)
        self._refresh()

    def setDefaultRule(self, rule: ExitRule) -> None:
        self.defaultEditor.setTarget("DEFAULT", rule)

    # ---- helpers
    def _refresh(self) -> None:
        self.table.setRowCount(len(self._positions))
        for r, p in enumerate(self._positions):
            rule = self._rules.get(p.key())
            self.table.setItem(r, 0, QTableWidgetItem(p.symbol))
            self.table.setItem(r, 1, QTableWidgetItem(f"{rule.target_inr:+.2f}" if rule and rule.target_inr else "-"))
            self.table.setItem(r, 2, QTableWidgetItem(f"{rule.stop_inr:+.2f}" if rule and rule.stop_inr else "-"))
            self.table.setItem(r, 3, QTableWidgetItem(f"{rule.trail_lock_inr:.2f}" if rule and rule.trail_lock_inr else "-"))
            self.table.setItem(r, 4, QTableWidgetItem(f"{rule.trail_giveback_inr:.2f}" if rule and rule.trail_giveback_inr else "-"))
            self.table.setItem(r, 5, QTableWidgetItem(rule.exit_mode.value if rule else "-"))
            self.table.setItem(r, 6, QTableWidgetItem("yes" if rule and rule.enabled else "no"))
            # store the position_key in column 0 for retrieval
            self.table.item(r, 0).setData(0x0100, p.key())

    def _on_select(self) -> None:
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return
        r = rows[0].row()
        item = self.table.item(r, 0)
        if not item:
            return
        key = item.data(0x0100)
        if not key:
            return
        rule = self._rules.get(key)
        self.editor.setTitle(f"Edit rule: {key}")
        self.editor.setTarget(key, rule)

    def _on_rule_saved(self, key: str, rule: ExitRule) -> None:
        if key == "DEFAULT":
            self.defaultRuleChanged.emit(rule)
        else:
            self.ruleSaved.emit(key, rule)
