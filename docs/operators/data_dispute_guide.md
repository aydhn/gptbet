---
owner_role: Operator
doc_family: runbook
freshness_window_days: 30
---

# Data Dispute Guide

When the reconciliation engine raises a dispute, it means multiple providers have submitted conflicting data with critical severity, and no single provider has enough trust dominance to automatically override the others.

## How to Handle Disputes
1. Check the `DisputeRecord` reasons.
2. Review the candidate values from each provider in the `ConsensusLineageRecord`.
3. Manually verify the correct value using a trusted third-party source.
4. (Future) Use the manual adjudication tool to resolve the dispute and feed the result back to the provider trust history.
