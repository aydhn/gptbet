import datetime
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class AllocationStatus(str, Enum):
    FULLY_ALLOCATED = "fully_allocated"
    PARTIALLY_ALLOCATED = "partially_allocated"
    REDUCED_BY_BUDGET = "reduced_by_budget"
    REDUCED_BY_CONCENTRATION = "reduced_by_concentration"
    REDUCED_BY_MARKET_CAP = "reduced_by_market_cap"
    REDUCED_BY_SPORT_CAP = "reduced_by_sport_cap"
    SKIPPED_BY_BUDGET = "skipped_by_budget"
    SKIPPED_BY_CORRELATION_GUARD = "skipped_by_correlation_guard"
    SKIPPED_BELOW_MIN_STAKE = "skipped_below_min_stake"
    INVALID_CANDIDATE = "invalid_candidate"

class PortfolioCandidateRecord(BaseModel):
    event_id: str
    event_datetime_utc: datetime.datetime
    sport: str
    market_type: str
    action_class: str
    selected_side: str

    proposed_stake_fraction: float
    proposed_stake_units: float
    bankroll_before_window: float

    signal_score: float = 0.0
    edge_estimate: float = 0.0
    confidence: float = 1.0
    uncertainty: float = 0.0
    disagreement: float = 0.0
    data_quality_score: float = 1.0

    regime_tags: List[str] = Field(default_factory=list)
    source_concentration_metadata: Dict[str, float] = Field(default_factory=dict)

    same_day_existing_deployed_risk: float = 0.0
    current_drawdown: float = 0.0
    current_loss_streak: int = 0

    decimal_odds: Optional[float] = None
    action_priority_tier: int = 1

class PortfolioAllocationRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    event_datetime_utc: datetime.datetime
    time_bucket_id: str

    proposed_stake_units: float
    proposed_stake_fraction: float
    allocated_stake_units: float
    allocated_stake_fraction: float

    allocation_status: AllocationStatus
    allocation_policy_name: str

    risk_budget_before: float
    risk_budget_after: float

    concentration_penalties: List[str] = Field(default_factory=list)
    throttle_reasons: List[str] = Field(default_factory=list)
    priority_score: float = 0.0
    warnings: List[str] = Field(default_factory=list)
    run_id: str

class ExposureBudgetRecord(BaseModel):
    global_daily_limit: float
    global_daily_used: float
    global_daily_remaining: float

    time_bucket_limit: float
    time_bucket_used: float
    time_bucket_remaining: float

    sport_limits: Dict[str, float] = Field(default_factory=dict)
    sport_used: Dict[str, float] = Field(default_factory=dict)
    sport_remaining: Dict[str, float] = Field(default_factory=dict)

    market_limits: Dict[str, float] = Field(default_factory=dict)
    market_used: Dict[str, float] = Field(default_factory=dict)
    market_remaining: Dict[str, float] = Field(default_factory=dict)

    action_class_limits: Dict[str, float] = Field(default_factory=dict)
    action_class_used: Dict[str, float] = Field(default_factory=dict)
    action_class_remaining: Dict[str, float] = Field(default_factory=dict)

    reserve_budget: float = 0.0

class ExposureBucketRecord(BaseModel):
    bucket_id: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    candidates: List[PortfolioCandidateRecord]
    total_proposed_fraction: float
    total_allocated_fraction: float

class ConcentrationRecord(BaseModel):
    sport_concentration: float
    market_concentration: float
    source_concentration: float
    overall_penalty: float

class CorrelationPlaceholderRecord(BaseModel):
    event_id_a: str
    event_id_b: str
    relation_type: str
    correlation_risk_level: str
    reason: str

class PortfolioSummaryRecord(BaseModel):
    total_proposed_stake: float = 0.0
    total_allocated_stake: float = 0.0
    allocation_ratio: float = 0.0
    skipped_candidates: int = 0
    partially_allocated_candidates: int = 0
    average_reduction_pct: float = 0.0

    daily_budget_utilization: float = 0.0
    bucket_budget_utilization: Dict[str, float] = Field(default_factory=dict)
    sport_budget_utilization: Dict[str, float] = Field(default_factory=dict)
    market_budget_utilization: Dict[str, float] = Field(default_factory=dict)

    approved_vs_candidate_split: Dict[str, float] = Field(default_factory=dict)

    concentration_penalty_counts: int = 0
    correlation_guard_skip_counts: int = 0

class PortfolioRunManifest(BaseModel):
    run_id: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    config: dict
    summary: PortfolioSummaryRecord
    artifact_paths: Dict[str, str] = Field(default_factory=dict)

class PortfolioConfig(BaseModel):
    default_allocation_strategy: str = "sequential_cap"
    daily_risk_budget_fraction: float = 0.15
    time_bucket_minutes: int = 60
    max_bucket_risk_fraction: float = 0.05
    sport_budget_caps: Dict[str, float] = Field(default_factory=lambda: {"football": 0.10, "basketball": 0.10})
    market_budget_caps: Dict[str, float] = Field(default_factory=lambda: {"1x2": 0.05, "ou_2_5": 0.05, "moneyline": 0.05})
    action_class_budget_caps: Dict[str, float] = Field(default_factory=lambda: {"approved_candidate": 0.15, "candidate": 0.05})
    reserve_budget_fraction: float = 0.02

    approved_priority_multiplier: float = 1.5
    candidate_priority_multiplier: float = 1.0

    concentration_penalty_weights: Dict[str, float] = Field(default_factory=lambda: {"sport": 0.1, "market": 0.1, "source": 0.05})

    same_event_related_market_guard: bool = True
    max_related_market_exposure: float = 0.03

    minimum_allocatable_stake_units: float = 1.0
    partial_allocation_allowed: bool = True
    correlation_guard_enabled: bool = True
