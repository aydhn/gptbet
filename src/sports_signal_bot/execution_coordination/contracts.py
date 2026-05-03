from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Set
from enum import Enum
import datetime

class ScheduleStatus(str, Enum):
    SCHEDULE_REQUESTED = "schedule_requested"
    SCHEDULE_ADMITTED = "schedule_admitted"
    SCHEDULE_WAITING_TOKEN = "schedule_waiting_token"
    SCHEDULE_WAITING_ARBITRATION = "schedule_waiting_arbitration"
    SCHEDULE_SERIALIZED = "schedule_serialized"
    SCHEDULE_PARALLEL_READY = "schedule_parallel_ready"
    SCHEDULE_RUNTIME_ASSIGNED = "schedule_runtime_assigned"
    SCHEDULE_THROTTLED = "schedule_throttled"
    SCHEDULE_SUSPENDED = "schedule_suspended"
    SCHEDULE_BLOCKED = "schedule_blocked"
    SCHEDULE_SUPERSEDED = "schedule_superseded"
    SCHEDULE_COMPLETED = "schedule_completed"

class PriorityBand(str, Enum):
    ROLLBACK_PRIORITY = "rollback_priority"
    CLOSURE_PRIORITY = "closure_priority"
    CRITICAL_RECOVERY = "critical_recovery"
    STABILIZATION_PRIORITY = "stabilization_priority"
    REPAIR_PRIORITY = "repair_priority"
    REVIEW_ONLY_PRIORITY = "review_only_priority"
    OPPORTUNISTIC_PRIORITY = "opportunistic_priority"

class TokenBrokerStatus(str, Enum):
    BROKER_HEALTHY = "broker_healthy"
    BROKER_TOKEN_PRESSURE = "broker_token_pressure"
    BROKER_RENEWAL_BACKLOG = "broker_renewal_backlog"
    BROKER_CONTENTION_HIGH = "broker_contention_high"
    BROKER_DEGRADED = "broker_degraded"
    BROKER_SUSPENDED = "broker_suspended"

class TokenFamily(str, Enum):
    STAGED_EXECUTION_TOKEN = "staged_execution_token"
    REHEARSAL_EXECUTION_TOKEN = "rehearsal_execution_token"
    ROLLBACK_ONLY_TOKEN = "rollback_only_token"
    REVIEW_ONLY_EXECUTION_TOKEN = "review_only_execution_token"
    FEDERATED_ADAPTATION_TOKEN = "federated_adaptation_token"
    CLOSURE_VERIFICATION_TOKEN = "closure_verification_token"
    RENEWAL_CANDIDATE_TOKEN = "renewal_candidate_token"

class ContentionFamily(str, Enum):
    SHARED_SOURCE_CONTENTION = "shared_source_contention"
    TOKEN_POOL_CONTENTION = "token_pool_contention"
    ROLLBACK_BINDING_CONTENTION = "rollback_binding_contention"
    REPLAY_CAPACITY_CONTENTION = "replay_capacity_contention"
    OBSERVABILITY_BANDWIDTH_CONTENTION = "observability_bandwidth_contention"
    CLOSURE_CONTROLLER_CONTENTION = "closure_controller_contention"
    APPROVAL_FRESHNESS_CONTENTION = "approval_freshness_contention"
    RUNTIME_WINDOW_OVERLAP_CONTENTION = "runtime_window_overlap_contention"
    FEDERATED_ADAPTATION_CONTENTION = "federated_adaptation_contention"
    DEGRADED_MODE_TRANSITION_CONTENTION = "degraded_mode_transition_contention"
    ROUTE_CACHE_SURFACE_CONTENTION = "route_cache_surface_contention"
    OVERLAY_MUTATION_CONTENTION = "overlay_mutation_contention"

class ContentionSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ConcurrencyClass(str, Enum):
    STRICTLY_SERIAL = "strictly_serial"
    BOUNDED_PARALLEL_LOW_RISK = "bounded_parallel_low_risk"
    BOUNDED_PARALLEL_MIXED_RISK_FORBIDDEN = "bounded_parallel_mixed_risk_forbidden"
    CLOSURE_EXCLUSIVE = "closure_exclusive"
    ROLLBACK_EXCLUSIVE = "rollback_exclusive"
    REVIEW_ONLY_PARALLEL = "review_only_parallel"
    SOURCE_SCOPED_SERIAL = "source_scoped_serial"

class FabricStatus(str, Enum):
    FABRIC_NORMAL = "fabric_normal"
    FABRIC_CAUTIOUS = "fabric_cautious"
    FABRIC_THROTTLED = "fabric_throttled"
    FABRIC_CONTENTION_HEAVY = "fabric_contention_heavy"
    FABRIC_CLOSURE_PRIORITY_MODE = "fabric_closure_priority_mode"
    FABRIC_ROLLBACK_PRIORITY_MODE = "fabric_rollback_priority_mode"
    FABRIC_DEGRADED = "fabric_degraded"
    FABRIC_RECOVERY_MODE = "fabric_recovery_mode"

class SchedulingWindowRecord(BaseModel):
    window_id: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    max_parallel_lanes: int
    reserved_for_rollback: bool = False
    reserved_for_closure: bool = False

class LaneScheduleRecord(BaseModel):
    schedule_id: str
    lane_ref: str
    requested_runtime_window: SchedulingWindowRecord
    assigned_runtime_window: Optional[SchedulingWindowRecord] = None
    priority_band: PriorityBand
    contention_status: str
    token_status: str
    closure_dependency_status: str
    schedule_status: ScheduleStatus
    warnings: List[str] = []

class TokenAllocationRecord(BaseModel):
    token_ref: str
    lane_ref: str
    allocation_time: datetime.datetime
    allocation_scope: str
    remaining_window: int
    step_quota: int
    renewal_eligibility: bool
    preemption_eligibility: bool
    closure_dependency: str
    warnings: List[str] = []

class TokenReservationRecord(BaseModel):
    reservation_id: str
    lane_ref: str
    desired_window: int
    desired_step_family_set: List[str]
    broker_priority: int
    reservation_status: str
    expiration: datetime.datetime

class ApprovalTokenBrokerRecord(BaseModel):
    broker_id: str
    token_pool_refs: List[str]
    active_allocations: List[TokenAllocationRecord]
    pending_reservations: List[TokenReservationRecord]
    renewal_backlog: int
    broker_policy_ref: str
    health_status: TokenBrokerStatus
    warnings: List[str] = []

class TokenBrokerDecisionRecord(BaseModel):
    decision_id: str
    lane_ref: str
    granted: bool
    allocation: Optional[TokenAllocationRecord] = None
    reason: str

class TokenPreemptionRecord(BaseModel):
    preemption_id: str
    preempting_lane_ref: str
    preempted_lane_ref: str
    reason: str
    time: datetime.datetime

class ContentionRecord(BaseModel):
    contention_id: str
    contention_family: ContentionFamily
    involved_lane_refs: List[str]
    shared_surface: str
    severity: ContentionSeverity
    current_resolution_state: str
    arbitration_ref: Optional[str] = None
    warnings: List[str] = []

class ArbitrationDecisionRecord(BaseModel):
    arbitration_id: str
    contention_id: str
    decision_type: str  # e.g., allow_parallel_execution, serialize_lanes
    winning_lane_refs: List[str]
    deferred_lane_refs: List[str]
    reason: str

class CoordinationLedgerEntryRecord(BaseModel):
    entry_id: str
    timestamp: datetime.datetime
    lane_ref: str
    event_type: str
    details: Dict[str, Any]

class ExecutionCoordinationFabricRecord(BaseModel):
    fabric_id: str
    active_lane_refs: List[str]
    queue_refs: List[str]
    scheduler_ref: str
    token_broker_ref: str
    contention_refs: List[str]
    arbitration_refs: List[str]
    coordination_status: FabricStatus
    warnings: List[str] = []

class CoordinationHealthRecord(BaseModel):
    timestamp: datetime.datetime
    fabric_status: FabricStatus
    active_schedules: int
    waiting_schedules: int
    active_contentions: int
    backlog_pressure_score: float
    warnings: List[str] = []

class MultiLaneSchedulerRecord(BaseModel):
    scheduler_id: str
    active_schedules: List[LaneScheduleRecord]
    waiting_schedules: List[LaneScheduleRecord]
    completed_schedules: List[LaneScheduleRecord]

class CoordinationAuditRecord(BaseModel):
    audit_id: str
    timestamp: datetime.datetime
    target_ref: str
    event: str
    outcome: str

class FairnessAdjustmentRecord(BaseModel):
    lane_ref: str
    original_priority: PriorityBand
    adjusted_priority: PriorityBand
    reason: str
