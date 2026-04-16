"""Scriptable validation step for the processed late-delivery dataset."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from olist_revenue_intelligence.config.settings import settings
from olist_revenue_intelligence.data.export_outputs import save_dataframe
from olist_revenue_intelligence.data.load_processed_data import load_late_delivery_dataset
from olist_revenue_intelligence.features.feature_engineering import get_feature_columns
from olist_revenue_intelligence.features.leakage_audit import audit_feature_columns


def build_modeling_dataset(
    input_path: str | Path | None = None,
    output_path: str | Path | None = None,
) -> pd.DataFrame:
    """Load, validate, and optionally re-export the retained modeling dataset."""

    df = load_late_delivery_dataset(input_path)
    leakage_audit = audit_feature_columns(get_feature_columns())
    save_dataframe(leakage_audit, settings.artifacts_dir / "leakage_audit.csv")
    if output_path is not None:
        save_dataframe(df, output_path)
    return df

