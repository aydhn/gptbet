---
title: "System Overview"
doc_family: "overview"
owner_role: "engineering_team"
owner_component: "general"
status: "active"
---

# System Overview

The Sports Signal Bot is a highly modular, extensible sports forecasting system.

It is designed with a provider-first ingestion approach, canonical schemas, quality gates, and an artifact-driven ML pipeline. The core engine dynamically weights signals and uses threshold optimization for dispatch decisions.

Key principles:
1. Provider-first data ingestion
2. Strict time-aware cross-validation (no data leakage)
3. Deterministic caching and incremental computation
4. Artifact-first modeling
