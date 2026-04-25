# Research Protocol Architecture (Walk-Forward)

## Why Walk-Forward over One-Shot Evaluation?
One-shot evaluation randomly shuffles data into train and test splits, destroying the temporal order. In sports forecasting, the information available strictly progresses linearly. Walk-forward testing prevents temporal leakage and gives a realistic view of how the model would perform in production as it retraining on expanding or rolling data windows.

## Scenario Definition
A Research Scenario defines everything required to run a backtest simulation:
- Time window controls (train size, calibration size, forward test size).
- The `planning_mode` (rolling vs expanding).
- Which sources/models are enabled.

## Planner and Window Lifecycle
The `WalkForwardPlanner` slices the requested dates into non-overlapping `WindowDefinition` periods. For each period, the orchestrator triggers data assembly, model training, and predictions for that explicit slice.

## Refresh Policies
Refresh policies control computation cost versus recency. We can specify logic such that models retrain every period (`always_retrain`) while calibration or stackers rebuild less frequently (`periodic_retrain`).

## Time-Sliced Reporting
Reporting provides a period-by-period view of degradation and stabilization instead of a single metric. By analyzing metric deltas and confidence shifts across time slices, we can accurately measure model stability.

## Stability and Degradation Flags
The reporting layer includes helpers to flag significant drops in out-of-fold performance or stability shifts, making it easier to diagnose regime changes or broken features over time.

## Future Extension Path
This protocol provides the foundation for:
1. Automated model governance.
2. Scheduled production retraining logic.
3. Live inference scheduling based on similar time windows.
