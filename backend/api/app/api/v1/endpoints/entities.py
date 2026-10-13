"""Tenant-scoped entity reads over the process-local development store."""

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from app.api.deps import current_user, tenant_record
from app.services import store

router = APIRouter()


class EntitySummary(BaseModel):
    id: str
    name: str
    entity_type: str
    risk_score: float = Field(ge=0, le=100)
    linked_count: int = 0
    last_activity: str | None = None


class EntityProfile(EntitySummary):
    hashed_identifiers: list[str] = Field(default_factory=list)
    transaction_count: int = 0
    geographic_flags: list[str] = Field(default_factory=list)
    dark_web_mentions: int = 0
    feature_contributions: dict | None = None


class NetworkGraph(BaseModel):
    nodes: list[dict]
    edges: list[dict]


@router.get("/", response_model=list[EntitySummary])
async def search_entities(
    q: str = Query(min_length=2, max_length=120),
    limit: int = Query(20, ge=1, le=100),
    user: dict = Depends(current_user),
):
    with store.lock:
        return [e.copy() for e in store.entities.values()
                if e["tenant_id"] == user["tenant_id"] and q.casefold() in e["name"].casefold()][:limit]


@router.get("/{entity_id}", response_model=EntityProfile)
async def get_entity(entity_id: str, user: dict = Depends(current_user)):
    with store.lock:
        return tenant_record(store.entities, entity_id, user).copy()


@router.get("/{entity_id}/network", response_model=NetworkGraph)
async def get_entity_network(entity_id: str, depth: int = Query(2, ge=1, le=4), user: dict = Depends(current_user)):
    with store.lock:
        tenant_record(store.entities, entity_id, user)
    return NetworkGraph(nodes=[], edges=[])


@router.get("/{entity_id}/transactions")
async def get_entity_transactions(
    entity_id: str,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    user: dict = Depends(current_user),
):
    with store.lock:
        tenant_record(store.entities, entity_id, user)
    return {"items": [], "total": 0}
