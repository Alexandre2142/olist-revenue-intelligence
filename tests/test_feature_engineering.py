"""Tests for feature definitions."""

from __future__ import annotations

import pandas as pd

from olist_revenue_intelligence.features.feature_engineering import (
    add_basic_order_features,
    get_feature_columns,
)


def test_feature_list_contains_only_expected_initial_features():
    features = get_feature_columns()

    assert "customer_state" in features
    assert "estimated_delivery_days" in features
    assert "review_score" not in features
    assert len(features) == 11


def test_add_basic_order_features_derives_safe_features():
    df = pd.DataFrame(
        {
            "order_revenue": [100.0],
            "n_items": [2],
            "purchase_dayofweek": [6],
        }
    )

    output = add_basic_order_features(df)

    assert output.loc[0, "order_revenue_per_item"] == 50.0
    assert output.loc[0, "is_weekend"] == 1

