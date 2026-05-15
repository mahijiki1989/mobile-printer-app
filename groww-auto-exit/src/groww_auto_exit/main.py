"""Application entrypoint.

Wires Settings -> secrets -> BrokerAdapter -> DB -> Notifications -> Worker -> UI.

The UI lives on the main Qt thread; the trading loop runs in a QThread via
`start_worker`. They communicate exclusively via Qt signals/slots.
"""
from __future__ import annotations

import logging
import sys
from typing import Optional

from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QApplication, QMessageBox

from . import secrets_store
from .broker.base import BrokerAdapter
from .broker.groww_adapter import GrowwAdapter
from .broker.mock_adapter import MockAdapter
from .broker.paper_adapter import PaperAdapter
from .config import Mode, Settings
from .db import Database
from .logging_setup import configure_logging
from .models import ExitMode, ExitRule, RuleMode
from .notifications import NotificationService
from .ui.main_window import MainWindow
from .utils.timeutils import today_str
from .workers.monitor_worker import MonitorWorker, start_worker

log = logging.getLogger(__name__)


def _make_broker(settings: Settings) -> BrokerAdapter:
    if settings.mode == Mode.MOCK:
        return MockAdapter()

    token = secrets_store.get_access_token()
    api_key, api_secret = secrets_store.get_api_key_pair()

    if not token and not (api_key and api_secret):
        # Fall back to mock if no credentials are configured. Settings UI lets
        # the user paste them and reconnect without a restart.
        log.warning("No Groww credentials in keyring, starting in MOCK mode.")
        return MockAdapter()

    real = GrowwAdapter(access_token=token, api_key=api_key, api_secret=api_secret)
    if settings.mode == Mode.PAPER:
        return PaperAdapter(real)
    return real


def _default_rule_factory(settings: Settings):
    def make() -> ExitRule:
        target = settings.default_target_inr if settings.default_target_inr > 0 else None
        stop = settings.default_stop_inr if settings.default_stop_inr < 0 else None
        return ExitRule(
            rule_mode=RuleMode.PER_POSITION,
            target_inr=target,
            stop_inr=stop,
            exit_mode=ExitMode.ONE_SHOT,
            enabled=True,
        )
    return make


class AppController(QObject):
    """Owns long-lived references and routes signals between UI and worker."""

    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.settings = settings
        settings.ensure_dirs()

        configure_logging(settings.log_dir)

        # Move bootstrap secrets to keyring then forget them.
        secrets_store.bootstrap_from_env(
            settings.bootstrap_access_token,
            settings.bootstrap_api_key,
            settings.bootstrap_api_secret,
        )

        self.db = Database(settings.db_path)
        self.notifier = NotificationService()

        self.account_target_inr: Optional[float] = None
        self.account_stop_inr: Optional[float] = None

        self.broker = _make_broker(settings)
        self.worker = MonitorWorker(
            self.broker,
            settings,
            self.db,
            self.notifier,
            default_rule_factory=_default_rule_factory(settings),
            account_target_inr=self.account_target_inr,
            account_stop_inr=self.account_stop_inr,
        )
        self.thread = None  # set after start

        self.window = MainWindow(settings)
        self._wire_signals()
        self._populate_initial_state()

    # ----------------------------------------------------------------- wire

    def _wire_signals(self) -> None:
        w = self.worker
        ui = self.window

        # worker -> UI
        w.positionsUpdated.connect(ui.setPositions)
        w.statusChanged.connect(ui.setStatus)
        w.connectionChanged.connect(ui.setConnection)
        w.eventLogged.connect(ui.appendActivity)
        w.accountMtmUpdated.connect(ui.setAccountMtm)

        # UI -> worker (queued because worker lives on its own thread)
        ui.panicRequested.connect(w.request_panic, Qt.ConnectionType.QueuedConnection)
        ui.pauseToggled.connect(w.set_paused, Qt.ConnectionType.QueuedConnection)
        ui.ruleSaved.connect(self._on_rule_saved)
        ui.ruleCleared.connect(w.clear_rule, Qt.ConnectionType.QueuedConnection)
        ui.defaultRuleChanged.connect(self._on_default_rule_changed)
        ui.accountRuleChanged.connect(self._on_account_rule_changed)
        ui.manualExitRequested.connect(w.manual_exit, Qt.ConnectionType.QueuedConnection)
        ui.modeChangeRequested.connect(self._on_mode_change)
        ui.secretsSaveRequested.connect(self._on_secrets_save)
        ui.settingsChanged.connect(self._on_settings_changed)
        ui.exportEventsRequested.connect(self._on_export_events)

    def _populate_initial_state(self) -> None:
        self.window.setRules(self.db.all_rules())
        self.window.setDefaultRule(_default_rule_factory(self.settings)())
        self.window.setActivity(self.db.recent_events(limit=200))
        self.window.setMode(self.settings.mode)
        self.window.setDailyPnl(self.db.get_realised_pnl(today_str()))

    # ------------------------------------------------------------ run/stop

    def run(self) -> None:
        self.thread = start_worker(self.worker)
        self.window.show()

    def shutdown(self) -> None:
        try:
            self.worker.stop()
        except Exception:
            pass
        if self.thread is not None:
            self.thread.quit()
            self.thread.wait(2000)
        try:
            self.db.close()
        except Exception:
            pass

    # --------------------------------------------------------- ui handlers

    def _on_rule_saved(self, position_key: str, rule: ExitRule) -> None:
        self.worker.set_rule(position_key, rule)
        self.window.setRules(self.db.all_rules())

    def _on_default_rule_changed(self, rule: ExitRule) -> None:
        # Update the worker's factory with the new defaults.
        def factory(_rule=rule):
            return ExitRule(
                rule_mode=_rule.rule_mode,
                target_inr=_rule.target_inr,
                stop_inr=_rule.stop_inr,
                trail_lock_inr=_rule.trail_lock_inr,
                trail_giveback_inr=_rule.trail_giveback_inr,
                exit_mode=_rule.exit_mode,
                partial_qty=_rule.partial_qty,
                enabled=_rule.enabled,
            )
        self.worker._default_rule_factory = factory  # noqa: SLF001 - intentional

    def _on_account_rule_changed(self, target, stop) -> None:
        self.account_target_inr = float(target) if target else None
        self.account_stop_inr = float(stop) if stop else None
        self.worker.account_target_inr = self.account_target_inr
        self.worker.account_stop_inr = self.account_stop_inr

    def _on_secrets_save(self, token: str, api_key: str, api_secret: str) -> None:
        if token:
            secrets_store.set(secrets_store.KEY_ACCESS_TOKEN, token)
        if api_key:
            secrets_store.set(secrets_store.KEY_API_KEY, api_key)
        if api_secret:
            secrets_store.set(secrets_store.KEY_API_SECRET, api_secret)
        QMessageBox.information(
            self.window, "Credentials saved",
            "Restart will pick up new credentials, or change mode to reconnect.",
        )

    def _on_mode_change(self, mode: Mode) -> None:
        # Stop current worker, swap broker, start a new worker.
        try:
            self.worker.stop()
        except Exception:
            pass
        if self.thread is not None:
            self.thread.quit()
            self.thread.wait(2000)

        self.settings.mode = mode
        self.broker = _make_broker(self.settings)
        self.worker = MonitorWorker(
            self.broker, self.settings, self.db, self.notifier,
            default_rule_factory=_default_rule_factory(self.settings),
            account_target_inr=self.account_target_inr,
            account_stop_inr=self.account_stop_inr,
        )
        self._wire_signals()
        self.thread = start_worker(self.worker)
        self.window.setMode(mode)

    def _on_settings_changed(self, new: Settings) -> None:
        self.settings = new
        # Apply runtime-tunable values without restart.
        self.worker.settings = new
        self.worker.executor.settings = new
        self.worker.risk.settings = new

    def _on_export_events(self, path: str) -> None:
        try:
            n = self.db.export_events_csv(path)
        except Exception as e:
            QMessageBox.warning(self.window, "Export", f"Failed: {e}")
            return
        QMessageBox.information(self.window, "Export", f"Wrote {n} rows to:\n{path}")


def main() -> int:
    settings = Settings.from_env()
    app = QApplication(sys.argv)
    app.setApplicationName("Groww Auto-Exit")

    controller = AppController(settings)
    controller.run()

    rc = app.exec()
    controller.shutdown()
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
