---
title: "Release Governance"
doc_family: "governance"
owner_role: "platform"
owner_component: "release"
status: "active"
---

# Release Governance

## Policy
No candidate artifact may be promoted to stable without:
1. Running in the `canary` channel for a minimum of 48 hours.
2. Passing all Quality Gates.
3. Explicit approval from the `core_ml` team.

## Approval Boundary
Operators cannot promote candidates to stable. They can only transition them to canary.
