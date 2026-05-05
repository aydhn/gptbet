---
title: Consistency Ledgers Maintenance Runbook
family: consistency_ledgers
owner_role: Principal Alignment Federation Engineer
freshness_window: 90d
---

# Maintenance Runbook

## Adding a New Strategy
1. Create a new class extending `BaseConsistencyLedgerStrategy` in `src/sports_signal_bot/consistency_ledgers/strategies/`.
2. Override the relevant `apply_*_rules` methods to implement the new constraints.
3. Import and add the strategy to `__all__` in `strategies/__init__.py`.
4. Register the strategy in the `STRATEGIES` dictionary in `cli.py`.

## Adding a New Contradiction Family
1. Add the new value to `ContradictionFamily` in `contracts.py`.
2. Update `detect_consistency_contradictions` in `contradictions.py` to identify the new contradiction scenario.
3. Update `classify_contradiction_severity` in `contradictions.py` to assign the appropriate severity (moderate, high, critical).
