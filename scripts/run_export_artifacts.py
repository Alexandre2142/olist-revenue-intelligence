"""Export lightweight non-model artifacts for portfolio review."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from olist_revenue_intelligence.config.settings import settings
from olist_revenue_intelligence.data.export_outputs import save_dataframe
from olist_revenue_intelligence.features.feature_engineering import get_feature_columns
from olist_revenue_intelligence.features.leakage_audit import audit_feature_columns
from olist_revenue_intelligence.models.compare_models import compare_metric_files
from olist_revenue_intelligence.utils.paths import ensure_project_directories


def main() -> None:
    ensure_project_directories()
    save_dataframe(audit_feature_columns(get_feature_columns()), settings.artifacts_dir / "leakage_audit.csv")
    comparison = compare_metric_files()
    print(f"Exported leakage audit and model comparison with {len(comparison)} rows.")


if __name__ == "__main__":
    main()

