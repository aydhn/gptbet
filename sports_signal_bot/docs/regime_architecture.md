# Regime Architecture

This document describes the structure and usage of the Regime phase (Phase 14) within the sports signal bot platform.

## Why Regimes Matter
Instead of relying on a single, global evaluation metric, real-world models and strategies perform differently under various conditions (e.g., highly volatile markets vs. clear favorites, early season vs. late season). The regime layer brings this concept to life as a first-class citizen, systematically segmenting model predictions and strategy behavior by objective condition profiles.

## Multi-Axis Regime Taxonomy
Our design acknowledges that a single event can belong to multiple regimes simultaneously. Hence, we evaluate regimes across multiple independent axes ("families"):

- **Form**: Recent team performance (e.g., both hot, mixed form).
- **Market Disagreement**: Measures how much our sources diverge in their probabilities.
- **Volatility/Uncertainty**: Measured by prediction entropy (e.g., highly uncertain games).
- **Data Quality**: Captures how complete our features and sources are.
- **Schedule**: Tracks rest days and fixture congestion.
- **Season**: Early, mid, and late season phases.
- **Performance (Period-level)**: Tracks stability and performance trends (e.g., degrading, recovering) across research windows.

## Event vs Period Regimes
- **Event-Level**: Determined immediately before a match begins. Only utilizes data available at that time (e.g., form, pre-match market disagreement, current season progress).
- **Period-Level**: Derived from historical performance over past periods. Useful for research planning, monitoring model drift, or triggering retraining events.

## Sample-Size Awareness
Every regime includes coverage statistics. Analyzing a regime with only 5 events can be misleading. Guardrails are in place to warn or filter when a regime sample size falls below configured thresholds (`minimum_rows_per_regime`).

## Integration with Evaluation and Research
Regimes plug seamlessly into the evaluation system. Using `evaluate_with_regime_filter`, you can generate leaderboards or pairwise comparisons scoped entirely to a specific regime context (e.g., "Which model performs best under High Source Disagreement?").

## Future Extension Path
- **Regime-Aware Weighting**: Adjusting ensemble weights based on the current regime.
- **Regime-Conditioned Stackers**: Stacker models that take regime labels as features.
- **Dynamic Refresh Triggers**: Triggering research, retrains, or recalibrations when entering "degrading" or "unstable" regimes.
