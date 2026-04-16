"""Train benchmark models and export comparison artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from olist_revenue_intelligence.models.compare_models import compare_metric_files
from olist_revenue_intelligence.models.train_logistic_regression import train_logistic_regression_model
from olist_revenue_intelligence.models.train_random_forest import train_random_forest_model
from olist_revenue_intelligence.models.train_xgboost import train_xgboost_model
from olist_revenue_intelligence.utils.logging_utils import configure_logging
from olist_revenue_intelligence.utils.paths import ensure_project_directories


def main() -> None:
    configure_logging()
    ensure_project_directories()
    train_logistic_regression_model()
    train_random_forest_model()
    train_xgboost_model()
    comparison = compare_metric_files()
    print(comparison.to_string(index=False))


if __name__ == "__main__":
    main()

