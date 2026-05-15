"""
Windows packaging helper.

Usage (from a Windows machine with Python 3.11 + venv activated):

    python -m pip install -r requirements.txt
    python build_windows.py

This invokes PyInstaller with the bundled `app.spec` and produces:

    dist/GrowwAutoExit/GrowwAutoExit.exe

Notes:
- The build is windowed (no console).
- `growwapi` and `PySide6` are added as hidden imports because PyInstaller's
  static analysis can miss dynamic plugin loaders.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    spec = ROOT / "app.spec"
    if not spec.exists():
        print(f"Spec file not found: {spec}", file=sys.stderr)
        return 2

    # Clean previous builds for reproducibility.
    for sub in ("build", "dist"):
        p = ROOT / sub
        if p.exists():
            shutil.rmtree(p, ignore_errors=True)

    cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm", str(spec)]
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
