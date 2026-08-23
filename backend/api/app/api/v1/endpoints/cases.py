"""Case management workflow for analysts."""

from typing import List, Optional
from enum import Enum
from fastapi import APIRouter, Query
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class CasePriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CaseStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PENDING_REVIEW = "pending_review"
    CLOSED = "closed"


class Case(BaseModel):
    id: str
    title: str
    priority: CasePriority
    status: CaseStatus = CaseStatus.OPEN
    assigned_to: Optional[str] = None
    entity_ids: List[str] = []
    alert_ids: List[str] = []
    notes: List[dict] = []
    created_at: datetime
    updated_at: Optional[datetime] = None


class CaseCreate(BaseModel):
    title: str
    priority: CasePriority = CasePriority.MEDIUM
    entity_ids: List[str] = []
    alert_ids: List[str] = []
    initial_note: Optional[str] = None


class CaseNote(BaseModel):
    content: str


@router.get("/", response_model=List[Case])
async def list_cases(
    status: Optional[CaseStatus] = None,
    priority: Optional[CasePriority] = None,
    assigned_to: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
):
    """Case queue with priority flags."""
    return []


@router.post("/", response_model=Case)
async def create_case(payload: CaseCreate):
    # TODO: create case, link entities/alerts, audit log
    from fastapi import HTTPException
    raise HTTPException(status_code=501, detail="Not implemented (scaffold)")


@router.get("/{case_id}", response_model=Case)
async def get_case(case_id: str):
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Case not found (scaffold)")


@router.post("/{case_id}/notes")
async def add_note(case_id: str, note: CaseNote):
    # TODO: append immutable note + audit
    return {"status": "ok", "case_id": case_id}


@router.patch("/{case_id}/assign")
async def assign_case(case_id: str, assignee_id: str):
    # TODO: manager/admin only
    return {"status": "ok", "case_id": case_id, "assigned_to": assignee_id}
