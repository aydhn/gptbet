from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
import datetime

class GuardOutcome(str, Enum):
    PASS = "guard_pass"
    WARN = "guard_warn"
    REVIEW_REQUIRED = "review_required"
    BLOCK = "guard_block"
    BLOCK_CRITICAL = "guard_block_critical"

class RuntimeStatus(str, Enum):
    INITIALIZED = "runtime_initialized"
    AWAITING_WINDOW = "awaiting_runtime_window"
    AWAITING_VALIDATION = "awaiting_token_validation"
    READY = "ready_to_enter_step"
    EXECUTING = "executing_step"
    PAUSED_BY_GUARD = "paused_by_guard"
    PAUSED_BY_STOP = "paused_by_stop_condition"
    RENEWAL_PENDING = "renewal_pending"
    RENEWAL_DENIED = "renewal_denied"
    ROLLBACK_PENDING = "rollback_pending"
    ROLLBACK_EXECUTING = "rollback_executing"
    CLOSURE_VERIFYING = "closure_verifying"
    COMPLETED_CLEAN = "completed_clean"
    COMPLETED_CAVEATED = "completed_with_caveats"
    FAILED = "failed_runtime"
    BLOCKED = "blocked_runtime"
    EXPIRED = "expired_runtime"

class StepStatus(str, Enum):
    PENDING = "pending"
    EXECUTING = "executing"
    EXECUTED = "executed"
    CHECKPOINT_PENDING = "checkpoint_pending"
    CHECKPOINT_FAILED = "checkpoint_failed"
    ROLLBACK_REQUIRED = "rollback_required"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    EXPIRED = "expired"

class RenewalStatus(str, Enum):
    REQUESTED = "renewal_requested"
    UNDER_REVIEW = "renewal_under_review"
    APPROVED = "renewal_approved"
    APPROVED_TIGHTER = "renewal_approved_with_tighter_scope"
    DENIED = "renewal_denied"
    EXPIRED = "renewal_expired"
    SUPERSEDED = "renewal_superseded"

class RollbackStatus(str, Enum):
    IDLE = "rollback_idle"
    ARMED = "rollback_armed"
    READY = "rollback_ready"
    TRIGGERED = "rollback_triggered"
    EXECUTING = "rollback_executing"
    CHECKPOINT_VERIFYING = "rollback_checkpoint_verifying"
    COMPLETED_CLEAN = "rollback_completed_clean"
    COMPLETED_CAVEATED = "rollback_completed_with_caveats"
    FAILED = "rollback_failed"
    BLOCKED = "rollback_blocked"

class ClosureStatus(str, Enum):
    PENDING = "closure_pending"
    SIGNAL_COLLECTION = "closure_signal_collection"
    VERIFYING = "closure_verifying"
    CLEAN = "closure_clean"
    CAVEATED = "closure_caveated"
    FAILED = "closure_failed"
    ROLLBACK_RECOMMENDED = "rollback_recommended"
    REVIEW_REQUIRED = "review_required_after_closure"
    STALE = "closure_stale"

class CompletionClass(str, Enum):
    VERIFIED = "completion_verified"
    VERIFIED_CAVEATS = "completion_verified_with_caveats"
    NOT_VERIFIED = "completion_not_verified"
    FAILED = "completion_failed"
    SUPERSEDED = "completion_superseded"
    REVIEW_REQUIRED = "completion_review_required"

class LiveExecutionEngineRecord(BaseModel):
    engine_id: str
    engine_family: str
    supported_lane_families: List[str]
    runtime_policy_ref: str
    renewal_policy_ref: str
    rollback_policy_ref: str
    closure_policy_ref: str
    active_status: str
    warnings: List[str] = []

class RuntimeWindowRecord(BaseModel):
    start_time: str
    end_time: str
    max_duration_sec: int
    allowed_step_count: int
    allowed_step_families: List[str]
    pause_allowance_sec: int
    renewal_allowed: bool
    rollback_window_sec: int
    closure_verification_window_sec: int

class ExecutionLaneRuntimeRecord(BaseModel):
    runtime_id: str
    lane_ref: str
    token_ref: str
    runtime_window: RuntimeWindowRecord
    active_step_ref: Optional[str] = None
    runtime_status: RuntimeStatus
    observed_checkpoints: List[str] = []
    triggered_stop_conditions: List[str] = []
    closure_ref: Optional[str] = None
    warnings: List[str] = []

class RuntimeStepRecord(BaseModel):
    step_ref: str
    step_family: str
    planned_order: int
    actual_start: Optional[str] = None
    actual_end: Optional[str] = None
    token_scope_validation: bool = False
    pre_step_guard_state: str = ""
    post_step_checkpoints: List[str] = []
    observability_refs: List[str] = []
    rollback_ready_state: bool = False
    step_status: StepStatus = StepStatus.PENDING
    warnings: List[str] = []

class ExecutionTokenRenewalRecord(BaseModel):
    renewal_id: str
    prior_token_ref: str
    lane_ref: str
    renewal_request_ref: str
    renewal_decision_ref: str
    new_token_ref: Optional[str] = None
    renewal_status: RenewalStatus
    warnings: List[str] = []

class LaneRollbackAutomatonRecord(BaseModel):
    automaton_id: str
    lane_ref: str
    rollback_binding_ref: str
    current_state: RollbackStatus
    transition_refs: List[str] = []
    trigger_refs: List[str] = []
    rollback_status: RollbackStatus
    warnings: List[str] = []

class SupervisedClosureControllerRecord(BaseModel):
    controller_id: str
    lane_ref: str
    closure_session_ref: str
    required_closure_signals: List[str] = []
    required_checkpoint_refs: List[str] = []
    closure_status: ClosureStatus
    decision_ref: Optional[str] = None
    warnings: List[str] = []

class RuntimeLedgerEntryRecord(BaseModel):
    entry_id: str
    runtime_id: str
    timestamp: str
    event_type: str
    details: Dict[str, Any] = {}

class LiveExecutionManifest(BaseModel):
    manifest_id: str
    timestamp: str
    runtimes: List[ExecutionLaneRuntimeRecord]
    renewals: List[ExecutionTokenRenewalRecord]
    rollback_automata: List[LaneRollbackAutomatonRecord]
    closure_controllers: List[SupervisedClosureControllerRecord]
    summary: Dict[str, Any] = {}
