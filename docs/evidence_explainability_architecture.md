---
owner_role: "evidence_engineering"
doc_family: "architecture"
freshness_days: 90
---

# Evidence & Explainability Architecture

## Why Lineage Alone is Not Enough
Lineage tracks data movement. Evidence & Explainability (E&E) answers "Why?". It translates technical lineage into an audience-aware explanation of decisions, blocks, and scores.

## Evidence Bundle Anatomy
An Evidence Bundle is a container for:
- Claims (e.g. "Signal score was 0.88")
- Citations (e.g. "Ref: Model Output artifact 123")
- Lineage Graph
- Caveats & Confidence

## Integrations
The E&E layer integrates deeply with the Reconciliation engine to extract disputes, and the Decision Engine to explain why something was blocked or approved.
