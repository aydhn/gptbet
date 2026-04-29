---
title: "Decision Log"
doc_family: "maintenance"
owner_role: "engineering_team"
owner_component: "general"
status: "active"
---

# Decision Log

## Date: 2024-04-29
**Decision Title:** Implement Strict Time-Aware CV
**Context:** Need to prevent data leakage in forecasting models.
**Chosen Option:** Enforce Walk-Forward and Expanding Window CV only.
**Rejected Alternatives:** K-Fold CV with shuffling.
**Consequences:** Training is slower and more complex, but models are reliable.
**Related Components:** `core_ml`
