"""The single background worker that drives the trading loop.

Lives on its own QThread. It owns:

- the BrokerAdapter (and its connection lifecycle)
- the PositionMonitor (polling + optional WS push)
- the RuleEngine + RiskGuard
- the ExitExecutor

It emits Qt signals into the UI for every interesting event, and exposes
slots for user actions (panic, pause/resume, set rule, manual exit).
"""
from __future__ import annotations

import logging
import time
from dataclasses import asdict
from typing import Optional, Sequence

from PySide6.QtCore import QObject, QThread, Signal, Slot

from ..broker.base import (
    AuthError,
    BrokerAdapter,
    BrokerError,
    TransientError,
)
from ..config import Settings
from ..db import Database, make_event
from ..models import (
    AuditEvent,
    EventType,
    ExitRule,
    Position,
    StatusBadge,
)
from ..notifications import NotificationService, Severity
from ..services.exit_executor import ExitExecutor
from ..services.position_monitor import PositionMonitor
from ..services.risk_guard import RiskGuard
from ..services.rule_engine import Action, RuleEngine, evaluate_account_rule

log = logging.getLogger(__name__)


class MonitorWorker(QObject):
    """QObject moved into a QThread - drives the whole trading loop."""

    # ---------- signals (worker -> UI) ----------
    positionsUpdated = Signal(list)               # list[Position]
    positionDetected = Signal(object)             # Position
    positionClosed = Signal(str)                  # position_key
    ruleArmed = Signal(str, object)               # position_key, ExitRule
    thresholdNear = Signal(str, float)            # position_key, near_pct
    exitTriggered = Signal(str, str)              # position_key, reason
    orderUpdated = Signal(str, str, str)          # position_key, order_id, status
    statusChanged = Signal(object)                # StatusBadge
    connectionChanged = Signal(bool, str)         # connected, message
    eventLogged = Signal(object)                  # AuditEvent
    accountMtmUpdated = Signal(float)             # combined account MTM

    # ---------- internal flow control ----------
    _kickTick = Signal()

    def __init__(
        self,
        broker: BrokerAdapter,
        settings: Settings,
        db: Database,
        notifier: NotificationService,
        default_rule_factory,
        account_target_inr: Optional[float] = None,
        account_stop_inr: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.broker = broker
        self.settings = settings
        self.db = db
        self.notifier = notifier
        self._default_rule_factory = default_rule_factory
        self.account_target_inr = account_target_inr
        self.account_stop_inr = account_stop_inr

        self.risk = RiskGuard(settings)
        self.engine = RuleEngine()
        self.executor = ExitExecutor(broker, self.risk, settings, on_event=self._on_exit_event)
        self.monitor = PositionMonitor(
            broker,
            on_snapshot=self._on_snapshot,
            on_new=self._on_new_position,
            on_closed=self._on_position_closed,
            poll_interval_seconds=settings.poll_interval_seconds,
        )

        self._running = False
        self._paused = False
        self._panic_request = False
        self._stop_request = False
        self._badge = StatusBadge.MONITORING

    # ----------------------------------------------------------- lifecycle

    @Slot()
    def start(self) -> None:
        """Entry point invoked once the thread is started."""
        self._running = True
        self._stop_request = False

        self._connect_broker()
        # Optional WS subscription for derivative position updates.
        if self.settings.use_websocket and self.broker.supports_websocket():
            try:
                self.broker.subscribe_positions(self.monitor.on_feed_push)
            except Exception as e:
                log.warning("ws subscribe failed: %s", e)

        self._loop()

    @Slot()
    def stop(self) -> None:
        self._stop_request = True

    @Slot(bool)
    def set_paused(self, paused: bool) -> None:
        self._paused = bool(paused)
        self._emit_badge(StatusBadge.MONITORING if not paused else StatusBadge.ARMED)

    @Slot()
    def request_panic(self) -> None:
        self._panic_request = True

    @Slot(str, object)
    def set_rule(self, position_key: str, rule: ExitRule) -> None:
        self.db.upsert_rule(position_key, rule)
        ev = make_event(
            EventType.RULE_SET,
            f"rule set for {position_key}",
            position_key=position_key,
            payload=_rule_to_payload(rule),
        )
        self._record(ev)

    @Slot(str)
    def clear_rule(self, position_key: str) -> None:
        self.db.delete_rule(position_key)
        ev = make_event(EventType.RULE_SET, f"rule cleared for {position_key}",
                        position_key=position_key, payload={"cleared": True})
        self._record(ev)

    @Slot(object)
    def manual_exit(self, position: Position) -> None:
        """Send an immediate exit for one position, regardless of rule."""
        outcome = self.executor.square_off(position, reason="manual")
        if outcome.realised_delta:
            self._add_realised_to_db(outcome.realised_delta)

    # ------------------------------------------------------------ main loop

    def _loop(self) -> None:
        next_tick = time.monotonic()
        while not self._stop_request:
            if self._panic_request:
                self._handle_panic()
                self._panic_request = False

            if self._paused:
                time.sleep(0.2)
                continue

            try:
                positions = self.monitor.tick()
                self.risk.record_reconnect()
                self._evaluate_all(positions)
            except AuthError as e:
                log.error("auth error: %s", e)
                self.connectionChanged.emit(False, f"auth: {e}")
                self._emit_badge(StatusBadge.ERROR)
                self._record(make_event(EventType.ERROR, f"auth: {e}"))
                # back off and try to reconnect once
                time.sleep(2.0)
                self._connect_broker()
            except (TransientError, BrokerError) as e:
                tripped = self.risk.record_disconnect()
                log.warning("broker error in tick: %s (kill_switch=%s)", e, tripped)
                self.connectionChanged.emit(False, str(e))
                self._record(make_event(EventType.DISCONNECTED, str(e)))
                if tripped:
                    self._emit_badge(StatusBadge.ERROR)
                    self._record(make_event(EventType.KILL_SWITCH,
                                            "kill switch tripped after repeated disconnects"))
                    self.notifier.notify(
                        "Groww Auto-Exit: kill switch",
                        "Repeated disconnects. Auto-exit paused.",
                        severity=Severity.ERROR,
                    )
                time.sleep(min(5.0, self.settings.poll_interval_seconds * 2))

            # Steady cadence regardless of work duration.
            next_tick += self.settings.poll_interval_seconds
            sleep_for = max(0.0, next_tick - time.monotonic())
            time.sleep(min(sleep_for, self.settings.poll_interval_seconds))

        # graceful shutdown
        try:
            self.broker.unsubscribe_positions()
        except Exception:
            pass
        try:
            self.broker.disconnect()
        except Exception:
            pass
        self._record(make_event(EventType.APP_STOP, "worker stopped"))

    # ----------------------------------------------------------- connection

    def _connect_broker(self) -> None:
        try:
            self.broker.connect()
            self.connectionChanged.emit(True, "connected")
            self._emit_badge(StatusBadge.MONITORING)
            self._record(make_event(EventType.CONNECTED, f"connected via {self.broker.name}"))
        except AuthError as e:
            self.connectionChanged.emit(False, f"auth: {e}")
            self._emit_badge(StatusBadge.ERROR)
            self._record(make_event(EventType.ERROR, f"auth: {e}"))
            self.notifier.notify(
                "Groww Auto-Exit",
                "Authentication failed. Check your token in Settings.",
                severity=Severity.ERROR,
            )
        except Exception as e:
            self.connectionChanged.emit(False, str(e))
            self._emit_badge(StatusBadge.ERROR)
            self._record(make_event(EventType.ERROR, f"connect: {e}"))

    # ---------------------------------------------------------- evaluation

    def _evaluate_all(self, positions: Sequence[Position]) -> None:
        if not positions:
            self.accountMtmUpdated.emit(0.0)
            return

        self.accountMtmUpdated.emit(sum(p.mtm for p in positions))

        rules = self.db.all_rules()
        any_armed = False
        for p in positions:
            rule = rules.get(p.key()) or self._default_rule_factory()
            decision = self.engine.evaluate(p, rule)
            if decision.action == Action.ARM:
                any_armed = True
                self.ruleArmed.emit(p.key(), rule)
            elif decision.action == Action.THRESHOLD_NEAR:
                self.thresholdNear.emit(p.key(), decision.near_pct)
                self.notifier.notify(
                    "Threshold near",
                    f"{p.symbol} MTM {p.mtm:+.2f}",
                    severity=Severity.WARN, sound=False,
                )
            elif decision.action == Action.TRIGGER_EXIT:
                self._fire_exit(p, rule, decision.reason, decision.exit_quantity)

        # Account-level combined rule
        acct = evaluate_account_rule(list(positions), self.account_target_inr, self.account_stop_inr)
        if acct.action == Action.TRIGGER_EXIT:
            self._record(make_event(EventType.EXIT_TRIGGERED,
                                    f"account-level: {acct.reason}",
                                    payload={"scope": "account"}))
            self._emit_badge(StatusBadge.EXIT_TRIGGERED)
            for p in positions:
                self._fire_exit(p, self._default_rule_factory(), "account-rule", p.abs_quantity)

        if any_armed and self._badge == StatusBadge.MONITORING:
            self._emit_badge(StatusBadge.ARMED)

    def _fire_exit(self, position: Position, rule: ExitRule, reason: str, qty: int) -> None:
        # Risk gate
        snap = self.monitor.snapshot()
        guard = self.risk.can_exit(
            position.key(),
            open_positions_count=len(snap),
        )
        if not guard.allowed:
            log.info("exit blocked for %s: %s", position.key(), guard.reason)
            self._record(make_event(
                EventType.RULE_ARMED,
                f"trigger blocked by risk guard: {guard.reason}",
                position_key=position.key(),
                payload={"reason": reason},
            ))
            return

        self._emit_badge(StatusBadge.EXIT_TRIGGERED)
        self.exitTriggered.emit(position.key(), reason)
        self.notifier.notify(
            "Exit triggered",
            f"{position.symbol} reason={reason}",
            severity=Severity.SUCCESS,
        )

        outcome = self.executor.square_off(position, rule, quantity=qty, reason=reason)
        if outcome.ok:
            self._emit_badge(StatusBadge.EXITED)
            self.notifier.notify(
                "Exit filled",
                f"{position.symbol} qty={outcome.order.filled_quantity if outcome.order else 0}",
                severity=Severity.SUCCESS,
            )
        else:
            self._emit_badge(StatusBadge.ERROR)
            self.notifier.notify(
                "Exit failed",
                f"{position.symbol}: {outcome.reason}",
                severity=Severity.ERROR,
            )

        if outcome.realised_delta:
            self._add_realised_to_db(outcome.realised_delta)

    def _handle_panic(self) -> None:
        self._record(make_event(EventType.PANIC_EXIT, "panic exit-all requested"))
        self.notifier.notify(
            "PANIC EXIT", "Squaring off all positions immediately.",
            severity=Severity.WARN,
        )
        try:
            positions = self.broker.get_positions()
        except Exception as e:
            log.error("panic: failed to fetch positions: %s", e)
            self._emit_badge(StatusBadge.ERROR)
            return
        self.executor.panic_exit_all(positions)
        self._emit_badge(StatusBadge.MONITORING)

    # ---------------------------------------------------------- callbacks

    def _on_snapshot(self, positions: Sequence[Position]) -> None:
        self.positionsUpdated.emit(list(positions))

    def _on_new_position(self, p: Position) -> None:
        self.positionDetected.emit(p)
        self._record(make_event(
            EventType.POSITION_DETECTED,
            f"detected {p.symbol} qty={p.quantity} avg={p.avg_price}",
            position_key=p.key(),
            payload={"avg_price": p.avg_price, "qty": p.quantity},
        ))
        self.notifier.notify(
            "New position", f"{p.symbol} qty={p.quantity} avg={p.avg_price}",
            severity=Severity.INFO,
        )
        # Auto-attach default rule if no per-position rule exists.
        if self.db.get_rule(p.key()) is None:
            rule = self._default_rule_factory()
            if rule.target_inr is not None or rule.stop_inr is not None:
                self.db.upsert_rule(p.key(), rule)
                self._record(make_event(
                    EventType.RULE_SET,
                    f"default rule attached for {p.symbol}",
                    position_key=p.key(),
                    payload=_rule_to_payload(rule),
                ))

    def _on_position_closed(self, key: str) -> None:
        self.positionClosed.emit(key)
        self._record(make_event(EventType.POSITION_CLOSED, f"closed {key}", position_key=key))

    def _on_exit_event(self, etype: str, payload: dict) -> None:
        try:
            ev_type = EventType(etype)
        except ValueError:
            ev_type = EventType.ERROR
        self._record(make_event(
            ev_type,
            payload.get("reason") or payload.get("status") or etype.lower(),
            position_key=payload.get("position_key"),
            order_id=payload.get("order_id"),
            payload=payload,
        ))
        if "order_id" in payload and payload.get("order_id"):
            self.orderUpdated.emit(
                payload.get("position_key") or "",
                str(payload["order_id"]),
                str(payload.get("status") or etype),
            )

    # -------------------------------------------------------------- helpers

    def _emit_badge(self, badge: StatusBadge) -> None:
        if badge != self._badge:
            self._badge = badge
            self.statusChanged.emit(badge)

    def _record(self, ev: AuditEvent) -> None:
        try:
            self.db.log_event(ev)
        except Exception as e:  # pragma: no cover
            log.warning("db log failed: %s", e)
        self.eventLogged.emit(ev)

    def _add_realised_to_db(self, delta: float) -> None:
        from ..utils.timeutils import today_str
        try:
            self.db.add_realised_pnl(today_str(), float(delta))
        except Exception:
            pass


# ---------------------------------------------------------------- helpers

def _rule_to_payload(rule: ExitRule) -> dict:
    """Serialise an ExitRule to a JSON-friendly dict."""
    d = asdict(rule)
    # Enum -> str
    d["rule_mode"] = rule.rule_mode.value
    d["exit_mode"] = rule.exit_mode.value
    return d


# ------------------------------------------------------------------ runner

def start_worker(worker: MonitorWorker) -> QThread:
    """Move `worker` onto a fresh QThread and start it. Returns the thread."""
    thread = QThread()
    worker.moveToThread(thread)
    thread.started.connect(worker.start)
    thread.start()
    return thread
