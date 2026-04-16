"""Threshold analysis for risk-prioritization use cases."""

from __future__ import annotations

import numpy as np
import pandas as pd

from olist_revenue_intelligence.models.evaluate import classification_metrics


def analyze_thresholds(
    y_true: pd.Series | np.ndarray,
    y_probability: pd.Series | np.ndarray,
    thresholds: list[float] | None = None,
) -> pd.DataFrame:
    """Evaluate model behavior across candidate operating thresholds."""

    candidate_thresholds = thresholds or [round(value, 2) for value in np.arange(0.1, 0.91, 0.05)]
    rows = [
        classification_metrics(y_true, y_probability, threshold=threshold)
        for threshold in candidate_thresholds
    ]
    return pd.DataFrame(rows)


def apply_threshold(probability: float, threshold: float) -> int:
    """Convert a probability into an operational risk flag."""

    return int(float(probability) >= float(threshold))


def interpretation(probability: float, threshold: float) -> str:
    """Return a compact business-friendly interpretation."""

    if probability >= threshold:
        return "High late-delivery risk: prioritize this order for operational review."
    return "Lower late-delivery risk: monitor normally unless other business rules apply."

