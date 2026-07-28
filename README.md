# Olist Revenue Intelligence Command Center

Business intelligence, late-delivery risk modeling, and lightweight AI engineering for the Brazilian Olist e-commerce dataset.

## Overview

This project combines three complementary layers:

1. **Business intelligence** to identify markets and product segments exposed to operational friction.
2. **Predictive modeling** to estimate late-delivery risk at order level before the delivery outcome is known.
3. **Lightweight AI engineering** to package the retained model into reproducible Python workflows, saved artifacts, tests, Docker configuration, and a small FastAPI service.

The project started as a BI and decision-support analysis. Its central business thesis is that Olist's strategic challenge is not revenue generation alone, but the uneven exposure of valuable markets and product segments to delivery friction.

The machine-learning extension translates this business problem into an operational prioritization use case: identifying orders that may require attention before delays materialize.

---

## Business Problem

Revenue performance should not be analyzed independently from operational execution.

A market or product category may generate substantial revenue while remaining disproportionately exposed to:

* delivery delays;
* operational complexity;
* fragmented seller participation;
* customer dissatisfaction;
* uneven geographical service quality.

The BI layer examines these patterns at market and segment level.

The predictive layer addresses a related order-level question:

> Given the information available before delivery, which orders present the highest risk of arriving late?

The objective is not to automate operational decisions. The model is intended to support prioritization when review or intervention capacity is limited.

---

## Key Business Findings

The Power BI analysis covers approximately 96,000 orders, 93,000 customers, and R$15 million in revenue.

> The dashboard-wide late-delivery rate of `6.8%` is calculated on the broader analytical population. The `8.11%` prevalence reported in the modeling section refers specifically to the held-out machine-learning test set.

### 1. Revenue is highly concentrated geographically

São Paulo alone represents approximately `37.4%` of total revenue, while the five largest states account for `73.2%`.

This concentration creates a dual priority:

- preserve execution quality in the largest healthy anchor markets;
- address operational weakness where high revenue exposure overlaps with delivery friction.

**Decision implication:** operational resources should be allocated according to commercial exposure, rather than treating all underperforming states equally.

### 2. Rio de Janeiro is the most commercially significant fragile market

Rio de Janeiro represents approximately `13.3%` of total revenue, but records:

- a late-delivery rate of `12.1%`;
- approximately `3.0` percentage points more delays than the global benchmark;
- an average review score of `3.97`, below the broader benchmark.

Bahia, Ceará, and Pará also display elevated late-delivery rates between approximately `11.2%` and `13.8%`, combined with below-benchmark customer feedback.

**Decision implication:** Rio de Janeiro should be the first geographic remediation priority because it combines substantial revenue exposure with weaker execution. Bahia, Ceará, and Pará form a second intervention group.

### 3. The customer base shows limited repeat behavior

The repeat-customer rate is approximately `3.0%`, while single-order customers account for roughly `94.4%` of revenue.

This indicates that commercial scale is currently driven primarily by customer acquisition and transaction volume rather than strong repeat purchasing.

**Decision implication:** delivery reliability and post-purchase experience should be treated not only as operational issues, but also as potential customer-retention levers.

### 4. Portfolio value is not evenly distributed across risk segments

The category portfolio contains a substantial core-fragile segment that represents the largest revenue block, despite weaker operational characteristics.

The seller portfolio also shows that seller counts and revenue contribution are not aligned uniformly across healthy and fragile groups.

**Decision implication:** category and seller interventions should prioritize segments where revenue concentration and operational fragility overlap, instead of focusing only on the weakest isolated entities.

---

## Business Intelligence Dashboard

### Executive overview

![Olist Revenue Intelligence executive overview](powerbi/screenshots/p1.png)

The executive page consolidates business scale, execution health, geographic exposure, and category-portfolio risk into a single decision-oriented view.

### Geographic exposure and operational friction

![Olist geographic exposure and operational friction](powerbi/screenshots/p5.png)

The geographic analysis distinguishes healthy anchor markets from fragile priority markets by combining revenue share, late-delivery performance, and customer-review signals.

### Strategic recommendations

![Olist strategic recommendations](powerbi/screenshots/p6.png)

The final page converts the analytical findings into sequenced priorities: stabilize high-value fragile markets, protect healthy anchors, and allocate intervention effort according to exposure.

---

## Decision Layers

### Business Intelligence

The Power BI component supports strategic and operational analysis across dimensions such as:

* revenue;
* geography;
* product categories;
* order characteristics;
* customer experience;
* delivery performance.

Its purpose is to locate areas where commercially important activity overlaps with operational friction.

### Predictive Risk Modeling

The modeling component estimates the probability that an individual order will be delivered late.

Only information available before the delivery outcome is retained. Variables based on reviews, actual delivery timestamps, and other post-outcome information are excluded to reduce target leakage.

### Local Model Serving

The retained pipeline is exposed through a small FastAPI application.

The API demonstrates how the model artifact can be loaded and queried locally. It is a portfolio-oriented serving layer, not a production deployment platform.

---

## Solution Architecture

```mermaid
flowchart TD
    A[Raw Olist data] --> B[Data preparation and validation]
    B --> C[Processed analytical datasets]

    C --> D[Power BI decision-support analysis]
    C --> E[Late-delivery modeling pipeline]

    E --> F[Feature definitions and leakage audit]
    F --> G[Model training and tuning]
    G --> H[Saved model pipeline and metrics]
    H --> I[Threshold analysis]
    H --> J[FastAPI prediction service]

    J --> K[Local API or Docker deployment]
```

The Power BI and machine-learning components use the same broader business context but serve different decision levels:

* Power BI supports market- and segment-level diagnosis.
* The predictive model supports order-level risk prioritization.
* FastAPI demonstrates local model consumption.

---

## What This Repository Demonstrates

### Analytics and modeling

* Business-first problem formulation
* Order-level late-delivery target definition
* Leakage-aware feature selection
* Benchmark model comparison
* Random Forest and XGBoost tuning
* Threshold-based operating analysis
* Business interpretation of precision–recall trade-offs

### Python and AI engineering

* Modular package structure under `src/`
* Reproducible training and tuning scripts
* Saved pipelines and supporting artifacts
* Configuration-driven feature definitions
* FastAPI model serving
* Request and response validation
* Basic pytest coverage
* Docker packaging for local serving

This repository is intentionally scoped as a strong local analytics and AI-engineering project.

It does **not** claim to implement a complete enterprise MLOps platform. The project deliberately excludes:

* cloud deployment;
* MLflow;
* Airflow;
* Kubernetes;
* authentication and authorization;
* automated CI/CD;
* live monitoring;
* frontend application frameworks.

---

## Modeling Scope

The prediction target is:

```text
is_late
```

The model predicts late-delivery risk at order level.

### Leakage control

The feature set is restricted to variables that can reasonably be known before delivery.

Excluded variables include:

* actual delivery information;
* customer reviews;
* post-outcome timestamps;
* variables directly derived from the final delivery result.

This prevents the model from relying on information that would not be available when an operational decision must be made.

### Expected model inputs

The retained model uses the following features:

* `order_revenue`
* `n_items`
* `n_sellers`
* `n_categories`
* `customer_state`
* `estimated_delivery_days`
* `purchase_month`
* `purchase_dayofweek`
* `purchase_hour`
* `is_weekend`
* `order_revenue_per_item`

---

## Retained Model

The retained operational configuration is:

```text
model = tuned XGBoost
demonstration_threshold = 0.70
```

The complete preprocessing and prediction logic is saved as a reusable model pipeline.

The retained threshold should not be interpreted as a universally optimal classification threshold. It represents one specific operating mode.

### Strict-escalation interpretation

At a threshold of `0.70`, the model generates very few positive alerts.

This produces the following behavior:

* relatively high confidence in the orders that are flagged;
* very limited coverage of all late deliveries;
* high precision relative to broader thresholds;
* extremely low recall.

This configuration is appropriate only when:

* manual review capacity is limited;
* false alerts are costly;
* the objective is to escalate a small number of high-risk cases.

It is not appropriate when the business objective is to detect a large proportion of all delayed orders.

The model should therefore be treated as a **risk-ranking and prioritization tool**, not as an autonomous decision system.

---

## Model Results

The models were evaluated on a held-out test set containing 19,294 orders.

- Late orders: 1,565
- Non-late orders: 17,729
- Late-delivery prevalence: 8.11%

Because the target is imbalanced, model selection emphasizes ROC-AUC and average precision rather than accuracy alone.

| Model | ROC-AUC | Average Precision | Precision @ 0.70 | Recall @ 0.70 | F1 @ 0.70 | Positive Alerts |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.6863 | 0.1624 | 21.54% | 19.68% | 20.57% | 1,430 |
| Random Forest | 0.7508 | 0.2325 | 34.83% | 15.85% | 21.78% | 712 |
| Tuned Random Forest | 0.7577 | 0.2402 | 33.83% | 20.51% | 25.54% | 949 |
| XGBoost | 0.7635 | 0.2522 | — | 0.00% | 0.00% | 0 |
| Tuned XGBoost | **0.7683** | **0.2567** | 100.00%* | 0.06% | 0.13% | 1 |

\* The observed precision of 100% is based on a single positive prediction and should not be interpreted as a robust estimate of operational precision.

### Model selection

The tuned XGBoost pipeline is retained because it provides the strongest overall probability-ranking performance:

- ROC-AUC: `0.7683`
- Average precision: `0.2567`
- Cross-validation average precision: `0.2513`

Its average precision is substantially higher than the test-set late-delivery prevalence of `8.11%`, indicating useful ranking signal despite the difficulty of the classification problem.

The retained model should primarily be interpreted as a risk-scoring model: orders with higher predicted probabilities are ranked as more operationally exposed.

### Threshold interpretation

At the demonstration threshold of `0.70`, tuned XGBoost flags only one order out of 19,294 test observations.

This produces:

- 1 true positive;
- 0 false positives;
- 1,564 false negatives;
- recall of approximately `0.06%`.

The threshold therefore represents an extremely restrictive escalation policy, not a general-purpose delay-detection configuration.

Threshold selection should be treated as a separate business decision based on:

- available intervention capacity;
- the cost of investigating false alerts;
- the cost of missed late deliveries;
- the required balance between precision and coverage.

A lower threshold would be required for broader operational triage.

## Project Structure

```text
data/
  raw/                        Raw data placeholders
  processed/                  Processed analytical and modeling datasets
  exports/                    Generated analytical exports

notebooks/
  ...                         Original BI and data-science notebooks

powerbi/
  ...                         Power BI report files and screenshots

src/
  olist_revenue_intelligence/
    config/                   Settings and retained feature configuration
    data/                     Loading, validation, and export helpers
    features/                 Feature definitions, preprocessing, leakage audit
    models/                   Training, tuning, evaluation, registry, prediction
    api/                      FastAPI schemas, services, and routes
    utils/                    Paths, logging, and shared helpers

models/
  trained/                    Saved model pipelines
  metrics/                    Evaluation and threshold artifacts
  ...                         Additional generated model outputs

scripts/
  ...                         Executable local workflows

tests/
  ...                         Lightweight pytest suite

deployment/
  Dockerfile
  compose.yaml
  start.sh                    Local container startup configuration

docs/
  ...                         Portfolio-oriented documentation
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd olist-revenue-intelligence
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install the project

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

---

## Data Requirements

The modeling workflow expects a processed order-level dataset at:

```text
data/processed/late_delivery_modeling_dataset.csv
```

Expected minimum columns:

* `order_id`
* `is_late`
* `order_revenue`
* `n_items`
* `n_sellers`
* `n_categories`
* `customer_state`
* `estimated_delivery_days`
* `purchase_month`
* `purchase_dayofweek`
* `purchase_hour`
* `is_weekend`
* `order_revenue_per_item`

The repository structure separates raw data, processed datasets, exports, trained models, and generated evaluation artifacts.

---

## Run the Modeling Workflow

The scripts are separated by responsibility so that individual stages can be rerun independently.

### Validate the modeling dataset

Validate the processed dataset and export the leakage audit:

```bash
python scripts/run_build_modeling_dataset.py
```

### Train benchmark models

Train the benchmark model set:

```bash
python scripts/run_train_all_models.py
```

### Tune candidate models

Tune Random Forest and XGBoost, then retain the tuned XGBoost pipeline:

```bash
python scripts/run_tuning.py
```

### Analyze classification thresholds

Generate threshold-analysis artifacts for the retained model:

```bash
python scripts/run_threshold_analysis.py
```

### Export portfolio artifacts

Export lightweight metrics, configuration, and model documentation artifacts:

```bash
python scripts/run_export_artifacts.py
```

---

## Launch the API

Run the API locally:

```bash
python scripts/run_api_local.py
```

Open the interactive API documentation at:

```text
http://localhost:8000/docs
```

### Main endpoints

* `GET /health`
* `GET /model-info`
* `POST /predict`

### Example prediction request

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

The prediction response provides the model's estimated late-delivery risk and the classification associated with the retained operating threshold.

---

## Docker

From the `deployment/` directory:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

The Compose configuration mounts the local `models/` directory so that the API can load:

```text
models/trained/best_model_pipeline.joblib
```

The Docker setup is intended for local reproducibility and serving demonstrations. It does not imply cloud or enterprise production readiness.

---

## Testing

Run the test suite with:

```bash
pytest
```

The tests use:

* small synthetic datasets;
* temporary model artifacts;
* isolated API and pipeline checks.

They do not require the complete Olist dataset or the committed retained model artifact.

---

## Scope and Limitations

* The model supports operational prioritization, not autonomous decision-making.
* The retained `0.70` threshold represents strict high-confidence escalation.
* The retained threshold has very low recall and should not be presented as broad delay detection.
* Alternative thresholds should be evaluated according to intervention capacity and the relative costs of false positives and false negatives.
* The feature set is intentionally narrow and leakage-aware.
* The API processes one order at a time for clarity.
* The Docker setup is local-only.
* No cloud infrastructure, production monitoring, authentication, or automated retraining is implemented.
* Model metrics must be interpreted in the context of delivery-risk triage and business cost trade-offs.

---

## Intended Portfolio Signal

This project demonstrates the ability to connect:

* business analysis;
* decision-support reporting;
* leakage-aware predictive modeling;
* model evaluation and threshold selection;
* modular Python engineering;
* local API serving;
* testing and containerization.

The central objective is not to maximize technical complexity. It is to package an analytically coherent business problem into a reproducible and interpretable applied-AI workflow.
