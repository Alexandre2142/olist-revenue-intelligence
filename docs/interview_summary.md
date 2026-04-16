# Interview Summary

This project demonstrates how a BI-oriented analytics project can be extended into a modest AI Engineer package without pretending to be a production platform.

Key points to explain:

- The business problem is not just revenue generation; it is the overlap between commercially important segments and delivery friction.
- The ML model supports risk prioritization for late delivery at order level.
- Feature selection is leakage-aware: review and post-delivery fields are excluded.
- The package adds reproducibility through scripts, saved artifacts, tests, and Docker.
- FastAPI serves the retained model with the retained `0.7` threshold, best described as a high-confidence alert threshold rather than a broad recall-oriented triage setting.
- The solution avoids unnecessary tools such as MLflow, Airflow, Kubernetes, and cloud deployment because they are not needed for this portfolio scope.
