"""Mock adapter for offline / UI / regression testing.

It hosts a small in-memory book of positions and a price oscillator that walks
LTP up and down so the rule engine can be exercised without any network.

Use `mode=mock` in config to wire this up.
"""
from __future__ import annotations

import logging
import math
import threading
import time
import uuid
from dataclasses import replace
from typing import Optional

from ..models import (
    Exchange,
    OrderRequest,
    OrderResult,
    OrderStatus,
    Position,
    Product,
    Segment,
    TransactionType,
)
from .base import BrokerAdapter

log = logging.getLogger(__name__)


def _seed_book() -> dict[str, Position]:
    """A small representative portfolio: one F&O long, one cash short."""
    nifty = Position(
        symbol="NIFTY24500CE",
        exchange=Exchange.NSE, segment=Segment.FNO, product=Product.NRML,
        quantity=50, avg_price=110.20, ltp=110.20, contract_size=1,
        groww_symbol="NSE-NIFTY-30Sep25-24500-CE",
    )
    rel = Position(
        symbol="RELIANCE",
        exchange=Exchange.NSE, segment=Segment.CASH, product=Product.MIS,
        quantity=-10, avg_price=2840.0, ltp=2840.0, contract_size=1,
    )
    return {p.key(): p for p in (nifty, rel)}


class MockAdapter(BrokerAdapter):
    name = "mock"

    def __init__(self, drift_per_tick: float = 0.6) -> None:
        self._book = _seed_book()
        self._t0 = time.time()
        self._drift = drift_per_tick
        self._connected = False
        self._lock = threading.RLock()
        self._orders: dict[str, OrderResult] = {}

    # ----- lifecycle
    def connect(self) -> None:
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False

    @property
    def connected(self) -> bool:
        return self._connected

    # ----- positions
    def get_positions(self) -> list[Position]:
        with self._lock:
            return [self._with_drifted_ltp(p) for p in self._book.values() if p.quantity != 0]

    def get_ltp(self, position: Position) -> float:
        with self._lock:
            p = self._book.get(position.key(), position)
            return self._drifted_price(p)

    # ----- orders
    def place_order(self, req: OrderRequest) -> OrderResult:
        with self._lock:
            order_id = f"MOCK-{uuid.uuid4().hex[:10]}"
            key = f"{req.exchange.value}:{req.segment.value}:{req.symbol}:{req.product.value}"
            pos = self._book.get(key)
            fill_price = self._drifted_price(pos) if pos else (req.price or 0.0)

            if pos is not None:
                signed = req.quantity if req.transaction_type == TransactionType.BUY else -req.quantity
                new_qty = pos.quantity + signed
                if new_qty == 0:
                    self._book.pop(key, None)
                else:
                    self._book[key] = replace(pos, quantity=new_qty)

            res = OrderResult(
                order_id=order_id,
                status=OrderStatus.EXECUTED,
                filled_quantity=req.quantity,
                avg_fill_price=float(fill_price),
                raw={"mock": True, "request": req.__dict__},
                placed_at=time.time(),
                order_reference_id=req.order_reference_id,
            )
            self._orders[order_id] = res
            log.info(
                "[mock] %s %s qty=%s @ %.2f -> %s",
                req.transaction_type.value, req.symbol, req.quantity, fill_price, order_id,
            )
            return res

    def get_order_status(self, order_id: str) -> OrderResult:
        with self._lock:
            return self._orders.get(order_id) or OrderResult(
                order_id=order_id, status=OrderStatus.UNKNOWN
            )

    # ----- price simulation
    def _drifted_price(self, p: Optional[Position]) -> float:
        if p is None:
            return 0.0
        elapsed = time.time() - self._t0
        # smooth oscillation around avg_price for visual / test friendliness
        return p.avg_price + math.sin(elapsed * 0.5) * self._drift * max(p.avg_price * 0.01, 1.0)

    def _with_drifted_ltp(self, p: Position) -> Position:
        return replace(p, ltp=self._drifted_price(p))

    # ----- test helpers (used by tests/UI)
    def force_set_ltp(self, key: str, ltp: float) -> None:
        with self._lock:
            if key in self._book:
                self._book[key] = replace(self._book[key], ltp=ltp)

    def force_add_position(self, p: Position) -> None:
        with self._lock:
            self._book[p.key()] = p
