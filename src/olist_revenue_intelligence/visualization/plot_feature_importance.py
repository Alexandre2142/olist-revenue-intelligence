"""Plot saved feature-importance artifacts."""

from __future__ import annotations

import pandas as pd


def plot_feature_importance(feature_importance: pd.DataFrame, top_n: int = 20):
    """Create a horizontal feature-importance chart."""

    import matplotlib.pyplot as plt

    required = {"feature", "importance"}
    if not required.issubset(feature_importance.columns):
        raise ValueError("Feature importance table must contain feature and importance columns.")
    top_features = feature_importance.sort_values("importance", ascending=False).head(top_n)
    axis = top_features.sort_values("importance").plot.barh(x="feature", y="importance", legend=False)
    axis.set_xlabel("importance")
    axis.set_ylabel("")
    plt.tight_layout()
    return axis

