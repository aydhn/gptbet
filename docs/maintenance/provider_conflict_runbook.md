---
owner_role: Operator
doc_family: runbook
freshness_window_days: 30
---

# Provider Conflict Runbook

This runbook describes how to handle provider conflicts surfaced by the reconciliation engine.

## Types of Conflicts

### Fixtures
- **Kickoff Time Mismatch**: Usually resolved by `freshest_trusted`. Watch for major timezone offsets.
- **Home/Away Swap**: If suspected, manual review is usually needed.

### Odds
- **Line Value Mismatch**: Handled by `balanced_consensus` or `freshest_trusted_outlier_guard`.
- **Decimal Odds Outlier**: Outliers from a single provider are automatically trimmed.

### Results
- **Final Score Mismatch**: Critical severity. Requires a dispute and manual override if the providers do not reach consensus.

## Dealing with Disputes
If a `DisputeRecord` is created, it means the automated arbitration strategies could not safely select a winner.
1. Find the `DisputeRecord` in the queue.
2. Read the decision explanation from `ConsensusLineageRecord`.
3. Provide an authoritative override.
