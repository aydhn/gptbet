---
owner: release_ops
family: guide
freshness: 30d
---

# Promote, Hold, Revise, Kill Guide

When evaluating a Candidate Release Package, the final decision falls into one of these actions:

- **Promote**: `promote_candidate_lane`
  The candidate is ready. A release draft is generated.
- **Hold**: `hold_candidate`
  The candidate is good but waiting on gate backlogs or missing approvals.
- **Revise**: `revise_candidate`
  The candidate shows promise but the scope is too broad, or simulation results were mixed. It needs narrowing and re-entry.
- **Kill**: `kill_candidate`
  The candidate failed safety checks, or a better successor exists. It is permanently removed from the active pipeline.
- **Supersede**: `supersede_candidate`
  A newer, better candidate exists for the same scope.

Operators can view the detailed rationale for these decisions in the `CandidatePromotionDecisionRecord`.
