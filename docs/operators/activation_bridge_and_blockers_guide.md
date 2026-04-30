---
owner: "Platform Operators"
family: "operators"
freshness_window: "30d"
---

# Activation Bridge & Blockers Guide

## Activation Bridge
The Activation Bridge produces a `ActivationBridgePackageRecord` without modifying the active pointer. It serves as an activation-ready transfer object containing:
- Candidate Package Refs
- Rollback Safety Notes
- Activation Constraints

## Blockers
Blockers prevent handoffs. Critical blockers like unresolved disputes or missing approvals will trigger a `HOLD` or `KILL` decision.
