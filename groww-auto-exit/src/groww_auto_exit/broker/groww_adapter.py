"""Adapter for Groww's official Python SDK (`growwapi`).

Reference: https://groww.in/trade-api/docs/python-sdk

We deliberately keep the surface narrow: only the methods the rest of the
application needs. Field names from the SDK's response dicts can vary slightly
across versions, so we read defensively via `_safe_get` helpers.

This adapter never automates any Groww UI. It uses the SDK's HTTP/WebSocket
endpoints exclusively.
"""
from __future__ import annotations

import logging
import threading
from typing import Any, Optional

from ..models import (
    Exchange,
    OrderRequest,
    OrderResult,
    OrderStatus,
    OrderType,
    Position,
    Product,
    Segment,
    TransactionType,
    Validity,
)
from .base import (
    AuthError,
    BrokerAdapter,
    BrokerError,
    PositionCallback,
    RateLimitError,
    TransientError,
)

log = logging.getLogger(__name__)


# Map our enums onto whatever string constants the SDK exposes. We resolve
# these lazily because the SDK class attributes are defined on the live
# instance.
def _sdk_const(api: Any, name: str, fallback: str) -> str:
    return getattr(api, name, fallback)


class GrowwAdapter(BrokerAdapter):
    """Real Groww broker adapter."""

    name = "groww"

    def __init__(
        self,
        access_token: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
    ) -> None:
        if not access_token and not (api_key and api_secret):
            raise AuthError(
                "Provide either access_token or (api_key + api_secret) for Groww."
            )
        self._access_token = access_token
        self._api_key = api_key
        self._api_secret = api_secret
        self._api: Any = None
        self._feed: Any = None
        self._connected = False
        self._lock = threading.RLock()
        self._position_cb: Optional[PositionCallback] = None

    # ------------------------------------------------------------ lifecycle
    def connect(self) -> None:
        try:
            from growwapi import GrowwAPI  # type: ignore
        except Exception as e:  # pragma: no cover - import issue
            raise BrokerError(
                "growwapi SDK is not installed. `pip install growwapi`."
            ) from e

        try:
            token = self._access_token
            if not token:
                # Some SDK builds expose a helper to mint a token.
                token = GrowwAPI.get_access_token(  # type: ignore[attr-defined]
                    api_key=self._api_key, secret=self._api_secret
                )
                self._access_token = token

            self._api = GrowwAPI(token)

            # Lightweight liveness check. Exact method name can differ
            # across SDK versions; we try the most common one and fall
            # back to a positions fetch.
            try:
                _ = self._api.get_user_details()  # type: ignore[attr-defined]
            except AttributeError:
                _ = self._api.get_positions()  # type: ignore[attr-defined]

            self._connected = True
            log.info("Connected to Groww API")
        except Exception as e:
            self._connected = False
            msg = str(e).lower()
            if "auth" in msg or "token" in msg or "401" in msg or "403" in msg:
                raise AuthError(str(e)) from e
            raise TransientError(f"Groww connect failed: {e}") from e

    def disconnect(self) -> None:
        self._connected = False
        if self._feed is not None:
            try:
                self._feed.disconnect()  # type: ignore[attr-defined]
            except Exception:
                pass
            self._feed = None
        self._api = None

    @property
    def connected(self) -> bool:
        return self._connected and self._api is not None

    # ------------------------------------------------------------- positions
    def get_positions(self) -> list[Position]:
        self._require_api()
        try:
            with self._lock:
                raw = self._api.get_positions()  # type: ignore[attr-defined]
        except Exception as e:
            raise self._classify(e)

        items = _extract_list(raw, ("positions", "data"))
        out: list[Position] = []
        for item in items:
            try:
                pos = self._to_position(item)
            except Exception as e:
                log.warning("Skipping unparsable position row: %s (%s)", item, e)
                continue
            if pos.quantity != 0:
                out.append(pos)
        return out

    def get_ltp(self, position: Position) -> float:
        self._require_api()
        api = self._api
        try:
            with self._lock:
                quote = api.get_ltp(  # type: ignore[attr-defined]
                    exchange=_sdk_const(api, f"EXCHANGE_{position.exchange.value}", position.exchange.value),
                    segment=_sdk_const(api, f"SEGMENT_{position.segment.value}", position.segment.value),
                    trading_symbol=position.symbol,
                )
        except AttributeError:
            # Some SDK versions provide get_quote returning a dict with last_price.
            with self._lock:
                quote = api.get_quote(  # type: ignore[attr-defined]
                    exchange=_sdk_const(api, f"EXCHANGE_{position.exchange.value}", position.exchange.value),
                    segment=_sdk_const(api, f"SEGMENT_{position.segment.value}", position.segment.value),
                    trading_symbol=position.symbol,
                )
        except Exception as e:
            raise self._classify(e)

        return float(_first_float(
            quote, ("last_price", "ltp", "lastPrice", "price", "last_traded_price")
        ) or position.ltp)

    # ---------------------------------------------------------------- orders
    def place_order(self, req: OrderRequest) -> OrderResult:
        self._require_api()
        api = self._api
        try:
            kwargs = {
                "trading_symbol": req.symbol,
                "exchange": _sdk_const(api, f"EXCHANGE_{req.exchange.value}", req.exchange.value),
                "segment": _sdk_const(api, f"SEGMENT_{req.segment.value}", req.segment.value),
                "product": _sdk_const(api, f"PRODUCT_{req.product.value}", req.product.value),
                "order_type": _sdk_const(api, f"ORDER_TYPE_{req.order_type.value}", req.order_type.value),
                "transaction_type": _sdk_const(
                    api, f"TRANSACTION_TYPE_{req.transaction_type.value}", req.transaction_type.value
                ),
                "validity": _sdk_const(api, f"VALIDITY_{req.validity.value}", req.validity.value),
                "quantity": int(req.quantity),
                "order_reference_id": req.order_reference_id,
            }
            if req.price is not None:
                kwargs["price"] = float(req.price)
            if req.trigger_price is not None:
                kwargs["trigger_price"] = float(req.trigger_price)

            with self._lock:
                resp = api.place_order(**kwargs)  # type: ignore[attr-defined]
        except Exception as e:
            raise self._classify(e)

        return _to_order_result(resp, fallback_ref=req.order_reference_id)

    def get_order_status(self, order_id: str) -> OrderResult:
        self._require_api()
        try:
            with self._lock:
                resp = self._api.get_order_status(order_id=order_id)  # type: ignore[attr-defined]
        except AttributeError:
            with self._lock:
                resp = self._api.get_order_details(order_id=order_id)  # type: ignore[attr-defined]
        except Exception as e:
            raise self._classify(e)

        result = _to_order_result(resp)
        if result.order_id is None:
            result = OrderResult(
                order_id=order_id,
                status=result.status,
                filled_quantity=result.filled_quantity,
                avg_fill_price=result.avg_fill_price,
                rejection_reason=result.rejection_reason,
                raw=result.raw,
                order_reference_id=result.order_reference_id,
            )
        return result

    # ------------------------------------------------------------------- WS
    def supports_websocket(self) -> bool:
        try:
            from growwapi import GrowwFeed  # type: ignore  # noqa: F401
            return True
        except Exception:
            return False

    def subscribe_positions(self, cb: PositionCallback) -> None:
        try:
            from growwapi import GrowwFeed  # type: ignore
        except Exception as e:
            log.info("GrowwFeed not available, skipping subscribe: %s", e)
            return

        self._require_api()
        self._position_cb = cb
        try:
            self._feed = GrowwFeed(self._access_token)
            # The SDK exposes a derivative position update stream. If your
            # account/SDK version names this differently, adjust here.
            sub = getattr(self._feed, "subscribe_to_position_updates", None)
            if sub is None:
                log.info("This GrowwFeed build has no position update stream")
                return
            sub(self._on_feed_event)  # type: ignore[misc]
            log.info("Subscribed to Groww position update stream")
        except Exception as e:
            log.warning("Failed to subscribe to GrowwFeed: %s", e)
            self._feed = None

    def unsubscribe_positions(self) -> None:
        if self._feed is None:
            return
        try:
            self._feed.disconnect()  # type: ignore[attr-defined]
        except Exception:
            pass
        self._feed = None
        self._position_cb = None

    # ----- internals ----------------------------------------------------

    def _on_feed_event(self, payload: Any) -> None:
        if self._position_cb is None:
            return
        try:
            items = _extract_list(payload, ("positions", "data"))
            poses = []
            for item in items:
                try:
                    poses.append(self._to_position(item))
                except Exception:
                    continue
            self._position_cb([p for p in poses if p.quantity != 0])
        except Exception as e:  # pragma: no cover
            log.warning("Position feed callback error: %s", e)

    def _require_api(self) -> None:
        if self._api is None:
            raise AuthError("Groww API not connected.")

    @staticmethod
    def _classify(e: Exception) -> BrokerError:
        msg = str(e).lower()
        if "rate" in msg and "limit" in msg:
            return RateLimitError(str(e))
        if "401" in msg or "auth" in msg or "token" in msg:
            return AuthError(str(e))
        if "timeout" in msg or "connection" in msg or "5" in msg[:3]:
            return TransientError(str(e))
        return BrokerError(str(e))

    @staticmethod
    def _to_position(d: dict) -> Position:
        sym = _first(d, ("trading_symbol", "tradingSymbol", "symbol"))
        exch = _first(d, ("exchange", "exchg"))
        seg = _first(d, ("segment", "seg"))
        prod = _first(d, ("product", "product_type", "productType"))
        net_qty = _first(d, ("net_quantity", "netQuantity", "quantity", "qty"))
        avg = _first(d, ("avg_price", "average_price", "avgPrice", "avgCostPrice", "avg_buy_price"))
        ltp = _first(d, ("ltp", "last_price", "lastPrice"))
        realised = _first(d, ("realised_pnl", "realized_pnl", "realisedPnl"))
        lot = _first(d, ("lot_size", "lotSize", "contract_size", "multiplier"))
        groww_sym = _first(d, ("groww_symbol", "growwSymbol"))

        if sym is None or exch is None or seg is None or prod is None:
            raise ValueError(f"Missing fields in position payload: {d}")

        return Position(
            symbol=str(sym),
            exchange=Exchange(str(exch).upper()),
            segment=Segment(str(seg).upper()),
            product=Product(str(prod).upper()),
            quantity=int(net_qty or 0),
            avg_price=float(avg or 0.0),
            ltp=float(ltp or 0.0),
            realised_pnl=float(realised or 0.0),
            groww_symbol=str(groww_sym) if groww_sym else None,
            contract_size=int(lot or 1),
            raw=dict(d),
        )


# ----------------------------------------------------------------- helpers

def _extract_list(raw: Any, keys: tuple[str, ...]) -> list[dict]:
    if raw is None:
        return []
    if isinstance(raw, list):
        return [r for r in raw if isinstance(r, dict)]
    if isinstance(raw, dict):
        for k in keys:
            v = raw.get(k)
            if isinstance(v, list):
                return [r for r in v if isinstance(r, dict)]
            if isinstance(v, dict):
                # Some APIs return {"positions": {"net": [...], "day": [...]}}
                for inner in v.values():
                    if isinstance(inner, list):
                        return [r for r in inner if isinstance(r, dict)]
        # Some APIs return the dict at the top level for a single record.
        if any(k in raw for k in ("trading_symbol", "tradingSymbol", "symbol")):
            return [raw]
    return []


def _first(d: dict, keys: tuple[str, ...]) -> Any:
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return None


def _first_float(d: Any, keys: tuple[str, ...]) -> Optional[float]:
    if not isinstance(d, dict):
        return None
    v = _first(d, keys)
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


_GROWW_STATUS_MAP = {
    "NEW": OrderStatus.NEW,
    "ACKED": OrderStatus.ACKED,
    "APPROVED": OrderStatus.APPROVED,
    "EXECUTED": OrderStatus.EXECUTED,
    "COMPLETED": OrderStatus.COMPLETED,
    "REJECTED": OrderStatus.REJECTED,
    "FAILED": OrderStatus.FAILED,
    "CANCELLED": OrderStatus.CANCELLED,
    "TRIGGER_PENDING": OrderStatus.TRIGGER_PENDING,
}


def _to_order_result(resp: Any, fallback_ref: Optional[str] = None) -> OrderResult:
    if resp is None:
        return OrderResult(order_id=None, status=OrderStatus.UNKNOWN, order_reference_id=fallback_ref)
    d = resp if isinstance(resp, dict) else getattr(resp, "__dict__", {}) or {}
    oid = _first(d, ("order_id", "orderId", "id"))
    status_str = _first(d, ("order_status", "orderStatus", "status"))
    status = _GROWW_STATUS_MAP.get(str(status_str).upper(), OrderStatus.UNKNOWN) if status_str else OrderStatus.UNKNOWN
    filled = _first(d, ("filled_quantity", "filledQuantity", "executed_quantity"))
    avg = _first(d, ("avg_fill_price", "average_price", "avgFillPrice", "average_fill_price"))
    rej = _first(d, ("rejection_reason", "rejectionReason", "remark", "remarks"))
    ref = _first(d, ("order_reference_id", "orderReferenceId")) or fallback_ref
    return OrderResult(
        order_id=str(oid) if oid is not None else None,
        status=status,
        filled_quantity=int(filled or 0),
        avg_fill_price=float(avg or 0.0),
        rejection_reason=str(rej) if rej else None,
        raw=d if isinstance(resp, dict) else {"_repr": repr(resp)},
        order_reference_id=str(ref) if ref else None,
    )
