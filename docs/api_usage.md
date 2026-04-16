# API Usage

Start the API locally:

```bash
python scripts/run_api_local.py
```

Or with Docker Compose:

```bash
cd deployment
docker compose up --build
```

Health check:

```bash
curl http://localhost:8000/health
```

Model metadata:

```bash
curl http://localhost:8000/model-info
```

Prediction example:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

If `models/trained/best_model_pipeline.joblib` does not exist yet, run tuning or training first.

