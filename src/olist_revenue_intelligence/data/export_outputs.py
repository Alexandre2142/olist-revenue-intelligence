"""Export metrics, tabular artifacts, and prediction samples."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def save_json(data: dict[str, Any], path: str | Path) -> Path:
    """Save a dictionary as pretty JSON."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return output_path


def load_json(path: str | Path) -> dict[str, Any]:
    """Load a JSON dictionary from disk."""

    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_dataframe(df: pd.DataFrame, path: str | Path, index: bool = False) -> Path:
    """Save a DataFrame to CSV."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=index)
    return output_path


def export_prediction_sample(
    df: pd.DataFrame,
    probabilities: list[float],
    path: str | Path,
    threshold: float,
) -> Path:
    """Save a small order-level prediction sample for documentation or QA."""

    sample = df.copy()
    sample["predicted_probability"] = probabilities
    sample["predicted_class"] = (sample["predicted_probability"] >= threshold).astype(int)
    return save_dataframe(sample, path)

