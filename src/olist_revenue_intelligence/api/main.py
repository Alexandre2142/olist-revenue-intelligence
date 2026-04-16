"""FastAPI app for serving late-delivery risk predictions."""

from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException

from olist_revenue_intelligence.api.schemas import (
    HealthResponse,
    ModelInfoResponse,
    OrderPredictionRequest,
    PredictionResponse,
)
from olist_revenue_intelligence.api.service import PredictionService, get_prediction_service
from olist_revenue_intelligence.api.utils import normalize_state_code

app = FastAPI(
    title="Olist Revenue Intelligence API",
    version="0.1.0",
    description="Late-delivery risk scoring for the Olist Revenue Intelligence Command Center.",
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Return a simple health check."""

    return HealthResponse(status="ok", service="olist-revenue-intelligence")


@app.get("/model-info", response_model=ModelInfoResponse)
def model_info(
    service: PredictionService = Depends(get_prediction_service),
) -> ModelInfoResponse:
    """Return retained model metadata and feature expectations."""

    return ModelInfoResponse(**service.model_info())


@app.post("/predict", response_model=PredictionResponse)
def predict(
    request: OrderPredictionRequest,
    service: PredictionService = Depends(get_prediction_service),
) -> PredictionResponse:
    """Score one order for late-delivery risk."""

    payload = request.model_dump()
    payload["customer_state"] = normalize_state_code(payload["customer_state"])
    try:
        result = service.predict(payload)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return PredictionResponse(**result)

