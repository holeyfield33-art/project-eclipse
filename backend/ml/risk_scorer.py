"""
Eclipse Risk Scoring Engine

Transparent, explainable 0–100 risk score using weighted logistic regression
+ SHAP values for every decision.

Factors (weights sum to 1.0):
  - Transaction velocity          25%
  - Linkages to high-risk entities 20%
  - Geographic red flags          15%
  - Account age & activity        10%
  - Behavioral anomaly            20%
  - Dark web mentions             10%
"""

from typing import Dict, Any, Optional
import numpy as np
from dataclasses import dataclass


WEIGHTS = {
    "transaction_velocity": 0.25,
    "high_risk_linkages": 0.20,
    "geographic_red_flags": 0.15,
    "account_age_activity": 0.10,
    "behavioral_anomaly": 0.20,
    "dark_web_mentions": 0.10,
}


@dataclass
class RiskResult:
    score: float  # 0–100
    factors: Dict[str, float]  # normalized 0–1 contributions
    shap_values: Optional[Dict[str, float]] = None
    explanation: Optional[str] = None


class RiskScorer:
    """
    MVP scorer. Replace logistic model with trained sklearn/TF model
    and real SHAP explainer in production.
    """

    def __init__(self):
        # Placeholder coefficients – train on historical labels
        self.coefficients = {k: 1.0 for k in WEIGHTS}
        self.intercept = -2.0

    def score(self, features: Dict[str, float]) -> RiskResult:
        """
        features: dict of factor name -> raw value (already 0–1 normalized preferred)
        """
        # Ensure all factors present
        feats = {k: float(features.get(k, 0.0)) for k in WEIGHTS}

        # Weighted linear combination → sigmoid → 0–100
        linear = self.intercept
        for name, weight in WEIGHTS.items():
            linear += weight * self.coefficients[name] * feats[name]

        prob = 1.0 / (1.0 + np.exp(-linear))
        score = float(np.clip(prob * 100.0, 0.0, 100.0))

        # Simple attribution (true SHAP would use TreeExplainer / KernelExplainer)
        shap_approx = {
            name: weight * self.coefficients[name] * feats[name]
            for name, weight in WEIGHTS.items()
        }

        return RiskResult(
            score=round(score, 2),
            factors=feats,
            shap_values=shap_approx,
            explanation=self._explain(score, shap_approx),
        )

    def _explain(self, score: float, shap: Dict[str, float]) -> str:
        top = sorted(shap.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
        parts = [f"{k.replace('_', ' ')} ({v:+.2f})" for k, v in top]
        level = "HIGH" if score >= 75 else "MEDIUM" if score >= 40 else "LOW"
        return f"Risk level {level} ({score:.1f}). Top drivers: {', '.join(parts)}."


# Singleton for serving
scorer = RiskScorer()


if __name__ == "__main__":
    # Quick smoke test
    sample = {
        "transaction_velocity": 0.8,
        "high_risk_linkages": 0.6,
        "geographic_red_flags": 0.3,
        "account_age_activity": 0.9,
        "behavioral_anomaly": 0.7,
        "dark_web_mentions": 0.2,
    }
    result = scorer.score(sample)
    print(result)
