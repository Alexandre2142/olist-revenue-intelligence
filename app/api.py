"""Compatibility entrypoint for running the API as ``uvicorn app.api:app``."""

from olist_revenue_intelligence.api.main import app

__all__ = ["app"]

