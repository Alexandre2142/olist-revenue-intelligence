"""Compact tuning routine for the random-forest benchmark."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split

from olist_revenue_intelligence.config.settings import settings
from olist_revenue_intelligence.data.export_outputs import save_json
from olist_revenue_intelligence.data.load_processed_data import load_late_delivery_dataset, split_features_target
from olist_revenue_intelligence.features.preprocessing import build_model_pipeline
from olist_revenue_intelligence.models.evaluate import evaluate_model
from olist_revenue_intelligence.models.registry import save_model
from olist_revenue_intelligence.models.train_random_forest import export_random_forest_feature_importance


def tune_random_forest_model(
    df: pd.DataFrame | None = None,
    output_path: str | Path | None = None,
    metrics_path: str | Path | None = None,
    n_iter: int = 8,
    cv: int = 3,
) -> tuple[object, dict[str, object]]:
    """Tune a random forest as a transparent benchmark against XGBoost."""

    dataset = df if df is not None else load_late_delivery_dataset()
    x, y = split_features_target(dataset)
    stratify = y if y.nunique() == 2 else None
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=stratify
    )
    pipeline = build_model_pipeline(
        RandomForestClassifier(class_weight="balanced", random_state=42, n_jobs=-1)
    )
    search = RandomizedSearchCV(
        pipeline,
        {
            "model__n_estimators": [150, 250, 350],
            "model__max_depth": [6, 10, 14, None],
            "model__min_samples_leaf": [2, 5, 10],
            "model__max_features": ["sqrt", "log2", None],
        },
        n_iter=n_iter,
        cv=cv,
        scoring="average_precision",
        random_state=42,
        n_jobs=-1,
    )
    search.fit(x_train, y_train)
    best_model = search.best_estimator_
    metrics = evaluate_model(best_model, x_test, y_test, threshold=settings.default_threshold)
    metrics.update(
        {
            "model_name": "tuned_random_forest",
            "best_params": search.best_params_,
            "best_cv_score": float(search.best_score_),
        }
    )
    save_model(best_model, output_path or settings.trained_models_dir / "random_forest_pipeline.joblib")
    save_json(metrics, metrics_path or settings.metrics_dir / "tuned_random_forest_metrics.json")
    export_random_forest_feature_importance(best_model)
    return best_model, metrics
