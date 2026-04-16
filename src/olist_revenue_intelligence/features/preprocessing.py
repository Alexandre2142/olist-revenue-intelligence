"""Preprocessing pipeline for late-delivery modeling."""

from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from olist_revenue_intelligence.features.feature_engineering import (
    get_categorical_features,
    get_numeric_features,
)


def _one_hot_encoder() -> OneHotEncoder:
    """Create a OneHotEncoder compatible with recent and older sklearn versions."""

    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def build_preprocessor() -> ColumnTransformer:
    """Build preprocessing for numeric and categorical model features."""

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", _one_hot_encoder()),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, get_numeric_features()),
            ("categorical", categorical_pipeline, get_categorical_features()),
        ],
        remainder="drop",
    )


def build_model_pipeline(estimator) -> Pipeline:
    """Attach the standard preprocessor to an estimator."""

    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("model", estimator),
        ]
    )

