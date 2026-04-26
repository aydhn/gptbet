# Threshold Optimization Architecture (Phase 18)

## Why Thresholding After Signal Scoring?

The Signal Scoring Engine (Phase 17) evaluates the confidence, uncertainty, and edge of predictions, producing a continuous signal score. However, not every signal is worth acting on. Threshold optimization is the necessary intermediate layer that converts continuous scores into discrete decisions (accept/reject) based on market-specific trade-offs between coverage (how many signals we accept) and quality (how accurate or profitable those signals are).

Without a thresholding layer, downstream systems (like a policy engine or bankroll manager) would have to make ad-hoc decisions. This layer formalizes the decision boundary using out-of-sample optimization.

## Precision vs Coverage Tradeoff

In quantitative systems, there is an inherent trade-off:
- High thresholds lead to high precision but low coverage (too few signals to be operationally viable).
- Low thresholds lead to high coverage but lower average precision/edge (too much noise).

The Threshold Optimization layer formalizes this by creating a **Frontier**, allowing the system to pick a point that satisfies predefined constraints (e.g., minimum coverage) while maximizing an objective (e.g., average edge or accuracy).

## Frontier / Sweep Logic

The sweep engine operates as follows:
1. **Grid Generation:** Produces a set of candidate thresholds (e.g., score from 0.0 to 1.0 in increments of 0.05).
2. **Evaluation:** For each candidate, it applies the threshold to the out-of-sample signal records, splitting them into `accepted` and `rejected` sets.
3. **Metric Calculation:** It computes coverage, average edge, log loss, precision, etc., for the `accepted` set.
4. **Objective & Constraint Checking:** It calculates the objective value (e.g., a balanced metric of accuracy and coverage) and verifies constraints (e.g., minimum accepted count > 10).
5. **Selection:** The candidate that maximizes the objective while passing constraints is selected to form the `ThresholdPolicy`.

## Objective and Constraint Design

- **Objectives:** `precision_oriented`, `probabilistic_quality`, `balanced`, `edge_aware`, `conservative`.
- **Constraints:** Minimum coverage rate, minimum accepted count, maximum uncertainty penalty, maximum log loss.

These are entirely config-driven.

## Market-Specific Threshold Policies

Football 1x2 behaves differently than Basketball Totals. Therefore, threshold optimization is run per-market. The resulting `ThresholdPolicyRecord` is specific to `sport` and `market_type`, ensuring that difficult markets can have stricter thresholds than highly predictable ones.

## Future Extension Path

This phase leaves explicit hooks for future phases:
- **Regime-Specific Thresholds (Phase 14 integration):** Applying tighter thresholds during high-volatility regimes.
- **Bankroll-Aware Tuning:** Adjusting thresholds based on current bankroll drawdown.
- **Online Threshold Adaptation:** Dynamically shifting thresholds as recent market efficiency changes.
- **Policy Engine (Next Phase):** Consuming the `SelectivePredictionRecord` to trigger actual operational actions.
