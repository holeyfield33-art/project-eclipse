from fastapi import APIRouter, Depends

from app.api.v1.endpoints import auth, entities, alerts, cases, reports, health
from app.api.deps import require
from app.core.rbac import Permission

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(entities.router, prefix="/entities", tags=["entities"], dependencies=[Depends(require(Permission.ENTITIES_READ))])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"], dependencies=[Depends(require(Permission.ALERTS_READ))])
api_router.include_router(cases.router, prefix="/cases", tags=["cases"], dependencies=[Depends(require(Permission.CASES_READ))])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"], dependencies=[Depends(require(Permission.REPORTS_READ))])
