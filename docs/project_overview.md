# Project Overview

Olist Revenue Intelligence Command Center is a business-first analytics project based on the Brazilian Olist e-commerce dataset. The core idea is that revenue performance should be interpreted together with market exposure and operational friction, especially delivery risk.

The AI Engineer layer sits after the BI and data science work. It packages the late-delivery model into reusable Python modules, saves artifacts, exposes a small FastAPI service, and adds tests and Docker packaging.

The retained machine learning task is order-level late-delivery risk prioritization. It is not intended to be a high-precision autonomous classifier.

