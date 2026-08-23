"""Alert management – live feed, prioritization, actions."""

from typing import List, Optional
from enum import Enum
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from datetime import datetime

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
    risk_score: float = Field(..., ge=0, le=100)
    severity: AlertSeverity
    status: AlertStatus = AlertStatus.NEW
    title: str
    description: str
    factors: dict = {}  # contributing risk factors + SHAP
    created_at: datetime
    updated_at: Optional[datetime] = None


class AlertAction(BaseModel):
    action: str  # flag | freeze | report | escalate | dismiss
    note: Optional[str] = None


@router.get("/", response_model=List[Alert])
async def list_alerts(
    severity: Optional[AlertSeverity] = None,
    status: Optional[AlertStatus] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = 0,
):
    """Live feed of alerts with optional filters."""
    # TODO: query from Postgres / Elasticsearch ordered by risk + recency
    return []


@router.get("/overview")
async def threat_overview():
    """High/Medium/Low counts, new alerts, geographic summary."""
    return {
        "high": 0,
        "medium": 0,
        "low": 0,
        "new_last_24h": 0,
        "geographic_heatmap": [],
    }


@router.get("/{alert_id}", response_model=Alert)
async def get_alert(alert_id: str):
    # TODO
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Alert not found (scaffold)")


@router.post("/{alert_id}/actions")
async def perform_action(alert_id: str, action: AlertAction):
    """Flag, freeze, report, escalate, or dismiss an alert."""
    # TODO: update status, write immutable audit log, optionally trigger workflows
    return {"status": "accepted", "alert_id": alert_id, "action": action.action}
