from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from ..simulation.contracts import RiskLevel

class TournamentFamily(str, Enum):
    THRESHOLD_TOURNAMENT = "threshold_tournament"
    POLICY_BOUNDARY_TOURNAMENT = "policy_boundary_tournament"
    PROVIDER_ROUTING_TOURNAMENT = "provider_routing_tournament"
    RECONCILIATION_TRUST_TOURNAMENT = "reconciliation_trust_tournament"
    WEIGHTING_TOURNAMENT = "weighting_tournament"
    ALIAS_RESOLUTION_TOURNAMENT = "alias_resolution_tournament"
    MIXED_SCOPE_EXPLORATORY_TOURNAMENT = "mixed_scope_exploratory_tournament"

class ObjectiveDirection(str, Enum):
    MAXIMIZE = "maximize"
    MINIMIZE = "minimize"

class SafetyLane(str, Enum):
    SAFE_SHORTLIST_LANE = "safe_shortlist_lane"
    ADVISORY_LANE = "advisory_lane"
    EXPLORATORY_LANE = "exploratory_lane"
    BLOCKED_LANE = "blocked_lane"
    INVALID_LANE = "invalid_lane"

class ShortlistTier(str, Enum):
    TIER_1_REVIEW_NOW = "tier_1_review_now"
    TIER_2_GOOD_BUT_NEEDS_MORE_EVIDENCE = "tier_2_good_but_needs_more_evidence"
    TIER_3_EXPLORATORY = "tier_3_exploratory"
    TIER_4_REJECT = "tier_4_reject"

class RecommendationAction(str, Enum):
    REJECT_CANDIDATE = "reject_candidate"
    KEEP_AS_ADVISORY = "keep_as_advisory"
    SHORTLIST_FOR_REVIEW = "shortlist_for_review"
    SHORTLIST_FOR_APPROVAL = "shortlist_for_approval"
    REQUEST_ADDITIONAL_SIMULATION = "request_additional_simulation"
    MERGE_WITH_SIMILAR_CANDIDATE = "merge_with_similar_candidate"
    NARROW_SCOPE_AND_RETRY = "narrow_scope_and_retry"
    BLOCKED_FOR_SAFETY = "blocked_for_safety"
    INCOMPARABLE_RETEST_REQUIRED = "incomparable_retest_required"

class GateBurdenBand(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class TournamentWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str

class TournamentUniverseRecord(BaseModel):
    universe_id: str
    replay_window: Dict[str, datetime]
    target_sports: List[str]
    target_markets: List[str]
    baseline_snapshot_id: str
    release_channel_base: str
    seed: Optional[int] = None
    gate_requirements_profile: str
    caveats: List[str] = Field(default_factory=list)

class TournamentRequestRecord(BaseModel):
    tournament_id: str
    tournament_family: TournamentFamily
    target_component_family: str
    audience_profile: str
    candidate_ids: List[str]
    baseline_ref: str
    simulation_mode: str
    comparison_universe: TournamentUniverseRecord
    selection_policy: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    warnings: List[TournamentWarningRecord] = Field(default_factory=list)

class TournamentCandidateRecord(BaseModel):
    candidate_id: str
    suggestion_id: str
    patch_id: str
    target_component_family: str
    scope: Dict[str, Any]
    risk_level: RiskLevel
    support_strength: float
    confidence_band: str
    estimated_blast_radius: float
    simulation_ref: str
    warnings: List[TournamentWarningRecord] = Field(default_factory=list)

class TournamentBatchRecord(BaseModel):
    batch_id: str
    tournament_id: str
    universe_id: str
    candidates: List[TournamentCandidateRecord]

class TournamentMetricRecord(BaseModel):
    metric_name: str
    value: float
    direction: ObjectiveDirection
    is_constraint: bool = False
    constraint_threshold: Optional[float] = None

class CandidateComparisonRecord(BaseModel):
    comparison_id: str
    candidate_id: str
    metrics: List[TournamentMetricRecord]
    raw_simulation_ref: str
    lane: Optional[SafetyLane] = None

class DominanceRelationRecord(BaseModel):
    relation_id: str
    dominating_candidate_id: str
    dominated_candidate_id: str
    dominating_metrics: List[str]
    explanation: str

class ParetoFrontRecord(BaseModel):
    front_index: int
    candidate_ids: List[str]
    relations: List[DominanceRelationRecord]

class TournamentRankingRecord(BaseModel):
    candidate_id: str
    pareto_front: int
    secondary_rank: int
    lane: SafetyLane
    total_score: Optional[float] = None
    explanation: str

class TournamentGateRequirementRecord(BaseModel):
    candidate_id: str
    burden_band: GateBurdenBand
    required_smoke_suites: List[str]
    required_regression_suites: List[str]
    required_scenario_suites: List[str]
    approval_required: bool
    canary_mandatory: bool
    manual_adjudication_follow_up_needed: bool

class TournamentEvidenceRecord(BaseModel):
    evidence_id: str
    candidate_id: str
    simulation_bundle_ref: str
    citations: List[str]

class CandidateScorecardRecord(BaseModel):
    scorecard_id: str
    candidate_id: str
    key_gains: List[str]
    key_regressions: List[str]
    risk_summary: str
    support_summary: str
    scope_summary: str
    gate_burden: TournamentGateRequirementRecord
    evidence_refs: List[TournamentEvidenceRecord]
    caveats: List[str]

class TournamentRecommendationRecord(BaseModel):
    recommendation_id: str
    candidate_id: str
    action: RecommendationAction
    tier: Optional[ShortlistTier] = None
    rationale: str
    merge_target_id: Optional[str] = None

class CandidateShortlistRecord(BaseModel):
    shortlist_id: str
    tournament_id: str
    tier: ShortlistTier
    ranked_candidates: List[TournamentRankingRecord]
    recommendations: List[TournamentRecommendationRecord]

class TournamentManifest(BaseModel):
    manifest_id: str
    tournament_id: str
    request: TournamentRequestRecord
    batch: TournamentBatchRecord
    pareto_fronts: List[ParetoFrontRecord]
    rankings: List[TournamentRankingRecord]
    scorecards: List[CandidateScorecardRecord]
    shortlists: List[CandidateShortlistRecord]
    created_at: datetime = Field(default_factory=datetime.utcnow)
