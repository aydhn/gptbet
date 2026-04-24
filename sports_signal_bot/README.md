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
