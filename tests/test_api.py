"""Tests for FastAPI endpoints."""

from __future__ import annotations

import pandas as pd
from fastapi.testclient import TestClient
from sklearn.linear_model import LogisticRegression

from olist_revenue_intelligence.api.main import app
from olist_revenue_intelligence.api.service import PredictionService, get_prediction_service
from olist_revenue_intelligence.features.preprocessing import build_model_pipeline
from olist_revenue_intelligence.models.registry import save_model


def _training_frame() -> tuple[pd.DataFrame, pd.Series]:
    x = pd.DataFrame(
        {
            "order_revenue": [20, 30, 80, 100, 150, 200],
            "n_items": [1, 1, 2, 2, 3, 3],
            "n_sellers": [1, 1, 1, 1, 2, 2],
            "n_categories": [1, 1, 1, 2, 2, 3],
            "customer_state": ["SP", "RJ", "SP", "MG", "BA", "SP"],
            "estimated_delivery_days": [7, 9, 12, 20, 25, 30],
            "purchase_month": [1, 2, 3, 4, 5, 6],
            "purchase_dayofweek": [0, 1, 2, 3, 5, 6],
            "purchase_hour": [9, 10, 11, 12, 20, 21],
            "is_weekend": [0, 0, 0, 0, 1, 1],
            "order_revenue_per_item": [20, 30, 40, 50, 50, 66.7],
        }
    )
    y = pd.Series([0, 0, 0, 1, 1, 1])
    return x, y


def _sample_payload() -> dict[str, float | int | str]:
    return {
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


def test_health_endpoint():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_endpoint_with_real_temporary_pipeline(tmp_path):
    x, y = _training_frame()
    model = build_model_pipeline(LogisticRegression(max_iter=1000))
    model.fit(x, y)
    model_path = tmp_path / "model.joblib"
    save_model(model, model_path)

    service = PredictionService(model_path=model_path, threshold=0.7)
    app.dependency_overrides[get_prediction_service] = lambda: service
    client = TestClient(app)

    response = client.post("/predict", json=_sample_payload())

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert 0 <= response.json()["predicted_probability"] <= 1
    assert response.json()["predicted_class"] in {0, 1}
    assert response.json()["threshold_used"] == 0.7


def test_model_info_reports_service_threshold(tmp_path):
    model_path = tmp_path / "model.joblib"
    model_path.write_bytes(b"placeholder")
    service = PredictionService(model_path=model_path, threshold=0.42)
    app.dependency_overrides[get_prediction_service] = lambda: service
    client = TestClient(app)

    response = client.get("/model-info")

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["threshold"] == 0.42
    assert response.json()["model_artifact_available"] is True
