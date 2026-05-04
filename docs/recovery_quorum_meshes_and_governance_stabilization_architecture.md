# Recovery Quorum Meshes & Governance Stabilization Architecture (Phase 87)

## Overview
Phase 87 introduces the Sovereign Governance Stabilization layer. It elevates the system from having basic "governance recovery escalators and successor registries" to a state where recovery decisions are coordinated across quorum meshes.

## Core Concepts
*   **Recovery Quorum Meshes**: Recovery quorums are evaluated across a mesh rather than single nodes, bounded by scope and authority.
*   **Successor Federation Councils**: Ambiguity in successor resolution across registries is handled explicitly by federation councils.
*   **Exception Lineage Registries**: Exceptions are tracked not just by status, but by their full lineage chain (origin, replays, successors).
*   **Sovereign Governance Stabilization Programs**: Stabilization is a programmatic flow with checkpoints and stages, not a single decision button.

## Guiding Rules
1.  **Sovereignty Dominates**: No mesh, council, lineage, or stabilization program can override a local `deny` or hard safety floor.
2.  **Lineage is Primary**: Currentness, replay states, and lineage integrity cap the strength of any bounded recovery hint. Stale lineage cannot be presented as healthy.
3.  **Future-Ready**: Built as an API for future phases like recovery mesh federations, successor adjudication exchanges, and bounded stabilization automation.
