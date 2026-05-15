"""Operational safety checks that wrap the rule-engine output.

The risk guard is the gate between "the rule says exit" and "actually send an
order". It knows about:

- trading-hours window
- daily realised-loss cap
- per-position cooldown after a recent exit
- maximum number of open positions allowed
- a kill-switch counter that trips after N broker disconnects in a row
- a circuit breaker that trips after N consecutive order rejections
- order deduplication per position (prevents firing twice on one threshold)

It is deliberately conservative: when in doubt, deny.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..config import Settings
from ..utils.timeutils import is_within_window, today_str


@dataclass
class GuardResult:
    allowed: bool
    reason: str


class RiskGuard:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._lock = threading.RLock()
        self._last_exit_at: dict[str, float] = {}  # position_key -> ts of last exit attempt
        self._inflight: set[str] = set()           # position_key currently being exited
        self._disconnects = 0
        self._consecutive_rejections = 0
        self._kill_switch_tripped = False
        self._panic_active = False
        self._daily_realised_loss: dict[str, float] = {}  # day -> realised loss (negative)

    # ------------------------------------------------------------ accounting

    def record_disconnect(self) -> bool:
        """Increment the disconnect counter, return True if kill switch trips now."""
        with self._lock:
            self._disconnects += 1
            if self._disconnects >= self.settings.kill_switch_disconnects:
                self._kill_switch_tripped = True
            return self._kill_switch_tripped

    def record_reconnect(self) -> None:
        with self._lock:
            self._disconnects = 0

    def record_order_result(self, *, rejected: bool) -> None:
        with self._lock:
            if rejected:
                self._consecutive_rejections += 1
            else:
                self._consecutive_rejections = 0

    def record_realised_pnl(self, delta: float, *, day: Optional[str] = None) -> float:
        d = day or today_str()
        with self._lock:
            self._daily_realised_loss[d] = self._daily_realised_loss.get(d, 0.0) + float(delta)
            return self._daily_realised_loss[d]

    def set_realised_pnl(self, day: str, value: float) -> None:
        with self._lock:
            self._daily_realised_loss[day] = float(value)

    def trip_kill_switch(self, on: bool = True) -> None:
        with self._lock:
            self._kill_switch_tripped = bool(on)

    def set_panic(self, on: bool) -> None:
        with self._lock:
            self._panic_active = bool(on)

    @property
    def kill_switch_tripped(self) -> bool:
        with self._lock:
            return self._kill_switch_tripped

    @property
    def panic_active(self) -> bool:
        with self._lock:
            return self._panic_active

    # -------------------------------------------------------------- inflight

    def begin_exit(self, position_key: str) -> bool:
        with self._lock:
            if position_key in self._inflight:
                return False
            self._inflight.add(position_key)
            return True

    def end_exit(self, position_key: str) -> None:
        with self._lock:
            self._inflight.discard(position_key)
            self._last_exit_at[position_key] = time.time()

    # ------------------------------------------------------------------ check

    def can_exit(
        self,
        position_key: str,
        *,
        open_positions_count: int,
        now: Optional[datetime] = None,
        day: Optional[str] = None,
    ) -> GuardResult:
        """Decide whether an exit order may be sent right now."""
        n = now or datetime.now()
        d = day or today_str(n)

        with self._lock:
            if self._panic_active:
                # Panic always allows exits, bypass other checks.
                return GuardResult(True, "panic mode")

            if self._kill_switch_tripped:
                return GuardResult(False, "kill-switch tripped")

            if self._consecutive_rejections >= 3:
                return GuardResult(
                    False,
                    f"circuit breaker: {self._consecutive_rejections} consecutive rejections",
                )

            if not is_within_window(
                n, self.settings.trading_hours_start, self.settings.trading_hours_end
            ):
                return GuardResult(False, "outside trading hours")

            if open_positions_count > self.settings.max_open_positions:
                return GuardResult(
                    False,
                    f"open positions {open_positions_count} > max "
                    f"{self.settings.max_open_positions}",
                )

            realised = self._daily_realised_loss.get(d, 0.0)
            cap = self.settings.daily_max_loss_inr
            if cap < 0 and realised <= cap:
                return GuardResult(
                    False,
                    f"daily loss cap reached ({realised:.2f} <= {cap:.2f})",
                )

            last = self._last_exit_at.get(position_key)
            if last is not None:
                cooldown = self.settings.cooldown_seconds
                if (n.timestamp() - last) < cooldown:
                    return GuardResult(
                        False,
                        f"cooldown active for {position_key} ({cooldown}s)",
                    )

            if position_key in self._inflight:
                return GuardResult(False, "exit already in flight")

        return GuardResult(True, "ok")
