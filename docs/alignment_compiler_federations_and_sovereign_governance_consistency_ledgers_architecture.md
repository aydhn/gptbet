---
title: Alignment Compiler Federations & Sovereign Governance Consistency Ledgers Architecture
family: consistency_ledgers
owner_role: Principal Alignment Federation Engineer
freshness_window: 90d
---

# Architecture Overview (Phase 98)

This document outlines the Phase 98 implementation of Sovereign Governance Consistency Ledgers. The goal is to provide bounded, explainable, and caveat-preserving visibility across alignment federations, dispute meshes, and evidence exchanges without overriding local sovereignty.

## Core Components

1. **Alignment Compiler Federations**
   - Combines outputs from multiple alignment compilers into a federated band.
   - Preserves penalties, ceilings, caveats, and `no_safe_recovery_hint` visibility.
   - Any stale member downgrades the entire federation's currentness and agreement band.

2. **Dispute Tribunal Meshes**
   - Coordinates dispute tribunals into a mesh for bounded deliberation.
   - Validates node and edge currentness.
   - Prevents scope widening (e.g., routing a narrow case through a wide edge).
   - Computes global mesh pressure, which can downgrade routes to `review_only` or suppress them entirely if critical.

3. **Evidence Exchange Clearers**
   - Matches evidence requests with available listings.
   - Strict compatibility checks prevent scope mismatches.
   - Fairness and pressure mechanisms ensure that critical requests are handled, even if the outcome is degraded.
   - Generates bounded, review-only, caveated, or no-safe clearing routes.

4. **Sovereign Governance Consistency Ledgers**
   - Replayable, non-authoritative ledger tracking consistency shifts and contradictions.
   - Maps alignment outputs and clearing decisions to consistency states (`consistent_with_caps`, `stale_consistency`, `contradicted`, etc.).
   - Explicitly models contradictions (e.g., `freshness_contradiction`, `no_safe_visibility_contradiction`) with lineage tracking.

## Guardrails

- **Local Sovereignty Wins**: No federation, mesh route, clearing, or ledger entry can bypass a local `deny` decision.
- **Freshness is Load-Bearing**: Stale inputs immediately cap outcomes (e.g., strong agreement becomes weak agreement, bounded routes become review-only).
- **No-Safe Preservation**: Any presence of a `no_safe_recovery_hint` will immediately cap routes and persist through the ledger to ensure maximum visibility to human operators.
