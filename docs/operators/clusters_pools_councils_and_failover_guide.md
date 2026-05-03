# Clusters, Pools, Councils, and Failover Guide

This guide is intended for operators managing the Phase 74 Distributed Coordination Fabric.

## 1. Managing Clusters and Shards
Clusters group nodes into logical coordination units. When inspecting load, pay attention to the shard distribution. Unbalanced shards may indicate a need for manual reassignment if the active strategy (e.g., `ConservativeDistributedFabricStrategy`) is aggressively isolating workloads.

## 2. Monitoring Broker Pools
Broker pools manage token ownership partitions. The most critical metric is **Ownership Divergence**. If a partition lacks an active owner, or if two brokers claim the same partition, the cluster health status will shift to `degraded`.

## 3. Federated Arbitration Councils
Councils resolve cross-node contentions. Operators should review council cases that result in `serialize_across_nodes` or `require_review_before_runtime`. High volumes of such outcomes indicate that the fabric is starved for shared resources like rollback bounds or closure reserves.

## 4. Failover and Revalidation
Failovers are automated but cautious. Upon detecting a node failure, a target node is selected.
**Crucial Step:** The target node must undergo revalidation against the cluster snapshot. If the snapshot is stale, failover is blocked, and manual intervention is required. This prevents stale tokens from being honored.
