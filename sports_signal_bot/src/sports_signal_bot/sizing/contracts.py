import datetime
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SizingStrategyName(str, Enum):
    FRACTIONAL_KELLY = "fractional_kelly"
    CAPPED_FRACTIONAL_KELLY = "capped_fractional_kelly"
    CONFIDENCE_ADJUSTED_KELLY = "confidence_adjusted_kelly"
    EDGE_BAND_SIZING = "edge_band_sizing"
    CONSERVATIVE_RESEARCH = "conservative_research"
    HYBRID_KELLY_FLAT_FLOOR = "hybrid_kelly_flat_floor"


class StakeSizingInputRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    action_class: str
    selected_side: str

    final_selection_probability: float
    market_odds: float  # decimal odds
    implied_probability: float

    signal_score: float = 0.0
    edge_estimate: float = 0.0
    confidence_score: float = 1.0

    uncertainty_penalty: float = 0.0
    disagreement_penalty: float = 0.0
    data_quality_penalty: float = 0.0
    source_health_penalty: float = 0.0
    regime_adjustment: float = 1.0

    current_bankroll: float
    current_drawdown_pct: float = 0.0
    current_loss_streak: int = 0
    same_day_exposure: float = 0.0


class KellyEstimateRecord(BaseModel):
    b: float
    p: float
    q: float
    full_kelly_fraction: float
    fractional_kelly_fraction: float
    warnings: List[str] = Field(default_factory=list)


class RiskLimitRecord(BaseModel):
    per_decision_capped: bool = False
    drawdown_throttled: bool = False
    streak_throttled: bool = False
    bankroll_floor_applied: bool = False
    market_cap_applied: bool = False
    throttle_multiplier: float = 1.0
    original_fraction: float
    capped_fraction: float
    warnings: List[str] = Field(default_factory=list)


class SizingComponentRecord(BaseModel):
    edge_multiplier: float = 1.0
    confidence_multiplier: float = 1.0
    uncertainty_multiplier: float = 1.0
    data_quality_multiplier: float = 1.0
    regime_multiplier: float = 1.0
    combined_multiplier: float = 1.0


class SizingDecisionRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    action_class: str
    selected_side: str
    sizing_strategy_name: str

    bankroll_before: float

    raw_size_fraction: float
    adjusted_size_fraction: float
    final_stake_units: float
    final_stake_fraction: float

    edge_estimate: float
    calibrated_probability: float
    decimal_odds: float

    kelly_fraction_raw: Optional[float] = None
    kelly_fraction_fractional: Optional[float] = None

    risk_throttles_applied: List[str] = Field(default_factory=list)
    caps_applied: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    run_id: str


class SizingSummaryRecord(BaseModel):
    total_sized_decisions: int = 0
    average_raw_kelly: float = 0.0
    average_final_stake_fraction: float = 0.0
    capped_decision_count: int = 0
    throttled_decision_count: int = 0
    skipped_sizing_reasons: Dict[str, int] = Field(default_factory=dict)
    market_sizing_summary: Dict[str, float] = Field(default_factory=dict)
    action_class_sizing_summary: Dict[str, float] = Field(default_factory=dict)


class SizingManifest(BaseModel):
    run_id: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    sport: str
    market: str
    strategy: str
    config: dict
    summary: SizingSummaryRecord
    artifact_paths: Dict[str, str] = Field(default_factory=dict)


class AllocationThrottleRecord(BaseModel):
    drawdown_multiplier: float = 1.0
    streak_multiplier: float = 1.0
    exposure_multiplier: float = 1.0
    final_throttle: float = 1.0


class ExposureBudgetRecord(BaseModel):
    daily_budget_remaining: float
    market_budget_remaining: float
    concurrent_budget_remaining: float


class SizingConfig(BaseModel):
    default_sizing_strategy: SizingStrategyName = SizingStrategyName.FRACTIONAL_KELLY
    fractional_kelly_default: float = 0.25
    fractional_kelly_by_market: Dict[str, float] = Field(default_factory=dict)

    max_fraction_per_decision: float = 0.05
    min_stake_units: float = 1.0
    max_stake_units: float = 500.0

    confidence_multiplier_bounds: tuple[float, float] = (0.5, 1.2)
    uncertainty_penalty_bounds: tuple[float, float] = (0.0, 0.5)
    disagreement_penalty_bounds: tuple[float, float] = (0.0, 0.5)

    drawdown_throttle_bands: Dict[float, float] = Field(
        default_factory=dict
    )  # e.g., {0.10: 0.8, 0.20: 0.5}
    losing_streak_throttle_bands: Dict[int, float] = Field(
        default_factory=dict
    )  # e.g., {5: 0.8, 10: 0.5}
    action_class_fraction_caps: Dict[str, float] = Field(
        default_factory=dict
    )  # e.g., {'approved_candidate': 1.0, 'candidate': 0.5}

    bankroll_floor_buffer: float = 0.0
    missing_odds_policy: str = "skip"  # skip, fallback
