# Dynamic Weighting Architecture

## Why Weighting After Source Selection?
In Phase 15, the Source Selection layer determines which sources are *eligible* for a given event/market. However, not all eligible sources are created equal. The dynamic weighting layer assigns context-aware weights to these sources, transitioning from a binary "include/exclude" to a soft, continuous weighting scale.

## Component-Based Weighting
The weight for each source is determined by an explainable, additive scoring system consisting of:
- **Base Prior**: Derived from source family and market type.
- **Trust Component**: Derived from Phase 15 historical trust scores.
- **Regime Fit**: Reflects how well the source performs in the current specific regime.
- **Disagreement Penalty**: A mild penalty for sources that diverge heavily from the peer consensus.
- **Recency/Stale Penalty**: Decreases weight if the source or its calibration is stale.
- **Health Component**: Adjusts based on recent operational health.
- **Calibration Bonus**: A small bonus if the source is actively calibrated.

## Balance: Trust + Regime + Disagreement
The hybrid strategy balances these factors. Trust is the stable anchor, while regime fit provides context-aware adjustments. Disagreement acts as a mild regulator, preventing over-reliance on outlier predictions unless their trust score strongly justifies it.

## Caps, Floors, and Numerical Safety
All weights are subject to normalization, with configured `min_weight_floor` and `max_weight_cap` to ensure no single source dominates completely (unless it's the only eligible source), and no source is zeroed out if it passed eligibility.

## Ensemble Integration
The weighting layer runs before the `DynamicWeightedAverageEnsembler`, outputting `DynamicWeightRecord` metadata that the ensembler reads to combine probabilities.

## Future Extension Paths
- **Optimizer-Tuned Weights**: Learning component weights via an optimizer.
- **Online Adaptation**: Updating weights incrementally per event result.
- **Bayesian Confidence Blending**: Moving beyond additive scores to true variance-weighted blending.
