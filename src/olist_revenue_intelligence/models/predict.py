"""Prediction helpers shared by scripts and the API service."""

from __future__ import annotations

from typing import Any

import pandas as pd

from olist_revenue_intelligence.config.settings import settings
from olist_revenue_intelligence.data.validate_inputs import validate_prediction_frame
from olist_revenue_intelligence.models.evaluate import get_positive_class_probabilities
from olist_revenue_intelligence.models.registry import load_model
from olist_revenue_intelligence.models.thresholding import apply_threshold, interpretation


def predict_late_delivery_risk(
    payload: dict[str, Any] | pd.DataFrame,
    model: Any | None = None,
    threshold: float | None = None,
) -> dict[str, float | int | str]:
    """Predict late-delivery risk for a single order payload."""

    threshold_used = settings.default_threshold if threshold is None else threshold
    frame = payload.copy() if isinstance(payload, pd.DataFrame) else pd.DataFrame([payload])
    validate_prediction_frame(frame, settings.model_features)

    fitted_model = model if model is not None else load_model()
    probability = float(get_positive_class_probabilities(fitted_model, frame[settings.model_features])[0])
    predicted_class = apply_threshold(probability, threshold_used)
    return {
        "predicted_probability": probability,
        "predicted_class": predicted_class,
        "threshold_used": float(threshold_used),
        "interpretation": interpretation(probability, threshold_used),
    }


def batch_predict_late_delivery_risk(
    df: pd.DataFrame,
    model: Any | None = None,
    threshold: float | None = None,
) -> pd.DataFrame:
    """Score a DataFrame of orders and return probabilities plus threshold flags."""

    threshold_used = settings.default_threshold if threshold is None else threshold
    validate_prediction_frame(df, settings.model_features)
    fitted_model = model if model is not None else load_model()
    probabilities = get_positive_class_probabilities(fitted_model, df[settings.model_features])
    output = df.copy()
    output["predicted_probability"] = probabilities
    output["predicted_class"] = (output["predicted_probability"] >= threshold_used).astype(int)
    output["threshold_used"] = threshold_used
    return output

