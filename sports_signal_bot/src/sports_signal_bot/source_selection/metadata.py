from datetime import datetime, timezone
from typing import Dict, Optional

from pydantic import BaseModel, Field


class EvaluationMetadata(BaseModel):
    """Historical performance metadata for a source."""

    recent_log_loss: Optional[float] = None
    recent_brier_score: Optional[float] = None
    calibration_error: Optional[float] = None
    benchmark_relative_performance: float = 0.0
    stability_score: float = 1.0
    evaluation_timestamp: Optional[str] = None


class RefreshMetadata(BaseModel):
    """Information about source artifacts freshness."""

    last_model_refresh_timestamp: Optional[str] = None
    last_calibration_refresh_timestamp: Optional[str] = None
    is_stale_flag: bool = False


class RegimeProfileMetadata(BaseModel):
    """Regime-specific performance profile."""

    regime_scores: Dict[str, float] = Field(default_factory=dict)
    regime_sample_sizes: Dict[str, int] = Field(default_factory=dict)


class SourceMetadataRecord(BaseModel):
    """Composite metadata record loaded for a specific source during an event run."""

    source_name: str
    event_id: str
    sport: str
    market_type: str

    is_prediction_available: bool = False
    prediction_probabilities: Dict[str, float] = Field(default_factory=dict)

    is_calibrated: bool = False

    refresh_info: RefreshMetadata = Field(default_factory=RefreshMetadata)
    eval_info: EvaluationMetadata = Field(default_factory=EvaluationMetadata)
    regime_profile: RegimeProfileMetadata = Field(default_factory=RegimeProfileMetadata)

    recent_coverage_rate: float = 1.0  # 0.0 to 1.0
    has_invalid_probabilities: bool = False

    @property
    def model_age_days(self) -> float:
        if not self.refresh_info.last_model_refresh_timestamp:
            return 999.0
        try:
            dt = datetime.fromisoformat(
                self.refresh_info.last_model_refresh_timestamp.replace("Z", "+00:00")
            )
            now = datetime.now(timezone.utc)
            return (now - dt).total_seconds() / 86400.0
        except ValueError:
            return 999.0

    @property
    def calibration_age_days(self) -> float:
        if not self.refresh_info.last_calibration_refresh_timestamp:
            return 999.0
        try:
            dt = datetime.fromisoformat(
                self.refresh_info.last_calibration_refresh_timestamp.replace(
                    "Z", "+00:00"
                )
            )
            now = datetime.now(timezone.utc)
            return (now - dt).total_seconds() / 86400.0
        except ValueError:
            return 999.0


class SourceMetadataLoader:
    """Mock/Placeholder loader for fetching source metadata for an event.
    In a real implementation, this would read from manifest stores, MLflow, or a DB."""

    def load_metadata(
        self, source_name: str, event_id: str, sport: str, market_type: str
    ) -> SourceMetadataRecord:
        # Default mock record
        return SourceMetadataRecord(
            source_name=source_name,
            event_id=event_id,
            sport=sport,
            market_type=market_type,
            is_prediction_available=True,
            is_calibrated=True,
            recent_coverage_rate=1.0,
            refresh_info=RefreshMetadata(
                last_model_refresh_timestamp=datetime.now(timezone.utc).isoformat(),
                last_calibration_refresh_timestamp=datetime.now(
                    timezone.utc
                ).isoformat(),
            ),
            eval_info=EvaluationMetadata(recent_log_loss=0.6, recent_brier_score=0.2),
        )
