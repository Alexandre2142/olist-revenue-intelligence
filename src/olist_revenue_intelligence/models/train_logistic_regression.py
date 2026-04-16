"""Train a simple logistic-regression benchmark model."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from olist_revenue_intelligence.config.settings import settings
from olist_revenue_intelligence.data.export_outputs import save_json
from olist_revenue_intelligence.data.load_processed_data import load_late_delivery_dataset, split_features_target
from olist_revenue_intelligence.features.preprocessing import build_model_pipeline
from olist_revenue_intelligence.models.evaluate import evaluate_model
from olist_revenue_intelligence.models.registry import save_model


def train_logistic_regression_model(
    df: pd.DataFrame | None = None,
    output_path: str | Path | None = None,
    metrics_path: str | Path | None = None,
) -> tuple[object, dict[str, float | int]]:
    """Train and save the logistic regression benchmark."""

    dataset = df if df is not None else load_late_delivery_dataset()
    x, y = split_features_target(dataset)
    stratify = y if y.nunique() == 2 else None
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=stratify
    )
    model = build_model_pipeline(LogisticRegression(max_iter=1000, class_weight="balanced"))
    model.fit(x_train, y_train)
    metrics = evaluate_model(model, x_test, y_test, threshold=settings.default_threshold)
    metrics["model_name"] = "logistic_regression"
    save_model(model, output_path or settings.trained_models_dir / "logistic_regression_pipeline.joblib")
    save_json(metrics, metrics_path or settings.metrics_dir / "logistic_regression_metrics.json")
    return model, metrics

