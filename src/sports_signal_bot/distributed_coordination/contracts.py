import datetime
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class CoordinationClusterRecord(BaseModel):
    cluster_id: str
    cluster_name: str
    cluster_family: str
    member_node_refs: List[str]
    scheduler_pool_refs: List[str]
    broker_pool_refs: List[str]
    council_refs: List[str]
    tenancy_policy_ref: str
    active_status: str
    warnings: List[str] = []

class CoordinationNodeRecord(BaseModel):
    node_id: str
    cluster_ref: str
    roles: List[str]
    active: bool

class ClusterMembershipRecord(BaseModel):
    cluster_ref: str
    node_ref: str
    joined_at: datetime.datetime
    status: str

class BrokerPoolRecord(BaseModel):
    broker_pool_id: str
    pool_family: str
    member_broker_refs: List[str]
    allocation_strategy: str
    ownership_partitions: Dict[str, Any]
    renewal_backlog_refs: List[str]
    failover_policy: str
    health_status: str
    warnings: List[str] = []

class BrokerPoolMemberRecord(BaseModel):
    broker_ref: str
    pool_ref: str
    weight: float

class BrokerOwnershipRecord(BaseModel):
    broker_ref: str
    partition_ref: str
    owned_since: datetime.datetime

class BrokerPoolAllocationRecord(BaseModel):
    allocation_id: str
    pool_ref: str
    broker_ref: str
    lane_ref: str

class RenewalBacklogShardRecord(BaseModel):
    shard_id: str
    pool_ref: str
    pending_renewals: int

class FederatedArbitrationCouncilRecord(BaseModel):
    council_id: str
    council_family: str
    participating_node_refs: List[str]
    participating_scheduler_refs: List[str]
    participating_broker_refs: List[str]
    precedence_policy_ref: str
    decision_status: str
    warnings: List[str] = []

class CouncilCaseRecord(BaseModel):
    case_id: str
    council_ref: str
    contention_ref: str
    opened_at: datetime.datetime
    status: str

class CouncilVoteRecord(BaseModel):
    vote_id: str
    case_ref: str
    voter_ref: str
    position: str

class CouncilDecisionRecord(BaseModel):
    decision_id: str
    case_ref: str
    outcome: str
    reasoning: str

class TenancyIsolationRecord(BaseModel):
    isolation_id: str
    tenant_or_domain_ref: str
    allowed_lane_families: List[str]
    forbidden_shared_surfaces: List[str]
    token_scope_policy: str
    approval_boundary_policy: str
    visibility_boundary_policy: str
    warnings: List[str] = []

class TenantRuntimeBoundaryRecord(BaseModel):
    boundary_id: str
    tenant_ref: str
    max_concurrent_lanes: int

class DomainApprovalBoundaryRecord(BaseModel):
    boundary_id: str
    domain_ref: str
    required_freshness_seconds: int

class ClusterFailoverRecord(BaseModel):
    failover_id: str
    cluster_ref: str
    failed_node_ref: str
    target_node_ref: str
    status: str

class FailoverCandidateRecord(BaseModel):
    candidate_id: str
    node_ref: str
    readiness_score: float

class DistributedFabricManifest(BaseModel):
    manifest_id: str
    timestamp: datetime.datetime
    cluster_refs: List[str]

class DistributedFabricWarningRecord(BaseModel):
    warning_id: str
    target_ref: str
    message: str

class DistributedFabricAuditRecord(BaseModel):
    audit_id: str
    timestamp: datetime.datetime
    target_ref: str
    event: str

class SchedulerShardRecord(BaseModel):
    shard_id: str
    shard_family: str
    assigned_node_ref: str
    load: float

class ShardOwnershipRecord(BaseModel):
    shard_ref: str
    node_ref: str
    owned_since: datetime.datetime

class ShardLoadRecord(BaseModel):
    shard_ref: str
    active_lanes: int
    pending_lanes: int

class ShardReassignmentRecord(BaseModel):
    reassignment_id: str
    shard_ref: str
    from_node_ref: str
    to_node_ref: str
    reason: str

class CouncilParticipantRecord(BaseModel):
    participant_id: str
    council_ref: str
    node_ref: str

class CouncilPrecedenceRuleRecord(BaseModel):
    rule_id: str
    council_ref: str
    priority: int
    description: str

class CouncilConflictMatrixRecord(BaseModel):
    matrix_id: str
    council_ref: str
    conflicts: Dict[str, Any]

class CouncilOutcomeRecord(BaseModel):
    outcome_id: str
    decision_ref: str
    action_taken: str

class SnapshotMembershipRecord(BaseModel):
    snapshot_ref: str
    cluster_ref: str
    member_nodes: List[str]

class SnapshotOwnershipRecord(BaseModel):
    snapshot_ref: str
    broker_ownerships: Dict[str, str]
    shard_ownerships: Dict[str, str]

class SnapshotBacklogRecord(BaseModel):
    snapshot_ref: str
    renewal_backlogs: Dict[str, int]
    closure_backlogs: Dict[str, int]

class SnapshotValidityRecord(BaseModel):
    snapshot_ref: str
    is_valid: bool
    reason: str

class SnapshotSupersessionRecord(BaseModel):
    supersession_id: str
    old_snapshot_ref: str
    new_snapshot_ref: str
    timestamp: datetime.datetime

class ClusterSnapshotLineageRecord(BaseModel):
    lineage_id: str
    snapshot_ref: str
    parent_snapshot_ref: Optional[str] = None
    created_at: datetime.datetime

class ClusterSnapshotRecord(BaseModel):
    snapshot_id: str
    cluster_ref: str
    timestamp: datetime.datetime
    lineage_ref: str
    membership: SnapshotMembershipRecord
    ownership: SnapshotOwnershipRecord
    backlog: SnapshotBacklogRecord
    validity: SnapshotValidityRecord

class FailoverTriggerRecord(BaseModel):
    trigger_id: str
    cluster_ref: str
    reason: str

class FailoverRevalidationRecord(BaseModel):
    revalidation_id: str
    failover_ref: str
    status: str

class FailoverHandoffRecord(BaseModel):
    handoff_id: str
    failover_ref: str
    from_node_ref: str
    to_node_ref: str

class FailoverRecoveryStatusRecord(BaseModel):
    status_id: str
    failover_ref: str
    state: str

class ClusterFairnessRecord(BaseModel):
    fairness_id: str
    cluster_ref: str
    score: float

class TenantFairnessRecord(BaseModel):
    tenant_fairness_id: str
    tenant_ref: str
    score: float

class DistributedStarvationRiskRecord(BaseModel):
    risk_id: str
    target_ref: str
    risk_level: str

class FairnessScopeRecord(BaseModel):
    scope_id: str
    target_ref: str
    bounds: Dict[str, Any]
