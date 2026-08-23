"""Entity resolution, profiles, network graph, risk scores."""

from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


class EntitySummary(BaseModel):
    id: str
    name: str
    entity_type: str  # person | company | wallet | account
    risk_score: float = Field(..., ge=0, le=100)
    linked_count: int = 0
    last_activity: Optional[str] = None


class EntityProfile(EntitySummary):
    hashed_identifiers: List[str] = []
    transaction_count: int = 0
    geographic_flags: List[str] = []
    dark_web_mentions: int = 0
    shap_explanation: Optional[dict] = None


class NetworkNode(BaseModel):
    id: str
    label: str
    risk_score: float
    entity_type: str


class NetworkEdge(BaseModel):
    source: str
    target: str
    relationship: str
    weight: float = 1.0


class NetworkGraph(BaseModel):
    nodes: List[NetworkNode]
    edges: List[NetworkEdge]


@router.get("/", response_model=List[EntitySummary])
async def search_entities(
    q: str = Query(..., min_length=2, description="Name, account, wallet, or company"),
    limit: int = Query(20, ge=1, le=100),
):
    """Search entities by name, account number, wallet address, or company."""
    # TODO: query Elasticsearch + Neo4j
    return []


@router.get("/{entity_id}", response_model=EntityProfile)
async def get_entity(entity_id: str):
    """Full entity profile with risk score and SHAP explanation."""
    # TODO: fetch from Postgres + Neo4j + ML explainability service
    raise HTTPException(status_code=404, detail="Entity not found (scaffold)")


@router.get("/{entity_id}/network", response_model=NetworkGraph)
async def get_entity_network(entity_id: str, depth: int = Query(2, ge=1, le=4)):
    """Interactive network graph of connected entities."""
    # TODO: Neo4j Cypher query for neighborhood
    return NetworkGraph(nodes=[], edges=[])


@router.get("/{entity_id}/transactions")
async def get_entity_transactions(
    entity_id: str,
    limit: int = Query(50, ge=1, le=500),
    offset: int = 0,
):
    """Timeline of transactions for an entity."""
    # TODO: Postgres + Elasticsearch
    return {"items": [], "total": 0}
