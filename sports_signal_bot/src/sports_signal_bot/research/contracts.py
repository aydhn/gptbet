import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class WindowDefinition(BaseModel):
    """Defines the time windows for a single walk-forward period."""

    period_id: int
    train_start: datetime.date
    train_end: datetime.date
    calibration_start: Optional[datetime.date] = None
    calibration_end: Optional[datetime.date] = None
    forward_start: datetime.date
    forward_end: datetime.date

    # Flags indicating what needs to be refreshed this period
    should_retrain: bool = True
    should_recalibrate: bool = True
    should_reensemble: bool = True
    should_refresh_stacker: bool = False


class WalkForwardPlan(BaseModel):
    """The complete sequence of periods for a research scenario."""

    scenario_id: str
    sport: str
    market_type: str
    periods: List[WindowDefinition]
    total_periods: int
    planning_mode: str


class ResearchScenario(BaseModel):
    """Defines the configuration for a research run."""

    scenario_id: str
    sport: str
    market_type: str
    start_date: datetime.date
    end_date: datetime.date

    planning_mode: str = "expanding"  # expanding, rolling, anchored, fixed
    initial_train_window_days: int = 180
    calibration_window_days: Optional[int] = 30
    forward_test_window_days: int = 30

    retrain_frequency: int = 1  # Retrain every N periods
    recalibration_frequency: int = 1  # Recalibrate every N periods
    reensemble_frequency: int = 1  # Rebuild ensemble every N periods
    stacker_refresh_frequency: Optional[int] = None

    minimum_rows_guard: int = 100
    skip_period_if_insufficient_data: bool = True
    enabled_sources: List[str] = Field(default_factory=list)
    enabled_models: List[str] = Field(default_factory=list)
    monthly_reporting_enabled: bool = True


class PeriodRunRecord(BaseModel):
    """Tracks the execution of a single period."""

    period_id: int
    scenario_id: str
    window: WindowDefinition
    status: str  # success, skipped, failed

    retrained_model_names: List[str] = Field(default_factory=list)
    reused_model_names: List[str] = Field(default_factory=list)

    calibrator_refresh_status: str = "not_applicable"
    ensemble_refresh_status: str = "not_applicable"
    stacker_refresh_status: str = "not_applicable"

    evaluation_summary: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)
    output_artifact_paths: Dict[str, str] = Field(default_factory=dict)


class PeriodPerformanceRecord(BaseModel):
    """Performance metrics for a single period."""

    period_id: int
    metrics_by_source: Dict[
        str, Dict[str, float]
    ]  # source_name -> metric_name -> value
    best_source: str
    ensemble_lift: float = 0.0
    stacker_lift: float = 0.0
    calibration_gain: float = 0.0
    num_events_evaluated: int


class TimeSliceSummaryRecord(BaseModel):
    """Aggregated reporting across multiple periods."""

    scenario_id: str
    period_performances: List[PeriodPerformanceRecord]

    # Trends across periods
    log_loss_trend: Dict[
        str, List[float]
    ]  # source_name -> list of log loss over periods
    accuracy_trend: Dict[str, List[float]]
    brier_trend: Dict[str, List[float]]
    coverage_trend: Dict[str, List[float]]

    cumulative_leaderboard: Dict[str, Dict[str, float]]
    warnings: List[str] = Field(default_factory=list)


class ResearchRunManifest(BaseModel):
    """Top-level manifest for the entire research run."""

    run_id: str
    run_timestamp: str
    scenario: ResearchScenario

    total_periods: int
    completed_periods: int
    skipped_periods: int

    source_families_involved: List[str]
    aggregate_summary_paths: Dict[str, str]
    warnings: List[str] = Field(default_factory=list)
    config_snapshot: Dict[str, Any]
