from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class AdjudicationSeverity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class AdjudicationQueuePriority(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"
    urgent = "urgent"

class AdjudicationCaseFamily(str, Enum):
    data_conflict_case = "data_conflict_case"
    identity_mapping_case = "identity_mapping_case"
    result_settlement_case = "result_settlement_case"
    odds_arbitration_case = "odds_arbitration_case"
    policy_boundary_case = "policy_boundary_case"
    why_not_review_case = "why_not_review_case"
    provider_reliability_case = "provider_reliability_case"
    release_judgment_case = "release_judgment_case"
    repeated_pattern_case = "repeated_pattern_case"
    knowledge_suggestion_case = "knowledge_suggestion_case"

class ResolutionType(str, Enum):
    # Data / Entity
    accept_source_a_over_b = "accept_source_a_over_b"
    override_field_value = "override_field_value"
    confirm_consensus = "confirm_consensus"
    mark_dispute_unresolved = "mark_dispute_unresolved"
    resolve_team_alias = "resolve_team_alias"
    resolve_event_identity = "resolve_event_identity"
    mark_provider_field_untrusted = "mark_provider_field_untrusted"
    split_merged_entities = "split_merged_entities"

    # Decision / Policy
    confirm_policy_decision = "confirm_policy_decision"
    mark_false_block = "mark_false_block"
    mark_false_no_bet = "mark_false_no_bet"
    escalate_to_rule_suggestion = "escalate_to_rule_suggestion"
    keep_block_with_note = "keep_block_with_note"
    classify_borderline_case = "classify_borderline_case"

    # Knowledge / Memory
    create_precedent = "create_precedent"
    update_precedent = "update_precedent"
    deprecate_precedent = "deprecate_precedent"
    create_rule_suggestion = "create_rule_suggestion"
    promote_feedback_to_memory = "promote_feedback_to_memory"
    reject_feedback_for_memory = "reject_feedback_for_memory"

    # Provider / Trust
    penalize_provider_for_family = "penalize_provider_for_family"
    clear_provider_penalty = "clear_provider_penalty"
    require_manual_review_for_provider_pattern = "require_manual_review_for_provider_pattern"
    confirm_recurring_conflict_pattern = "confirm_recurring_conflict_pattern"


class AdjudicationCaseStatus(str, Enum):
    queued = "queued"
    in_review = "in_review"
    resolved = "resolved"
    resolved_with_caveat = "resolved_with_caveat"
    unresolved = "unresolved"
    deferred = "deferred"
    escalated = "escalated"
    superseded = "superseded"
    archived = "archived"

class FeedbackStatus(str, Enum):
    captured = "captured"
    pending_validation = "pending_validation"
    accepted_for_memory = "accepted_for_memory"
    accepted_for_limited_scope = "accepted_for_limited_scope"
    rejected_for_memory = "rejected_for_memory"
    deprecated = "deprecated"
    superseded = "superseded"

class KnowledgeEntryStatus(str, Enum):
    active = "active"
    provisional = "provisional"
    expired = "expired"
    deprecated = "deprecated"
    archived = "archived"

class AutoApplyLevel(str, Enum):
    none = "none"
    advisory_only = "advisory_only"
    scoped_auto_apply = "scoped_auto_apply"
    approval_required = "approval_required"

class KnowledgeScopeType(str, Enum):
    single_entity = "single_entity"
    single_provider_family = "single_provider_family"
    sport_specific = "sport_specific"
    market_specific = "market_specific"
    provider_family_scoped = "provider_family_scoped"
    season_window = "season_window"
    global_advisory_only = "global_advisory_only"

class MemoryType(str, Enum):
    alias_resolution_memory = "alias_resolution_memory"
    provider_conflict_memory = "provider_conflict_memory"
    policy_boundary_memory = "policy_boundary_memory"
    result_resolution_memory = "result_resolution_memory"
    release_judgment_memory = "release_judgment_memory"
    review_pattern_memory = "review_pattern_memory"

class AdjudicationCaseRecord(BaseModel):
    case_id: str
    case_type: AdjudicationCaseFamily
    target_entity_type: str
    target_entity_id: str
    sport: Optional[str] = None
    market_type: Optional[str] = None
    source_component: str
    severity: AdjudicationSeverity
    evidence_bundle_ref: str
    dispute_refs: List[str] = Field(default_factory=list)
    current_status: AdjudicationCaseStatus = AdjudicationCaseStatus.queued
    queue_priority: AdjudicationQueuePriority = AdjudicationQueuePriority.normal
    created_at: datetime = Field(default_factory=datetime.utcnow)
    warnings: List[str] = Field(default_factory=list)

class AdjudicationDecisionRecord(BaseModel):
    decision_id: str
    case_id: str
    operator_id: str
    decision_type: str
    resolution_type: ResolutionType
    resolution_payload: Dict[str, Any]
    confidence_in_resolution: float
    rationale_code: str
    operator_note: str
    applied_scope: str
    decision_timestamp_utc: datetime = Field(default_factory=datetime.utcnow)
    requires_secondary_review: bool = False
    warnings: List[str] = Field(default_factory=list)
    secondary_reviewer_id: Optional[str] = None
    secondary_review_status: Optional[str] = None

class ResolutionRecord(BaseModel):
    resolution_id: str
    case_id: str
    resolution_family: str
    resolution_status: str
    corrected_value: Optional[Any] = None
    chosen_source: Optional[str] = None
    selected_precedent: Optional[str] = None
    feedback_eligibility: bool
    memory_write_allowed: bool
    effective_scope: str
    expiry: Optional[datetime] = None
    related_entities: List[str] = Field(default_factory=list)
    caveats: List[str] = Field(default_factory=list)

class ResolutionReasonRecord(BaseModel):
    reason_code: str
    description: str

class KnowledgeScopeRecord(BaseModel):
    scope_type: KnowledgeScopeType
    target_value: str
    constraints: Dict[str, Any] = Field(default_factory=dict)

class PrecedentRecord(BaseModel):
    precedent_id: str
    precedent_title: str
    case_family: AdjudicationCaseFamily
    pattern_signature: str
    applicable_scope: KnowledgeScopeRecord
    source_constraints: Dict[str, Any] = Field(default_factory=dict)
    confidence_band: str
    created_from_case: str
    created_by_operator: str
    validity_window: str
    supersedes: Optional[List[str]] = Field(default_factory=list)
    superseded_by: Optional[str] = None
    usage_count: int = 0
    review_status: str

class MemoryLinkRecord(BaseModel):
    source_case_id: str
    target_memory_id: str
    link_type: str

class FeedbackSignalRecord(BaseModel):
    signal_id: str
    source_resolution_id: str
    signal_type: str
    payload: Dict[str, Any]
    status: FeedbackStatus = FeedbackStatus.captured
    confidence: float

class KnowledgeEntryRecord(BaseModel):
    entry_id: str
    memory_type: MemoryType
    schema_version: str = "1.0"
    content: Dict[str, Any]
    scope: KnowledgeScopeRecord
    status: KnowledgeEntryStatus = KnowledgeEntryStatus.active
    derived_from_feedback_ids: List[str] = Field(default_factory=list)
    expiry: Optional[datetime] = None

class AdjudicationQueueRecord(BaseModel):
    queue_id: str
    cases: List[AdjudicationCaseRecord] = Field(default_factory=list)

class AdjudicationSummaryRecord(BaseModel):
    open_cases: int
    resolved_cases: int
    unresolved_cases: int
    cases_by_type: Dict[str, int]
    cases_by_severity: Dict[str, int]
    memory_entries_created: int
    precedent_match_rate: float
    feedback_accepted_count: int
    feedback_rejected_count: int
    urgent_backlog_count: int
    secondary_review_required_count: int

class AdjudicationManifest(BaseModel):
    manifest_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"
    summary: AdjudicationSummaryRecord
    case_ids: List[str]

class ResolutionAuditRecord(BaseModel):
    audit_id: str
    resolution_id: str
    operator_id: str
    action: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class FeedbackApplicationRecord(BaseModel):
    application_id: str
    feedback_id: str
    auto_apply_allowed: bool
    requires_secondary_review: bool
    scope_limit: str
    expiry: Optional[datetime] = None
    risk_level: str
    consumer_components: List[str] = Field(default_factory=list)

class RuleSuggestionRecord(BaseModel):
    suggestion_id: str
    case_id: str
    proposed_rule: str
    rationale: str

class HumanCorrectionRecord(BaseModel):
    correction_id: str
    case_id: str
    corrected_field: str
    old_value: Any
    new_value: Any
    resolution_basis: str
    evidence_refs: List[str] = Field(default_factory=list)
    scope: str
    confidence: float
    reversibility: bool
    propagate_to_memory: bool

class FeedbackApplicationPolicy(BaseModel):
    auto_apply_allowed: bool
    requires_secondary_review: bool
    scope_limit: str
    expiry: Optional[str] = None
    risk_level: str
    consumer_components: List[str] = Field(default_factory=list)

class PolicyFeedbackRecord(BaseModel):
    feedback_id: str
    case_id: str
    policy_ref: str
    feedback_note: str

class ThresholdFeedbackRecord(BaseModel):
    feedback_id: str
    case_id: str
    threshold_ref: str
    suggested_value: float
    rationale: str

class RuleSuggestionBundleRecord(BaseModel):
    bundle_id: str
    suggestions: List[RuleSuggestionRecord]
