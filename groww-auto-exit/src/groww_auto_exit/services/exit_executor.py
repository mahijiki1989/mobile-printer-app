"""Exit executor.

Translates a trigger from the rule engine into a concrete order request, sends
it via the broker adapter, polls for terminal status and reports back. Includes:

- duplicate-trigger protection via RiskGuard.begin_exit/end_exit
- exponential-backoff retries on transient API/network failures
- terminal status polling with a soft timeout
- realised-PnL bookkeeping (best-effort) so the kill switch can react
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Callable, Optional

from ..broker.base import (
    AuthError,
    BrokerAdapter,
    BrokerError,
    RateLimitError,
    TransientError,
)
from ..config import ExitOrderType, Settings
from ..models import (
    ExitRule,
    OrderRequest,
    OrderResult,
    OrderStatus,
    OrderType,
    Position,
    TERMINAL_STATUSES,
    TransactionType,
    Validity,
)
from ..utils.retry import with_retry
from .risk_guard import RiskGuard

log = logging.getLogger(__name__)


@dataclass
class ExitOutcome:
    ok: bool
    reason: str
    order: Optional[OrderResult] = None
    realised_delta: float = 0.0


# Hook so the UI / DB can be informed about lifecycle events.
ExitEventHook = Callable[[str, dict], None]


class ExitExecutor:
    def __init__(
        self,
        broker: BrokerAdapter,
        risk: RiskGuard,
        settings: Settings,
        on_event: Optional[ExitEventHook] = None,
    ) -> None:
        self.broker = broker
        self.risk = risk
        self.settings = settings
        self.on_event = on_event or (lambda *_: None)

    # --------------------------------------------------------------- public

    def square_off(
        self,
        position: Position,
        rule: Optional[ExitRule] = None,
        *,
        quantity: Optional[int] = None,
        reason: str = "rule",
    ) -> ExitOutcome:
        """Send an exit order for `position`. Returns when the order reaches a
        terminal status or the soft timeout expires."""
        key = position.key()
        if not self.risk.begin_exit(key):
            return ExitOutcome(False, "exit already in flight")

        try:
            qty = self._resolve_qty(position, rule, quantity)
            if qty <= 0:
                return ExitOutcome(False, "resolved quantity is 0")

            req = self._build_request(position, qty)
            self.on_event(
                "EXIT_TRIGGERED",
                {
                    "position_key": key,
                    "reason": reason,
                    "request": req.__dict__,
                },
            )

            order = self._place_with_retry(req)
            self.on_event(
                "ORDER_PLACED",
                {"position_key": key, "order_id": order.order_id, "status": order.status.value},
            )

            final = self._wait_for_terminal(order)

            if final.status in (OrderStatus.EXECUTED, OrderStatus.COMPLETED):
                self.risk.record_order_result(rejected=False)
                # crude realised pnl estimate, sign-aware
                side = 1 if position.is_long else -1
                realised = (
                    (final.avg_fill_price - position.avg_price)
                    * final.filled_quantity * position.contract_size * side
                )
                self.risk.record_realised_pnl(realised)
                self.on_event(
                    "ORDER_FILLED",
                    {
                        "position_key": key,
                        "order_id": final.order_id,
                        "filled": final.filled_quantity,
                        "avg_price": final.avg_fill_price,
                        "realised": realised,
                    },
                )
                return ExitOutcome(True, "filled", final, realised_delta=realised)

            # Non-terminal or rejected
            rejected = final.status in (OrderStatus.REJECTED, OrderStatus.FAILED)
            self.risk.record_order_result(rejected=rejected)
            self.on_event(
                "ORDER_REJECTED" if rejected else "ORDER_FAILED",
                {
                    "position_key": key,
                    "order_id": final.order_id,
                    "status": final.status.value,
                    "reason": final.rejection_reason,
                },
            )
            return ExitOutcome(False, f"order ended {final.status.value}", final)

        except AuthError as e:
            log.error("auth error during exit: %s", e)
            self.on_event("ERROR", {"reason": f"auth: {e}"})
            return ExitOutcome(False, f"auth error: {e}")
        except BrokerError as e:
            log.error("broker error during exit: %s", e)
            self.on_event("ERROR", {"reason": f"broker: {e}"})
            return ExitOutcome(False, f"broker error: {e}")
        finally:
            self.risk.end_exit(key)

    # ---------------------------------------------------------------- batch

    def panic_exit_all(self, positions: list[Position]) -> list[ExitOutcome]:
        """Square off every supplied position. Bypasses cooldown via panic mode."""
        self.risk.set_panic(True)
        try:
            outcomes: list[ExitOutcome] = []
            for p in positions:
                outcomes.append(self.square_off(p, reason="panic"))
            return outcomes
        finally:
            self.risk.set_panic(False)

    # ------------------------------------------------------------- internals

    def _resolve_qty(
        self, position: Position, rule: Optional[ExitRule], explicit: Optional[int]
    ) -> int:
        if explicit is not None:
            return min(position.abs_quantity, max(0, int(explicit)))
        if rule is not None:
            from ..models import ExitMode
            if rule.exit_mode == ExitMode.PARTIAL and rule.partial_qty:
                return min(position.abs_quantity, int(rule.partial_qty))
        return position.abs_quantity

    def _build_request(self, position: Position, qty: int) -> OrderRequest:
        # Reverse side to flatten the position.
        txn = TransactionType.SELL if position.is_long else TransactionType.BUY

        if self.settings.exit_order_type == ExitOrderType.LIMIT:
            slippage = max(0.0, self.settings.limit_slippage_pct) / 100.0
            # Pay-up for taker-style fills: longs sell at LTP*(1-slippage), shorts buy at LTP*(1+slippage).
            if position.is_long:
                price = round(position.ltp * (1 - slippage), 2)
            else:
                price = round(position.ltp * (1 + slippage), 2)
            return OrderRequest(
                symbol=position.symbol,
                exchange=position.exchange,
                segment=position.segment,
                product=position.product,
                transaction_type=txn,
                quantity=qty,
                order_type=OrderType.LIMIT,
                price=price,
                validity=Validity.DAY,
            )

        return OrderRequest(
            symbol=position.symbol,
            exchange=position.exchange,
            segment=position.segment,
            product=position.product,
            transaction_type=txn,
            quantity=qty,
            order_type=OrderType.MARKET,
            validity=Validity.DAY,
        )

    def _place_with_retry(self, req: OrderRequest) -> OrderResult:
        return with_retry(
            lambda: self.broker.place_order(req),
            attempts=4,
            base_delay=0.4,
            max_delay=4.0,
            retry_on=(TransientError, RateLimitError),
            label="place_order",
        )

    def _wait_for_terminal(self, order: OrderResult, soft_timeout: float = 8.0) -> OrderResult:
        if order.order_id is None or order.status in TERMINAL_STATUSES:
            return order
        deadline = time.time() + soft_timeout
        latest = order
        while time.time() < deadline:
            try:
                latest = self.broker.get_order_status(order.order_id)
            except (TransientError, RateLimitError):
                time.sleep(0.4)
                continue
            except BrokerError as e:
                log.warning("status poll failed: %s", e)
                break
            if latest.status in TERMINAL_STATUSES:
                return latest
            time.sleep(0.4)
        return latest
