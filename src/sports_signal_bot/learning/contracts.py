from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class SupportStrength(str, Enum):
    weak = "weak"
    moderate = "moderate"
    strong = "strong"
    insufficient = "insufficient"

class SuggestionConfidenceBand(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"
    exploratory_only = "exploratory_only"
    unsafe_to_apply = "unsafe_to_apply"

class SuggestionRiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class RecommendationMode(str, Enum):
    advisory_only = "advisory_only"
    candidate_patch = "candidate_patch"
    candidate_rule_bundle = "candidate_rule_bundle"
    manual_review_required = "manual_review_required"
    blocked = "blocked"

class SuggestionStatus(str, Enum):
    generated = "generated"
    advisory_only = "advisory_only"
    pending_review = "pending_review"
    approved_for_simulation = "approved_for_simulation"
    rejected = "rejected"
    superseded = "superseded"
    promoted_to_candidate_patch = "promoted_to_candidate_patch"
    archived = "archived"

class SuggestionScopeType(str, Enum):
    single_entity = "single_entity"
    provider_and_family_scoped = "provider_and_family_scoped"
    sport_specific = "sport_specific"
    market_specific = "market_specific"
    strategy_specific = "strategy_specific"
    slot_specific = "slot_specific"
    seasonal_window_scoped = "seasonal_window_scoped"
    advisory_global = "advisory_global"
    prohibited_global_change = "prohibited_global_change"

class SuggestionFamily(str, Enum):
    provider_priority_adjustment = "provider_priority_adjustment_suggestion"
    provider_penalty_damper = "provider_penalty_damper_suggestion"
    alias_resolution_memory = "alias_resolution_memory_suggestion"
    conflict_severity_threshold = "conflict_severity_threshold_suggestion"
    low_confidence_acceptance_rule = "low_confidence_acceptance_rule_suggestion"
    stable_source_preference = "stable_source_preference_suggestion"
    odds_outlier_rule_tuning = "odds_outlier_rule_tuning_suggestion"

    no_bet_zone_boundary = "no_bet_zone_boundary_suggestion"
    borderline_candidate_policy = "borderline_candidate_policy_suggestion"
    threshold_band_shift = "threshold_band_shift_suggestion"
    rationale_priority_tuning = "rationale_priority_tuning_suggestion"
    approval_gate_threshold = "approval_gate_threshold_suggestion"
    market_specific_threshold_refinement = "market_specific_threshold_refinement_suggestion"

    source_family_prior_adjustment = "source_family_prior_adjustment_suggestion"
    regime_fit_damping_tuning = "regime_fit_damping_tuning_suggestion"
    disagreement_penalty_tuning = "disagreement_penalty_tuning_suggestion"
    calibrated_preference_rule = "calibrated_preference_rule_suggestion"
    stale_source_penalty_tuning = "stale_source_penalty_tuning_suggestion"

    anomaly_threshold_tuning = "anomaly_threshold_tuning_suggestion"
    freeze_trigger_sensitivity = "freeze_trigger_sensitivity_suggestion"
    degrade_policy_tuning = "degrade_policy_tuning_suggestion"
    canary_guard_tightening = "canary_guard_tightening_suggestion"
    rollback_trigger_advisory = "rollback_trigger_advisory_suggestion"

    precedent_scope_narrowing = "precedent_scope_narrowing_suggestion"
    feedback_auto_apply_restriction = "feedback_auto_apply_restriction_suggestion"
    secondary_review_threshold = "secondary_review_threshold_suggestion"
    memory_expiry_adjustment = "memory_expiry_adjustment_suggestion"


class FeedbackSignalAggregateRecord(BaseModel):
    aggregate_id: str
    target_component_family: str
    signal_type: str
    aggregated_cases: List[str]
    total_signals: int
    common_payload_elements: Dict[str, Any]
    time_span_days: int
    contradictory_signals_count: int

class PatternSupportRecord(BaseModel):
    support_count: int
    distinct_case_count: int
    distinct_operator_count: Optional[int] = None
    distinct_period_count: int
    evidence_diversity_score: float
    contradiction_burden: float
    recency_weight: float
    precedent_alignment: float
    strength: SupportStrength

class PatternCandidateRecord(BaseModel):
    pattern_id: str
    pattern_signature: str
    component_family: str
    condition_summary: Dict[str, Any]
    support: PatternSupportRecord
    unique_case_count: int
    operator_consistency: float
    time_span: str
    scope: str
    contradictory_cases: List[str]
    candidate_action: str

class RuleExtractionRecord(BaseModel):
    extraction_id: str
    pattern_id: str
    condition_block: Dict[str, Any]
    action_block: Dict[str, Any]
    exclusions: List[str]
    safety_constraints: Dict[str, Any]
    expiry_or_review_window: str
    target_config_family: str

class SuggestionScopeRecord(BaseModel):
    scope_type: SuggestionScopeType
    target_entities: List[str]
    constraints: Dict[str, Any]
    is_safe: bool
    blast_radius_estimate: str

class SuggestionRiskRecord(BaseModel):
    risk_level: SuggestionRiskLevel
    scope_breadth: str
    target_component_criticality: str
    historical_instability: bool
    overrides_safety_boundary: bool
    downstream_blast_radius: str
    risk_drivers: List[str]

class SuggestionConfidenceRecord(BaseModel):
    confidence_band: SuggestionConfidenceBand
    support_strength: SupportStrength
    human_consistency: float
    contradiction_burden_category: str
    cross_period_stability: bool
    downstream_risk: SuggestionRiskLevel
    caveats: List[str]

class SuggestionWarningRecord(BaseModel):
    warning_code: str
    message: str
    severity: str

class RuleSuggestionRecordV2(BaseModel):
    suggestion_id: str
    suggestion_family: SuggestionFamily
    target_component_family: str
    target_parameter_or_rule: str
    proposed_change_type: str
    current_value_snapshot: Any
    proposed_value_or_rule: Any
    scope: SuggestionScopeRecord
    support_count: int
    support_strength: SupportStrength
    confidence_score: SuggestionConfidenceRecord
    estimated_risk: SuggestionRiskRecord
    evidence_refs: List[str]
    precedent_refs: List[str]
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    status: SuggestionStatus = SuggestionStatus.generated
    warnings: List[SuggestionWarningRecord] = Field(default_factory=list)
    structured_rule: Optional[RuleExtractionRecord] = None
    recommendation_mode: RecommendationMode = RecommendationMode.advisory_only

class TuningSuggestionRecord(BaseModel):
    # Backward compatible alias / generic wrapper
    suggestion: RuleSuggestionRecordV2

class SuggestionBundleRecord(BaseModel):
    bundle_id: str
    suggestions: List[RuleSuggestionRecordV2]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    target_components: List[str]
    aggregate_risk: SuggestionRiskLevel
    version: str = "1.0"

class SuggestionSimulationRecord(BaseModel):
    simulation_id: str
    suggestion_id: str
    affected_runs_estimate: int
    dry_run_supported: bool
    required_quality_gates: List[str]
    approval_required: bool

class AssimilationDecisionRecord(BaseModel):
    decision_id: str
    suggestion_id: str
    decision_status: SuggestionStatus
    assigned_review_route: str
    simulation_required: bool
    release_path_proposed: str
    rationale: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PatternConflictRecord(BaseModel):
    conflict_id: str
    pattern_a_id: str
    pattern_b_id: str
    conflict_description: str

class LearningSummaryRecord(BaseModel):
    total_feedback_aggregates: int
    pattern_candidate_count: int
    generated_suggestions_count: int
    advisory_count: int
    candidate_patch_count: int
    high_risk_suggestion_count: int
    low_support_suppressed_count: int
    required_approval_count: int
    required_simulation_count: int
    suggestions_by_family: Dict[str, int]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SuggestionManifest(BaseModel):
    manifest_id: str
    version: str = "1.0"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    summary: LearningSummaryRecord
    bundles: List[SuggestionBundleRecord]
