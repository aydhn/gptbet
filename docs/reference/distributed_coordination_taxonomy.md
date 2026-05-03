# Distributed Coordination Taxonomy

## Cluster Families
- `local_coordination_cluster`
- `federated_coordination_cluster`
- `rollback_priority_cluster`
- `closure_priority_cluster`
- `review_isolated_cluster`
- `tenant_partitioned_cluster`

## Node Roles
- `scheduler_node`
- `broker_node`
- `arbitration_node`
- `closure_observer_node`
- `rollback_reserve_node`
- `review_boundary_node`
- `snapshot_coordinator_node`
- `failover_candidate_node`

## Health Statuses
- `healthy`: Operating normally.
- `pressured`: High renewal backlogs.
- `degraded`: Ownership divergence or stale snapshots.
- `failover_needed`: Node offline or unstable.
