"""Credential storage backed by the OS keyring.

On Windows this is the Credential Manager. On macOS, the Keychain. On Linux,
Secret Service (libsecret). The `keyring` package handles the platform glue.

We never write secrets to disk in plain text. The `.env` file is only used for
*bootstrap* (first-run) secret entry; afterwards values live in the keyring.
"""
from __future__ import annotations

from typing import Optional

import keyring

SERVICE = "GrowwAutoExit"

KEY_ACCESS_TOKEN = "groww_access_token"
KEY_API_KEY = "groww_api_key"
KEY_API_SECRET = "groww_api_secret"


def get(key: str) -> Optional[str]:
    try:
        return keyring.get_password(SERVICE, key)
    except Exception:  # pragma: no cover - keyring backend errors
        return None


def set(key: str, value: str) -> None:  # noqa: A001 - intentional API name
    keyring.set_password(SERVICE, key, value)


def clear(key: str) -> None:
    try:
        keyring.delete_password(SERVICE, key)
    except keyring.errors.PasswordDeleteError:
        pass


def bootstrap_from_env(
    access_token: Optional[str],
    api_key: Optional[str],
    api_secret: Optional[str],
) -> None:
    """Move any bootstrap values from env into the keyring. Idempotent."""
    if access_token:
        set(KEY_ACCESS_TOKEN, access_token)
    if api_key:
        set(KEY_API_KEY, api_key)
    if api_secret:
        set(KEY_API_SECRET, api_secret)


def get_access_token() -> Optional[str]:
    return get(KEY_ACCESS_TOKEN)


def get_api_key_pair() -> tuple[Optional[str], Optional[str]]:
    return get(KEY_API_KEY), get(KEY_API_SECRET)
