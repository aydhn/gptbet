# Phase 75: Multi-Region Execution Fabric & Sovereign Governance

This phase establishes a multi-region bounded execution fabric on top of the distributed execution coordination clusters, adding broker sharding, cross-cluster recovery treaties, and sovereignty-aware remediation governance.

## Purpose

The goal is to safely extend bounded remediation coordination across regions without sacrificing local safety floors or implicitly relaxing throughput. Broker shards hold explicit ownership, recovery operations require explicit treaties, and sovereignty policies take precedence over both treaties and performance.

## Core Taxonomies

- **Region Affinities**: `hard_local_affinity`, `preferred_local_affinity`, `treaty_transfer_affinity`, `failover_affinity`
- **Broker Shards**: `execution_token_shard`, `renewal_shard`, `rollback_reserve_shard`
- **Treaty Families**: `review_delegation_treaty`, `bounded_runtime_treaty`, `failover_assistance_treaty`
- **Sovereignty Families**: `local_only_sovereignty`, `review_export_limited_sovereignty`

## Key Capabilities

1. **Broker Sharding**: Token broker pools are sharded by region, tenant, and review scope, enforcing strict ownership and safe handoff mechanisms.
2. **Cross-Cluster Treaties**: Operations between clusters (delegation, review, failover assistance) require explicitly negotiated treaties with expiry boundaries.
3. **Sovereignty Rules**: Domains enforce their own non-portable token requirements and observability export limits, which override treaty allowances.
4. **Cross-Region Admissions & Failover**: Safe bounds check for target regions based on snapshot freshness and revalidation policies.

## Execution

```bash
# Evaluate Multi-Region Fabric setup
python -m sports_signal_bot.main multi-region run-multi-region-fabric-pass

# Inspect treaties
python -m sports_signal_bot.main multi-region preview-recovery-treaties

# View available execution strategies
python -m sports_signal_bot.main multi-region list-multi-region-fabric-strategies
```

# Sports Signal Bot

Sports Signal Bot is an advanced ecosystem for sports forecasting, orchestration, discovery, and governance.

## Features

- Verifier Portal
- Ecosystem Discovery
- Evidence & Explainability
- Transparency
- Streaming Discovery & Observability Fabric (Phase 67)

## Getting Started

1. Set up the environment
2. Run `python -m sports_signal_bot.main --help`

## Streaming Discovery & Observability Fabric

The streaming discovery and observability fabric layer operates on events as signals, adapting routes based on anomalies and ensuring visibility into ecosystem health.

## Resilience Advisor & Recovery Orchestration (Phase 69)
The system includes an autonomous, bounded resilience advisor that observes failure patterns and synthesizes safe, reviewable remediation playbooks and orchestration plans. See `docs/resilience_advisor_and_recovery_orchestration_architecture.md` for details.

## Remediation Lane Architecture & Bounded Execution (Phase 71)

The remediation lane layer divides automated recovery into safe, narrow lanes. Instead of blanket automation, recovery steps must pass readiness gates and operate under short-lived Bounded Execution Tokens derived from review approvals.
- Execution is strictly bounded by scope, token validity, and step families.
- All lanes must achieve Closed-Loop Verification to be considered completed.
- Federated playbook catalogs can safely exchange recovery plans which must be adapted locally.

Run `python -m sports_signal_bot.main remediation-lanes run-remediation-lanes-pass` to simulate lane eligibility, token issuance, closed-loop readiness, closure verification, federated catalog adaptation, and automation preparation.

### Phase 73: Supervised Execution Coordination Fabric
The system now includes an Execution Coordination Fabric that provides safe, bounded concurrency for multiple remediation lanes. Rather than acting as a general-purpose scheduler, it explicitly coordinates contention over shared surfaces (like data sources, rollback paths, and token capacity) to ensure safety always takes precedence over parallelism.

Core mechanisms:
* **Approval-Token Broker**: Manages token allocation and renewals centrally to prevent exhaustion and unauthorized scope widening.
* **Contention Arbitration Engine**: Detects shared dependencies and arbitrates conflicts based on strict safety precedence (e.g., rollback or closure priority always preempts opportunistic repair).
* **Multi-Lane Scheduler**: Evaluates lane readiness and schedules runtime windows based on broker and arbitration decisions.
* **Coordination Ledger**: Maintains an audit trail of all scheduling and brokerage decisions for explainability.

**Key CLI Commands:**
- `python -m sports_signal_bot.main execution-coordination run-execution-coordination-pass`
- `python -m sports_signal_bot.main execution-coordination preview-multi-lane-schedules`

### Phase 74: Distributed Execution Coordination Fabric
The system now expands execution coordination into a distributed cluster model, utilizing scheduler shards and broker pools to coordinate remediation lanes across multiple nodes while strictly enforcing bounded execution constraints, tenancy isolation, and safe failovers via federated arbitration councils.

**Key CLI Commands:**
- `python -m sports_signal_bot.main distributed-coordination run-distributed-coordination-pass`
- `python -m sports_signal_bot.main distributed-coordination preview-coordination-clusters`
- `python -m sports_signal_bot.main distributed-coordination list-distributed-coordination-strategies`

**Why Distribution Does Not Relax Safety:**
Distribution enables bounded execution parallelism and scalability by federating workloads. It explicitly avoids diluting lane or token boundaries. Any cross-node contentions that conflict with tenancy or safety isolation rules are escalated to councils and blocked or serialized, prioritizing safe execution over unsafe throughput.

### Phase 76: Sovereign Runtime Corridors
This layer adds treaty-backed remediation corridors standard, policy-border translation ledger discipline, and a regional assurance continuity controller layer to the multi-region execution fabric. Cross-region remediation flows only over explicit narrow corridors, tracked by translation ledgers, maintaining explicit assurance continuity.

### Phase 78: Registry Conformance & Sovereign Interoperability Policy
The system establishes a registry conformance layer to govern corridors, attestations, treaty benchmarking, and policy conformance packaging. This ensures discoverability, supersession awareness, and bounded exchange of continuity attestations without bypassing sovereignty.

**Key capabilities:**
- **Corridor Registries**: Manage currentness, freshness, and supersession of governance targets.
- **Attestation Exchanges**: Bound exchange of continuity attestations with explicit caveats and scopes.
- **Treaty Benchmarking**: Compare treaty dimensions against standard baselines to compute alignment.
- **Policy Conformance Packs**: Package evidence and identify gaps to determine overall conformance status.

**Run a pass:**
- `python -m sports_signal_bot.main registry-conformance run-registry-conformance-pass`

## Phase 79: Federation Ecosystem
The Federation Ecosystem phase establishes corridor registry federation, attestation exchange hubs, treaty baseline catalogs, and sovereign policy attestation ecosystems.
It enables federated discoverability and structured attestation routing while strictly adhering to local sovereignty and bounded claims disciplines.

### Key Commands:
- `python -m sports_signal_bot.main federation-ecosystem run-federation-ecosystem-pass`
- `python -m sports_signal_bot.main federation-ecosystem preview-registry-federations`
- `python -m sports_signal_bot.main federation-ecosystem preview-attestation-hubs`

For details, refer to `docs/corridor_registry_federation_and_attestation_hubs_architecture.md`.

## Ecosystem Resilience (Phase 80)
The **Ecosystem Resilience** layer adds federated trust overlays, hub routing meshes, baseline marketplace signals, and ecosystem resilience controllers over the sovereign ecosystem.

- **Trust Overlays**: Treat federated registry currentness and attestation values as interpretable layers, computing a `TrustOverlayBand` without granting direct admission rights. High scores cannot override local sovereignty denials.
- **Hub Routing Meshes**: Orchestrate multi-hub attestation pathways. Meshes strictly bounds routes, dropping path preference (`PREFERRED_BOUNDED_PATH`, `DEGRADED_FALLBACK_PATH`, etc.) without expanding visibility scopes.
- **Baseline Marketplace Signals**: Treat baseline catalog signals as bounded projection hints to boost or decay trust, enforcing staleness and corroboration limits.
- **Resilience Controllers**: Oversee ecosystem health (pressure, controller state degradation) by reducing pipeline projections and enforcing caution/degraded states without issuing runtime authorizations.

These mechanisms are explicitly separated from standard routing governance. Mesh paths are bounded hints, overlays explain decisions (vs authorizing them), and signals are never authoritative.

Commands:
```bash
python -m sports_signal_bot.main ecosystem-resilience run-ecosystem-resilience-pass
python -m sports_signal_bot.main ecosystem-resilience preview-trust-overlays
```
