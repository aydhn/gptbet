# Witness Consensus and Challenge Guide for Operators

Operators are responsible for monitoring the health of the Witness Mesh.

## Key Metrics to Watch
- Witness coverage of critical events (must be >= 2).
- Count of open challenges (should be near 0).
- Count of `UNRESOLVED_ESCALATED` challenges.

## Actions
- If a witness node goes offline, investigate immediately, as it degrades consensus and readiness scores.
- Review expired challenges to ensure they are escalated to anomaly adjudication.
