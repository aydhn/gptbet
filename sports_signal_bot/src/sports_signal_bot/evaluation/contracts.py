from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd
from pydantic import BaseModel, Field


class EvaluationDataset(BaseModel):
    aligned_predictions_frame: pd.DataFrame
    sources: List[str]
    target_metadata: Dict[str, Any]
    comparison_universe_definition: Dict[str, Any]
    warnings: List[str] = Field(default_factory=list)

    model_config = {"arbitrary_types_allowed": True}


class EvaluationRunManifest(BaseModel):
    run_id: str
    sport: str
    market_type: str
    sources_evaluated: List[str]
    same_sample_policy: bool
    common_universe_size: int
    ranking_metric: str
    leaderboard_path: str
    comparison_table_path: str
    segment_report_paths: Dict[str, str] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)
    config_snapshot: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ClassLevelMetricRecord(BaseModel):
    class_name: str
    precision: float
    recall: float
    f1_score: float
    support: int


class EvaluationSummaryRecord(BaseModel):
    source_name: str
    source_family: str
    sport: str
    market_type: str
    row_count: int
    coverage_rate: float
    log_loss: Optional[float] = None
    brier: Optional[float] = None
    accuracy: Optional[float] = None
    macro_f1: Optional[float] = None
    average_confidence: Optional[float] = None
    average_entropy: Optional[float] = None
    class_metrics: Optional[List[ClassLevelMetricRecord]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LeaderboardRow(BaseModel):
    rank: int
    source_name: str
    source_family: str
    sport: str
    market_type: str
    row_count: int
    coverage_rate: float
    log_loss: Optional[float] = None
    brier: Optional[float] = None
    accuracy: Optional[float] = None
    macro_f1: Optional[float] = None
    ece: Optional[float] = None
    warnings: List[str] = Field(default_factory=list)


class SegmentEvaluationRecord(BaseModel):
    segment_type: str
    segment_value: str
    row_count: int
    metrics: Dict[str, float]
    lift_vs_baseline: Optional[Dict[str, float]] = None


class ConfidenceBucketRecord(BaseModel):
    bucket_label: str
    bucket_min: float
    bucket_max: float
    count: int
    accuracy: float
    avg_log_loss: float
    avg_predicted_confidence: float
    empirical_win_rate: float


class PairwiseComparisonRecord(BaseModel):
    source_a: str
    source_b: str
    common_event_count: int
    delta_log_loss: float
    delta_brier: float
    delta_accuracy: float
    source_a_wins: int
    source_b_wins: int
    ties: int
    better_on_common_universe: str


class EvaluationComparisonRecord(BaseModel):
    base_source: str
    compared_source: str
    pairwise_stats: PairwiseComparisonRecord
