from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class DisagreementThresholds(BaseModel):
    low: float = 0.05
    high: float = 0.15


class FavoriteProbThresholds(BaseModel):
    clear_favorite: float = 0.65
    market_close_diff: float = 0.10


class EntropyThresholds(BaseModel):
    high: float = 0.8


class DataCompletenessThresholds(BaseModel):
    high_completeness_max_missing: float = 0.05
    low_completeness_min_missing: float = 0.20


class SparseHistoryThresholds(BaseModel):
    low_history_max_matches: int = 5


class CongestionThresholds(BaseModel):
    congested_min_matches: int = 3
    congested_days_window: int = 10


class SeasonProgressBuckets(BaseModel):
    early_max: float = 0.25
    late_min: float = 0.75


class PerformanceDegradationThresholds(BaseModel):
    degrading_min_delta: float = 0.02
    recovering_min_delta: float = -0.02


class PeriodRules(BaseModel):
    lookback_periods: int = 3
    min_history: int = 5


class RegimeThresholdsConfig(BaseModel):
    disagreement_thresholds: DisagreementThresholds = Field(
        default_factory=DisagreementThresholds
    )
    favorite_prob_thresholds: FavoriteProbThresholds = Field(
        default_factory=FavoriteProbThresholds
    )
    entropy_thresholds: EntropyThresholds = Field(default_factory=EntropyThresholds)
    data_completeness_thresholds: DataCompletenessThresholds = Field(
        default_factory=DataCompletenessThresholds
    )
    sparse_history_thresholds: SparseHistoryThresholds = Field(
        default_factory=SparseHistoryThresholds
    )
    short_rest_days: int = 3
    congestion_match_count_thresholds: CongestionThresholds = Field(
        default_factory=CongestionThresholds
    )
    season_progress_buckets: SeasonProgressBuckets = Field(
        default_factory=SeasonProgressBuckets
    )
    performance_degradation_thresholds: PerformanceDegradationThresholds = Field(
        default_factory=PerformanceDegradationThresholds
    )
    minimum_rows_per_regime: int = 100


class RegimeConfig(BaseModel):
    enabled_regime_families: List[str] = Field(default_factory=list)
