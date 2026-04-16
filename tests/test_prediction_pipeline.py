"""Tests for local model persistence and inference."""

from __future__ import annotations

import pandas as pd
from sklearn.linear_model import LogisticRegression

from olist_revenue_intelligence.features.preprocessing import build_model_pipeline
from olist_revenue_intelligence.models.predict import predict_late_delivery_risk
from olist_revenue_intelligence.models.registry import load_model, save_model


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


def test_saved_pipeline_loads_and_predicts(tmp_path):
    x, y = _training_frame()
    model = build_model_pipeline(LogisticRegression(max_iter=1000))
    model.fit(x, y)
    model_path = tmp_path / "model.joblib"
    save_model(model, model_path)

    loaded = load_model(model_path)
    result = predict_late_delivery_risk(x.iloc[0].to_dict(), model=loaded, threshold=0.7)

    assert 0 <= result["predicted_probability"] <= 1
    assert result["predicted_class"] in {0, 1}
    assert result["threshold_used"] == 0.7

