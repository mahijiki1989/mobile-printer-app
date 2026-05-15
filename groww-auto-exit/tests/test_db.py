"""Database layer tests."""
from __future__ import annotations

import json
from pathlib import Path

from groww_auto_exit.db import Database, make_event
from groww_auto_exit.models import (
    EventType, ExitMode, ExitRule, RuleMode,
)


def test_rule_roundtrip(tmp_path: Path):
    db = Database(tmp_path / "t.sqlite3")
    rule = ExitRule(
        rule_mode=RuleMode.PER_POSITION,
        target_inr=1000.0,
        stop_inr=-500.0,
        trail_lock_inr=600.0,
        trail_giveback_inr=200.0,
        exit_mode=ExitMode.PARTIAL,
        partial_qty=25,
        enabled=True,
    )
    db.upsert_rule("NSE:CASH:RELIANCE:MIS", rule)
    got = db.get_rule("NSE:CASH:RELIANCE:MIS")
    assert got is not None
    assert got.target_inr == 1000.0
    assert got.stop_inr == -500.0
    assert got.exit_mode == ExitMode.PARTIAL
    assert got.partial_qty == 25
    assert got.enabled is True


def test_rule_upsert_replaces(tmp_path: Path):
    db = Database(tmp_path / "t.sqlite3")
    db.upsert_rule("k", ExitRule(target_inr=100.0))
    db.upsert_rule("k", ExitRule(stop_inr=-100.0))
    got = db.get_rule("k")
    assert got.target_inr is None
    assert got.stop_inr == -100.0


def test_rule_delete(tmp_path: Path):
    db = Database(tmp_path / "t.sqlite3")
    db.upsert_rule("k", ExitRule(target_inr=100.0))
    db.delete_rule("k")
    assert db.get_rule("k") is None


def test_events_log_and_query(tmp_path: Path):
    db = Database(tmp_path / "t.sqlite3")
    db.log_event(make_event(EventType.APP_START, "started"))
    db.log_event(make_event(
        EventType.EXIT_TRIGGERED,
        "trigger fired",
        position_key="k1",
        order_id="O123",
        payload={"foo": 1},
    ))
    rows = db.recent_events(limit=10)
    assert len(rows) == 2
    # Most recent first
    assert rows[0].event_type == EventType.EXIT_TRIGGERED
    assert rows[0].payload == {"foo": 1}


def test_events_export_csv(tmp_path: Path):
    db = Database(tmp_path / "t.sqlite3")
    for i in range(5):
        db.log_event(make_event(EventType.APP_START, f"e{i}"))
    dest = tmp_path / "out.csv"
    n = db.export_events_csv(dest)
    assert n == 5
    text = dest.read_text(encoding="utf-8")
    assert "event_type" in text.splitlines()[0]
    assert "APP_START" in text


def test_daily_pnl(tmp_path: Path):
    db = Database(tmp_path / "t.sqlite3")
    assert db.get_realised_pnl("2026-05-15") == 0.0
    assert db.add_realised_pnl("2026-05-15", -100.0) == -100.0
    assert db.add_realised_pnl("2026-05-15", -50.0) == -150.0
    assert db.get_realised_pnl("2026-05-15") == -150.0


def test_kv_store(tmp_path: Path):
    db = Database(tmp_path / "t.sqlite3")
    assert db.kv_get("foo") is None
    db.kv_set("foo", "bar")
    assert db.kv_get("foo") == "bar"
    db.kv_set("foo", "baz")
    assert db.kv_get("foo") == "baz"
