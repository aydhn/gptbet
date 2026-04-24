# Ensemble Architecture (Phase 10)

## Purpose
The Ensemble layer is responsible for combining heterogeneous prediction sources (benchmarks, probabilistic models, raw ML, and calibrated ML) into a single, reliable probabilistic forecast. This serves as the meta-prediction backbone before generating actionable signals.

## Why Do We Need an Ensemble Layer?
We have multiple models predicting the same outcomes:
- Naive Benchmarks (Random, Uniform, Majority)
- Bookmaker-Implied Probabilities
- Elo/Rating Benchmarks
- Sport-specific Probabilistic Cores (Football Poisson, Basketball Structural)
- ML Models (Raw and Calibrated)

Rather than picking a single model, we want to:
1. Smooth out individual model variance.
2. Fall back gracefully if a preferred model fails.
3. Leverage domain-specific rules (e.g., trust Poisson more for totals, ML more for moneyline).

## Source Standardization
Before combining, all sources are converted to a `StandardizedPredictionRecord`. This common contract ensures every input has:
- `event_id`, `sport`, `market_type`
- `class_labels`, `probabilities`
- `source_family`, `source_name`, `is_calibrated`

## Class Alignment Problem
Different models might output different class orders or partial classes (e.g., a model might only predict "1" and "2" but miss "X"). The ensemble layer forces alignment to a reference class order. Missing classes are safely filled with 0.0 probability.

## Weighting and Reliability
- **Simple Average**: Uniformly weights all eligible sources.
- **Weighted Average**: Uses static configuration weights.
- **Reliability Weighted**: Dynamically derives weights based on out-of-sample metrics (Log Loss, Brier Score) passed via a reliability table.

## Calibrated Preference Policy
A core rule: "If a calibrated version of a model exists, prefer it over the raw version."
Modes supported: `prefer_calibrated`, `calibrated_only`, `raw_only`, `all`.

## Disagreement Diagnostics
For every ensemble output, we generate diagnostics to feed downstream meta-learning:
- `entropy`: Uncertainty of the final distribution.
- `max_disagreement`: Fraction of models disagreeing on the top class.
- `source_variance`: Mean probability variance across sources.

## Future Extension Path
Phase 10 builds the API and simple combining logic. Future phases (11+) can easily plug into this by replacing `SimpleAverage` with Stacking Regressors, Bayesian Model Averaging (BMA), or dynamic market-specific optimizers.
