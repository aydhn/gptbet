---
owner_role: Principal Data Reliability Engineer
doc_family: architecture
freshness_window_days: 90
---

# Reconciliation & Arbiter Architecture

## Why Provider Abstraction is Not Enough
While the provider abstraction layer handles basic routing and failover, it operates on a "first successful response wins" paradigm. In multi-source environments, this leads to silent acceptance of conflicting data. The Reconciliation layer sits above the abstraction layer to explicitly identify, categorize, and resolve these conflicts.

## Grouping and Normalization
Before arbitration, observations from multiple sources are grouped by `entity_key` (e.g., match ID). Fields are then canonicalized to ensure apples-to-apples comparison.

## Conflict Taxonomy
Conflicts are explicitly categorized and assigned a severity:
- **Low**: Minor discrepancies (e.g., team name alias).
- **Medium**: Time differences within a tolerance window.
- **High**: Significant line value differences.
- **Critical**: Opposing result statuses (e.g., "finished" vs "cancelled").

## Trust and Confidence Model
Consensus is not merely an average. Trust is dynamically calculated based on provider quality, health, and historical accuracy. The arbitration output includes a `confidence_score` reflecting the level of agreement and trust.

## Dispute Escalation
When a critical conflict cannot be safely resolved automatically, the system raises a `DisputeRecord` instead of a silent compromise. These disputes are routed to human operators.

## Future Extensions
This architecture is designed to support future phases including:
- Learning-based arbiters
- Provider reputation decay based on historical disputes
- Human adjudication workflows
