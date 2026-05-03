# Corridor Registries, Attestation Exchanges & Conformance Packs Architecture (Phase 78)

## Overview
Phase 78 evolves the corridor governance system from ad-hoc capability discovery to a structured registry conformance layer. It introduces formal corridor registries, bounded attestation exchanges, treaty baseline benchmarks, and policy conformance packaging.

## Core Concepts

### 1. Corridor Registries
Registries serve as structured sources of governance truth. They are NOT execution authorities. They track lineage, supersession, freshness, and the "current" pointer for corridors and treaties.

### 2. Attestation Exchanges
Continuity attestations can be exchanged between registries, but they are bounded. They must include scope, caveats, and validity windows. They do not override local sovereignty.

### 3. Treaty Benchmarking
Treaties are compared against `TreatyBenchmarkBaselineRecord` configurations to determine if they are stronger, aligned, narrower, or weaker than expectations. Missing dimensions are explicitly tracked.

### 4. Policy Conformance Packs
A conformance pack evaluates multiple dimensions (treaties, corridors, translation ledgers) against available evidence. Any blocking gaps explicitly cap the overall conformance status, and evidence pointers must be machine-checkable.

## Key Principles
- **Registries are for discoverability**, not runtime authority.
- **Exchanges must be bounded** with explicit scopes and validity watchers.
- **Benchmarks guide, not override**. Local sovereignty wins.
- **Conformance packs must be machine-checkable**, not prose.
- **Currentness matters**. Expired entries cannot be current.
