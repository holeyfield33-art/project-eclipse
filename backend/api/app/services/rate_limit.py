"""Process-local request limits for development; use shared storage in production."""

from collections import defaultdict, deque
from threading import RLock
from time import monotonic

from fastapi import HTTPException, Request

_lock = RLock()
_hits: dict[tuple[str, str], deque[float]] = defaultdict(deque)


def check(request: Request, endpoint: str, limit: int) -> None:
    key = (endpoint, request.client.host if request.client else "unknown")
    now = monotonic()
    with _lock:
        hits = _hits[key]
        while hits and hits[0] <= now - 60:
            hits.popleft()
        if len(hits) >= limit:
            raise HTTPException(status_code=429, detail="Too many requests")
        hits.append(now)


def reset_for_tests() -> None:
    with _lock:
        _hits.clear()
