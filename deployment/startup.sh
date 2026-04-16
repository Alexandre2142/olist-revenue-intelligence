#!/usr/bin/env sh
set -e

uvicorn olist_revenue_intelligence.api.main:app --host 0.0.0.0 --port 8000

