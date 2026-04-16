"""Tests for processed dataset loading."""

from __future__ import annotations

import pandas as pd

from olist_revenue_intelligence.data.load_processed_data import (
    load_late_delivery_dataset,
    split_features_target,
)
from olist_revenue_intelligence.features.feature_engineering import FEATURE_COLUMNS


def _sample_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_id": ["a", "b"],
            "is_late": [0, 1],
            "order_revenue": [50.0, 120.0],
            "n_items": [1, 2],
            "n_sellers": [1, 1],
            "n_categories": [1, 2],
            "customer_state": ["SP", "RJ"],
            "estimated_delivery_days": [10.0, 18.0],
            "purchase_month": [1, 2],
            "purchase_dayofweek": [0, 6],
            "purchase_hour": [10, 21],
            "is_weekend": [0, 1],
            "order_revenue_per_item": [50.0, 60.0],
        }
    )


def test_load_late_delivery_dataset_validates_required_columns(tmp_path):
    path = tmp_path / "late_delivery_modeling_dataset.csv"
    _sample_frame().to_csv(path, index=False)

    loaded = load_late_delivery_dataset(path)

    assert list(loaded.columns) == list(_sample_frame().columns)
    assert len(loaded) == 2


def test_split_features_target_uses_retained_features():
    x, y = split_features_target(_sample_frame())

    assert list(x.columns) == FEATURE_COLUMNS
    assert y.tolist() == [0, 1]

