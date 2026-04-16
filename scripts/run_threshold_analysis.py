"""Create threshold analysis for the retained best model."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from olist_revenue_intelligence.config.settings import settings
from olist_revenue_intelligence.data.export_outputs import save_dataframe
from olist_revenue_intelligence.data.load_processed_data import load_late_delivery_dataset, split_features_target
from olist_revenue_intelligence.models.evaluate import get_positive_class_probabilities
from olist_revenue_intelligence.models.registry import load_model
from olist_revenue_intelligence.models.thresholding import analyze_thresholds
from olist_revenue_intelligence.utils.logging_utils import configure_logging
from olist_revenue_intelligence.utils.paths import ensure_project_directories


def main() -> None:
    configure_logging()
    ensure_project_directories()
    df = load_late_delivery_dataset()
    x, y = split_features_target(df)
    model = load_model()
    probabilities = get_positive_class_probabilities(model, x)
    threshold_table = analyze_thresholds(y, probabilities)
    save_dataframe(threshold_table, settings.artifacts_dir / "threshold_analysis.csv")
    sample = df[[settings.id_column, *settings.model_features]].head(100).copy()
    sample["predicted_probability"] = probabilities[: len(sample)]
    sample["predicted_class"] = (sample["predicted_probability"] >= settings.default_threshold).astype(int)
    save_dataframe(sample, settings.artifacts_dir / "final_prediction_sample.csv")
    print(threshold_table.to_string(index=False))


if __name__ == "__main__":
    main()

