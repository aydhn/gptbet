---
owner: reviewers
family: guide
freshness_window_days: 60
---

# Auto Decision Boundary Guide

## Hard Safety Blocks
The engine strictly respects hard blocks:
- **Manual Overrides**: If a reviewer applies a manual override, the system will not auto-progress the candidate.
- **Stale Simulations**: If the last simulation is older than the configured limit (e.g., 24 hours), progression is blocked.
- **Unresolved Disputes**: Active disputes immediately block automation.
- **Failed Quality Gates**: If `gate_cleanliness` is `< 1.0`, progression is blocked.

## Approval Boundaries
Candidates with `risk_level == "high"` or `scope_breadth == "broad"` strictly require explicit approval (`approval_status == "approved"`) to progress. If pending, they are marked as `approval_required`.

## Heuristic Scoring
Even if hard boundaries are cleared, candidates must earn a minimum progression score (`minimum_progression_score`) via their `readiness_score`, `evidence_completeness`, and `gate_cleanliness` to advance.
