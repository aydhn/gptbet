# Reviewer Guide: Race Probes, Stale Reads, and Idempotency

## Overview
Reviewers must verify that concurrency artifacts demonstrate safety before approving a release.

## What to Look For
1. **Race Probes:** Check `race_probe_runs.json`. A run status of `race_detected` means the execution schedule perturbation found a discrepancy.
2. **Stale Reads:** Check `stale_read_report.json`. Ensure no reads exceed their `drift_window_ref`.
3. **Idempotency:** Check `idempotency_report.json`. Side-effect writes must have idempotency keys, and duplicate attempts should be safely neutralized, not re-executed silently.
