from pydantic import BaseModel
from typing import List, Dict, Optional, Literal, Any
from datetime import datetime


class RemediationCopilotRecord(BaseModel):
    copilot_id: str
    copilot_family: str
    supported_playbook_families: List[str]
    approval_policy_ref: str
    rehearsal_policy_ref: str
    automation_preparation_policy_ref: str
    active_status: str
    warnings: List[str] = []


class CopilotSessionRecord(BaseModel):
    session_id: str
    incident_ref: str
    recommended_playbook_refs: List[str]
    selected_playbook_ref: Optional[str] = None
    current_stage: str
    review_packet_ref: Optional[str] = None
    approval_request_ref: Optional[str] = None
    rehearsal_refs: List[str] = []
    readiness_ref: Optional[str] = None
    warnings: List[str] = []


class CopilotRecommendationRecord(BaseModel):
    session_id: str
    incident_ref: str
    recommended_playbooks: List[str]
    rationale: str
    warnings: List[str] = []


class CopilotReviewPacketParams(BaseModel):
    session_id: str
    incident_summary: str
    matched_patterns: List[str]
    confidence_score: float
    selected_playbook_rationale: str
    scoped_steps: List[str]
    required_guards: List[str]
    rehearsal_proposal: str
    rollback_notes: str
    expected_signals: List[str]
    stop_conditions: List[str]
    approval_requirements: List[str]


class CopilotReviewPacketRecord(BaseModel):
    packet_id: str
    session_id: str
    incident_summary: str
    matched_patterns: List[str]
    confidence_score: float
    selected_playbook_rationale: str
    scoped_steps: List[str]
    rejected_step_alternatives: List[str]
    required_guards: List[str]
    rehearsal_proposal: str
    rollback_notes: str
    expected_signals: List[str]
    stop_conditions: List[str]
    approval_requirements: List[str]
    caveats: List[str] = []


class CopilotApprovalRequestParams(BaseModel):
    packet_ref: str
    approval_family: str
    scope: str
    max_duration_seconds: int
    allowed_step_families: List[str]
    forbidden_conditions: List[str]
    rollback_requirement: str
    observability_requirement: str
    review_owner: str


class CopilotApprovalRequestRecord(BaseModel):
    request_id: str
    packet_ref: str
    approval_family: str
    scope: str
    max_duration_seconds: int
    allowed_step_families: List[str]
    forbidden_conditions: List[str]
    rollback_requirement: str
    observability_requirement: str
    review_owner: str


class CopilotApprovalDecisionRecord(BaseModel):
    request_ref: str
    decision: Literal[
        "approved_for_rehearsal",
        "approved_with_scope_restrictions",
        "approved_with_caveats",
        "review_required",
        "blocked_by_risk",
        "denied",
        "expired",
    ]
    approved_by: str
    notes: str
    applied_restrictions: List[str] = []


class RehearsalLedgerRecord(BaseModel):
    ledger_id: str
    ledger_family: str
    target_incident_family: str
    entries: List[Dict[str, Any]]
    last_updated_at: datetime
    integrity_refs: Optional[List[str]] = None
    warnings: List[str] = []


class ExecutionReadinessRecord(BaseModel):
    readiness_id: str
    session_ref: str
    status: Literal[
        "not_ready",
        "review_only_ready",
        "rehearsal_ready",
        "staged_execution_preparation_ready",
        "blocked",
        "stale_ready",
        "superseded_ready",
    ]
    approval_completeness: bool
    scope_boundedness: bool
    rehearsal_success: bool
    guard_pass_status: bool
    rollback_completeness: bool
    observability_completeness: bool
    confidence_sufficiency: bool
    federated_playbook_adaptation_safety: bool
    no_unresolved_critical_blockers: bool
    freshness_of_incident_context: bool
    blockers: List[str] = []


class PlaybookExecutionPreparationRecord(BaseModel):
    preparation_id: str
    playbook_ref: str
    incident_ref: str
    scoped_steps: List[str]
    forbidden_steps: List[str]
    required_approvals: List[str]
    rehearsal_requirements: List[str]
    rollback_requirements: List[str]
    observability_requirements: List[str]
    current_status: str
    warnings: List[str] = []


class PortablePlaybookParams(BaseModel):
    family: str
    step_taxonomy: List[str]
    scope_constraints: List[str]
    required_guards: List[str]
    required_approvals: List[str]
    rehearsal_requirements: List[str]
    rollback_notes: str
    observability_expectations: List[str]
    known_safe_subset_notes: str
    nonportable_step_markers: List[str]
    confidence_notes: str


class PortablePlaybookRecord(BaseModel):
    playbook_id: str
    family: str
    step_taxonomy: List[str]
    scope_constraints: List[str]
    required_guards: List[str]
    required_approvals: List[str]
    rehearsal_requirements: List[str]
    rollback_notes: str
    observability_expectations: List[str]
    known_safe_subset_notes: str
    nonportable_step_markers: List[str]
    confidence_notes: str


class PlaybookAdaptationRecord(BaseModel):
    adaptation_id: str
    portable_playbook_ref: str
    outcome: Literal[
        "adapted_clean",
        "adapted_with_restrictions",
        "adapted_review_only",
        "adaptation_blocked",
        "quarantined_for_manual_mapping",
    ]
    applied_local_restrictions: List[str]
    warnings: List[str] = []


class AutomationEnvelopeParams(BaseModel):
    allowed_step_families: List[str]
    maximum_scope: str
    required_guards: List[str]
    required_approvals_retained: List[str]
    required_rehearsal_evidence: List[str]
    required_rollback_guarantees: List[str]
    forbidden_incident_families: List[str]
    observability_minimums: List[str]
    stop_conditions: List[str]


class AutomationEnvelopeRecord(BaseModel):
    envelope_id: str
    allowed_step_families: List[str]
    maximum_scope: str
    required_guards: List[str]
    required_approvals_retained: List[str]
    required_rehearsal_evidence: List[str]
    required_rollback_guarantees: List[str]
    forbidden_incident_families: List[str]
    observability_minimums: List[str]
    stop_conditions: List[str]
    expiration: datetime


class SelfHealingPreparationRecord(BaseModel):
    preparation_id: str
    session_ref: str
    eligibility_status: Literal[
        "not_candidate",
        "candidate_with_review",
        "bounded_candidate",
        "blocked_for_automation",
        "stale_candidate",
    ]
    envelope_ref: Optional[str] = None
    warnings: List[str] = []


class RehearsalEntryRecord(BaseModel):
    entry_id: str
    entry_family: Literal[
        "rehearsal_started",
        "rehearsal_step_passed",
        "rehearsal_step_failed",
        "rehearsal_stopped_by_guard",
        "rehearsal_assertion_failed",
        "rehearsal_rollback_check_passed",
        "rehearsal_completed",
        "readiness_updated",
    ]
    timestamp: datetime
    details: str
