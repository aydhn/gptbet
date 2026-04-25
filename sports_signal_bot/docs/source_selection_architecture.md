# Source Selection Architecture

## Why Source Selection Before Weighting?

In a robust forecasting system, not all sources are equally reliable at all times. A model might be highly accurate historically but currently operating on stale data, or a source might perform exceptionally well in regular seasons but poorly during playoffs (regimes).

By evaluating eligibility *before* assigning weights in an ensemble or stacker:
1.  **Reduces Noise:** We prevent the downstream models from having to learn to ignore broken or extremely stale sources.
2.  **Improves Transparency:** We can explicitly explain *why* a source was not used (e.g., "Model age > 30 days").
3.  **Enhances Safety:** We guarantee that critical events always have *some* fallback source, even if the primary models fail to meet quality thresholds.

## Trust Score Components

The Trust Score is a normalized value (0.0 to 1.0) calculated from:

*   **Performance (30%):** Based on recent log loss, brier score, and benchmark-relative performance.
*   **Recency (20%):** Penalizes models that haven't been retrained or calibrated recently. Stale flags immediately zero this component.
*   **Coverage (20%):** Rewards sources that consistently provide predictions for the required markets.
*   **Regime Fit (20%):** Evaluates historical performance specifically within the regimes active for the current event (dampened for low sample sizes).
*   **Data Quality (10%):** Penalizes sources producing invalid probabilities (NaNs) or exhibiting upstream data issues.

## Eligibility Policies

The decision to include a source is governed by a chain of policies:

1.  **BasicAvailabilityPolicy:** Checks if a prediction actually exists and contains valid probabilities.
2.  **QualityThresholdPolicy:** Enforces minimum standards (e.g., `min_trust_score`, `max_model_age_days`).
3.  **RegimeAwarePolicy:** Can explicitly exclude sources with extremely poor historical performance in the active regimes.
4.  **PreferredCalibratedPolicy:** If a calibrated version of a source family exists, it drops the uncalibrated (raw) versions to avoid redundancy.
5.  **FallbackSafetyPolicy:** Ensures a minimum number of sources are eligible. If not, it attempts to "rescue" priority fallback sources.

## Exclusion Taxonomy

Standardized reasons for why a source was rejected:
*   `source_unavailable`
*   `invalid_probabilities`
*   `low_trust_score`
*   `insufficient_recent_coverage`
*   `stale_model`
*   `low_regime_evidence`
*   `replaced_by_calibrated_variant`

## Future Extension Paths

*   **Dynamic Routing:** Routing specific events to entirely different pipeline branches based on the eligibility profile.
*   **Cost-Aware Selection:** Factoring in the computational or API cost of querying a source against its expected value.
*   **Live Source Health Monitoring:** Real-time dashboards monitoring the trust scores of sources across the system.
