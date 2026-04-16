"""Tests for preprocessing behavior."""

from __future__ import annotations

import pandas as pd

from olist_revenue_intelligence.features.preprocessing import build_preprocessor


def test_preprocessor_handles_numeric_missing_values_and_unknown_categories():
    train = pd.DataFrame(
        {
            "order_revenue": [50.0, None, 100.0],
            "n_items": [1, 2, 1],
            "n_sellers": [1, 1, 1],
            "n_categories": [1, 1, 2],
            "customer_state": ["SP", "RJ", "SP"],
            "estimated_delivery_days": [10.0, 20.0, 12.0],
            "purchase_month": [1, 2, 3],
            "purchase_dayofweek": [0, 5, 2],
            "purchase_hour": [9, 21, 14],
            "is_weekend": [0, 1, 0],
            "order_revenue_per_item": [50.0, 25.0, 100.0],
        }
    )
    test = train.copy()
    test.loc[0, "customer_state"] = "MG"

    preprocessor = build_preprocessor()
    preprocessor.fit(train)
    transformed = preprocessor.transform(test)

    assert transformed.shape[0] == 3
    assert transformed.shape[1] >= 11

