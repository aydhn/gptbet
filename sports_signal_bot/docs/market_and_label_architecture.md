# Market & Label Architecture

## Overview
This document describes the foundational logic for what the models in this system actually predict, how to evaluate those predictions, and how we protect against data leakage.

## Market Taxonomy
We use a canonical registry for all markets.
Instead of dealing with strings like `O/U 2.5` or `Match Winner`, we define canonical ExtendedMarketType enums (e.g., `FOOTBALL_OVER_UNDER`, `BASKETBALL_MATCH_WINNER`).
Each market is registered with its specific settlement rules, required inputs, and whether it supports multiple lines or push outcomes.

## Label Validity Lifecycle
Labels are not just values. They have statuses:
- **VALID**: Fully resolvable.
- **VOID**: e.g., a push on an integer handicap, or a cancelled match.
- **INVALID**: The event is finished, but required fields (like score) are missing.
- **PENDING**: The event has not finished yet.
- **UNSUPPORTED**: The settlement rule hasn't been written yet.

This lifecycle ensures the model is never trained on noisy or incorrectly resolved data.

## Settlement Rules
All settlement logic uses pure functions inside `resolvers.py`.
They take an `EventResultRecord` (and an optional line) and output the resolved class string, the validity status, and an error reason if applicable.

## Benchmark Framework
Before training complex models, we establish robust baselines:
1. **Random / Uniform**: Baseline metrics for log-loss and accuracy.
2. **Majority Class**: To ensure the model learns more than just class imbalance.
3. **Bookmaker-Implied**: The strongest benchmark. We map the latest pre-match snapshot into probabilities. If the ML model can't beat this, it doesn't have an edge.
4. **Simple Rating**: A placeholder for future Elo/Glicko baselines.

## Leakage Risks and Pre-Match Snapshots
Data leakage is the death of betting models. We enforce strict guardrails:
- Label data relies *only* on `result_timestamp_utc`.
- Benchmark generation and feature engineering must *only* use snapshots where `snapshot_ts_utc <= event_start_time_utc`.
- The `audit/leakage.py` module strictly flags any event where odds snapshots occur after the match begins.

## Why Build This Now?
Defining the benchmark and label resolution early forces discipline. It ensures that when we write the ML training loops in Phase 4+, the inputs (features) and the targets (labels) are cleanly separated by the event start time boundary, and our definition of "success" is anchored to beating real baselines.
