"""Tenant-scoped alert reads; alert actions await a durable workflow."""

from datetime import datetime, timedelta, timezone
from enum import Enum

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from app.api.deps import current_user, tenant_record
from app.core.rbac import can_perform_alert_action
from app.services import store

router = APIRouter()


class AlertSeverity(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AlertStatus(str, Enum):
    NEW = "new"
    INVESTIGATING = "investigating"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"


class Alert(BaseModel):
    id: str
    entity_id: str
    entity_name: str
    risk_score: float = Field(ge=0, le=100)
    severity: AlertSeverity
    status: AlertStatus = AlertStatus.NEW
    title: str
    description: str
    factors: dict = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime | None = None


class AlertAction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: str
    note: str | None = Field(default=None, max_length=2000)


@router.get("/", response_model=list[Alert])
async def list_alerts(
    severity: AlertSeverity | None = None,
    status: AlertStatus | None = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    user: dict = Depends(current_user),
):
    with store.lock:
        records = [a.copy() for a in store.alerts.values() if a["tenant_id"] == user["tenant_id"]]
    records = [a for a in records if (severity is None or a["severity"] == severity)
               and (status is None or a["status"] == status)]
    records.sort(key=lambda a: a["created_at"], reverse=True)
    return records[offset:offset + limit]


@router.get("/overview")
async def threat_overview(user: dict = Depends(current_user)):
    with store.lock:
        records = [a.copy() for a in store.alerts.values() if a["tenant_id"] == user["tenant_id"]]
    recent = datetime.now(timezone.utc) - timedelta(hours=24)
    return {
        "high": sum(a["severity"] == AlertSeverity.HIGH for a in records),
        "medium": sum(a["severity"] == AlertSeverity.MEDIUM for a in records),
        "low": sum(a["severity"] == AlertSeverity.LOW for a in records),
        "new_last_24h": sum(a["status"] == AlertStatus.NEW and a["created_at"] >= recent for a in records),
        "geographic_heatmap": [],
    }


@router.get("/{alert_id}", response_model=Alert)
async def get_alert(alert_id: str, user: dict = Depends(current_user)):
    with store.lock:
        return tenant_record(store.alerts, alert_id, user).copy()


@router.post("/{alert_id}/actions")
async def perform_action(alert_id: str, action: AlertAction, user: dict = Depends(current_user)):
    if not can_perform_alert_action(user["role"], action.action):
        raise HTTPException(status_code=403, detail="Forbidden")
    with store.lock:
        tenant_record(store.alerts, alert_id, user)
    raise HTTPException(status_code=501, detail="Alert actions require a persistent audited workflow")
