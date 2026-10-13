"""Tenant-scoped, process-local case workflow for development."""

from datetime import datetime, timezone
from enum import Enum

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from app.api.deps import current_user, require, tenant_record
from app.core.rbac import Permission
from app.services import audit, store

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
    status: CaseStatus
    assigned_to: str | None = None
    entity_ids: list[str]
    alert_ids: list[str]
    notes: list[dict]
    created_at: datetime
    updated_at: datetime | None = None


class CaseCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=1, max_length=200)
    priority: CasePriority = CasePriority.MEDIUM
    entity_ids: list[str] = Field(default_factory=list, max_length=100)
    alert_ids: list[str] = Field(default_factory=list, max_length=100)
    initial_note: str | None = Field(default=None, max_length=2000)


class CaseNote(BaseModel):
    model_config = ConfigDict(extra="forbid")
    content: str = Field(min_length=1, max_length=2000)


@router.get("/", response_model=list[Case])
async def list_cases(
    status: CaseStatus | None = None,
    priority: CasePriority | None = None,
    assigned_to: str | None = None,
    limit: int = Query(50, ge=1, le=200),
    user: dict = Depends(current_user),
):
    with store.lock:
        records = [c.copy() for c in store.cases.values() if c["tenant_id"] == user["tenant_id"]]
    return [c for c in records if (status is None or c["status"] == status)
            and (priority is None or c["priority"] == priority)
            and (assigned_to is None or c["assigned_to"] == assigned_to)][:limit]


@router.post("/", response_model=Case, status_code=201)
async def create_case(payload: CaseCreate, user: dict = Depends(require(Permission.CASES_WRITE))):
    with store.lock:
        for entity_id in payload.entity_ids:
            tenant_record(store.entities, entity_id, user)
        for alert_id in payload.alert_ids:
            tenant_record(store.alerts, alert_id, user)
        now = datetime.now(timezone.utc)
        case = {"id": store.new_id(), "tenant_id": user["tenant_id"], "title": payload.title,
                "priority": payload.priority, "status": CaseStatus.OPEN, "assigned_to": None,
                "entity_ids": payload.entity_ids.copy(), "alert_ids": payload.alert_ids.copy(),
                "notes": [], "created_at": now, "updated_at": None}
        if payload.initial_note:
            case["notes"].append({"actor_id": user["id"], "content": payload.initial_note, "timestamp": now.isoformat()})
        store.cases[case["id"]] = case
        audit.record(user["tenant_id"], user["id"], "case.create", case["id"])
        return case


@router.get("/{case_id}", response_model=Case)
async def get_case(case_id: str, user: dict = Depends(current_user)):
    with store.lock:
        return tenant_record(store.cases, case_id, user).copy()


@router.post("/{case_id}/notes", response_model=Case)
async def add_note(case_id: str, note: CaseNote, user: dict = Depends(require(Permission.CASES_WRITE))):
    with store.lock:
        case = tenant_record(store.cases, case_id, user)
        now = datetime.now(timezone.utc)
        case["notes"].append({"actor_id": user["id"], "content": note.content, "timestamp": now.isoformat()})
        case["updated_at"] = now
        audit.record(user["tenant_id"], user["id"], "case.note", case_id)
        return case.copy()


@router.patch("/{case_id}/assign", response_model=Case)
async def assign_case(case_id: str, assignee_id: str, user: dict = Depends(require(Permission.CASES_ASSIGN))):
    with store.lock:
        case = tenant_record(store.cases, case_id, user)
        assignee = tenant_record(store.users, assignee_id, user)
        if not assignee["active"]:
            raise HTTPException(status_code=404, detail="Not found")
        case["assigned_to"] = assignee_id
        case["updated_at"] = datetime.now(timezone.utc)
        audit.record(user["tenant_id"], user["id"], "case.assign", case_id)
        return case.copy()
