---
owner: Principal Federated Governance Engineer
family: control_plane
freshness_window: 30d
---

# Delegation Precedence Guide

Reviewers must ensure that code changes respect the federated precedence rules:
1. Global emergency overrides beat all.
2. Cross-cutting critical planes beat family planes.
3. Family domains beat cohort adoption rules.

Never approve a PR that allows a child plane to bypass a parent's budget constraint.
