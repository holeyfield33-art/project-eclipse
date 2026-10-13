"""Process-local development store; never a production persistence boundary."""

from __future__ import annotations

from threading import RLock
from uuid import uuid4

lock = RLock()
users: dict[str, dict] = {}
entities: dict[str, dict] = {}
alerts: dict[str, dict] = {}
cases: dict[str, dict] = {}
audit_events: dict[str, list[dict]] = {}


def new_id() -> str:
    return uuid4().hex


def reset_for_tests() -> None:
    with lock:
        for collection in (users, entities, alerts, cases, audit_events):
            collection.clear()
