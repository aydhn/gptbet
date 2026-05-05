# Runbook: Concurrency Hardening Pack 03

## Daily Maintenance
Run `python -m sports_signal_bot.main concurrency run-hardening-pack-03` as part of CI.
If the overall health indicates release blockers, inspect the specific JSON artifacts generated.

## Troubleshooting
- **Race Detected:** Look at the perturbation strategy used (e.g., `reverse`, `interleave`). Attempt to reproduce locally with the same seed.
- **Overparallelized Plan:** Reduce `max_parallelism` or `lane_count` in the plan configuration to bring it back under the safety threshold.
- **Drift Detected:** Indicates a stale read. Investigate the `drift_window_ref` and whether the cache/snapshot strategy needs tuning.
