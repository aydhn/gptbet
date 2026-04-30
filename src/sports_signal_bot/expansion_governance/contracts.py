from pydantic import BaseModel, Field
from enum import Enum
from typing import Dict, Any, List, Optional
from datetime import datetime

class ExpansionStatus(str, Enum):
    EXPANSION_NORMAL = "expansion_normal"
    EXPANSION_CAUTIOUS = "expansion_cautious"
    EXPANSION_THROTTLED = "expansion_throttled"
    EXPANSION_HOLD = "expansion_hold"
    SELECTIVE_FAMILY_FREEZE = "selective_family_freeze"
    GLOBAL_EMERGENCY_PAUSE = "global_emergency_pause"
    ROLLBACK_STABILIZATION_MODE = "rollback_stabilization_mode"
    RECOVERY_MONITORING_MODE = "recovery_monitoring_mode"

class ExpansionWaveStatus(str, Enum):
    SCHEDULED_WAVE = "scheduled_wave"
    ACTIVE_WAVE = "active_wave"
    THROTTLED_WAVE = "throttled_wave"
    PAUSED_WAVE = "paused_wave"
    SHRUNK_WAVE = "shrunk_wave"
    ROLLBACK_WAVE = "rollback_wave"
    COMPLETED_WAVE = "completed_wave"
    ABANDONED_WAVE = "abandoned_wave"

class ConflictSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class PressureBand(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    SEVERE = "severe"
    CRITICAL = "critical"

class CouncilDecision(str, Enum):
    CONTINUE_EXPANSION = "continue_expansion"
    THROTTLE_EXPANSION = "throttle_expansion"
    HOLD_NEW_GROWTH = "hold_new_growth"
    FREEZE_FAMILY = "freeze_family"
    PAUSE_ALL_GROWTH = "pause_all_growth"
    INITIATE_SELECTIVE_ROLLBACK = "initiate_selective_rollback"
    ENTER_RECOVERY_MODE = "enter_recovery_mode"

class ExpansionControlStateRecord(BaseModel):
    control_state_id: str
    active_cohort_ids: List[str] = Field(default_factory=list)
    active_wave_ids: List[str] = Field(default_factory=list)
    global_status: ExpansionStatus = ExpansionStatus.EXPANSION_NORMAL
    global_risk_budget_usage: float = 0.0
    global_pressure_score: float = 0.0
    emergency_flags: List[str] = Field(default_factory=list)
    family_freeze_states: Dict[str, bool] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    warnings: List[str] = Field(default_factory=list)

class ExpansionWaveRecord(BaseModel):
    wave_id: str
    included_cohorts: List[str] = Field(default_factory=list)
    target_families: List[str] = Field(default_factory=list)
    concurrency_level: int
    budget_cost: float
    activation_window: Dict[str, Any]
    coordination_notes: str
    current_status: ExpansionWaveStatus = ExpansionWaveStatus.SCHEDULED_WAVE
    warnings: List[str] = Field(default_factory=list)

class ExpansionBudgetRecord(BaseModel):
    budget_id: str
    budget_family: str
    total_budget: float
    used_budget: float = 0.0
    reserved_budget: float = 0.0
    remaining_budget: float
    budget_status: str
    drivers: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    warnings: List[str] = Field(default_factory=list)

class BudgetBurnRecord(BaseModel):
    burn_id: str
    budget_id: str
    burned_amount: float
    reason: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ExpansionPressureRecord(BaseModel):
    pressure_id: str
    pressure_score: float
    pressure_band: PressureBand
    drivers: Dict[str, float] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CrossCohortConflictRecord(BaseModel):
    conflict_id: str
    conflict_family: str
    involved_cohorts: List[str]
    severity: ConflictSeverity
    description: str

class CrossFamilyInteractionRecord(BaseModel):
    interaction_id: str
    involved_families: List[str]
    interaction_type: str
    severity: ConflictSeverity

class CircuitBreakerRecord(BaseModel):
    breaker_id: str
    trigger_condition: str
    action_taken: str
    affected_scope: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CircuitBreakerTriggerRecord(BaseModel):
    trigger_id: str
    trigger_type: str
    threshold_exceeded: bool
    description: str

class CircuitBreakerActionRecord(BaseModel):
    action_id: str
    trigger_id: str
    action_type: str
    manual_ack_required: bool

class BreakerEvaluationRecord(BaseModel):
    evaluation_id: str
    triggers_fired: List[CircuitBreakerTriggerRecord]
    actions_proposed: List[CircuitBreakerActionRecord]

class BreakerRecoveryRecord(BaseModel):
    recovery_id: str
    breaker_id: str
    recovery_status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class EmergencyPauseRecord(BaseModel):
    pause_id: str
    reason: str
    paused_at: datetime = Field(default_factory=datetime.utcnow)
    paused_cohorts: List[str] = Field(default_factory=list)
    paused_waves: List[str] = Field(default_factory=list)

class SelectiveRollbackDirectiveRecord(BaseModel):
    directive_id: str
    reason: str
    target_cohorts: List[str] = Field(default_factory=list)
    target_families: List[str] = Field(default_factory=list)
    rollback_level: str

class GlobalThrottleDecisionRecord(BaseModel):
    decision_id: str
    throttle_level: str
    reason: str
    affected_families: List[str]

class ExpansionCouncilRecord(BaseModel):
    council_id: str
    decision: CouncilDecision
    rationale: str
    lens_evaluations: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ControlTowerSummaryRecord(BaseModel):
    summary_id: str
    global_status: str
    active_waves: int
    active_cohorts: int
    budget_usage_summary: Dict[str, float]
    global_pressure_band: str
    family_freezes: List[str]
    top_blockers: List[str]
    emergency_breaker_state: str
    recommended_actions: List[str]
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class ExpansionGovernanceManifest(BaseModel):
    manifest_id: str
    control_state: ExpansionControlStateRecord
    council_decision: ExpansionCouncilRecord
    control_tower_summary: ControlTowerSummaryRecord
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class ExpansionDecisionRecord(BaseModel):
    decision_id: str
    target_id: str
    decision_type: str
    reason: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class GlobalFreezeRecord(BaseModel):
    freeze_id: str
    frozen_families: List[str]
    reason: str
    frozen_at: datetime = Field(default_factory=datetime.utcnow)

class ExpansionWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class WaveCoordinationRecord(BaseModel):
    coordination_id: str
    wave_id: str
    coordination_status: str

class FamilyExposureRecord(BaseModel):
    exposure_id: str
    family: str
    concurrent_cohorts: int
    total_budget_usage: float

class ExpansionAuditRecord(BaseModel):
    audit_id: str
    action_type: str
    target_id: str
    details: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class InteractionNodeRecord(BaseModel):
    node_id: str
    node_type: str # cohort, wave, family, shared_resource
    name: str

class InteractionEdgeRecord(BaseModel):
    edge_id: str
    source_node_id: str
    target_node_id: str
    edge_type: str # competes_with, depends_on, increases_risk_for, etc.

class ExpansionInteractionGraphRecord(BaseModel):
    graph_id: str
    nodes: List[InteractionNodeRecord]
    edges: List[InteractionEdgeRecord]

class ThrottleDirectiveRecord(BaseModel):
    directive_id: str
    target_scope: Dict[str, Any]
    throttle_rules: Dict[str, Any]

class ThrottlePolicyRecord(BaseModel):
    policy_id: str
    description: str
    rules: Dict[str, Any]

class ThrottleEffectRecord(BaseModel):
    effect_id: str
    directive_id: str
    impacted_cohorts: int

class WaveCooldownRecord(BaseModel):
    cooldown_id: str
    wave_id: str
    ends_at: datetime

class WaveAdmissionRuleRecord(BaseModel):
    rule_id: str
    description: str
    conditions: Dict[str, Any]

class FamilySequencingRecord(BaseModel):
    sequence_id: str
    family_order: List[str]

class RollbackCapacityRecord(BaseModel):
    capacity_id: str
    total_capacity: int
    used_capacity: int
    available_capacity: int

class RecoveryModeRecord(BaseModel):
    mode_id: str
    is_active: bool
    entered_at: Optional[datetime] = None
    exit_criteria: List[str] = Field(default_factory=list)

class StabilizationWindowRecord(BaseModel):
    window_id: str
    target_id: str
    ends_at: datetime
