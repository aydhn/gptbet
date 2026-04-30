# Rollout Stage Interpretation Guide

When reviewing staged candidates, use the following guide:

1. **Shadow (`shadow_candidate_channel`)**
   - Goal: Check if the candidate acts wildly different or crashes.
   - Look for: `shadow_verified` evidence packets.

2. **Candidate Eval (`candidate_eval_channel`)**
   - Goal: Evaluate against fleet conflicts and stricter monitoring.
   - Look for: Conflicting candidates, capacity drops.

3. **Live-Like Safe (`live_like_safe_channel`)**
   - Goal: Compare against `stable_reference` with ops-level strictness.
   - Look for: No degradation in core KPIs compared to the live setup.

A rollback to shadow (`rollback_to_shadow`) means we detected an issue, but it's not a hard failure; it needs revision or more observation.
