# Reviewers Guide: Freshness, Caps & Narrative Integrity

When reviewing assurance outputs and board decisions, ensure the following constraints are honored:
1. **Snapshot Freshness**: Stale components > 3600 seconds trigger immediate block or degraded states.
2. **Caps**: Board resolution should always apply reasonable constraints to the restoration ceiling.
3. **Narrative Integrity**: No safety-critical metrics (e.g. `no_safe_recovery_hint`) should be abstracted away from executive summaries.
