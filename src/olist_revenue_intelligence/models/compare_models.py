"""Utilities for comparing saved model metrics."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from olist_revenue_intelligence.config.settings import settings
from olist_revenue_intelligence.data.export_outputs import load_json, save_dataframe


def compare_metric_files(
    metric_paths: list[str | Path] | None = None,
    output_path: str | Path | None = None,
) -> pd.DataFrame:
    """Load JSON metric files and export a compact comparison table."""

    paths = (
        [Path(path) for path in metric_paths]
        if metric_paths
        else sorted(settings.metrics_dir.glob("*metrics.json"))
    )
    records = []
    for path in paths:
        if path.exists():
            metrics = load_json(path)
            metrics["source_file"] = path.name
            records.append(metrics)
    comparison = pd.DataFrame(records)
    if not comparison.empty:
        preferred = [
            "model_name",
            "threshold",
            "precision",
            "recall",
            "f1",
            "roc_auc",
            "average_precision",
            "source_file",
        ]
        ordered = [column for column in preferred if column in comparison.columns]
        comparison = comparison[ordered + [c for c in comparison.columns if c not in ordered]]
    save_dataframe(comparison, output_path or settings.artifacts_dir / "model_comparison.csv")
    return comparison

