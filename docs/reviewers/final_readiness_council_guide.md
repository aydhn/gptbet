---
owner: "Council Approvers"
family: "reviewers"
freshness_window: "30d"
---

# Final Readiness Council Guide

## Council Lenses
The council evaluates candidates using deterministic lenses:
- **Safety Lens**: Checks for rollback procedures and risk levels.
- **Evidence Lens**: Validates evidence completeness scores.
- **Simulation Lens**: Ensures simulation results are not stale.
- **Governance Lens**: Confirms required approvals and docs.
- **Rollout History Lens**: Evaluates stability across staged channels.

## Output
The council outputs a `CouncilDecisionType` such as `APPROVE_HANDOFF`, `HOLD_FOR_MORE_EVIDENCE`, or `KILL_CANDIDATE_BEFORE_HANDOFF`.
