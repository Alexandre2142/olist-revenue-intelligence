"""Lightweight local model and artifact registry."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib

from olist_revenue_intelligence.config.settings import settings
from olist_revenue_intelligence.data.export_outputs import load_json, save_json


def save_model(model: Any, path: str | Path) -> Path:
    """Persist a fitted model pipeline."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)
    return output_path


def load_model(path: str | Path | None = None) -> Any:
    """Load a fitted model pipeline from disk."""

    model_path = Path(path) if path is not None else settings.best_model_path
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model artifact not found at {model_path}. Run training or set MODEL_PATH."
        )
    return joblib.load(model_path)


def save_model_metadata(metadata: dict[str, Any], path: str | Path | None = None) -> Path:
    """Save metadata describing the retained model artifact."""

    metadata_path = Path(path) if path else settings.metrics_dir / "final_model_metrics.json"
    return save_json(metadata, metadata_path)


def load_model_metadata(path: str | Path | None = None) -> dict[str, Any]:
    """Load retained model metadata if available."""

    metadata_path = Path(path) if path else settings.metrics_dir / "final_model_metrics.json"
    if not metadata_path.exists():
        return {
            "model_name": settings.final_model_name,
            "threshold": settings.default_threshold,
            "status": "metadata_not_found",
        }
    return load_json(metadata_path)


def promote_to_best_model(source_path: str | Path, destination_path: str | Path | None = None) -> Path:
    """Copy a trained candidate artifact into the standard best-model path."""

    source = Path(source_path)
    destination = Path(destination_path) if destination_path else settings.best_model_path
    if not source.exists():
        raise FileNotFoundError(f"Candidate model artifact not found at {source}.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(source.read_bytes())
    return destination

