"""Main window: side nav, stacked tabs, top toolbar with mode banner."""
from __future__ import annotations

from typing import Sequence

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QMessageBox,
    QStackedWidget, QToolBar, QVBoxLayout, QWidget, QMainWindow, QStatusBar,
)

from ..config import Mode, Settings
from ..models import AuditEvent, ExitRule, Position, StatusBadge
from .activity_view import ActivityView
from .dashboard_view import DashboardView
from .positions_view import PositionsView
from .rules_view import RulesView
from .settings_view import SettingsView
from .theme import COLOR_LOSS, DARK_QSS


_TABS = ["Dashboard", "Positions", "Rules", "Activity", "Settings"]


class MainWindow(QMainWindow):
    # Signals routed up to main.py wiring (which connects them to the worker).
    panicRequested = Signal()
    pauseToggled = Signal(bool)
    ruleSaved = Signal(str, object)             # position_key, ExitRule
    ruleCleared = Signal(str)                   # position_key
    defaultRuleChanged = Signal(object)         # ExitRule
    accountRuleChanged = Signal(object, object) # target, stop
    manualExitRequested = Signal(object)        # Position
    modeChangeRequested = Signal(object)        # Mode
    secretsSaveRequested = Signal(str, str, str)
    settingsChanged = Signal(object)            # Settings
    exportEventsRequested = Signal(str)

    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.setWindowTitle("Groww Auto-Exit")
        self.setMinimumSize(1100, 720)
        self.setStyleSheet(DARK_QSS)
        self._settings = settings
        self._positions: list[Position] = []
        self._rules: dict[str, ExitRule] = {}
        self._build()

    # ----- build ----------------------------------------------------------

    def _build(self) -> None:
        # toolbar with mode banner
        tb = QToolBar()
        tb.setMovable(False)
        self.addToolBar(tb)
        self.modeBanner = QLabel("PAPER")
        self.modeBanner.setObjectName("liveBanner")
        self.modeBanner.setVisible(self._settings.mode == Mode.LIVE)
        tb.addWidget(self.modeBanner)

        # central layout: side nav + stack
        central = QWidget()
        self.setCentralWidget(central)
        outer = QHBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self.nav = QListWidget()
        self.nav.setObjectName("sideNav")
        self.nav.setFixedWidth(180)
        for label in _TABS:
            QListWidgetItem(label, self.nav)
        self.nav.setCurrentRow(0)

        self.stack = QStackedWidget()

        # Tabs
        self.dashboardView = DashboardView()
        self.positionsView = PositionsView()
        self.rulesView = RulesView()
        self.activityView = ActivityView()
        self.settingsView = SettingsView(self._settings)

        for w in (self.dashboardView, self.positionsView, self.rulesView,
                  self.activityView, self.settingsView):
            self.stack.addWidget(w)

        self.nav.currentRowChanged.connect(self.stack.setCurrentIndex)

        outer.addWidget(self.nav)
        outer.addWidget(self.stack, 1)

        # status bar
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready")

        # wire child signals out
        self.dashboardView.panicRequested.connect(self._confirm_panic)
        self.dashboardView.pauseToggled.connect(self.pauseToggled.emit)
        self.positionsView.manualExitRequested.connect(self._confirm_manual_exit)
        self.rulesView.ruleSaved.connect(self.ruleSaved.emit)
        self.rulesView.ruleCleared.connect(self.ruleCleared.emit)
        self.rulesView.defaultRuleChanged.connect(self.defaultRuleChanged.emit)
        self.activityView.exportRequested.connect(self.exportEventsRequested.emit)
        self.settingsView.modeChangeRequested.connect(self.modeChangeRequested.emit)
        self.settingsView.secretsSaveRequested.connect(self.secretsSaveRequested.emit)
        self.settingsView.settingsChanged.connect(self._apply_settings_locally)
        self.settingsView.accountRuleChanged.connect(self.accountRuleChanged.emit)

    def _apply_settings_locally(self, new: Settings) -> None:
        self._settings = new
        self.modeBanner.setVisible(new.mode == Mode.LIVE)
        self.settingsChanged.emit(new)

    # ----- worker -> UI slots --------------------------------------------

    def setPositions(self, positions: Sequence[Position]) -> None:
        self._positions = list(positions)
        # rebuild rule summary text (target/stop) for the positions view
        summary = {
            k: self._summarise_rule(r) for k, r in self._rules.items()
        }
        self.positionsView.setRulesSummary(summary)
        self.positionsView.setPositions(positions)
        self.rulesView.setPositions(list(positions))
        self.dashboardView.setOpenPositionsCount(len(positions))

    def setRules(self, rules: dict[str, ExitRule]) -> None:
        self._rules = dict(rules)
        self.rulesView.setRules(self._rules)

    def setDefaultRule(self, rule: ExitRule) -> None:
        self.rulesView.setDefaultRule(rule)

    def setStatus(self, badge: StatusBadge) -> None:
        self.dashboardView.setStatusBadge(badge)
        self.statusBar().showMessage(f"Status: {getattr(badge, 'value', badge)}")

    def setConnection(self, connected: bool, message: str) -> None:
        self.dashboardView.setConnection(connected, message)

    def setMode(self, mode: Mode) -> None:
        self.modeBanner.setText(mode.value.upper())
        self.modeBanner.setVisible(mode == Mode.LIVE)
        self._settings.mode = mode

    def setAccountMtm(self, mtm: float) -> None:
        self.dashboardView.setAccountMtm(mtm)

    def setDailyPnl(self, pnl: float) -> None:
        self.dashboardView.setDailyPnl(pnl)

    def appendActivity(self, ev: AuditEvent) -> None:
        self.activityView.appendEvent(ev)

    def setActivity(self, evs: list[AuditEvent]) -> None:
        self.activityView.setEvents(evs)

    # ----- internal -------------------------------------------------------

    def _confirm_panic(self) -> None:
        ok = QMessageBox.question(
            self, "Panic exit",
            "This will square off ALL open positions. Continue?",
        )
        if ok == QMessageBox.StandardButton.Yes:
            self.panicRequested.emit()

    def _confirm_manual_exit(self, position: Position) -> None:
        if self._settings.mode == Mode.LIVE and self._settings.require_live_confirm:
            ok = QMessageBox.question(
                self, "Confirm manual exit",
                f"Send LIVE square-off for {position.symbol} qty={position.abs_quantity}?",
            )
            if ok != QMessageBox.StandardButton.Yes:
                return
        self.manualExitRequested.emit(position)

    @staticmethod
    def _summarise_rule(rule: ExitRule) -> str:
        parts = []
        if rule.target_inr is not None:
            parts.append(f"+{rule.target_inr:.0f}")
        if rule.stop_inr is not None:
            parts.append(f"{rule.stop_inr:.0f}")
        if rule.trail_lock_inr is not None:
            parts.append(f"trail@{rule.trail_lock_inr:.0f}")
        return " / ".join(parts) if parts else "-"
