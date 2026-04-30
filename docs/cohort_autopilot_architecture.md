---
owner: Principal Adoption Autopilot Engineer
family: deployment_governance
freshness_window_days: 90
---

# Cohort Autopilot Architecture (Phase 50)

This document describes the Cohort Autopilot Architecture, enabling safe, controlled segment-based adoption of rollout candidates.

## Why Cohorts?
Global stable adoption is risky. We need to gradually increase the scope of adoption. Cohorts allow us to test changes on small, clearly defined segments (e.g., specific sports or markets) before exposing the entire system.

## Autonomous Verification Windows
Following activation, the autopilot continuously verifies the cohort's health through defined windows (Immediate, Short, Medium, Stability). Clean windows lead to growth eligibility; regressions trigger pauses or rollbacks.

## Growth, Pause, Shrink, Rollback
- **Growth:** Progressing a cohort to a higher activation level.
- **Pause:** Halting growth due to stale verification or minor warnings.
- **Shrink:** Reducing the scope of a cohort due to localized issues.
- **Rollback:** Fully reverting a cohort due to critical regressions.

## Fleet-Aware Autopilot
The autopilot manages multiple cohorts simultaneously, enforcing global risk budgets and growth quotas to prevent systemic instability.
