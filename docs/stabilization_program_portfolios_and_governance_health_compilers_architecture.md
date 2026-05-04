# Stabilization Program Portfolios and Governance Health Compilers Architecture

This document describes the Phase 88 architecture for the stabilization portfolio and governance health compiler layers.

## Core Concepts

The goal of this phase is to move from single stabilization programs and lineage chains to portfolio-level prioritization and holistic health compilation. This is a read-only, non-authoritative layer that provides explainable bounded health outputs without overriding sovereignty or hard safety limits.

### 1. Stabilization Program Portfolios
Portfolios group and prioritize stabilization programs. They manage burden distribution, identify blockages (like exception-heavy or replay-heavy states), and sort entries by priority bands without expanding scope.

### 2. Lineage Replay Fabrics
Replay fabrics route validation workloads across nodes and channels. They provide critical input on replay stability and pressure, ensuring that stale or mismatched replays cap restoration efforts.

### 3. Successor Convergence Registries
Registries track how well successor resolutions are converging. Weak or stale convergence produces debt that directly degrades compiled governance health.

### 4. Sovereign Governance Health Compilers
Compilers ingest currentness, replay, convergence, and lineage states to produce bounded health bands and restoration ceilings. They execute passes (e.g., sovereignty_pass) and apply penalties, ensuring that failures lead to degraded outputs.

## Principles
- **Portfolios Organize, They Do Not Authorize**: Priority affects ordering, not runtime rights.
- **Sovereignty Wins**: Hard constraints and local deny cannot be bypassed by high compiled health.
- **Staleness is Fatal**: Expired lineages or stale replays cap health at `review_only`.
- **Fail-Safe Compilation**: Failures in critical passes downgrade health bands visibly and explicitly.

## Integration
This architecture hooks into existing models (Phase 77-87): Governance Stabilization, Recovery, Exceptions, and Sovereign Mediation.
