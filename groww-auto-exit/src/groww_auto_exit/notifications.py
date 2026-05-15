"""Desktop notification + sound alerts.

Uses `plyer` for cross-platform desktop popups. The sound uses the stdlib
winsound module on Windows, falling back to a no-op on other platforms.
Notifications never raise - failure must not crash the trading loop.
"""
from __future__ import annotations

import logging
import sys
from enum import Enum
from typing import Optional

log = logging.getLogger(__name__)


class Severity(str, Enum):
    INFO = "INFO"
    WARN = "WARN"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


class NotificationService:
    """Thin facade over `plyer.notification` + `winsound`."""

    def __init__(self, app_name: str = "Groww Auto-Exit", enabled: bool = True) -> None:
        self.app_name = app_name
        self.enabled = enabled
        self._notif = None
        self._winsound = None
        try:
            from plyer import notification  # type: ignore
            self._notif = notification
        except Exception as e:  # pragma: no cover - optional
            log.warning("plyer not available, desktop popups disabled: %s", e)

        if sys.platform.startswith("win"):
            try:
                import winsound  # type: ignore
                self._winsound = winsound
            except Exception:  # pragma: no cover - non-Windows
                self._winsound = None

    def notify(
        self,
        title: str,
        message: str,
        *,
        severity: Severity = Severity.INFO,
        sound: bool = True,
        timeout: int = 6,
    ) -> None:
        if not self.enabled:
            return

        if self._notif is not None:
            try:
                self._notif.notify(
                    title=title,
                    message=message,
                    app_name=self.app_name,
                    timeout=timeout,
                )
            except Exception as e:
                log.debug("Desktop notification failed: %s", e)

        if sound and self._winsound is not None:
            try:
                if severity == Severity.ERROR:
                    self._winsound.MessageBeep(self._winsound.MB_ICONHAND)
                elif severity == Severity.WARN:
                    self._winsound.MessageBeep(self._winsound.MB_ICONEXCLAMATION)
                elif severity == Severity.SUCCESS:
                    self._winsound.MessageBeep(self._winsound.MB_OK)
                else:
                    self._winsound.MessageBeep(self._winsound.MB_ICONASTERISK)
            except Exception:
                pass
