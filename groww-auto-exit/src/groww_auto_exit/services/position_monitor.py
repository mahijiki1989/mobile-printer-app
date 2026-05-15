"""Position monitor.

Polls the broker for current positions on a fixed cadence and, where supported,
also receives push updates from `GrowwFeed`. Emits structured callbacks that
the UI/worker subscribes to.

This service does NOT make trading decisions. It only reports what's open.
"""
from __future__ import annotations

import logging
import threading
import time
from typing import Callable, Optional, Sequence

from ..broker.base import BrokerAdapter, BrokerError
from ..models import Position

log = logging.getLogger(__name__)

PositionsListener = Callable[[Sequence[Position]], None]
NewPositionListener = Callable[[Position], None]
ClosedPositionListener = Callable[[str], None]  # position_key


class PositionMonitor:
    """Tracks the currently open set, fires events on diff."""

    def __init__(
        self,
        broker: BrokerAdapter,
        on_snapshot: PositionsListener,
        on_new: NewPositionListener,
        on_closed: ClosedPositionListener,
        poll_interval_seconds: float = 2.0,
    ) -> None:
        self.broker = broker
        self.on_snapshot = on_snapshot
        self.on_new = on_new
        self.on_closed = on_closed
        self.poll_interval_seconds = poll_interval_seconds

        self._known: dict[str, Position] = {}
        self._lock = threading.RLock()
        self._last_error: Optional[str] = None

    @property
    def last_error(self) -> Optional[str]:
        return self._last_error

    # ---------------------------------------------------------------- public

    def snapshot(self) -> list[Position]:
        with self._lock:
            return list(self._known.values())

    def tick(self) -> list[Position]:
        """Run one poll cycle. Returns the freshly observed set."""
        try:
            current = self.broker.get_positions()
            self._last_error = None
        except BrokerError as e:
            self._last_error = str(e)
            log.warning("broker error during tick: %s", e)
            raise
        self._diff_and_emit(current)
        return current

    def on_feed_push(self, positions: Sequence[Position]) -> None:
        """Wire this to a websocket push callback (optional)."""
        try:
            self._diff_and_emit(positions)
        except Exception as e:  # pragma: no cover
            log.warning("feed push handler failed: %s", e)

    # -------------------------------------------------------------- internal

    def _diff_and_emit(self, current: Sequence[Position]) -> None:
        with self._lock:
            current_map = {p.key(): p for p in current}
            previous_keys = set(self._known.keys())
            current_keys = set(current_map.keys())

            new_keys = current_keys - previous_keys
            closed_keys = previous_keys - current_keys

            self._known = current_map

        # Fire listeners outside the lock so they can call back safely.
        for k in new_keys:
            try:
                self.on_new(current_map[k])
            except Exception as e:
                log.warning("on_new listener error for %s: %s", k, e)
        for k in closed_keys:
            try:
                self.on_closed(k)
            except Exception as e:
                log.warning("on_closed listener error for %s: %s", k, e)
        try:
            self.on_snapshot(list(current_map.values()))
        except Exception as e:
            log.warning("on_snapshot listener error: %s", e)
