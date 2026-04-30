---
owner: Expansion Control Plane
family: Architecture
freshness_window_days: 90
---

# Expansion Governance Architecture (Phase 51)

## Overview
This phase introduces a central governance layer above individual cohort autopilots. It manages multiple waves, cross-family interactions, and global risk budgets to safely coordinate large-scale expansion.

## Key Concepts
*   **Global Risk Budgets**: Limits total concurrent risk across the system.
*   **Pressure Model**: Quantifies systemic burden from conflicts, backlog, and warnings.
*   **Circuit Breakers**: Emergency triggers that can pause or shrink operations automatically.
*   **Expansion Council & Control Tower**: Deterministic aggregation of metrics to generate unified decisions (Continue, Throttle, Hold, Freeze, Pause).

## Core Strategies
*   `ConservativeExpansionGovernanceStrategy`: Strict thresholds, favors safety.
*   `BalancedControlTowerStrategy`: Balances throughput and risk (Default).
*   `FamilyFirstProtectionStrategy`: Prioritizes isolating risk to specific families.
