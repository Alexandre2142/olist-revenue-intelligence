"""Small, realistic hyperparameter tuning routine for XGBoost."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from xgboost import XGBClassifier

from olist_revenue_intelligence.config.settings import settings
from olist_revenue_intelligence.data.export_outputs import save_json
from olist_revenue_intelligence.data.load_processed_data import (
    load_late_delivery_dataset,
    split_features_target,
)
from olist_revenue_intelligence.features.preprocessing import build_model_pipeline
from olist_revenue_intelligence.models.evaluate import evaluate_model
from olist_revenue_intelligence.models.registry import promote_to_best_model, save_model
from olist_revenue_intelligence.models.train_xgboost import export_xgboost_feature_importance


def tune_xgboost_model(
    df: pd.DataFrame | None = None,
    output_path: str | Path | None = None,
    metrics_path: str | Path | None = None,
    n_iter: int = 8,
    cv: int = 3,
    threshold: float | None = None,
) -> tuple[object, dict[str, object]]:
    """Tune XGBoost using a compact randomized search and save the retained model."""

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

    base_estimator = XGBClassifier(
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1,
    )
    pipeline = build_model_pipeline(base_estimator)
    search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions={
            "model__n_estimators": [150, 250, 350],
            "model__max_depth": [2, 3, 4],
            "model__learning_rate": [0.03, 0.05, 0.08],
            "model__subsample": [0.8, 0.9, 1.0],
            "model__colsample_bytree": [0.8, 0.9, 1.0],
        },
        n_iter=n_iter,
        scoring="average_precision",
        cv=cv,
        random_state=42,
        n_jobs=-1,
    )
    search.fit(x_train, y_train)
    best_model = search.best_estimator_
    threshold_used = settings.default_threshold if threshold is None else threshold
    metrics = evaluate_model(best_model, x_test, y_test, threshold=threshold_used)
    metrics.update(
        {
            "model_name": settings.final_model_name,
            "best_params": search.best_params_,
            "best_cv_score": float(search.best_score_),
            "operational_note": "Risk prioritization model, not an autonomous classifier.",
        }
    )

    candidate_path = save_model(
        best_model,
        output_path or settings.trained_models_dir / "xgboost_pipeline.joblib",
    )
    promote_to_best_model(candidate_path)
    save_json(metrics, metrics_path or settings.metrics_dir / "tuned_xgboost_metrics.json")
    save_json(metrics, settings.metrics_dir / "final_model_metrics.json")
    export_xgboost_feature_importance(best_model)
    return best_model, metrics
