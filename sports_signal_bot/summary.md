### 1. Phase 13 Implementation Summary

I have implemented the Phase 13 Walk-Forward Research Protocol. The system is now capable of translating a high-level research scenario into a fully deterministic time-sliced walk-forward plan.

Key components added:
*   **ResearchScenario & WalkForwardPlan (contracts.py):** Defining start/end dates, expanding vs rolling windows, and refresh frequencies.
*   **WalkForwardPlanner (planner.py):** Translates scenario configurations into explicit train, calibration, and forward-test date windows.
*   **RefreshPolicyResolver (policies.py):** Evaluates whether a base model, calibration layer, ensemble, or stacker needs to be retrained or reused for a given window based on user configuration.
*   **PeriodRunner (period_runner.py):** Mocks the execution of a single period (dataset building, training, evaluating) using the generated window definitions. Includes data sufficiency guards.
*   **TimeSliceReporter & Stability (reporting.py, stability.py):** Tracks log loss and accuracy changes across the sequence of periods. Generates warnings if significant drops in performance occur.
*   **Manifests & Artifacts (manifests.py, artifacts.py):** Persists window-level artifacts and a top-level `ResearchRunManifest` with configuration snapshots and performance arrays.
*   **CLI Orchestration:** Exposed `plan-research`, `run-research`, `preview-time-slices`, and `list-research-scenarios` via Typer.

### 2. File Tree Update
```
sports_signal_bot/
├── configs/
│   └── research/
│       ├── basketball.yaml
│       ├── default.yaml
│       └── football.yaml
├── docs/
│   └── research_protocol_architecture.md
├── src/
│   └── sports_signal_bot/
│       ├── core/
│       │   └── paths.py (updated)
│       ├── main.py (updated)
│       └── research/
│           ├── __init__.py
│           ├── artifacts.py
│           ├── contracts.py
│           ├── manifests.py
│           ├── period_runner.py
│           ├── planner.py
│           ├── policies.py
│           ├── reporting.py
│           ├── runner.py
│           ├── scenarios.py
│           ├── stability.py
│           ├── utils.py
│           └── windows.py
└── tests/
    └── research/
        ├── test_insufficient_data_guard.py
        ├── test_period_metric_deltas.py
        ├── test_period_runner.py
        ├── test_refresh_policies.py
        ├── test_research_manifest.py
        ├── test_research_runner.py
        ├── test_reuse_vs_retrain_logic.py
        ├── test_time_slice_reporting.py
        ├── test_walkforward_planner.py
        └── test_window_generation.py
```

### 3. New and Changed Files (Highlights)
(The exact python content of the research modules have been included correctly in the system). Key logic highlights:
- `policies.py` dynamically computes retrain flags using modulo logic: `(period_id - 1) % freq == 0`.
- `runner.py` ties everything together using `PeriodRunner` to mock OOF outputs, passing them to `TimeSliceReporter` to create the final `time_slice_summary.json`.

### 4. Sample CLI Commands
```bash
python -m sports_signal_bot.main plan-research football 1x2 default
python -m sports_signal_bot.main run-research football ou_2_5 ou_2_5_rolling
python -m sports_signal_bot.main preview-time-slices basketball moneyline default
python -m sports_signal_bot.main list-research-scenarios
```

### 5. Expected Example Output
```
$ python -m sports_signal_bot.main preview-time-slices football 1x2 default
Starting Research Run for football - 1x2
Generating time slices for football - 1x2
Time-Slice Cumulative Leaderboard:
  - logistic_regression: {'log_loss': 0.65, 'accuracy': 0.55}
  - random_forest: {'log_loss': 0.65, 'accuracy': 0.55}
  - ensemble: {'log_loss': 0.63, 'accuracy': 0.57}
```

### 6. Acceptance Checklist
- [x] Walk-forward planner operates deterministically.
- [x] Research scenario definition structure defined.
- [x] Period runner logic scaffolds the execution lifecycle.
- [x] Retrain/recalibration policies respect scenario configs.
- [x] Time-sliced reporting aggregates metrics correctly.
- [x] Insufficient data guardrails are present.
- [x] CLI commands added and functional.
- [x] Unit tests cover all key logic and pass locally.

## Phase 15 Implementation Summary
Successfully implemented the Source Selection Engine according to requirements:
- **Contracts & Models**: Defined source eligibility records, trust score components, exclusion reasons, and summary stats.
- **Trust Scoring**: Implemented `SourceTrustScorer` integrating historical performance, model/calibration recency, market coverage, and regime fit, yielding a normalized score.
- **Policies**: Created `BasicAvailabilityPolicy`, `QualityThresholdPolicy`, `RegimeAwarePolicy`, `PreferredCalibratedPolicy`, and `FallbackSafetyPolicy` executed via `SourcePolicyChain`.
- **Reporting**: Generated `SourceSelectionManifest`, alongside CSV and JSON artifacts for tracking eligibility and trust scores.
- **Ensemble Integration**: Updated `input_builder.py` and `dataset.py` to optionally filter on eligible sources before aggregating predictions.
- **CLI & Configs**: Added Typer commands (`select-sources`, `preview-source-trust`, etc.) and mapped them to configurable rules in `configs/source_selection/`.
