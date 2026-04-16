"""Plot threshold-analysis artifacts."""

from __future__ import annotations

import pandas as pd


def plot_threshold_tradeoffs(threshold_analysis: pd.DataFrame):
    """Plot precision and recall across thresholds."""

    import matplotlib.pyplot as plt

    required = {"threshold", "precision", "recall"}
    if not required.issubset(threshold_analysis.columns):
        raise ValueError("Threshold table must include threshold, precision, and recall columns.")
    axis = threshold_analysis.plot.line(x="threshold", y=["precision", "recall"])
    axis.set_ylabel("score")
    axis.set_title("Threshold tradeoff")
    plt.tight_layout()
    return axis

