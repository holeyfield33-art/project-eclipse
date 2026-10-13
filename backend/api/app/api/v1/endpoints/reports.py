"""Pre-built and custom compliance reports (SAR, executive, etc.)."""

from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from datetime import date
from app.api.deps import require
from app.core.rbac import Permission

router = APIRouter()


class ReportTemplate(BaseModel):
    id: str
    name: str
    description: str
    formats: List[str]  # pdf | csv


@router.get("/templates", response_model=List[ReportTemplate])
async def list_templates():
    return [
        ReportTemplate(
            id="sar",
            name="Suspicious Activity Report (SAR)",
            description="Standard SAR template for regulatory filing",
            formats=["pdf", "csv"],
        ),
        ReportTemplate(
            id="compliance_summary",
            name="Compliance Summary",
            description="Period summary of alerts, cases, and dispositions",
            formats=["pdf", "csv"],
        ),
        ReportTemplate(
            id="executive",
            name="Executive Dashboard",
            description="High-level risk posture and trends",
            formats=["pdf"],
        ),
    ]


@router.get("/generate/{template_id}", dependencies=[Depends(require(Permission.REPORTS_GENERATE))])
async def generate_report(
    template_id: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    format: str = Query("pdf", pattern="^(pdf|csv)$"),
):
    """Generate a report. Returns downloadable file (scaffold returns stub)."""
    # TODO: query data, render PDF/CSV, stream response
    raise HTTPException(status_code=501, detail="Report generation is not implemented")
