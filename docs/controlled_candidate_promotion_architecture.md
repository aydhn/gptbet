---
owner: candidate_promotion_team
family: architecture
freshness: 30d
---

# Controlled Candidate Promotion Architecture

## Purpose
The Controlled Candidate Promotion layer bridges the gap between shortlisted candidates (from Phase 44 Tournaments) and actual release readiness. A shortlist is merely an admission ticket; it does not guarantee safe release. This architecture establishes a strict `promote-or-kill` framework, enforcing staged validations, explicit state machines, and evidence-backed readiness scores before a candidate can be proposed for active release channels.

## Key Principles
1. **Shortlist ≠ Release**: Shortlist is just the beginning.
2. **Staged Validation First**: Candidates go through Integrity, Safety, Simulation, Gates, and Review stages.
3. **Explicit State Machine**: Candidates move from `candidate_created` -> `pending_stage_validation` -> `quality_gates_passed` -> `candidate_ready`.
4. **Kill is a Valid Outcome**: Candidates failing safety or gates are explicitly killed.
5. **No Active State Mutation**: This layer produces a `CandidateReleasePackage` and makes a `promote_or_kill` decision. It does *not* mutate active `stable` or `canary` pointers directly.

## Stages
1. Integrity Stage
2. Safety Stage
3. Simulation Stage
4. Quality Gates Stage
5. Review / Approval Stage
6. Release Readiness Stage

## Future Extensions
- Staggered Candidate Waves
- Shadow Fleets
- Autonomous Kill-Switch Integration
