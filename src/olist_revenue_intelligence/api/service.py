"""Prediction service used by the FastAPI app."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from olist_revenue_intelligence.config.settings import settings
from olist_revenue_intelligence.models.predict import predict_late_delivery_risk
from olist_revenue_intelligence.models.registry import load_model, load_model_metadata


class PredictionService:
    """Small service wrapper that keeps the loaded model in memory."""

    def __init__(self, model_path: str | Path | None = None, threshold: float | None = None) -> None:
        self.model_path = Path(model_path) if model_path else settings.best_model_path
        self.threshold = settings.default_threshold if threshold is None else threshold
        self._model: Any | None = None

    @property
    def model_available(self) -> bool:
        """Return whether the configured artifact exists."""

        return self.model_path.exists()

    @property
    def model(self) -> Any:
        """Lazy-load the model artifact."""

        if self._model is None:
            self._model = load_model(self.model_path)
        return self._model

    def predict(self, payload: dict[str, Any]) -> dict[str, float | int | str]:
        """Run a single-order prediction."""

        return predict_late_delivery_risk(payload, model=self.model, threshold=self.threshold)

    def model_info(self) -> dict[str, Any]:
        """Return API-facing model metadata."""

        metadata = load_model_metadata()
        return {
            "model_name": str(metadata.get("model_name", settings.final_model_name)),
            "threshold": float(metadata.get("threshold", self.threshold)),
            "feature_count": len(settings.model_features),
            "features": settings.model_features,
            "model_artifact_available": self.model_available,
            "note": "Risk prioritization model, not a high-precision autonomous classifier.",
        }


@lru_cache(maxsize=1)
def get_prediction_service() -> PredictionService:
    """Cached service dependency for FastAPI."""

    return PredictionService()

