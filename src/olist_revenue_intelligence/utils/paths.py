"""Path helpers used by scripts and package modules."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXPORTS_DATA_DIR = DATA_DIR / "exports"
MODELS_DIR = PROJECT_ROOT / "models"
TRAINED_MODELS_DIR = MODELS_DIR / "trained"
METRICS_DIR = MODELS_DIR / "metrics"
ARTIFACTS_DIR = MODELS_DIR / "artifacts"


def ensure_directory(path: str | Path) -> Path:
    """Create a directory if needed and return it as a Path."""

    resolved = Path(path)
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def project_path(*parts: str) -> Path:
    """Build an absolute path from the project root."""

    return PROJECT_ROOT.joinpath(*parts)


def ensure_project_directories() -> None:
    """Create standard generated-output directories."""

    for path in [
        INTERIM_DATA_DIR,
        EXPORTS_DATA_DIR,
        TRAINED_MODELS_DIR,
        METRICS_DIR,
        ARTIFACTS_DIR,
    ]:
        ensure_directory(path)

