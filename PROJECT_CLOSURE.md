# Project Closure — Olist Revenue Intelligence

**Status:** Frozen case study  
**Strategic umbrella:** AxiomVela — Decision Intelligence Systems  
**Closure decision:** Preserve the repository as a completed foundational case study. Do not add commercial outreach or product features before the MSc exams and subsequent field learning during the internship.

## 1. Problem addressed

The project addresses the following decision problem:

> Given information available before delivery, which orders present the highest risk of arriving late and should therefore receive priority when operational review or intervention capacity is limited?

The intended role of the system is decision support. It ranks and prioritizes operational risk; it does not automate interventions or replace business judgment.

## 2. Delivered asset

The repository contains an end-to-end analytical and lightweight AI-engineering case study comprising:

- data preparation and validation workflows;
- a Power BI decision-support layer;
- leakage-aware feature engineering;
- benchmark and tuned classification models;
- saved preprocessing and prediction pipelines;
- threshold and operating-mode analysis;
- a local FastAPI scoring service;
- request and response validation;
- basic pytest coverage;
- Docker configuration for local serving;
- portfolio-oriented technical documentation.

## 3. Current validated result

The retained model is a tuned XGBoost pipeline evaluated on a held-out test set of 19,294 orders.

- **ROC-AUC:** `0.7683`
- **Average precision:** `0.2567`
- **Cross-validation average precision:** `0.2513`
- **Test-set late-delivery prevalence:** `8.11%`

These results support the existence of useful probability-ranking signal. They do not establish production readiness or economic impact.

The demonstration threshold of `0.70` is intentionally restrictive and flags only one order in the held-out test set. It must not be interpreted as a generally optimal operating threshold.

## 4. What the project demonstrates

The project demonstrates:

- technically feasible order-level late-delivery risk scoring;
- disciplined exclusion of post-outcome information and target leakage;
- comparative model evaluation under class imbalance;
- translation of predicted risk into an operational prioritization framing;
- integration of business intelligence, predictive modeling, model artifacts, API serving, tests, and local containerization;
- the structure of a decision-intelligence case study connecting data, prediction, prioritization, and possible action.

## 5. What the project does not demonstrate

The project does **not** establish:

- adoption by real operational users;
- production-grade reliability, security, governance, or monitoring;
- probability calibration suitable for operational decisions;
- a validated intervention protocol for flagged orders;
- causal effectiveness of any intervention;
- actual reductions in late deliveries;
- verified savings, avoided losses, or return on investment;
- access to sufficient real-time or intervention data;
- product–market fit;
- a validated commercial opportunity.

Any claim beyond technical feasibility and portfolio-level decision framing would therefore be unsupported.

## 6. Frozen backlog

The following items are explicitly deferred and are not part of the active project scope:

- calibration analysis, including ECE and reliability diagnostics;
- business-capacity and cost-sensitive threshold optimization;
- mixed-integer programming or other intervention-allocation solvers;
- MLflow or broader experiment-tracking infrastructure;
- cloud deployment;
- Airflow, Kubernetes, authentication, authorization, and CI/CD;
- live monitoring and drift detection;
- frontend application development;
- additional FastAPI features;
- new modeling features or algorithmic expansion;
- commercial packaging or outreach.

These items remain hypotheses or possible future extensions, not unfinished obligations.

## 7. Closure decision

Olist Revenue Intelligence is retained as the **foundational AxiomVela case study**.

Its strategic value is to demonstrate a coherent progression:

> data → prediction → prioritization → possible action → measurable outcome

The repository is now considered complete for its present purpose. Development is frozen so that effort can be redirected toward:

1. completing the MSc examinations;
2. successfully executing the primary internship;
3. observing real decision bottlenecks and operational constraints;
4. accumulating evidence before considering a product, service, or venture.

## 8. Conditions for reopening

The project, or a successor built from its logic, should be reopened only when there is credible evidence of all or most of the following:

1. **Recurring problem** — a concrete operational decision problem occurs repeatedly.
2. **Identifiable decision owner** — a team or individual is accountable for the decision.
3. **Usable data** — relevant inputs are available at the moment the decision must be made.
4. **Actionable intervention** — a realistic action can follow the score or recommendation.
5. **Observable outcome** — the effect of the action can be measured after execution.
6. **Economic relevance** — the problem has a material cost, risk, revenue, or service impact.
7. **Evaluation pathway** — historical intervention data, an A/B test, phased rollout, or another credible causal evaluation design is feasible.
8. **Governance compatibility** — confidentiality, compliance, explainability, and operational ownership constraints can be satisfied.

Without these conditions, further technical development would add complexity without increasing evidence.

## Final status

**Case study:** complete  
**Technical scope:** frozen  
**Commercial validation:** not started  
**Next priority:** MSc examinations, internship execution, and structured field observation
