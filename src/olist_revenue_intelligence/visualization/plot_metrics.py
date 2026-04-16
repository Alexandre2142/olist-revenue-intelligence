"""Plot model comparison metrics when matplotlib is available."""

from __future__ import annotations

import pandas as pd


def plot_metric_bars(comparison: pd.DataFrame, metric: str = "average_precision"):
    """Create a simple bar chart for a selected model-comparison metric."""

    import matplotlib.pyplot as plt

    if comparison.empty or metric not in comparison.columns:
        raise ValueError(f"Comparison table must include '{metric}'.")
    axis = comparison.plot.bar(x="model_name", y=metric, legend=False)
    axis.set_ylabel(metric)
    axis.set_xlabel("model")
    axis.set_title(f"Model comparison: {metric}")
    plt.tight_layout()
    return axis

