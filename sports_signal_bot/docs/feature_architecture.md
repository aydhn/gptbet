# Feature Architecture (Phase 4)

This document describes the design and components of the Feature Engineering phase for the Sports Signal Bot.

## Core Concepts

The feature pipeline converts raw tabular data (events, odds, etc.) into a leakage-safe feature matrix.

### Event-Time Aware Engineering
To prevent target leakage, every feature generated must rely strictly on information that was knowable *before* the `event_datetime_utc`. The utilities enforce this by comparing snapshot timestamps and past event times against the target event.

### Feature Registry and Factory
- **BaseFeatureBuilder**: Abstract base class for all plugins. Defines required inputs and expected output columns.
- **FeatureRegistry**: A central registry holding instances of `BaseFeatureBuilder`s. Allows filtering by sport or feature family.
- **FeatureFactory**: Resolves context and active builders, coordinates their execution, and handles failure modes gracefully.
- **FeatureSetAssembler**: Safely merges individual builder outputs into a cohesive matrix, performing validations (e.g., duplicated IDs, row count consistency).

### Missingness and Null Policy
The `apply_null_policy` utility standardizes handling missing data across the pipeline, supporting strategies like `keep_nulls`, `fill_defaults`, and `add_missing_indicators`.

### Manifest and Lineage
Every feature build run produces a JSON manifest detailing:
- Inputs used.
- Active builders.
- Columns produced.
- A summary of missing data (Null Summary).
- `run_id` for deterministic tracing in downstream training loops.

## Sport-Specific Builders
While shared builders (`rolling_form`, `rest`, `market_odds`) operate across all sports, sport-specific dynamics are encapsulated in dedicated modules (e.g., `football_team_strength`, `basketball_tempo`).

## Leakage Guardrails
1. **Snapshots**: `select_feature_snapshot` verifies that `snapshot_time_utc` is strictly less than `event_datetime_utc`.
2. **Rolling**: `calculate_rolling_aggregates` ensures aggregations do not see current or future rows.

## Why this Architecture?
A strict, modular registry prevents the feature code from devolving into a massive, tightly-coupled script. It isolates concerns, makes testing trivial, and provides deterministic builds (manifests) required for robust machine learning models.
