"""Validate and re-export the late-delivery modeling dataset artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from olist_revenue_intelligence.features.build_modeling_dataset import build_modeling_dataset
from olist_revenue_intelligence.utils.logging_utils import configure_logging
from olist_revenue_intelligence.utils.paths import ensure_project_directories


def main() -> None:
    configure_logging()
    ensure_project_directories()
    df = build_modeling_dataset()
    print(f"Validated modeling dataset with {len(df):,} rows.")


if __name__ == "__main__":
    main()

