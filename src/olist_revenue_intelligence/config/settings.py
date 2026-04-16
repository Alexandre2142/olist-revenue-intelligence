"""Central settings for the Olist Revenue Intelligence project."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


DEFAULT_MODEL_FEATURES: list[str] = [
    "order_revenue",
    "n_items",
    "n_sellers",
    "n_categories",
    "customer_state",
    "estimated_delivery_days",
    "purchase_month",
    "purchase_dayofweek",
    "purchase_hour",
    "is_weekend",
    "order_revenue_per_item",
]

NUMERIC_FEATURES: list[str] = [
    "order_revenue",
    "n_items",
    "n_sellers",
    "n_categories",
    "estimated_delivery_days",
    "purchase_month",
    "purchase_dayofweek",
    "purchase_hour",
    "is_weekend",
    "order_revenue_per_item",
]

CATEGORICAL_FEATURES: list[str] = ["customer_state"]


@dataclass(frozen=True)
class Settings:
    """Project settings with environment-variable overrides for serving."""

    project_root: Path = field(default_factory=_project_root)
    target_column: str = "is_late"
    id_column: str = "order_id"
    model_features: list[str] = field(default_factory=lambda: DEFAULT_MODEL_FEATURES.copy())
    numeric_features: list[str] = field(default_factory=lambda: NUMERIC_FEATURES.copy())
    categorical_features: list[str] = field(default_factory=lambda: CATEGORICAL_FEATURES.copy())
    final_model_name: str = "tuned_xgboost"
    default_threshold: float = field(
        default_factory=lambda: float(os.getenv("MODEL_THRESHOLD", "0.7"))
    )
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    @property
    def processed_dataset_path(self) -> Path:
        return self.project_root / "data" / "processed" / "late_delivery_modeling_dataset.csv"

    @property
    def trained_models_dir(self) -> Path:
        return self.project_root / "models" / "trained"

    @property
    def metrics_dir(self) -> Path:
        return self.project_root / "models" / "metrics"

    @property
    def artifacts_dir(self) -> Path:
        return self.project_root / "models" / "artifacts"

    @property
    def best_model_path(self) -> Path:
        env_path = os.getenv("MODEL_PATH")
        if env_path:
            path = Path(env_path)
            return path if path.is_absolute() else self.project_root / path
        return self.trained_models_dir / "best_model_pipeline.joblib"


settings = Settings()

