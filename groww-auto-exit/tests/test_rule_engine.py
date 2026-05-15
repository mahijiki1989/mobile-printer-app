"""Rule engine unit tests.

The engine is pure (no I/O), so we feed it synthetic Position/ExitRule pairs
and check the returned Decision is exactly what the spec promises.
"""
from __future__ import annotations

import pytest

from groww_auto_exit.models import (
    Exchange, ExitMode, ExitRule, Position, Product, RuleMode, Segment,
)
from groww_auto_exit.services.rule_engine import (
    Action, RuleEngine, evaluate_account_rule,
)


def _long(qty: int = 10, avg: float = 100.0, ltp: float = 100.0) -> Position:
    return Position(
        symbol="ACME", exchange=Exchange.NSE, segment=Segment.CASH,
        product=Product.MIS, quantity=qty, avg_price=avg, ltp=ltp,
    )


def _short(qty: int = 10, avg: float = 100.0, ltp: float = 100.0) -> Position:
    return Position(
        symbol="ACME", exchange=Exchange.NSE, segment=Segment.CASH,
        product=Product.MIS, quantity=-qty, avg_price=avg, ltp=ltp,
    )


def _fno_long(qty: int = 50, avg: float = 100.0, ltp: float = 100.0) -> Position:
    return Position(
        symbol="NIFTY24500CE", exchange=Exchange.NSE, segment=Segment.FNO,
        product=Product.NRML, quantity=qty, avg_price=avg, ltp=ltp,
        contract_size=1,
    )


# ----------------------------------------------------- target / stop


def test_long_target_triggers_exit_when_mtm_at_or_above_target():
    engine = RuleEngine()
    pos = _long(qty=10, avg=100.0, ltp=200.0)  # MTM = +1000
    rule = ExitRule(target_inr=1000.0)
    d = engine.evaluate(pos, rule)
    assert d.action == Action.TRIGGER_EXIT
    assert d.exit_quantity == 10


def test_long_below_target_is_armed():
    engine = RuleEngine()
    pos = _long(qty=10, avg=100.0, ltp=120.0)  # MTM = +200
    rule = ExitRule(target_inr=1000.0)
    d = engine.evaluate(pos, rule)
    assert d.action == Action.ARM


def test_long_stop_triggers_when_mtm_le_stop():
    engine = RuleEngine()
    pos = _long(qty=10, avg=100.0, ltp=49.0)  # MTM = -510
    rule = ExitRule(stop_inr=-500.0)
    d = engine.evaluate(pos, rule)
    assert d.action == Action.TRIGGER_EXIT


def test_short_target_triggers_when_price_falls():
    engine = RuleEngine()
    # short 10 from 100, price 90 -> MTM = +100. price 0 -> +1000.
    pos = _short(qty=10, avg=100.0, ltp=0.0)
    rule = ExitRule(target_inr=1000.0)
    d = engine.evaluate(pos, rule)
    assert d.action == Action.TRIGGER_EXIT


def test_short_stop_triggers_when_price_rises():
    engine = RuleEngine()
    # short 10 from 100, price 200 -> MTM = -1000.
    pos = _short(qty=10, avg=100.0, ltp=200.0)
    rule = ExitRule(stop_inr=-500.0)
    d = engine.evaluate(pos, rule)
    assert d.action == Action.TRIGGER_EXIT


# -------------------------------------------------------- threshold near


def test_threshold_near_band():
    engine = RuleEngine(near_band=0.20)
    pos = _long(qty=10, avg=100.0, ltp=185.0)  # MTM=+850, target=1000 -> 85%
    rule = ExitRule(target_inr=1000.0)
    d = engine.evaluate(pos, rule)
    assert d.action == Action.THRESHOLD_NEAR
    assert d.near_pct >= 0.80


# ----------------------------------------------------------- trailing


def test_trailing_locks_then_giveback_triggers():
    engine = RuleEngine()
    pos = _long(qty=10, avg=100.0, ltp=180.0)  # MTM=+800
    rule = ExitRule(
        target_inr=10_000.0,
        trail_lock_inr=500.0,
        trail_giveback_inr=200.0,
    )
    # Walk LTP up to lock the trail.
    d1 = engine.evaluate(pos, rule)
    assert rule.trail_locked is True
    assert d1.action in (Action.ARM, Action.THRESHOLD_NEAR)

    # Then walk back: MTM=+550, peak was 800, giveback 200 -> threshold 600.
    pos2 = _long(qty=10, avg=100.0, ltp=155.0)
    d2 = engine.evaluate(pos2, rule)
    assert d2.action == Action.TRIGGER_EXIT


def test_trailing_does_not_trigger_before_lock():
    engine = RuleEngine()
    pos = _long(qty=10, avg=100.0, ltp=120.0)  # MTM=+200
    rule = ExitRule(
        target_inr=10_000.0,
        trail_lock_inr=500.0,
        trail_giveback_inr=100.0,
    )
    d = engine.evaluate(pos, rule)
    assert d.action == Action.ARM
    assert rule.trail_locked is False


# ------------------------------------------------------- partial vs full


def test_partial_exit_returns_partial_qty():
    engine = RuleEngine()
    pos = _fno_long(qty=50, avg=100.0, ltp=120.0)  # MTM=+1000
    rule = ExitRule(
        target_inr=1000.0,
        exit_mode=ExitMode.PARTIAL,
        partial_qty=20,
    )
    d = engine.evaluate(pos, rule)
    assert d.action == Action.TRIGGER_EXIT
    assert d.exit_quantity == 20


# ------------------------------------------------------------ disabled


def test_disabled_rule_is_inert():
    engine = RuleEngine()
    pos = _long(qty=10, avg=100.0, ltp=200.0)
    rule = ExitRule(target_inr=1000.0, enabled=False)
    d = engine.evaluate(pos, rule)
    assert d.action == Action.HOLD


def test_no_thresholds_holds():
    engine = RuleEngine()
    rule = ExitRule()  # nothing set
    d = engine.evaluate(_long(), rule)
    assert d.action == Action.HOLD


# ---------------------------------------------------- exit_rule validators


def test_target_must_be_positive():
    with pytest.raises(ValueError):
        ExitRule(target_inr=-1.0)


def test_stop_must_be_negative():
    with pytest.raises(ValueError):
        ExitRule(stop_inr=10.0)


def test_partial_requires_qty():
    with pytest.raises(ValueError):
        ExitRule(exit_mode=ExitMode.PARTIAL)


# ------------------------------------------------------- account-level rule


def test_account_rule_triggers_combined_target():
    p1 = _long(qty=10, avg=100.0, ltp=160.0)  # +600
    p2 = _long(qty=10, avg=100.0, ltp=150.0)  # +500
    d = evaluate_account_rule([p1, p2], target_inr=1000.0, stop_inr=None)
    assert d.action == Action.TRIGGER_EXIT


def test_account_rule_triggers_combined_stop():
    p1 = _long(qty=10, avg=100.0, ltp=70.0)   # -300
    p2 = _long(qty=10, avg=100.0, ltp=70.0)   # -300
    d = evaluate_account_rule([p1, p2], target_inr=None, stop_inr=-500.0)
    assert d.action == Action.TRIGGER_EXIT


def test_account_rule_arms_when_in_band():
    p1 = _long(qty=10, avg=100.0, ltp=110.0)  # +100
    d = evaluate_account_rule([p1], target_inr=1000.0, stop_inr=-500.0)
    assert d.action == Action.ARM
