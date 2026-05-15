"""Application configuration.

Configuration is loaded from environment variables (and from a `.env` file in
the project root if present). Pydantic validates and coerces types.

Sensitive values (Groww access token / api key / api secret) are pulled in once
from the environment and then stored in the OS keyring via `secrets_store`.
After the first successful run users can blank these env vars.
"""
from __future__ import annotations

import os
from enum import Enum
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator

# Load .env from the project root if it exists. Safe to call multiple times.
load_dotenv()


class Mode(str, Enum):
    LIVE = "live"
    PAPER = "paper"
    MOCK = "mock"


class ExitOrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"


def _expand(p: str) -> str:
    """Expand %VAR% on Windows and ~ on POSIX."""
    return os.path.expandvars(os.path.expanduser(p))


def _default_data_dir() -> Path:
    base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~/.local/share")
    return Path(_expand(base)) / "GrowwAutoExit"


class Settings(BaseModel):
    """Strongly typed application settings."""

    mode: Mode = Field(default=Mode.PAPER)

    # Polling / connection
    poll_interval_seconds: float = Field(default=2.0, ge=0.5, le=60.0)
    use_websocket: bool = True
    kill_switch_disconnects: int = Field(default=5, ge=1, le=100)

    # Risk defaults
    default_target_inr: float = 1000.0
    default_stop_inr: float = -500.0
    daily_max_loss_inr: float = -5000.0
    max_open_positions: int = Field(default=10, ge=1, le=500)
    trading_hours_start: str = "09:15"
    trading_hours_end: str = "15:25"
    cooldown_seconds: int = Field(default=30, ge=0, le=3600)

    # Exit behaviour
    exit_order_type: ExitOrderType = ExitOrderType.MARKET
    limit_slippage_pct: float = Field(default=0.10, ge=0.0, le=10.0)
    require_live_confirm: bool = True

    # Storage
    db_path: Path = Field(default_factory=lambda: _default_data_dir() / "gae.sqlite3")
    log_dir: Path = Field(default_factory=lambda: _default_data_dir() / "logs")

    # Bootstrap-only secret values; DO NOT persist these in code.
    bootstrap_access_token: Optional[str] = None
    bootstrap_api_key: Optional[str] = None
    bootstrap_api_secret: Optional[str] = None

    @field_validator("trading_hours_start", "trading_hours_end")
    @classmethod
    def _check_hhmm(cls, v: str) -> str:
        h, _, m = v.partition(":")
        if not (h.isdigit() and m.isdigit() and 0 <= int(h) < 24 and 0 <= int(m) < 60):
            raise ValueError(f"Invalid HH:MM time: {v!r}")
        return v

    # ------------------------------------------------------------------ load
    @classmethod
    def from_env(cls) -> "Settings":
        env = os.environ

        def f(name: str, default: Optional[str] = None) -> Optional[str]:
            v = env.get(name, default)
            return v if v not in ("", None) else default

        return cls(
            mode=Mode(f("GAE_MODE", "paper") or "paper"),
            poll_interval_seconds=float(f("GAE_POLL_INTERVAL_SECONDS", "2") or 2),
            use_websocket=(f("GAE_USE_WEBSOCKET", "true") or "true").lower() == "true",
            kill_switch_disconnects=int(f("GAE_KILL_SWITCH_DISCONNECTS", "5") or 5),
            default_target_inr=float(f("GAE_DEFAULT_TARGET_INR", "1000") or 1000),
            default_stop_inr=float(f("GAE_DEFAULT_STOP_INR", "-500") or -500),
            daily_max_loss_inr=float(f("GAE_DAILY_MAX_LOSS_INR", "-5000") or -5000),
            max_open_positions=int(f("GAE_MAX_OPEN_POSITIONS", "10") or 10),
            trading_hours_start=f("GAE_TRADING_HOURS_START", "09:15") or "09:15",
            trading_hours_end=f("GAE_TRADING_HOURS_END", "15:25") or "15:25",
            cooldown_seconds=int(f("GAE_COOLDOWN_SECONDS", "30") or 30),
            exit_order_type=ExitOrderType(
                (f("GAE_EXIT_ORDER_TYPE", "market") or "market").lower()
            ),
            limit_slippage_pct=float(f("GAE_LIMIT_SLIPPAGE_PCT", "0.10") or 0.10),
            require_live_confirm=(
                (f("GAE_REQUIRE_LIVE_CONFIRM", "true") or "true").lower() == "true"
            ),
            db_path=Path(_expand(f("GAE_DB_PATH", str(_default_data_dir() / "gae.sqlite3"))
                                or str(_default_data_dir() / "gae.sqlite3"))),
            log_dir=Path(_expand(f("GAE_LOG_DIR", str(_default_data_dir() / "logs"))
                                 or str(_default_data_dir() / "logs"))),
            bootstrap_access_token=f("GROWW_ACCESS_TOKEN"),
            bootstrap_api_key=f("GROWW_API_KEY"),
            bootstrap_api_secret=f("GROWW_API_SECRET"),
        )

    # --------------------------------------------------------------- helpers
    def ensure_dirs(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
