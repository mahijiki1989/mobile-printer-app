"""Paper-trading adapter.

Wraps a real `GrowwAdapter` for read-only data (positions, LTP) but never
sends orders. Orders are simulated locally so the rule engine, executor and
UI behave exactly the same as in LIVE mode.

Use this for safe end-to-end validation before flipping to LIVE.
"""
from __future__ import annotations

import logging
import threading
import time
import uuid

from ..models import (
    OrderRequest,
    OrderResult,
    OrderStatus,
    Position,
    TransactionType,
)
from .base import BrokerAdapter, PositionCallback
from .groww_adapter import GrowwAdapter

log = logging.getLogger(__name__)


class PaperAdapter(BrokerAdapter):
    """Read-through to Groww + simulated order placement."""

    name = "paper"

    def __init__(self, real: GrowwAdapter) -> None:
        self._real = real
        self._lock = threading.RLock()
        self._orders: dict[str, OrderResult] = {}
        self._simulated_close: dict[str, int] = {}  # position_key -> qty already simulated-closed

    # ----- lifecycle
    def connect(self) -> None:
        self._real.connect()

    def disconnect(self) -> None:
        self._real.disconnect()

    @property
    def connected(self) -> bool:
        return self._real.connected

    # ----- positions
    def get_positions(self) -> list[Position]:
        positions = self._real.get_positions()
        if not self._simulated_close:
            return positions
        # Subtract simulated-closed quantities so the UI shows the "post-exit" state.
        adjusted: list[Position] = []
        for p in positions:
            closed = self._simulated_close.get(p.key(), 0)
            if closed == 0:
                adjusted.append(p)
                continue
            new_qty = p.quantity - closed if p.is_long else p.quantity + closed
            if new_qty == 0:
                continue
            adjusted.append(
                Position(
                    symbol=p.symbol, exchange=p.exchange, segment=p.segment,
                    product=p.product, quantity=new_qty, avg_price=p.avg_price,
                    ltp=p.ltp, realised_pnl=p.realised_pnl,
                    groww_symbol=p.groww_symbol, contract_size=p.contract_size,
                    raw=p.raw,
                )
            )
        return adjusted

    def get_ltp(self, position: Position) -> float:
        return self._real.get_ltp(position)

    # ----- orders
    def place_order(self, req: OrderRequest) -> OrderResult:
        with self._lock:
            order_id = f"PAPER-{uuid.uuid4().hex[:10]}"
            # Track simulated close for the position view.
            pos_key_prefix = f"{req.exchange.value}:{req.segment.value}:{req.symbol}:{req.product.value}"
            qty_signed = req.quantity if req.transaction_type == TransactionType.BUY else -req.quantity
            self._simulated_close[pos_key_prefix] = (
                self._simulated_close.get(pos_key_prefix, 0) + qty_signed
            )

            # Best-effort fill price using current LTP.
            try:
                fake = Position(
                    symbol=req.symbol, exchange=req.exchange, segment=req.segment,
                    product=req.product, quantity=1, avg_price=0.0, ltp=0.0,
                )
                ltp = self._real.get_ltp(fake)
            except Exception:
                ltp = req.price or 0.0

            res = OrderResult(
                order_id=order_id,
                status=OrderStatus.EXECUTED,
                filled_quantity=req.quantity,
                avg_fill_price=float(ltp),
                raw={"paper": True, "request": req.__dict__},
                placed_at=time.time(),
                order_reference_id=req.order_reference_id,
            )
            self._orders[order_id] = res
            log.info(
                "[paper] simulated %s %s qty=%s on %s @ %s -> %s",
                req.transaction_type.value, req.symbol, req.quantity,
                req.exchange.value, ltp, order_id,
            )
            return res

    def get_order_status(self, order_id: str) -> OrderResult:
        with self._lock:
            res = self._orders.get(order_id)
        if res is None:
            return OrderResult(order_id=order_id, status=OrderStatus.UNKNOWN)
        return res

    # ----- feed
    def supports_websocket(self) -> bool:
        return self._real.supports_websocket()

    def subscribe_positions(self, cb: PositionCallback) -> None:
        self._real.subscribe_positions(cb)

    def unsubscribe_positions(self) -> None:
        self._real.unsubscribe_positions()
