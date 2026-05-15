"""SQLite-backed persistence: rules, audit log, daily P&L, simple settings.

The schema is intentionally small and append-only for events. The DB lives in
`%LOCALAPPDATA%\\GrowwAutoExit\\gae.sqlite3` by default.
"""
from __future__ import annotations

import csv
import json
import sqlite3
import threading
import time
from pathlib import Path
from typing import Optional

from .models import (
    AuditEvent,
    EventType,
    ExitMode,
    ExitRule,
    RuleMode,
)


_SCHEMA = """
CREATE TABLE IF NOT EXISTS rules (
    position_key TEXT PRIMARY KEY,
    rule_mode    TEXT NOT NULL,
    target_inr   REAL,
    stop_inr     REAL,
    trail_lock_inr REAL,
    trail_giveback_inr REAL,
    exit_mode    TEXT NOT NULL,
    partial_qty  INTEGER,
    enabled      INTEGER NOT NULL DEFAULT 1,
    updated_at   REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    ts           REAL NOT NULL,
    event_type   TEXT NOT NULL,
    message      TEXT NOT NULL,
    position_key TEXT,
    order_id     TEXT,
    payload_json TEXT
);
CREATE INDEX IF NOT EXISTS idx_events_ts ON events(ts);
CREATE INDEX IF NOT EXISTS idx_events_pos ON events(position_key);

CREATE TABLE IF NOT EXISTS daily_pnl (
    day        TEXT PRIMARY KEY,   -- YYYY-MM-DD
    realised   REAL NOT NULL DEFAULT 0,
    updated_at REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS kv (
    k TEXT PRIMARY KEY,
    v TEXT
);
"""


class Database:
    """Thread-safe (via a lock) wrapper around a single sqlite3 connection.

    Sqlite3 is fine for this workload: low write rate, single-process.
    """

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._conn = sqlite3.connect(str(self.path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL;")
        self._conn.execute("PRAGMA synchronous=NORMAL;")
        with self._lock:
            self._conn.executescript(_SCHEMA)
            self._conn.commit()

    # --------------------------------------------------------------- close
    def close(self) -> None:
        with self._lock:
            self._conn.close()

    # --------------------------------------------------------------- rules
    def upsert_rule(self, position_key: str, rule: ExitRule) -> None:
        with self._lock:
            self._conn.execute(
                """
                INSERT INTO rules (
                    position_key, rule_mode, target_inr, stop_inr,
                    trail_lock_inr, trail_giveback_inr, exit_mode,
                    partial_qty, enabled, updated_at
                ) VALUES (?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(position_key) DO UPDATE SET
                    rule_mode=excluded.rule_mode,
                    target_inr=excluded.target_inr,
                    stop_inr=excluded.stop_inr,
                    trail_lock_inr=excluded.trail_lock_inr,
                    trail_giveback_inr=excluded.trail_giveback_inr,
                    exit_mode=excluded.exit_mode,
                    partial_qty=excluded.partial_qty,
                    enabled=excluded.enabled,
                    updated_at=excluded.updated_at
                """,
                (
                    position_key,
                    rule.rule_mode.value,
                    rule.target_inr,
                    rule.stop_inr,
                    rule.trail_lock_inr,
                    rule.trail_giveback_inr,
                    rule.exit_mode.value,
                    rule.partial_qty,
                    1 if rule.enabled else 0,
                    time.time(),
                ),
            )
            self._conn.commit()

    def get_rule(self, position_key: str) -> Optional[ExitRule]:
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM rules WHERE position_key = ?",
                (position_key,),
            ).fetchone()
        return _row_to_rule(row) if row else None

    def all_rules(self) -> dict[str, ExitRule]:
        with self._lock:
            rows = self._conn.execute("SELECT * FROM rules").fetchall()
        return {r["position_key"]: _row_to_rule(r) for r in rows}

    def delete_rule(self, position_key: str) -> None:
        with self._lock:
            self._conn.execute("DELETE FROM rules WHERE position_key=?", (position_key,))
            self._conn.commit()

    # --------------------------------------------------------------- events
    def log_event(self, ev: AuditEvent) -> int:
        with self._lock:
            cur = self._conn.execute(
                """INSERT INTO events
                   (ts, event_type, message, position_key, order_id, payload_json)
                   VALUES (?,?,?,?,?,?)""",
                (
                    ev.ts,
                    ev.event_type.value,
                    ev.message,
                    ev.position_key,
                    ev.order_id,
                    json.dumps(ev.payload, default=str) if ev.payload else None,
                ),
            )
            self._conn.commit()
            return int(cur.lastrowid)

    def recent_events(self, limit: int = 200) -> list[AuditEvent]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT * FROM events ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [_row_to_event(r) for r in rows]

    def export_events_csv(self, dest: Path) -> int:
        """Dump every event to a CSV file. Returns number of rows written."""
        dest = Path(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        n = 0
        with self._lock:
            rows = self._conn.execute(
                "SELECT * FROM events ORDER BY id ASC"
            ).fetchall()
        with dest.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(
                ["id", "ts", "event_type", "message", "position_key", "order_id", "payload_json"]
            )
            for r in rows:
                w.writerow(
                    [
                        r["id"],
                        r["ts"],
                        r["event_type"],
                        r["message"],
                        r["position_key"],
                        r["order_id"],
                        r["payload_json"] or "",
                    ]
                )
                n += 1
        return n

    # --------------------------------------------------------------- pnl
    def add_realised_pnl(self, day: str, delta: float) -> float:
        with self._lock:
            self._conn.execute(
                """INSERT INTO daily_pnl (day, realised, updated_at)
                   VALUES (?,?,?)
                   ON CONFLICT(day) DO UPDATE SET
                     realised = realised + excluded.realised,
                     updated_at = excluded.updated_at""",
                (day, delta, time.time()),
            )
            self._conn.commit()
            row = self._conn.execute(
                "SELECT realised FROM daily_pnl WHERE day=?", (day,)
            ).fetchone()
        return float(row["realised"]) if row else 0.0

    def get_realised_pnl(self, day: str) -> float:
        with self._lock:
            row = self._conn.execute(
                "SELECT realised FROM daily_pnl WHERE day=?", (day,)
            ).fetchone()
        return float(row["realised"]) if row else 0.0

    # --------------------------------------------------------------- kv
    def kv_get(self, k: str) -> Optional[str]:
        with self._lock:
            row = self._conn.execute("SELECT v FROM kv WHERE k=?", (k,)).fetchone()
        return row["v"] if row else None

    def kv_set(self, k: str, v: str) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT INTO kv(k,v) VALUES(?,?) ON CONFLICT(k) DO UPDATE SET v=excluded.v",
                (k, v),
            )
            self._conn.commit()


# ----------------------------------------------------------- row mapping

def _row_to_rule(row: sqlite3.Row) -> ExitRule:
    return ExitRule(
        rule_mode=RuleMode(row["rule_mode"]),
        target_inr=row["target_inr"],
        stop_inr=row["stop_inr"],
        trail_lock_inr=row["trail_lock_inr"],
        trail_giveback_inr=row["trail_giveback_inr"],
        exit_mode=ExitMode(row["exit_mode"]),
        partial_qty=row["partial_qty"],
        enabled=bool(row["enabled"]),
    )


def _row_to_event(row: sqlite3.Row) -> AuditEvent:
    payload = {}
    if row["payload_json"]:
        try:
            payload = json.loads(row["payload_json"])
        except json.JSONDecodeError:
            payload = {"_raw": row["payload_json"]}
    return AuditEvent(
        event_type=EventType(row["event_type"]),
        message=row["message"],
        position_key=row["position_key"],
        order_id=row["order_id"],
        payload=payload,
        ts=float(row["ts"]),
    )


# convenience for callers that want to log without constructing an AuditEvent
def make_event(
    event_type: EventType,
    message: str,
    *,
    position_key: Optional[str] = None,
    order_id: Optional[str] = None,
    payload: Optional[dict] = None,
) -> AuditEvent:
    return AuditEvent(
        event_type=event_type,
        message=message,
        position_key=position_key,
        order_id=order_id,
        payload=payload or {},
    )
