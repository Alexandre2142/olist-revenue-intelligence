"""Load processed datasets produced by the analytics and DS notebooks."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from olist_revenue_intelligence.config.settings import settings
from olist_revenue_intelligence.data.validate_inputs import (
    validate_binary_target,
    validate_no_leakage_columns,
    validate_required_columns,
)


def load_late_delivery_dataset(
    path: str | Path | None = None,
    nrows: int | None = None,
) -> pd.DataFrame:
    """Load the processed late-delivery modeling dataset."""

    dataset_path = Path(path) if path is not None else settings.processed_dataset_path
    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Processed modeling dataset not found at {dataset_path}. "
            "Run the notebook or scripts that export late_delivery_modeling_dataset.csv first."
        )

    df = pd.read_csv(dataset_path, nrows=nrows)
    required = [settings.id_column, settings.target_column, *settings.model_features]
    validate_required_columns(df, required, dataset_name=str(dataset_path))
    validate_no_leakage_columns(settings.model_features)
    validate_binary_target(df, settings.target_column)
    return df


def split_features_target(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    """Return leakage-aware model features and target."""

    validate_required_columns(
        df,
        [settings.target_column, *settings.model_features],
        dataset_name="late-delivery dataset",
    )
    x = df[settings.model_features].copy()
    y = df[settings.target_column].astype(int).copy()
    return x, y

