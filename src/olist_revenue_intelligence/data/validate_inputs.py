"""Input validation for processed analytical datasets."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


LEAKAGE_KEYWORDS: tuple[str, ...] = (
    "review",
    "score",
    "delivered",
    "delivery_delay",
    "actual_delivery",
    "approved_at",
    "carrier",
)


def validate_required_columns(
    df: pd.DataFrame,
    required_columns: Iterable[str],
    dataset_name: str = "dataset",
) -> None:
    """Raise a clear error if required columns are missing."""

    missing = [column for column in required_columns if column not in df.columns]
    if missing:
        raise ValueError(f"{dataset_name} is missing required columns: {missing}")


def validate_no_leakage_columns(columns: Iterable[str]) -> None:
    """Reject obvious post-outcome or review-derived features."""

    blocked = [
        column
        for column in columns
        if any(keyword in column.lower() for keyword in LEAKAGE_KEYWORDS)
        and column != "estimated_delivery_days"
    ]
    if blocked:
        raise ValueError(
            "Potential leakage columns detected. Remove post-delivery or review-based "
            f"variables before training: {blocked}"
        )


def validate_binary_target(df: pd.DataFrame, target_column: str) -> None:
    """Validate that the target column contains only 0/1 values."""

    values = set(df[target_column].dropna().unique().tolist())
    if not values.issubset({0, 1, False, True}):
        raise ValueError(
            f"Target column '{target_column}' must be binary 0/1. Found values: {sorted(values)}"
        )


def validate_prediction_frame(df: pd.DataFrame, feature_columns: Iterable[str]) -> None:
    """Validate a frame intended for model inference."""

    validate_required_columns(df, feature_columns, dataset_name="prediction payload")
    validate_no_leakage_columns(df.columns)

