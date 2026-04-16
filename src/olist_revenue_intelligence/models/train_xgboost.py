"""Train the retained XGBoost late-delivery risk model."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from olist_revenue_intelligence.config.settings import settings
from olist_revenue_intelligence.data.export_outputs import save_dataframe, save_json
from olist_revenue_intelligence.data.load_processed_data import (
    load_late_delivery_dataset,
    split_features_target,
)
from olist_revenue_intelligence.features.preprocessing import build_model_pipeline
from olist_revenue_intelligence.models.evaluate import evaluate_model
from olist_revenue_intelligence.models.registry import save_model


def build_xgboost_estimator(**overrides) -> XGBClassifier:
    """Create a conservative XGBoost classifier for tabular risk scoring."""

    params = {
        "n_estimators": 250,
        "max_depth": 3,
        "learning_rate": 0.05,
        "subsample": 0.9,
        "colsample_bytree": 0.9,
        "objective": "binary:logistic",
        "eval_metric": "logloss",
        "random_state": 42,
        "n_jobs": -1,
    }
    params.update(overrides)
    return XGBClassifier(**params)


def train_xgboost_model(
    df: pd.DataFrame | None = None,
    output_path: str | Path | None = None,
    metrics_path: str | Path | None = None,
    threshold: float | None = None,
    **estimator_overrides,
) -> tuple[object, dict[str, float | int]]:
    """Train, evaluate, and save the baseline XGBoost pipeline."""

    dataset = df if df is not None else load_late_delivery_dataset()
    x, y = split_features_target(dataset)
    stratify = y if y.nunique() == 2 else None
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=stratify,
    )

    pipeline = build_model_pipeline(build_xgboost_estimator(**estimator_overrides))
    pipeline.fit(x_train, y_train)
    threshold_used = settings.default_threshold if threshold is None else threshold
    metrics = evaluate_model(pipeline, x_test, y_test, threshold=threshold_used)
    metrics["model_name"] = "xgboost"

    save_model(pipeline, output_path or settings.trained_models_dir / "xgboost_pipeline.joblib")
    save_json(metrics, metrics_path or settings.metrics_dir / "xgboost_metrics.json")
    export_xgboost_feature_importance(pipeline)
    return pipeline, metrics


def export_xgboost_feature_importance(pipeline: object) -> Path:
    """Export transformed feature importances from a fitted XGBoost pipeline."""

    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]
    feature_names = preprocessor.get_feature_names_out()
    importance = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)
    return save_dataframe(importance, settings.artifacts_dir / "feature_importance_xgb.csv")
