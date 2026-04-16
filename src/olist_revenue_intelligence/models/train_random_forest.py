"""Train a random-forest benchmark model."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from olist_revenue_intelligence.config.settings import settings
from olist_revenue_intelligence.data.export_outputs import save_dataframe, save_json
from olist_revenue_intelligence.data.load_processed_data import load_late_delivery_dataset, split_features_target
from olist_revenue_intelligence.features.preprocessing import build_model_pipeline
from olist_revenue_intelligence.models.evaluate import evaluate_model
from olist_revenue_intelligence.models.registry import save_model


def train_random_forest_model(
    df: pd.DataFrame | None = None,
    output_path: str | Path | None = None,
    metrics_path: str | Path | None = None,
) -> tuple[object, dict[str, float | int]]:
    """Train and save the random forest benchmark."""

    dataset = df if df is not None else load_late_delivery_dataset()
    x, y = split_features_target(dataset)
    stratify = y if y.nunique() == 2 else None
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=stratify
    )
    estimator = RandomForestClassifier(
        n_estimators=250,
        max_depth=10,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    model = build_model_pipeline(estimator)
    model.fit(x_train, y_train)
    metrics = evaluate_model(model, x_test, y_test, threshold=settings.default_threshold)
    metrics["model_name"] = "random_forest"
    save_model(model, output_path or settings.trained_models_dir / "random_forest_pipeline.joblib")
    save_json(metrics, metrics_path or settings.metrics_dir / "random_forest_metrics.json")
    export_random_forest_feature_importance(model)
    return model, metrics


def export_random_forest_feature_importance(pipeline: object) -> Path:
    """Export transformed feature importances from a fitted RF pipeline."""

    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]
    feature_names = preprocessor.get_feature_names_out()
    importance = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)
    return save_dataframe(importance, settings.artifacts_dir / "feature_importance_rf.csv")
