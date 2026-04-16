"""Simple leakage audit for the retained feature list."""

from __future__ import annotations

import pandas as pd

from olist_revenue_intelligence.data.validate_inputs import LEAKAGE_KEYWORDS


def audit_feature_columns(feature_columns: list[str]) -> pd.DataFrame:
    """Return a feature-level audit table with a conservative leakage flag."""

    records: list[dict[str, object]] = []
    for feature in feature_columns:
        matched = [
            keyword
            for keyword in LEAKAGE_KEYWORDS
            if keyword in feature.lower() and feature != "estimated_delivery_days"
        ]
        records.append(
            {
                "feature": feature,
                "potential_leakage": bool(matched),
                "matched_terms": ", ".join(matched),
                "notes": "Retained pre-delivery feature" if not matched else "Review manually",
            }
        )
    return pd.DataFrame(records)

