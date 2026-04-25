import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RegimeDefinition(BaseModel):
    regime_family: str
    level: str  # event, period, source-period
    description: str
    required_inputs: List[str]
    assignment_type: str  # rule_based, threshold, derived, placeholder_ml
    minimum_data_requirements: Dict[str, Any] = Field(default_factory=dict)
    enabled: bool = True


class RegimeWarningRecord(BaseModel):
    warning_type: str
    message: str
    context: Dict[str, Any] = Field(default_factory=dict)


class EventRegimeRecord(BaseModel):
    event_id: str
    sport: str
    market_type: Optional[str] = None
    regime_family: str
    regime_label: str
    regime_value: Optional[float] = None
    assignment_method: str
    assigned_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    supporting_features: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)


class PeriodRegimeRecord(BaseModel):
    period_id: int
    sport: str
    market_type: Optional[str] = None
    regime_family: str
    regime_label: str
    derived_from_window: Dict[str, str] = Field(default_factory=dict)
    supporting_metrics: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)


class RegimeAssignmentResult(BaseModel):
    event_regimes: List[EventRegimeRecord] = Field(default_factory=list)
    period_regimes: List[PeriodRegimeRecord] = Field(default_factory=list)
    warnings: List[RegimeWarningRecord] = Field(default_factory=list)


class RegimeCoverageRecord(BaseModel):
    regime_family: str
    regime_label: str
    row_count: int
    coverage_rate: float
    minimum_rows_satisfied: bool
    source_coverage: Dict[str, float] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)


class RegimeEvaluationRecord(BaseModel):
    regime_family: str
    regime_label: str
    evaluation_summary: Dict[str, Any] = Field(default_factory=dict)


class RegimeManifest(BaseModel):
    run_id: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    active_families: List[str] = Field(default_factory=list)
    coverage_summaries: List[RegimeCoverageRecord] = Field(default_factory=list)
    evaluation_summaries: List[RegimeEvaluationRecord] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
