"""Structured logging configuration.

We use the stdlib `logging` module with a JSON-ish line formatter that is easy
to grep but also human readable. Logs go to both stderr and a rotating file
inside the app's log directory.
"""
from __future__ import annotations

import logging
import logging.handlers
import sys
from pathlib import Path


_FORMAT = (
    "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
)


def configure_logging(log_dir: Path, level: int = logging.INFO) -> None:
    """Configure root logging once. Idempotent for tests."""
    log_dir.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(level)

    # Avoid duplicate handlers if called twice.
    for h in list(root.handlers):
        root.removeHandler(h)

    fmt = logging.Formatter(_FORMAT)

    stream = logging.StreamHandler(sys.stderr)
    stream.setFormatter(fmt)
    root.addHandler(stream)

    fh = logging.handlers.RotatingFileHandler(
        log_dir / "groww_auto_exit.log",
        maxBytes=2_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    fh.setFormatter(fmt)
    root.addHandler(fh)

    # Quiet noisy libraries.
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("websocket").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
