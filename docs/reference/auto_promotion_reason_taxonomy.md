---
owner: system
family: reference
freshness_window_days: 120
---

# Auto Promotion Reason Taxonomy

## Decision Types
- `auto_progress`: Candidate advanced to the next stage.
- `auto_hold`: Candidate paused (e.g., stale gates, capacity).
- `auto_kill`: Candidate terminated safely.
- `auto_defer`: Candidate deferred.
- `review_required`: Manual intervention requested.
- `approval_required`: Explicit human approval needed based on boundary rules.
- `blocked_by_safety`: Failed hard safety check.
- `blocked_by_manual_override`: Human override present.
- `blocked_by_capacity`: Quota saturated.

## Kill Reason Codes
- `critical_safety_violation`
- `stale_or_invalid_simulation`
- `failed_required_quality_gates`
- `unresolved_critical_dispute`
- `superseded_by_stronger_candidate`
- `candidate_expired_without_readiness`

## Hold Reason Codes
- `missing_fresh_gate_results`
- `pending_approval`
- `pending_manual_review`
- `fleet_capacity_pressure`
- `unresolved_noncritical_conflicts`
