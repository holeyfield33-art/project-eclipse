"""Append-only application audit chain with server-derived actor and metadata."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

from app.services import store


def _digest(event: dict) -> str:
    return hashlib.sha256(json.dumps(event, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def record(tenant_id: str, actor_id: str, action: str, resource_id: str) -> dict:
    # Only opaque IDs and fixed action names enter the audit trail.
    with store.lock:
        chain = store.audit_events.setdefault(tenant_id, [])
        event = {
            "tenant_id": tenant_id,
            "actor_id": actor_id,
            "action": action,
            "resource_id": resource_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "previous_hash": chain[-1]["hash"] if chain else "0" * 64,
        }
        event["hash"] = _digest(event)
        chain.append(event)
        return event.copy()


def verify(tenant_id: str) -> bool:
    with store.lock:
        previous = "0" * 64
        for item in store.audit_events.get(tenant_id, []):
            event = item.copy()
            actual = event.pop("hash", None)
            if event.get("previous_hash") != previous or actual != _digest(event):
                return False
            previous = actual
        return True
