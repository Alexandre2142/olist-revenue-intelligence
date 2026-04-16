"""Evaluation helpers for late-delivery risk models."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def get_positive_class_probabilities(model: Any, x: pd.DataFrame) -> np.ndarray:
    """Return P(is_late=1) from a fitted classifier or pipeline."""

    if not hasattr(model, "predict_proba"):
        raise TypeError("Model must expose predict_proba for threshold-based risk scoring.")
    probabilities = model.predict_proba(x)
    if probabilities.ndim != 2 or probabilities.shape[1] < 2:
        raise ValueError("predict_proba output must contain probabilities for two classes.")
    return probabilities[:, 1]


def classification_metrics(
    y_true: pd.Series | np.ndarray,
    y_probability: pd.Series | np.ndarray,
    threshold: float = 0.5,
) -> dict[str, float | int]:
    """Compute threshold-aware metrics for a binary late-delivery model."""

    y_true_array = np.asarray(y_true).astype(int)
    y_probability_array = np.asarray(y_probability, dtype=float)
    y_pred = (y_probability_array >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true_array, y_pred, labels=[0, 1]).ravel()

    metrics: dict[str, float | int] = {
        "threshold": float(threshold),
        "accuracy": float(accuracy_score(y_true_array, y_pred)),
        "precision": float(precision_score(y_true_array, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true_array, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true_array, y_pred, zero_division=0)),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
    }

    if len(np.unique(y_true_array)) == 2:
        metrics["roc_auc"] = float(roc_auc_score(y_true_array, y_probability_array))
        metrics["average_precision"] = float(
            average_precision_score(y_true_array, y_probability_array)
        )
    else:
        metrics["roc_auc"] = 0.0
        metrics["average_precision"] = 0.0

    return metrics


def evaluate_model(
    model: Any,
    x_test: pd.DataFrame,
    y_test: pd.Series,
    threshold: float = 0.5,
) -> dict[str, float | int]:
    """Evaluate a fitted model on held-out data."""

    probabilities = get_positive_class_probabilities(model, x_test)
    return classification_metrics(y_test, probabilities, threshold=threshold)

