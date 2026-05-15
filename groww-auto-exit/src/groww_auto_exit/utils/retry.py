"""Tiny retry helpers tuned for trading APIs.

We deliberately wrap `tenacity` rather than expose it directly so the rest of
the codebase has a small, stable surface and we can swap engines later.
"""
from __future__ import annotations

import logging
from typing import Callable, Iterable, Type, TypeVar

from tenacity import (
    RetryError,
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

T = TypeVar("T")
log = logging.getLogger(__name__)


def with_retry(
    fn: Callable[[], T],
    *,
    attempts: int = 4,
    base_delay: float = 0.4,
    max_delay: float = 5.0,
    retry_on: Iterable[Type[BaseException]] = (Exception,),
    label: str = "op",
) -> T:
    """Run `fn` with exponential backoff on the listed exception types."""
    retry_types = tuple(retry_on)
    try:
        for attempt in Retrying(
            stop=stop_after_attempt(attempts),
            wait=wait_exponential(multiplier=base_delay, min=base_delay, max=max_delay),
            retry=retry_if_exception_type(retry_types),
            reraise=True,
        ):
            with attempt:
                return fn()
    except RetryError as e:  # pragma: no cover - tenacity bridging
        log.error("retry exhausted for %s: %s", label, e)
        raise
    raise RuntimeError("unreachable")  # pragma: no cover
