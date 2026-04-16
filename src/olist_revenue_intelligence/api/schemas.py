"""Pydantic schemas for the late-delivery prediction API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class OrderPredictionRequest(BaseModel):
    """Single-order payload using only pre-delivery features."""

    order_revenue: float = Field(..., ge=0, examples=[141.46])
    n_items: int = Field(..., ge=1, examples=[1])
    n_sellers: int = Field(..., ge=1, examples=[1])
    n_categories: int = Field(..., ge=1, examples=[1])
    customer_state: str = Field(..., min_length=2, max_length=2, examples=["SP"])
    estimated_delivery_days: float = Field(..., ge=0, examples=[19.1])
    purchase_month: int = Field(..., ge=1, le=12, examples=[7])
    purchase_dayofweek: int = Field(..., ge=0, le=6, examples=[1])
    purchase_hour: int = Field(..., ge=0, le=23, examples=[20])
    is_weekend: int = Field(..., ge=0, le=1, examples=[0])
    order_revenue_per_item: float = Field(..., ge=0, examples=[141.46])


class PredictionResponse(BaseModel):
    """Response returned by the prediction endpoint."""

    predicted_probability: float
    predicted_class: int
    threshold_used: float
    interpretation: str


class HealthResponse(BaseModel):
    """Basic service health response."""

    status: str
    service: str


class ModelInfoResponse(BaseModel):
    """Metadata describing the retained model configuration."""

    model_name: str
    threshold: float
    artifact_threshold: float | None = None
    feature_count: int
    features: list[str]
    model_artifact_available: bool
    note: str
