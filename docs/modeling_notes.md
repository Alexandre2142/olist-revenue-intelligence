# Modeling Notes

The late-delivery model is trained at order level with `is_late` as the binary target.

The tested model families are:

- Logistic Regression as a transparent baseline.
- Random Forest as a nonlinear benchmark.
- XGBoost as the retained final candidate.

The recommended operating configuration is tuned XGBoost with a threshold of `0.7`.

This threshold should be described precisely. In the current retained artifact, `0.7` behaves as a high-confidence alert threshold: it produces very few positive alerts, with high precision and extremely low recall. That makes it suitable for strict escalation, not for broad coverage of all late-delivery risk.

The output should help operations focus attention, not automatically decide business actions.

The model deliberately excludes review-based and post-delivery variables. Any future feature additions should pass the leakage audit before training.
