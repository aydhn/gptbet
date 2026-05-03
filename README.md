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
