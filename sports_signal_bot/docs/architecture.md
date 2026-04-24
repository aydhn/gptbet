# Architecture Notes

## Package-First Design
The project is structured as an installable Python package (`src/sports_signal_bot`). This prevents path manipulation issues, encourages clean absolute imports, and prepares the code for distribution or deployment on modular platforms without relative import spaghetti.

## Interface-Based Design
The core components (Data Providers, Feature Builders, Models, Notifiers) are heavily reliant on Abstract Base Classes (ABCs) and Protocols. This ensures that when we shift from `MockScheduleProvider` to a real API provider in future phases, the underlying logic in `SmokeRunner` (or its future equivalents) remains unchanged.

## Mock-First Smoke Pipeline
By implementing mock versions of our interfaces, we can build the orchestration layer (the runner) first. This proves that data flows correctly from fetching -> feature engineering -> prediction -> notification, without getting bogged down by rate limits, real API keys, or large dataset downloads during the foundation phase.

## No Scraping Rule
The system strictly prohibits HTML/DOM scraping. Relying on scraping causes high technical debt, brittle data pipelines, and maintenance nightmares when site layouts change. We will strictly use structured API endpoints or static data files.

## Notifier-First instead of Dashboard
Developing web dashboards (e.g., Streamlit, React) introduces a whole new paradigm of maintenance (hosting, auth, frontend code). For a low-budget, local-first predictive tool, pushing signals directly to a messaging platform (Telegram) is much faster, more actionable, and easier to maintain.

## Extensibility (Regimes, Optimizers, Backtests)
The folder structure already contains placeholders for `regimes/`, `optimizer/`, `backtest/`, and `benchmark/`. While currently empty or minimally populated, this structure acts as a blueprint. Future phases will drop concrete classes into these namespaces without altering the core module hierarchy.
