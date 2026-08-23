"""Lightweight FastAPI service for risk scoring + SHAP explanations."""

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Dict

from risk_scorer import scorer, RiskResult

app = FastAPI(title="Eclipse ML Service", version="2.0.0")


class ScoreRequest(BaseModel):
    features: Dict[str, float] = Field(
        ...,
        description="Normalized 0–1 feature values for the six risk factors",
    )


class ScoreResponse(BaseModel):
    score: float
    factors: Dict[str, float]
    shap_values: Dict[str, float]
    explanation: str


@app.get("/health")
async def health():
    return {"status": "ok", "service": "eclipse-ml"}


@app.post("/score", response_model=ScoreResponse)
async def score_entity(req: ScoreRequest):
    result: RiskResult = scorer.score(req.features)
    return ScoreResponse(
        score=result.score,
        factors=result.factors,
        shap_values=result.shap_values or {},
        explanation=result.explanation or "",
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
