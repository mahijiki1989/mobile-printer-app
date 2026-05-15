"""Broker adapter interface.

Each backend (real Groww, paper, mock) speaks the same surface, returning the
normalised model types from `groww_auto_exit.models`. The services layer is
written against this interface only - it never imports `growwapi` directly.

Errors are mapped to a small typed hierarchy so retry/backoff logic and the
RiskGuard can react predictably.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Optional, Sequence

from ..models import (
    OrderRequest,
    OrderResult,
    Position,
)


# ---------------------------------------------------------------- errors

class BrokerError(Exception):
    """Base class for any broker-side failure."""


class AuthError(BrokerError):
    """Authentication / token expiry failure. Caller should re-auth."""


class RateLimitError(BrokerError):
    """Broker says we are sending too many requests."""


class TransientError(BrokerError):
    """Network blip / 5xx / WS reconnect needed. Safe to retry."""


# ---------------------------------------------------------------- interface

# A callback receiving fresh `Position` snapshots from the WS feed.
PositionCallback = Callable[[Sequence[Position]], None]


class BrokerAdapter(ABC):
    """Normalised broker interface used by the services and UI."""

    name: str = "abstract"

    # ----- lifecycle ------------------------------------------------

    @abstractmethod
    def connect(self) -> None:
        """Establish credentials, sanity-check connectivity. Raises AuthError."""

    @abstractmethod
    def disconnect(self) -> None:
        """Tear down sessions and any websocket feed."""

    @property
    @abstractmethod
    def connected(self) -> bool: ...

    # ----- account / positions --------------------------------------

    @abstractmethod
    def get_positions(self) -> list[Position]:
        """Snapshot of all open positions (qty != 0)."""

    @abstractmethod
    def get_ltp(self, position: Position) -> float:
        """Latest traded price for a position's instrument."""

    # ----- orders ---------------------------------------------------

    @abstractmethod
    def place_order(self, req: OrderRequest) -> OrderResult:
        """Place an order. Synchronous. Returns initial status + order id."""

    @abstractmethod
    def get_order_status(self, order_id: str) -> OrderResult:
        """Fetch the latest known state of an order."""

    # ----- live feed (optional) -------------------------------------

    def supports_websocket(self) -> bool:
        """Whether `subscribe_positions` does anything useful."""
        return False

    def subscribe_positions(self, cb: PositionCallback) -> None:  # pragma: no cover
        """Optional: register a callback for live position updates.

        Default implementation is a no-op so polling-only adapters work.
        """
        return None

    def unsubscribe_positions(self) -> None:  # pragma: no cover
        return None
