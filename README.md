# Olist Revenue Intelligence Command Center

Business-first analytics and AI Engineer packaging for the Brazilian Olist e-commerce dataset.

## Purpose

This project started as a BI and decision-support analysis. The main thesis is that the strategic issue is not revenue generation alone, but the uneven exposure of important markets and product segments to operational friction.

The AI Engineer layer adds a clean Python package around the existing data science extension for late-delivery prediction. It keeps the business framing intact while adding modular code, reproducible scripts, saved artifacts, tests, Docker packaging, and a small FastAPI app.

## What This Package Demonstrates

- Modular Python project structure under `src/`
- Leakage-aware feature definitions
- Reproducible model training and tuning scripts
- Local artifact saving with `joblib`, JSON, and CSV outputs
- FastAPI model serving
- Basic pytest coverage
- Docker packaging for local API serving

This is intentionally not an enterprise MLOps platform. It avoids MLflow, Airflow, cloud deployment, CI/CD, Kubernetes, authentication systems, and frontend frameworks.

## Business and Modeling Framing

The prediction target is:

```text
is_late
```

The model predicts late-delivery risk at order level using pre-delivery features only. Review-based, actual-delivery, and other post-outcome variables are excluded to reduce leakage.

Retained operational configuration:

```text
model = tuned XGBoost
threshold = 0.7
```

The `0.7` threshold should be interpreted as a high-confidence alert threshold. In the current retained artifact, it produces very few positive alerts: precision is high, but recall is extremely low. This is useful for strict escalation, not broad late-delivery coverage.

The model is a risk prioritization tool, not a high-precision autonomous classifier.

## Project Structure

```text
data/                         Raw placeholders, processed datasets, and exports
notebooks/                    Original BI and DS notebooks
powerbi/                      Power BI report and screenshots
src/olist_revenue_intelligence/
  config/                     Settings and retained feature configuration
  data/                       Data loading, validation, and export helpers
  features/                   Feature definitions, leakage audit, preprocessing
  models/                     Training, tuning, evaluation, registry, prediction
  api/                        FastAPI schemas, service, and routes
  utils/                      Paths, logging, and shared helpers
models/                       Saved model pipelines, metrics, and artifacts
scripts/                      Runnable local workflows
tests/                        Lightweight pytest suite
deployment/                   Dockerfile, Compose file, and startup script
docs/                         Portfolio-ready documentation
```

## Installation

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

On macOS or Linux, activate with:

```bash
source .venv/bin/activate
```

## Data Assumption

The modeling dataset is expected at:

```text
data/processed/late_delivery_modeling_dataset.csv
```

Expected minimum columns:

- `order_id`
- `is_late`
- `order_revenue`
- `n_items`
- `n_sellers`
- `n_categories`
- `customer_state`
- `estimated_delivery_days`
- `purchase_month`
- `purchase_dayofweek`
- `purchase_hour`
- `is_weekend`
- `order_revenue_per_item`

## Run the Pipeline

Validate the processed modeling dataset and export the leakage audit:

```bash
python scripts/run_build_modeling_dataset.py
```

Train benchmark models:

```bash
python scripts/run_train_all_models.py
```

Tune Random Forest and XGBoost, then promote tuned XGBoost as the retained best model:

```bash
python scripts/run_tuning.py
```

Create threshold-analysis artifacts for the retained model:

```bash
python scripts/run_threshold_analysis.py
```

Export lightweight portfolio artifacts:

```bash
python scripts/run_export_artifacts.py
```

## Launch the API

Run locally:

```bash
python scripts/run_api_local.py
```

Then open:

```text
http://localhost:8000/docs
```

Main endpoints:

- `GET /health`
- `GET /model-info`
- `POST /predict`

Example prediction payload:

```json
{
  "order_revenue": 141.46,
  "n_items": 1,
  "n_sellers": 1,
  "n_categories": 1,
  "customer_state": "SP",
  "estimated_delivery_days": 19.1,
  "purchase_month": 7,
  "purchase_dayofweek": 1,
  "purchase_hour": 20,
  "is_weekend": 0,
  "order_revenue_per_item": 141.46
}
```

## Docker

From the `deployment/` folder:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

The Compose setup mounts the local `models/` folder so the API can use `models/trained/best_model_pipeline.joblib`.

## Testing

Run:

```bash
pytest
```

The tests use small synthetic data and temporary model artifacts, so they do not require the full Olist dataset or the committed production artifact.

## Limitations

- The retained model supports operational prioritization, not autonomous decision-making.
- The retained `0.7` threshold is intentionally conservative and should be presented as high-confidence alerting, not broad recall-oriented triage.
- The feature set is intentionally narrow and leakage-aware.
- The API serves one order at a time for clarity.
- Docker is local-only and does not imply cloud production deployment.
- Metrics should be interpreted in the context of delivery-risk triage and business cost tradeoffs.
