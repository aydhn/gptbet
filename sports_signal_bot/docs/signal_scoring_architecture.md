# Signal Scoring Architecture (Phase 17)

## Overview
Phase 17 introduces the Signal Scoring engine, a critical layer that transitions the system from producing raw probability estimates (via the Ensemble/Stacker layers) to generating operational, risk-aware signal scores. It evaluates the "edge" while heavily incorporating confidence, uncertainty, disagreement, data quality, and source health metrics.

## Why Signal Scoring After Ensemble/Stacker?
While the Stacker produces highly calibrated final probabilities, a raw probability difference (Edge) is insufficient for making robust decisions. A 5% edge derived from highly disagreeing models on sparse data is far riskier than a 3% edge derived from unanimous consensus on complete data. The Signal Scoring layer formalizes this distinction by creating explainable, bounded signal components.

## Core Components

### 1. Edge Computation
The primary driver of value. It is the difference between our final calibrated probability and the market-implied probability (normalized for overround).

### 2. Confidence and Uncertainty
- **Confidence**: Derived from the magnitude of the predicted probability, the gap to the next most likely class, and the overall sharpness (inverse entropy) of the distribution.
- **Uncertainty Penalty**: Applied when the output distribution is unusually flat (high entropy) or when underlying sources exhibit unstable behavior.

### 3. Disagreement and Data Quality Penalties
- **Disagreement**: Penalizes signals where underlying sources have high variance or disagree on the top predicted class.
- **Data Quality & Source Health**: Penalizes signals built on sparse history, high ratios of missing features, or reliance on stale/weak source components.

### 4. Regime-Aware Adjustment
A bounded modification applied based on Regime (Phase 14) labels. For instance, a "high data completeness" regime might provide a slight boost, while a "congested schedule" regime might induce a penalty.

## Ranking and Status Lifecycle
Signals are not just scored; they are evaluated against thresholds and given a status (`SCORED`, `WEAK_SIGNAL`, `NO_MARKET_REFERENCE`, `INVALID`, etc.). Valid signals are then ranked into tiers (S, A, B, C) based on the final score and tie-breaking metrics like raw edge and confidence.

## Future Extension Paths
This architecture acts as the immediate precursor to:
- **Threshold Optimization**: Finding the optimal score cutoffs to maximize simulated yield.
- **Bankroll Overlays & Policy Engine**: Translating signal ranks and tiers into discrete staking allocations.
- **Backtesting Engine**: Validating the signal score effectiveness over historical holdout datasets.
