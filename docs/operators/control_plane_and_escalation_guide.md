---
owner: Principal Federated Governance Engineer
family: control_plane
freshness_window: 30d
---

# Control Plane & Escalation Guide

A guide for operators managing the federated control planes.

## Delegated Action Lifecycle
1. Local plane proposes an action.
2. The action is evaluated against local budgets and policies.
3. If allowed, executed. If blocked, an escalation is created.
4. Escalations are routed based on `escalation.yaml` policies.

## Viewing the Mesh
Use `preview-mesh-topology` and `preview-budget-tree` to observe the global state and identify hotspots where escalations cluster.
