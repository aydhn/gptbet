# Staged Candidate Channels Architecture

The candidate channel omurga layer builds on top of Phase 45's candidate promotion logic. Its goal is NOT to immediately push candidates into production, but rather to safely guide them through rigorous evaluation environments (channels).

## Core Concepts
- **Channel Hierarchy**: Candidates start in Shadow, optionally transition to Candidate Eval, then to Live-like Safe.
- **Fleet Coordination**: Candidates do not live in a vacuum. A candidate "fleet" groups active candidate packages to discover conflicts and assess overall risk capacity.
- **Decisions**: Every stage boundary yields an explicit rollout decision: `progress_to_next_stage`, `hold_in_current_stage`, `rollback_to_shadow`, `retire_candidate`, or `supersede_with_better_candidate`.
- **Strategy Profiles**: We employ different progression strategies (e.g., `ConservativeStaged`, `BalancedPhased`, `FastSafeCandidateWave`) depending on risk appetites and candidate scopes.

The outputs are visible readiness states (`shadow_only_candidate`, `live_like_safe_ready`) which subsequent autonomous release phases will ingest.
