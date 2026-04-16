"""Plot a confusion matrix from metric JSON fields."""

from __future__ import annotations

import numpy as np


def plot_confusion_matrix_from_metrics(metrics: dict[str, int | float]):
    """Create a confusion matrix chart from exported metric values."""

    import matplotlib.pyplot as plt

    matrix = np.array(
        [
            [metrics.get("true_negatives", 0), metrics.get("false_positives", 0)],
            [metrics.get("false_negatives", 0), metrics.get("true_positives", 0)],
        ]
    )
    _, axis = plt.subplots()
    image = axis.imshow(matrix, cmap="Blues")
    axis.set_xticks([0, 1], labels=["Pred 0", "Pred 1"])
    axis.set_yticks([0, 1], labels=["Actual 0", "Actual 1"])
    for row in range(2):
        for col in range(2):
            axis.text(col, row, str(matrix[row, col]), ha="center", va="center")
    plt.colorbar(image, ax=axis)
    plt.tight_layout()
    return axis

