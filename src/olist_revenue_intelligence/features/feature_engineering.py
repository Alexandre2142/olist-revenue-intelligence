"""Feature definitions for the late-delivery risk model."""

from __future__ import annotations

import numpy as np
import pandas as pd

from olist_revenue_intelligence.config.settings import (
    CATEGORICAL_FEATURES,
    DEFAULT_MODEL_FEATURES,
    NUMERIC_FEATURES,
    settings,
)
from olist_revenue_intelligence.data.validate_inputs import validate_required_columns

ID_COLUMN = settings.id_column
TARGET_COLUMN = settings.target_column
FEATURE_COLUMNS = DEFAULT_MODEL_FEATURES.copy()


def add_basic_order_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create basic order-level features when source columns are present."""

    output = df.copy()
    if "order_revenue_per_item" not in output.columns and {"order_revenue", "n_items"}.issubset(
        output.columns
    ):
        n_items = output["n_items"].replace(0, np.nan)
        output["order_revenue_per_item"] = (output["order_revenue"] / n_items).fillna(0)

    if "is_weekend" not in output.columns and "purchase_dayofweek" in output.columns:
        output["is_weekend"] = output["purchase_dayofweek"].isin([5, 6]).astype(int)

    return output


def select_model_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return the retained leakage-aware model feature set."""

    validate_required_columns(df, FEATURE_COLUMNS, dataset_name="feature frame")
    return df[FEATURE_COLUMNS].copy()


def get_feature_columns() -> list[str]:
    """Return the ordered feature list used by training and serving."""

    return FEATURE_COLUMNS.copy()


def get_numeric_features() -> list[str]:
    """Return numeric feature names."""

    return NUMERIC_FEATURES.copy()


def get_categorical_features() -> list[str]:
    """Return categorical feature names."""

    return CATEGORICAL_FEATURES.copy()

