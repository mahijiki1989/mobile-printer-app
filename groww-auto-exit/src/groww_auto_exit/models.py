"""Domain models used across services and the UI.

These are intentionally framework-agnostic dataclasses with light validation,
not Pydantic models. They are passed across thread boundaries via Qt signals,
serialized to SQLite, and produced by every BrokerAdapter in a normalised form.
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


# ---------------------------------------------------------------- enums

class Exchange(str, Enum):
    NSE = "NSE"
    BSE = "BSE"
    MCX = "MCX"


class Segment(str, Enum):
    CASH = "CASH"
    FNO = "FNO"
    COMMODITY = "COMMODITY"


class Product(str, Enum):
    CNC = "CNC"     # delivery (cash)
    MIS = "MIS"     # intraday
    NRML = "NRML"   # carry-forward (F&O)


class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    SL = "SL"
    SL_M = "SL_M"


class Validity(str, Enum):
    DAY = "DAY"
    IOC = "IOC"


class OrderStatus(str, Enum):
    NEW = "NEW"
    ACKED = "ACKED"
    APPROVED = "APPROVED"
    EXECUTED = "EXECUTED"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    TRIGGER_PENDING = "TRIGGER_PENDING"
    UNKNOWN = "UNKNOWN"


TERMINAL_STATUSES = {
    OrderStatus.EXECUTED,
    OrderStatus.COMPLETED,
    OrderStatus.REJECTED,
    OrderStatus.FAILED,
    OrderStatus.CANCELLED,
}


class StatusBadge(str, Enum):
    MONITORING = "MONITORING"
    ARMED = "ARMED"
    EXIT_TRIGGERED = "EXIT_TRIGGERED"
    EXITED = "EXITED"
    ERROR = "ERROR"


# ---------------------------------------------------------------- positions

@dataclass(frozen=True)
class Position:
    """A normalised broker position.

    `quantity` follows the convention:
        positive -> net long
        negative -> net short
        0        -> closed (filtered out by services)
    """
    symbol: str                 # Groww trading_symbol
    exchange: Exchange
    segment: Segment
    product: Product
    quantity: int
    avg_price: float
    ltp: float
    realised_pnl: float = 0.0

    # Optional metadata for the UI / logs / orders.
    groww_symbol: Optional[str] = None       # e.g. "NSE-NIFTY-30Sep25-FUT"
    contract_size: int = 1                   # >1 for F&O lots
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def is_long(self) -> bool:
        return self.quantity > 0

    @property
    def is_short(self) -> bool:
        return self.quantity < 0

    @property
    def abs_quantity(self) -> int:
        return abs(self.quantity)

    @property
    def mtm(self) -> float:
        """Mark-to-market P&L in INR for the open quantity, sign-aware."""
        if self.quantity == 0:
            return self.realised_pnl
        side = 1 if self.is_long else -1
        unreal = (self.ltp - self.avg_price) * self.abs_quantity * self.contract_size * side
        return unreal + self.realised_pnl

    def key(self) -> str:
        """Stable identity for the position, used as map/audit key."""
        return f"{self.exchange.value}:{self.segment.value}:{self.symbol}:{self.product.value}"


# ---------------------------------------------------------------- rules

class RuleMode(str, Enum):
    PER_POSITION = "PER_POSITION"
    ACCOUNT = "ACCOUNT"


class ExitMode(str, Enum):
    ONE_SHOT = "ONE_SHOT"   # exit full quantity in one order
    PARTIAL = "PARTIAL"     # exit `partial_qty` only


@dataclass
class ExitRule:
    """User-defined auto-exit rule."""
    rule_mode: RuleMode = RuleMode.PER_POSITION
    target_inr: Optional[float] = None     # e.g. +1000.0
    stop_inr: Optional[float] = None       # e.g. -500.0
    trail_lock_inr: Optional[float] = None # e.g. lock once profit hits this value
    trail_giveback_inr: Optional[float] = None  # exit if profit retraces by this
    exit_mode: ExitMode = ExitMode.ONE_SHOT
    partial_qty: Optional[int] = None
    enabled: bool = True

    # Runtime trailing state. Not user-editable.
    trail_high_water: Optional[float] = None
    trail_locked: bool = False

    def __post_init__(self) -> None:
        if self.target_inr is not None and self.target_inr <= 0:
            raise ValueError("target_inr must be > 0 (a profit amount)")
        if self.stop_inr is not None and self.stop_inr >= 0:
            raise ValueError("stop_inr must be < 0 (a loss amount)")
        if self.exit_mode == ExitMode.PARTIAL and not self.partial_qty:
            raise ValueError("partial_qty is required when exit_mode=PARTIAL")


# ---------------------------------------------------------------- orders

@dataclass(frozen=True)
class OrderRequest:
    symbol: str
    exchange: Exchange
    segment: Segment
    product: Product
    transaction_type: TransactionType
    quantity: int
    order_type: OrderType
    price: Optional[float] = None
    trigger_price: Optional[float] = None
    validity: Validity = Validity.DAY
    order_reference_id: str = field(default_factory=lambda: f"GAE-{uuid.uuid4().hex[:12]}")


@dataclass
class OrderResult:
    order_id: Optional[str]
    status: OrderStatus
    filled_quantity: int = 0
    avg_fill_price: float = 0.0
    rejection_reason: Optional[str] = None
    raw: dict[str, Any] = field(default_factory=dict)
    placed_at: float = field(default_factory=time.time)
    order_reference_id: Optional[str] = None


# ---------------------------------------------------------------- audit

class EventType(str, Enum):
    APP_START = "APP_START"
    APP_STOP = "APP_STOP"
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    POSITION_DETECTED = "POSITION_DETECTED"
    POSITION_CLOSED = "POSITION_CLOSED"
    RULE_SET = "RULE_SET"
    RULE_ARMED = "RULE_ARMED"
    THRESHOLD_NEAR = "THRESHOLD_NEAR"
    EXIT_TRIGGERED = "EXIT_TRIGGERED"
    ORDER_PLACED = "ORDER_PLACED"
    ORDER_FILLED = "ORDER_FILLED"
    ORDER_REJECTED = "ORDER_REJECTED"
    ORDER_FAILED = "ORDER_FAILED"
    PANIC_EXIT = "PANIC_EXIT"
    KILL_SWITCH = "KILL_SWITCH"
    ERROR = "ERROR"


@dataclass
class AuditEvent:
    event_type: EventType
    message: str
    position_key: Optional[str] = None
    order_id: Optional[str] = None
    payload: dict[str, Any] = field(default_factory=dict)
    ts: float = field(default_factory=time.time)
