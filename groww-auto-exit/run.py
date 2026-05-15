"""Convenience entrypoint so the app can be launched as `python run.py`."""
from __future__ import annotations

import sys
from pathlib import Path

# Make `src` importable when running from a checkout (no install).
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from groww_auto_exit.main import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
