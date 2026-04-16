# Architecture

The project is organized into five practical layers:

1. Data and notebooks: original exploration, analytical dataset creation, and DS modeling.
2. Feature layer: leakage-aware feature definitions and preprocessing.
3. Model layer: benchmark training, tuning, evaluation, threshold analysis, local artifact registry, and prediction helpers.
4. API layer: FastAPI endpoints for health checks, model metadata, and single-order prediction.
5. Deployment and tests: Docker packaging and pytest coverage for the core behavior.

The design intentionally avoids heavy MLOps platforms. The goal is reproducibility and clarity, not enterprise ceremony.

