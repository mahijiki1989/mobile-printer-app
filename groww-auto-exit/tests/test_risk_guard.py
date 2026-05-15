"""Risk guard unit tests."""
from __future__ import annotations

from datetime import datetime

import pytest

from groww_auto_exit.config import Settings
from groww_auto_exit.services.risk_guard import RiskGuard


def _settings(**over) -> Settings:
    base = dict(
        trading_hours_start="09:15",
        trading_hours_end="15:25",
        cooldown_seconds=30,
        max_open_positions=10,
        daily_max_loss_inr=-5000.0,
        kill_switch_disconnects=3,
    )
    base.update(over)
    return Settings(**base)


def _at(hh: int, mm: int) -> datetime:
    return datetime(2026, 5, 15, hh, mm, 0)


def test_allows_within_hours_and_no_caps_breached():
    g = RiskGuard(_settings())
    r = g.can_exit("k1", open_positions_count=2, now=_at(10, 0), day="2026-05-15")
    assert r.allowed, r.reason


def test_blocks_outside_trading_hours():
    g = RiskGuard(_settings())
    r = g.can_exit("k1", open_positions_count=2, now=_at(8, 0), day="2026-05-15")
    assert not r.allowed
    assert "trading hours" in r.reason


def test_blocks_after_kill_switch_trips():
    g = RiskGuard(_settings(kill_switch_disconnects=2))
    g.record_disconnect()
    g.record_disconnect()
    assert g.kill_switch_tripped
    r = g.can_exit("k1", open_positions_count=1, now=_at(10, 0), day="2026-05-15")
    assert not r.allowed
    assert "kill" in r.reason.lower()


def test_blocks_after_daily_loss_cap():
    g = RiskGuard(_settings(daily_max_loss_inr=-1000.0))
    g.record_realised_pnl(-1500.0, day="2026-05-15")
    r = g.can_exit("k1", open_positions_count=1, now=_at(10, 0), day="2026-05-15")
    assert not r.allowed
    assert "loss cap" in r.reason


def test_blocks_after_circuit_breaker_rejections():
    g = RiskGuard(_settings())
    for _ in range(3):
        g.record_order_result(rejected=True)
    r = g.can_exit("k1", open_positions_count=1, now=_at(10, 0), day="2026-05-15")
    assert not r.allowed
    assert "circuit breaker" in r.reason


def test_resets_circuit_breaker_on_clean_fill():
    g = RiskGuard(_settings())
    g.record_order_result(rejected=True)
    g.record_order_result(rejected=True)
    g.record_order_result(rejected=False)
    r = g.can_exit("k1", open_positions_count=1, now=_at(10, 0), day="2026-05-15")
    assert r.allowed


def test_blocks_when_too_many_open_positions():
    g = RiskGuard(_settings(max_open_positions=2))
    r = g.can_exit("k1", open_positions_count=5, now=_at(10, 0), day="2026-05-15")
    assert not r.allowed
    assert "open positions" in r.reason


def test_dedup_via_inflight():
    g = RiskGuard(_settings())
    assert g.begin_exit("k1") is True
    assert g.begin_exit("k1") is False
    g.end_exit("k1")
    # cooldown now applies
    r = g.can_exit("k1", open_positions_count=1, now=_at(10, 0), day="2026-05-15")
    assert not r.allowed
    assert "cooldown" in r.reason


def test_panic_mode_overrides_other_blocks():
    g = RiskGuard(_settings())
    g.trip_kill_switch(True)
    g.set_panic(True)
    r = g.can_exit("k1", open_positions_count=1, now=_at(10, 0), day="2026-05-15")
    assert r.allowed
    assert "panic" in r.reason.lower()
