from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from uuid import UUID

class ResilienceAdvisorRecord(BaseModel):
    advisor_id: str
    advisor_family: str
    supported_incident_families: List[str]
    memory_policy: Dict[str, Any]
    synthesis_policy: Dict[str, Any]
    orchestration_policy: Dict[str, Any]
    review_mode: str
    active_status: bool
    warnings: List[str] = Field(default_factory=list)

class AdvisoryWarningRecord(BaseModel):
    warning_code: str
    warning_message: str

class AdvisorySessionRecord(BaseModel):
    session_id: str
    advisor_id: str
    timestamp: datetime
    input_signals: Dict[str, Any]
    produced_recommendations: List[str]

class FailureSignatureRecord(BaseModel):
    source_family: Optional[str] = None
    event_families: List[str] = Field(default_factory=list)
    lag_profile: Optional[Dict[str, Any]] = None
    trust_drift_profile: Optional[Dict[str, Any]] = None
    replay_mismatch_burden: Optional[float] = None
    swarm_agreement_status: Optional[str] = None
    relay_health_status: Optional[str] = None
    routing_instability_markers: List[str] = Field(default_factory=list)
    degraded_mode_transitions: List[str] = Field(default_factory=list)
    quarantine_pressure: Optional[float] = None
    freshness_decay_shape: Optional[str] = None
    conformance_blockers: List[str] = Field(default_factory=list)

class FailurePatternRecord(BaseModel):
    pattern_id: str
    pattern_family: str
    incident_signature: FailureSignatureRecord
    trigger_conditions: List[str]
    observed_symptoms: List[str]
    root_cause_hypotheses: List[str]
    remediation_history: List[str]
    recovery_outcome_summary: str
    confidence_notes: str
    warnings: List[str] = Field(default_factory=list)

class FailurePatternMemoryRecord(BaseModel):
    memory_id: str
    patterns: List[FailurePatternRecord]
    last_updated: datetime

class PatternSimilarityRecord(BaseModel):
    pattern_id: str
    similarity_score: float
    similarity_band: str
    explanation: str

class PatternMatchRecord(BaseModel):
    incident_ref: str
    matches: List[PatternSimilarityRecord]
    top_match_band: str

class RootCauseHypothesisRecord(BaseModel):
    hypothesis_id: str
    hypothesis_family: str
    confidence_score: float
    support_signals: List[str]

class HypothesisSupportRecord(BaseModel):
    hypothesis_id: str
    support_score: float

class HypothesisConflictRecord(BaseModel):
    hypothesis_id_1: str
    hypothesis_id_2: str
    conflict_reason: str

class HypothesisConfidenceRecord(BaseModel):
    hypothesis_id: str
    confidence_band: str

class PlaybookPrerequisiteRecord(BaseModel):
    prerequisite_type: str
    condition: str
    is_met: bool

class PlaybookRiskRecord(BaseModel):
    risk_level: str
    description: str

class PlaybookRollbackNoteRecord(BaseModel):
    step_id: str
    rollback_action: str

class PlaybookStepRecord(BaseModel):
    step_order: int
    step_family: str
    rationale: str
    preconditions: List[str] = Field(default_factory=list)
    safety_bounds: str
    success_criteria: str
    rollback_note: Optional[str] = None
    observability_note: Optional[str] = None

class RemediationPlaybookRecord(BaseModel):
    playbook_id: str
    playbook_family: str
    target_incident_family: str
    synthesized_from_pattern_refs: List[str]
    steps: List[PlaybookStepRecord]
    prerequisites: List[PlaybookPrerequisiteRecord]
    risk_notes: List[PlaybookRiskRecord]
    rollback_notes: List[PlaybookRollbackNoteRecord]
    expected_signals: List[str]
    warnings: List[str] = Field(default_factory=list)

class RecoveryGuardRecord(BaseModel):
    guard_id: str
    guard_family: str
    outcome: str
    reason: str

class RecoveryCheckpointRecord(BaseModel):
    checkpoint_id: str
    checkpoint_family: str
    status: str

class RecoveryActionSequenceRecord(BaseModel):
    sequence_id: str
    steps: List[PlaybookStepRecord]

class RecoveryOrchestrationPlanRecord(BaseModel):
    plan_id: str
    target_incident_ref: str
    selected_playbook_ref: str
    recommended_sequence: List[PlaybookStepRecord]
    gating_requirements: List[str]
    review_requirements: List[str]
    bounded_scope: bool
    rollback_strategy: str
    observability_requirements: List[str]
    warnings: List[str] = Field(default_factory=list)

class AdvisoryConfidenceRecord(BaseModel):
    confidence_band: str
    score: float
    factors: Dict[str, Any]

class AdvisoryDecisionRecord(BaseModel):
    decision_type: str
    rationale: str
    confidence_band: str

class RecoveryConstraintRecord(BaseModel):
    constraint_type: str
    value: str

class RecoveryApprovalHintRecord(BaseModel):
    approval_type: str
    reason: str

class ResilienceAdvisorManifest(BaseModel):
    manifest_id: str
    advisors: List[ResilienceAdvisorRecord]
    timestamp: datetime

class RecoveryAuditRecord(BaseModel):
    audit_id: str
    plan_id: str
    outcomes: Dict[str, str]

# Memory models
class PatternMemoryIndexRecord(BaseModel):
    index_id: str
    pattern_refs: List[str]

class PatternTimelineRecord(BaseModel):
    pattern_id: str
    timeline_features: Dict[str, Any]

class PatternLayerImpactRecord(BaseModel):
    pattern_id: str
    affected_layers: List[str]

class PatternOutcomeRecord(BaseModel):
    pattern_id: str
    recovery_outcome: str
    duration_seconds: float

class PatternApplicabilityRecord(BaseModel):
    pattern_id: str
    constraints: List[str]

# Playbook Library
class PlaybookLibraryRecord(BaseModel):
    library_id: str
    playbooks: List[RemediationPlaybookRecord]

class PlaybookLibraryIndexRecord(BaseModel):
    library_id: str
    indexed_by_family: Dict[str, List[str]]

class PlaybookUsageRecord(BaseModel):
    playbook_id: str
    usage_count: int
    success_rate: float

class PlaybookSupersessionRecord(BaseModel):
    old_playbook_id: str
    new_playbook_id: str
    reason: str

# Decisions
class AdvisoryRecommendationRecord(BaseModel):
    recommendation_id: str
    decision_type: str
    plan_ref: Optional[str] = None
    confidence: AdvisoryConfidenceRecord
    why_this_pattern_match: str
    remaining_risks: List[str]

class RecommendationBlockerRecord(BaseModel):
    recommendation_id: str
    blocker_reason: str

class RecommendationEvidenceGapRecord(BaseModel):
    recommendation_id: str
    evidence_gap: str

class RecommendationRiskSummaryRecord(BaseModel):
    recommendation_id: str
    risk_summary: str

# Guard models
class SequencingConstraintRecord(BaseModel):
    constraint_id: str
    description: str

class PlanCheckpointEvaluationRecord(BaseModel):
    plan_id: str
    checkpoint_evaluations: Dict[str, str]

class RecoveryExitCriterionRecord(BaseModel):
    criterion_id: str
    is_met: bool

class StepExecutionEligibilityRecord(BaseModel):
    step_id: str
    is_eligible: bool
    reason: str
