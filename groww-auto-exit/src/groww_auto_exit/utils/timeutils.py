"""Time helpers, primarily for the trading-hours filter and audit timestamps."""
from __future__ import annotations

from datetime import date, datetime, time as dtime
from typing import Optional


def parse_hhmm(s: str) -> dtime:
    h, _, m = s.partition(":")
    return dtime(int(h), int(m))


def is_within_window(
    now: datetime,
    start_hhmm: str,
    end_hhmm: str,
) -> bool:
    """True if `now`'s time-of-day is within [start, end] inclusive."""
    t = now.time().replace(second=0, microsecond=0)
    return parse_hhmm(start_hhmm) <= t <= parse_hhmm(end_hhmm)


def today_str(now: Optional[datetime] = None) -> str:
    n = now or datetime.now()
    return n.strftime("%Y-%m-%d")


def fmt_ts(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%H:%M:%S")
