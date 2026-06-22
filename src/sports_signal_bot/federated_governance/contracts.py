from pydantic import BaseModel, Field
from enum import Enum
from typing import Dict, Any, List, Optional
from datetime import datetime


class PlanePrecedence(int, Enum):
    CANDIDATE_LOCAL = 60
    COHORT_ADOPTION = 50
    FAMILY_DOMAIN = 40
    CROSS_CUTTING_CRITICAL = 30
    GLOBAL_GOVERNANCE = 20
    GLOBAL_EMERGENCY = 10


class PlaneCapability(str, Enum):
    OBSERVE_ONLY = "observe_only"
    RECOMMEND_ONLY = "recommend_only"
    LOCAL_PAUSE = "local_pause"
    LOCAL_SHRINK = "local_shrink"
    LOCAL_GROWTH_AUTHORITY = "local_growth_authority"
    LOCAL_BUDGET_ALLOCATION = "local_budget_allocation"
    CONFLICT_ESCALATION = "conflict_escalation"
    FAMILY_FREEZE_REQUEST = "family_freeze_request"
    LOCAL_CANDIDATE_ADMISSION = "local_candidate_admission"
    LOCAL_WAVE_SCHEDULING = "local_wave_scheduling"
    MANUAL_REVIEW_REQUEST = "manual_review_request"
    GLOBAL_OVERRIDE_REQUEST_ONLY = "global_override_request_only"


class DelegationMode(str, Enum):
    ADVISORY_ONLY = "advisory_only"
    SCOPED_AUTONOMY = "scoped_autonomy"
    BOUNDED_EXECUTION = "bounded_execution"
    APPROVAL_GATED_EXECUTION = "approval_gated_execution"
    ESCALATION_ONLY = "escalation_only"
    READ_ONLY = "read_only"


class EscalationOutcome(str, Enum):
    RESOLVED_LOCALLY_WITH_GUIDANCE = "resolved_locally_with_guidance"
    ESCALATED_TO_PARENT_PLANE = "escalated_to_parent_plane"
    ESCALATED_TO_GLOBAL_PLANE = "escalated_to_global_plane"
    ESCALATED_TO_CROSS_CUTTING_PLANE = "escalated_to_cross_cutting_plane"
    BLOCKED_PENDING_COUNCIL = "blocked_pending_council"
    CONVERTED_TO_EMERGENCY_CASE = "converted_to_emergency_case"
    DENIED = "denied"


class PlaneHealthBand(str, Enum):
    HEALTHY = "healthy"
    NOISY = "noisy"
    STRESSED = "stressed"
    UNSTABLE = "unstable"
    SUSPENDED = "suspended"


class PlaneTrustBand(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    LIMITED_AUTONOMY_ONLY = "limited_autonomy_only"


class ControlPlaneRecord(BaseModel):
    plane_id: str
    plane_name: str
    plane_family: str
    precedence: PlanePrecedence
    parent_plane_id: Optional[str] = None
    managed_scopes: List[str] = Field(default_factory=list)
    delegated_authorities: List[PlaneCapability] = Field(default_factory=list)
    escalation_targets: List[str] = Field(default_factory=list)
    active_status: bool = True
    safety_level: str = "standard"
    warnings: List[str] = Field(default_factory=list)
    health: PlaneHealthBand = PlaneHealthBand.HEALTHY
    trust: PlaneTrustBand = PlaneTrustBand.HIGH


class ControlPlaneScopeRecord(BaseModel):
    scope_id: str
    plane_id: str
    allowed_domains: List[str]


class DelegationPolicyRecord(BaseModel):
    delegation_id: str
    source_plane_id: str
    target_plane_id: str
    delegated_action_family: str
    delegated_scope: Dict[str, Any]
    delegation_mode: DelegationMode
    approval_requirements: List[str] = Field(default_factory=list)
    hard_boundaries: Dict[str, Any] = Field(default_factory=dict)
    expiry_policy: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)


class EscalationRuleRecord(BaseModel):
    rule_id: str
    condition: str
    target_plane_id: str


class FederatedDecisionRecord(BaseModel):
    decision_id: str
    plane_id: str
    action: str
    status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CrossPlaneConflictRecord(BaseModel):
    conflict_id: str
    planes_involved: List[str]
    description: str
    severity: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PlaneBudgetRecord(BaseModel):
    budget_id: str
    plane_id: str
    budget_type: str
    total_amount: float
    used_amount: float = 0.0
    reserved_amount: float = 0.0


class PlanePressureRecord(BaseModel):
    pressure_id: str
    plane_id: str
    pressure_score: float
    drivers: Dict[str, float] = Field(default_factory=dict)


class MeshPolicyRecord(BaseModel):
    policy_id: str
    policy_family: str
    description: str


class MeshCoordinationRecord(BaseModel):
    coordination_id: str
    planes: List[str]
    topic: str


class PlaneSummaryRecord(BaseModel):
    plane_id: str
    health: PlaneHealthBand
    trust: PlaneTrustBand
    active_escalations: int
    budget_utilization: float


class DelegatedActionRecord(BaseModel):
    action_id: str
    plane_id: str
    delegation_id: str
    payload: Dict[str, Any]
    status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class EscalationCaseRecord(BaseModel):
    case_id: str
    source_plane_id: str
    target_plane_id: str
    reason: str
    context: Dict[str, Any] = Field(default_factory=dict)
    status: str = "open"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class EscalationOutcomeRecord(BaseModel):
    outcome_id: str
    case_id: str
    outcome: EscalationOutcome
    rationale: str
    resolved_at: datetime = Field(default_factory=datetime.utcnow)


class OverridePrecedenceRecord(BaseModel):
    override_id: str
    plane_id: str
    target_action: str
    precedence_level: int


class PolicyCollisionRecord(BaseModel):
    collision_id: str
    policies_involved: List[str]
    planes_involved: List[str]
    description: str


class MeshTopologyRecord(BaseModel):
    topology_id: str
    nodes: List[str]
    edges: List[Dict[str, str]]


class GovernanceLinkRecord(BaseModel):
    link_id: str
    source_id: str
    target_id: str
    link_type: str


class EscalationTriggerRecord(BaseModel):
    trigger_id: str
    trigger_type: str
    threshold: float


class EscalationPathRecord(BaseModel):
    path_id: str
    source_plane_id: str
    target_plane_id: str


class EscalationPriorityRecord(BaseModel):
    priority_id: str
    level: int
    description: str


class EscalationCouncilHintRecord(BaseModel):
    hint_id: str
    case_id: str
    recommendation: str


class MeshPolicyBindingRecord(BaseModel):
    binding_id: str
    policy_family: str
    owner_plane: str
    consumer_planes: List[str]
    override_rules: Dict[str, Any]
    precedence_rank: int
    violation_action: str


class MeshNodeRecord(BaseModel):
    node_id: str
    plane_id: str
    node_type: str


class MeshEdgeRecord(BaseModel):
    edge_id: str
    source_node_id: str
    target_node_id: str
    relationship: str


class MeshHotspotRecord(BaseModel):
    hotspot_id: str
    location: str
    intensity: float
    description: str


class MeshTopologySummaryRecord(BaseModel):
    summary_id: str
    node_count: int
    edge_count: int
    hotspots: List[MeshHotspotRecord]


class BudgetDelegationRecord(BaseModel):
    delegation_id: str
    parent_plane_id: str
    child_plane_id: str
    amount: float
    budget_type: str


class BudgetTransferRecord(BaseModel):
    transfer_id: str
    source_plane_id: str
    target_plane_id: str
    amount: float
    budget_type: str


class BudgetLockRecord(BaseModel):
    lock_id: str
    plane_id: str
    amount: float
    reason: str


class BudgetViolationRecord(BaseModel):
    violation_id: str
    plane_id: str
    budget_type: str
    attempted_amount: float
    available_amount: float


class EmergencyOverrideRecord(BaseModel):
    override_id: str
    issuer_plane_id: str
    target_plane_id: Optional[str]
    action: str
    reason: str
    active: bool = True
    issued_at: datetime = Field(default_factory=datetime.utcnow)


class OverrideExpiryRecord(BaseModel):
    expiry_id: str
    override_id: str
    expires_at: datetime


class OverrideCooldownRecord(BaseModel):
    cooldown_id: str
    plane_id: str
    ends_at: datetime


class DelegatedActionLedgerRecord(BaseModel):
    ledger_id: str
    action_id: str
    status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class DelegatedExecutionRecord(BaseModel):
    execution_id: str
    action_id: str
    result: str


class DelegationDenialRecord(BaseModel):
    denial_id: str
    delegation_id: str
    reason: str


class DelegationThrottleRecord(BaseModel):
    throttle_id: str
    plane_id: str
    reason: str
    active: bool = True


class PlaneSuspensionRecord(BaseModel):
    suspension_id: str
    plane_id: str
    reason: str
    active: bool = True
    suspended_at: datetime = Field(default_factory=datetime.utcnow)


class AutonomyReductionRecord(BaseModel):
    reduction_id: str
    plane_id: str
    previous_mode: DelegationMode
    new_mode: DelegationMode
    reason: str


class FederatedSummaryInput(BaseModel):
    planes: List[ControlPlaneRecord]
    budgets: List[PlaneBudgetRecord]
    escalations: List[EscalationCaseRecord]
    topology: MeshTopologyRecord
    suspensions: List[PlaneSuspensionRecord]
    overrides: List[EmergencyOverrideRecord]


class FederatedManifest(BaseModel):
    manifest_id: str
    planes: List[ControlPlaneRecord]
    active_escalations: List[EscalationCaseRecord]
    budget_summary: Dict[str, PlaneBudgetRecord]
    mesh_hotspots: List[MeshHotspotRecord]
    suspensions: List[PlaneSuspensionRecord]
    overrides: List[EmergencyOverrideRecord]
    generated_at: datetime = Field(default_factory=datetime.utcnow)
