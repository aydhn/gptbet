# Tenancy Isolation and Distributed Arbitration Guide

This guide assists reviewers and architects in evaluating the safety boundaries of the Distributed Execution Coordination Fabric.

## Tenancy Isolation Boundaries
Reviewers must verify that `TenancyIsolationRecord` entries enforce strict boundaries.
- **Forbidden Shared Surfaces:** Ensure resources like `root_closure_pool` or `global_rollback_cache` are explicitly forbidden for cross-tenant sharing.
- **Validation:** When reviewing a new federated playbook adaptation, verify that its runtime fit does not quietly circumvent these isolation policies.

## Distributed Arbitration Precedence
When cross-node conflicts occur, the Arbitration Council steps in.
Reviewers must confirm that the precedence rules are respected:
1. Rollback safety is paramount.
2. Closure backlog obligations preempt new execution.
3. Tenant boundary integrity cannot be traded for throughput.

If a council decision results in an expanded scope, it is a severe violation of the system's core bounded-execution safety rules. Councils can only narrow, defer, serialize, or block execution.
