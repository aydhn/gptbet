# Sports Signal Bot

A modular, extensible, and scalable sports forecasting and signal bot built in Python. Designed to be a foundation for building complex, predictive models for football and basketball, with strong emphasis on local execution, open-source tools, and solid software engineering practices.

## Project Scope (Phase 1)
This repository represents Phase 1 of the development.

### What is done:
- Created the core project structure, packaging and dependency rules.
- Set up a clean configuration management system using `pydantic-settings`.
- Established a structured logging and exception handling base.
- Defined abstract base classes (interfaces) for data providers, features, models, notifications and orchestration.
- Created mock implementations for data providers and features to prove the architecture.
- Developed a "smoke" pipeline runner that simulates fetching data, processing features, making dummy predictions, and notifying.
- Added basic test coverage to ensure the skeleton is robust.

### What is NOT done:
- No real betting APIs integrated yet.
- No heavy ML models or training loops implemented.
- No web interface, dashboard, or browser automation.
- No live Telegram bot (only a mock stub is included).

## Installation

1. Ensure you have Python 3.11+ installed.
2. Clone the repository and navigate into the `sports_signal_bot` directory.
3. Create a virtual environment (optional but recommended):
   ```bash
   # python3 -m venv venv
   # source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install the package (including dev dependencies):
   ```bash
   pip install -e .[dev]
   ```
5. Copy the `.env.example` file to create your local `.env`:
   ```bash
   cp .env.example .env
   ```

## Usage

You can interact with the bot using the built-in CLI powered by Typer.

### Run the Smoke Pipeline
```bash
python -m sports_signal_bot.main smoke-run
```

### View Configuration
```bash
python -m sports_signal_bot.main show-config
```

### View Project Paths
```bash
python -m sports_signal_bot.main paths
```

## Running Tests
To ensure everything is working correctly, run the tests using `pytest`:
```bash
pytest tests/
```

## Future Phases Roadmap
- Integrate real schedule and odds APIs via the Provider interfaces.
- Build extensive feature engineering pipelines for football and basketball.
- Introduce scikit-learn / tree-based models and proper train/eval loops.
- Develop backtesting and benchmark engines to measure success using metrics beyond basic accuracy (e.g., log loss, calibration).

## Phase 2: Data Backbone
This phase introduced the core data backbone.

**Purpose**: To create a provider-agnostic, testable, expandable data ingestion layer to handle football and basketball data.
**Data Providers**: Supports file-based local ingestion (`FileProvider`) and deterministic mock generation (`MockProvider`). The architecture supports easy additions of free/open API adapters.
**Why no scraping?**: Web scraping is fragile. We strictly use structured data (APIs, CSVs, JSONs).
**Usage**:
- `python -m sports_signal_bot.main ingest-samples --sport football`
- `python -m sports_signal_bot.main validate-samples --sport football`

**Storage Layout**: Data lands in `data/raw/` first, gets normalized and validated to `data/processed/`, and run metadata goes to `data/processed/manifests/`.
**Alias Resolution**: Uses a YAML map (e.g. `team_aliases.sample.yaml`) to normalize differing provider team names into our canonical naming schema.
**Validation Summary**: You can view validation issues (e.g., duplicated events, missing fields, weird odds) in the generated manifest files or via the CLI command `validate-samples`.

## Phase 3: Markets, Labels, and Benchmark Engine
This phase introduced the core outcome resolution and benchmark system.

**Purpose**: To rigorously define what the model predicts, how to resolve outcomes (settlement), and how to generate deterministic canonical labels. It also establishes naive and bookmaker-implied baselines.
**Market Universe**: Supports definitions for 1X2, Over/Under, BTTS for football, and Moneyline, Spreads, Totals for basketball.
**Label Generation**: Deterministically generates labels (e.g., `football_ou_2_5`) from event results and market definitions.
**Benchmarks**: Provides a factory to evaluate models against Random, Uniform, Majority, and Bookmaker-Implied baselines.
**Leakage Guardrails**: Includes audit methods to detect post-event odds snapshots preventing data leakage during training and benchmark generation.
**Usage**:
- `python -m sports_signal_bot.main list-markets --sport football`
- `python -m sports_signal_bot.main generate-labels --sport football`
- `python -m sports_signal_bot.main run-benchmark-preview --sport football --market football_1x2`
- `python -m sports_signal_bot.main audit-leakage --sport football`

## Phase 4: Feature Engineering
This phase implemented the feature engineering backbone to convert raw data into learning-ready signals.

**Purpose**: To build a leakage-safe, extensible, and reproducible feature factory.
**Architecture**:
- Uses a `FeatureRegistry` to manage plugin-style `FeatureBuilder`s.
- `FeatureFactory` and `FeatureSetAssembler` orchestrate building and safely joining columns.
- Generates `FeatureManifestRecord` to track data lineage, ensuring model reproducibility.
**Guardrails**: Includes utilities for event-time safe rolling calculations and strictly pre-match odds snapshot selection.
**Usage**:
- `python -m sports_signal_bot.main list-feature-builders --sport football`
- `python -m sports_signal_bot.main build-features --sport football`
- `python -m sports_signal_bot.main preview-feature-matrix --sport basketball`

## Phase 5: Rating Engine
This phase introduced the temporal rating infrastructure for teams.

**Purpose**: Establish a robust, leakage-free strength estimation layer.
**Architecture**:
- Implements Elo Rating algorithms adapted for Football (draw-aware) and Basketball (margin-aware).
- Enforces strict Pre-Event Snapshot discipline for ML feature integrity.
- Extensible to future Bayesian updates.
**Usage**:
- `python -m sports_signal_bot.main build-ratings --sport football`
- `python -m sports_signal_bot.main preview-ratings --sport football`
- `python -m sports_signal_bot.main preview-rating-features --sport football`

## Phase 6: Football Probabilistic Core
Implemented a structural Poisson-based goal distribution model. Instead of directly predicting 1X2 outcomes, the system now models expected goals ($\lambda$) and generates an independent Poisson score matrix. From this matrix, consistent probabilities for 1X2, Over/Under, BTTS, and correct scores are deterministically extracted. This serves as the structural baseline for future Dixon-Coles integration, calibration, and ensembling. See `docs/football_probabilistic_core.md` for details.

## Phase 7: Basketball Probabilistic Core
Implemented a structural, normal-approximation based probabilistic engine for basketball markets. Instead of simulating possessions or relying on Poisson grids, it models expected points via pace and efficiency metrics, applying Gaussian variance to determine probabilities for Moneyline, Totals, and Spreads.
**Usage**:
- `python -m sports_signal_bot.main preview-basketball-model`
- `python -m sports_signal_bot.main preview-basketball-market --market moneyline`
- `python -m sports_signal_bot.main preview-basketball-market --market total_220_5`
- `python -m sports_signal_bot.main preview-basketball-diagnostics`
See `docs/basketball_probabilistic_core.md` for details on sign conventions and the normal approximation model.

## Phase 9: Probability Calibration
This phase introduced a robust probability calibration layer to ensure model outputs are reliable and trustworthy before being passed to downstream signal generation.

**Purpose**: To transition from raw predictions to calibrated probabilities using rigorous, out-of-sample techniques.
**Architecture**:
- Separate calibration layer (`CalibrationRunner`) that operates strictly on `ValidationPredictionRecord`s to prevent data leakage.
- Supports both Binary (Sigmoid, Isotonic) and Multiclass (One-Vs-Rest Wrapper) calibration.
- Generates `ReliabilityBinRecord`s and computes ECE (Expected Calibration Error) to quantify calibration quality.
- Produces a comprehensive `CalibrationRunManifest` comparing raw vs. calibrated metrics.
**Usage**:
- `python -m sports_signal_bot.main list-calibrators`
- `python -m sports_signal_bot.main run-calibration --sport football --market ou_2_5 --method binary_sigmoid`
- `python -m sports_signal_bot.main preview-reliability --sport football --market ou_2_5`
See `docs/calibration_architecture.md` for details.

## Phase 10: Ensemble Architecture
This phase added a robust meta-prediction layer to combine heterogeneous sources (benchmarks, probabilistic models, ML models) into a unified probability forecast.

**Purpose**: To move from single-model output to a combined, reliable signal. It handles class-order alignment, calibration preference, and missing source fallbacks.
**Architecture**:
- Establishes a common `StandardizedPredictionRecord`.
- Ensembler strategies: `simple_average`, `weighted_average`, `reliability_weighted`, `best_source_fallback`, `rule_based_hybrid`.
- Configurable policies to prefer calibrated predictions over raw ones.
- Generates rich diagnostic metadata (entropy, top class disagreement, variance).
**Usage**:
- `python -m sports_signal_bot.main preview-ensemble-sources --sport football --market 1x2`
- `python -m sports_signal_bot.main list-ensemblers`
- `python -m sports_signal_bot.main run-ensemble football 1x2`
- `python -m sports_signal_bot.main run-ensemble football ou_2_5 --ensembler weighted_average`
See `docs/ensemble_architecture.md` for details.

## Stacker Layer (Phase 11)
The **Stacker Layer** elevates the ensemble architecture by moving from heuristic rule-based combination to a learning-based stacker model. It gathers out-of-fold (OOF) predictions from various base models, standardizes them, and trains meta-models (like Logistic Regression or Gradient Boosting) to learn how to best combine signals.

Crucially, **OOF integrity is non-negotiable**—the stacker avoids temporal data leakage by only learning from predictions that were out-of-sample for the base models.

CLI Commands:
- `python -m sports_signal_bot.main build-meta-dataset --sport football --market 1x2`
- `python -m sports_signal_bot.main run-stacker --sport football --market 1x2 --model meta_logistic`
- `python -m sports_signal_bot.main preview-source-coverage --sport football --market 1x2`
- `python -m sports_signal_bot.main list-stackers`

For more details on the architecture, fallback strategies, and feature design, see `docs/stacker_architecture.md`.

## Phase 12: Centralized Evaluation
The repository now includes a centralized evaluation runner. It is designed to compare prediction outputs (from benchmark, ML, calibrated, ensemble, and stacker layers) fairly.
Key features:
* **Same-Sample Fairness**: By default, models are strictly evaluated on the exact overlapping set of events.
* **Leaderboards and Pairwise Comparisons**: Automatically generates ranked leaderboards and detailed head-to-head comparisons.
* **Confidence Bucket Analysis**: Bins predictions by confidence to assess calibration and empirical win rates.
* **Segments**: Supports slicing metrics by sport, market type, or source family.
* **CLI Commands**: `run-evaluation`, `preview-leaderboard`, `preview-pairwise`, `preview-confidence-buckets`, `list-evaluation-metrics`

## Regimes

The Regime layer allows systematic segmentation of model performance and behavior across varying conditions (e.g., source disagreement, season phase, team form).

- **Event-Level Regimes**: Assessed per game, completely prior to start time.
- **Period-Level Regimes**: Assessed per time period, looking at model stability and degradation.

**Usage:**
```bash
python -m sports_signal_bot.main assign-regimes --sport football --market 1x2
python -m sports_signal_bot.main preview-regime-coverage --sport football --market 1x2
python -m sports_signal_bot.main preview-period-regimes --sport basketball --market moneyline
python -m sports_signal_bot.main list-regime-families
```

Regime analysis produces coverages and evaluation metrics scoped to context, essential for subsequent optimization and dynamic weighting.

## Phase 15: Source Selection Engine

The Source Selection Engine acts as a gatekeeper before the ensemble/stacker layers. Instead of blindly blending all available predictive sources, this phase implements an intelligent, event-based eligibility evaluation.

Key features:
- **Trust Scoring:** Evaluates sources based on historical performance, recency (staleness), coverage, regime fit, and data quality.
- **Eligibility Policies:** Configurable rules (`BasicAvailability`, `QualityThreshold`, `RegimeAware`, `PreferredCalibrated`, `FallbackSafety`) determine if a source should be included for a specific event.
- **Regime-Aware:** Adapts trust based on how well a source performs in the specific regimes active for an event, with dampening for low sample sizes.
- **Standardized Exclusions:** Every exclusion is logged with a taxonomy of reasons (e.g., `stale_model`, `low_trust_score`) for transparency.
- **Reporting & Manifests:** Generates CSV and JSON artifacts detailing the selection decisions, trust scores, and exclusion reasons.

Use `python -m sports_signal_bot.main list-source-policies` and `select-sources` commands to interact with this layer.

## Phase 17: Signal Scoring Engine
This phase transforms final probabilities from the ensemble/stacker layers into operational, risk-aware signal scores. It computes market edges and applies sophisticated penalties for uncertainty, source disagreement, and poor data quality to rank and tier signals for actionable use. Note that this phase focuses entirely on signal quality and does not involve staking or bankroll management.

## Phase 18: Threshold Optimization

This phase elevates the system from producing continuous signal scores to making discrete, operationally-viable selection decisions via selective prediction.

**Purpose**: To systematically optimize the trade-off between coverage (quantity) and signal quality (precision, edge, log loss). It establishes out-of-sample data-driven boundaries to determine which signals are truly actionable.
**Architecture**:
- Implements a Sweep Engine that iterates over a threshold grid.
- Uses `ObjectiveEvaluator` and `ConstraintEvaluator` to balance metrics like log loss, precision, and edge.
- Supports multiple strategies: `score_only`, `score_and_edge`, `conservative_quality`, `coverage_balanced`.
- Exports a `ThresholdFrontierRecord` to visualize trade-offs and selecting the best point matching the constraints.
- Generates accepted vs. rejected signal sets with explicit rejection reasons.
- **Note**: This phase intentionally avoids stake sizing or bankroll management, deferring those strictly to the bankroll layer.

**Usage**:
- `python -m sports_signal_bot.main list-threshold-strategies`
- `python -m sports_signal_bot.main optimize-thresholds --sport football --market 1x2`
- `python -m sports_signal_bot.main preview-threshold-frontier --sport football --market 1x2`
- `python -m sports_signal_bot.main preview-accepted-signals --sport football --market ou_2_5`
- `python -m sports_signal_bot.main preview-threshold-policy --sport basketball --market moneyline`

See `docs/threshold_optimization_architecture.md` for architectural details.

## Phase 19: Policy Engine & No-Bet Zone
The system incorporates a robust Policy Engine layer.

- **Purpose**: Act as a quantitative decision gate between signal scoring/thresholding and actual bet sizing/dispatching.
- **Signal Status Lifecycle**: Defines a strict state machine (`scored` -> `candidate` -> `approved` or `no_bet_zone`).
- **No-Bet Zone**: A core philosophy. The system explicitly tags signals that are decent but have high uncertainty, disagreement, or borderline edge as `no_bet_zone`.
- **Action Classes**: Maps signal statuses to final action categories like `approved_candidate`, `watchlist`, and `no_action`.
- **Apply Policy**: `python -m sports_signal_bot.main apply-policy --sport football --market 1x2`

### Backtest Engine
A chronological backtest replay engine evaluates the policy engine decisions chronologically over time. This implements a decision-quality-only backtest approach allowing the performance evaluation of specific subset action classes (executed vs skipped vs void) before adding stake sizes or full capital overlay strategies.
Run it using:
```bash
python -m sports_signal_bot.main run-backtest --sport football --market 1x2
```

## Bankroll Overlay Engine (Phase 21)
The bankroll overlay layer sits on top of backtest evaluation to translate decision quality into capital curves, using test overlays like flat staking or fixed fractions.

It provides functionality for:
- Tracking capital growth via `CapitalCurveBuilder`.
- Evaluating peak-to-trough performance via `DrawdownAnalyzer`.
- Exposing simple CLI commands (`run-bankroll`, `preview-capital-curve`) to review strategies.

**Note:** This layer provides *research-grade* placeholders. Future phases will introduce concurrency handling and Kelly-optimized fractional betting.
\n## Phase 22: Advanced Sizing Engine\nBuilt an advanced, risk-aware stake sizing engine supporting Kelly variants, confidence dampening, and drawdown throttles. See `docs/advanced_sizing_architecture.md`.

## Phase 23: Portfolio Allocation & Exposure Management
This system incorporates a robust portfolio layer acting **after** the event-level sizing engine.
While the sizing engine finds the optimal stake for a single decision, the portfolio layer ensures safety across *many* decisions.

- **Daily Risk Budget**: Limits the absolute percentage of the bankroll exposed in a single day.
- **Run Portfolio**: Use `python -m sports_signal_bot.main portfolio run-portfolio --sport football --market 1x2` to see it in action.
- **Concentration & Correlation Guardrails**: Employs placeholders to cap heavy exposure in a single sport/market, and prevents double-dipping on highly correlated markets within the exact same event.

## Phase 25: Telegram Dispatch Layer

The Telegram Dispatch layer acts as the operator-facing interface, translating inference output (decision and review packets) into operator-friendly messages.

**Key features:**
- Separates messages logically into routing channels (decisions, review queue, summaries, warnings, alarms)
- Prevents spam via noise control and duplicate suppression window
- Enables operator review queue workflow for uncertain but high-potential bets
- Safe dry-run previews without active Telegram sending
- Retries on transient delivery failures
- Config-driven (channels, noise limits, routing rules)
