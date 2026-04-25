# Centralized Evaluation Architecture

The Evaluation module serves as the quantitative foundation for the Sports Signal Bot. It standardizes the comparison of multiple prediction sources (benchmarks, probabilistic models, raw ML, calibrated ML, ensembles, and stackers) by enforcing a strict "fairness first" policy.

## Why Centralized Evaluation?

Before this module, performance metrics were scattered. Model A might report accuracy on a 2000-event validation set, while Model B reported log loss on a 1500-event set. A centralized system ensures:
1. **Apples-to-Apples Comparisons**: The system guarantees models are evaluated on the exact same universe of events (`same_sample_only=True`).
2. **Consistent Metric Definitions**: Log loss, Brier score, and accuracy are calculated using exactly the same underlying logic.
3. **Auditability**: Every evaluation run produces a manifest, detailing exactly what was compared, the common universe size, and the configuration.

## Core Concepts

### Common Universe Alignment
The cornerstone of fairness. Before calculating any metrics, the evaluation pipeline intersects the `event_id` sets of all prediction sources being evaluated. Models are then evaluated *only* on this overlapping subset.

### Metric Taxonomy
- **Probabilistic**: Log Loss (primary), Brier Score, Average Confidence, Average Entropy.
- **Classification (Binary)**: Accuracy, Precision, Recall, F1, ROC AUC.
- **Classification (Multiclass)**: Accuracy, Macro F1, Weighted F1.

### Leaderboard Construction
Produces an ordered ranking of models. Configurable primary (e.g., `log_loss`) and secondary (e.g., `brier`) sorting metrics. Emits warnings if a model's coverage rate drops below thresholds.

### Pairwise Comparison
Provides an event-level head-to-head analysis of two prediction sources. Calculates delta log loss and determines which model was strictly "better on the common universe."

### Segment and Confidence Analysis
Slices performance metrics:
- **Segments**: Evaluates model performance partitioned by `sport`, `market_type`, `source_family`, etc.
- **Confidence Buckets**: Bins predictions by confidence (max predicted probability) to empirically evaluate calibration quality.

## Future Extension Path
- **Statistical Significance Tests**: Paired t-tests for loss metrics.
- **Regret Analysis**: Quantifying theoretical profit left on the table.
- **Profit-Aware Overlays**: Evaluating predictions via a backtester overlay to translate log loss into ROI.
