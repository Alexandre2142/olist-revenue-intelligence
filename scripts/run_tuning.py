"""Run compact tuning for RF and XGBoost, then retain tuned XGBoost as best model."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from olist_revenue_intelligence.models.compare_models import compare_metric_files
from olist_revenue_intelligence.models.tune_random_forest import tune_random_forest_model
from olist_revenue_intelligence.models.tune_xgboost import tune_xgboost_model
from olist_revenue_intelligence.utils.logging_utils import configure_logging
from olist_revenue_intelligence.utils.paths import ensure_project_directories


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-iter", type=int, default=8)
    parser.add_argument("--cv", type=int, default=3)
    args = parser.parse_args()

    configure_logging()
    ensure_project_directories()
    tune_random_forest_model(n_iter=args.n_iter, cv=args.cv)
    tune_xgboost_model(n_iter=args.n_iter, cv=args.cv)
    comparison = compare_metric_files()
    print(comparison.to_string(index=False))


if __name__ == "__main__":
    main()

