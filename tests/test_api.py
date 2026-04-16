"""Tests for FastAPI endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient

from olist_revenue_intelligence.api.main import app
from olist_revenue_intelligence.api.service import get_prediction_service


class FakePredictionService:
    def model_info(self):
        return {
            "model_name": "test_model",
            "threshold": 0.7,
            "feature_count": 11,
            "features": ["order_revenue"],
            "model_artifact_available": True,
            "note": "Risk prioritization model, not a high-precision autonomous classifier.",
        }

    def predict(self, payload):
        return {
            "predicted_probability": 0.81,
            "predicted_class": 1,
            "threshold_used": 0.7,
            "interpretation": "High late-delivery risk: prioritize this order for operational review.",
        }


def test_health_endpoint():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_endpoint_with_dependency_override():
    app.dependency_overrides[get_prediction_service] = lambda: FakePredictionService()
    client = TestClient(app)
    payload = {
        "order_revenue": 141.46,
        "n_items": 1,
        "n_sellers": 1,
        "n_categories": 1,
        "customer_state": "sp",
        "estimated_delivery_days": 19.1,
        "purchase_month": 7,
        "purchase_dayofweek": 1,
        "purchase_hour": 20,
        "is_weekend": 0,
        "order_revenue_per_item": 141.46,
    }

    response = client.post("/predict", json=payload)

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["predicted_class"] == 1
    assert response.json()["threshold_used"] == 0.7

