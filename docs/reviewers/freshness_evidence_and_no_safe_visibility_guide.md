# Reviewers Guide: Freshness, Evidence, and No-Safe Visibility

When reviewing evidence atlas outputs or federated narratives:

* **Staleness is Contagious**: A single stale node (e.g., an outdated debt entry) in a queried path will downgrade the entire output.
* **Caveat Preservation**: Check that `no_safe_visibility` flags remain explicit. Executive summaries must never strip these warnings.
* **Evidence Sufficiency**: Replay clearing councils require hard evidence to authorize bounded clearing; weak evidence always falls back to manual review or blocked states.
