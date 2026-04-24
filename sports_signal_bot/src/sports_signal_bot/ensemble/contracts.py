from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime

class StandardizedPredictionRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    label_name: Optional[str] = None
    source_family: str  # e.g., 'benchmark', 'probabilistic', 'ml_raw', 'ml_calibrated'
    source_name: str
    source_run_id: Optional[str] = None
    class_labels: List[str]
    probabilities: Dict[str, float]
    predicted_class: str
    prediction_status: str = "valid"
    is_calibrated: bool = False
    calibration_method: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)

class SourceContributionRecord(BaseModel):
    source_name: str
    source_family: str
    weight: float
    is_calibrated: bool
    status: str = "included"
    fallback_order: Optional[int] = None

class EnsembleDiagnosticsRecord(BaseModel):
    num_sources_eligible: int
    num_sources_used: int
    excluded_sources: List[str] = Field(default_factory=list)
    fallback_sources_used: List[str] = Field(default_factory=list)
    top_class_confidence: float = 0.0
    entropy: float = 0.0
    max_disagreement: float = 0.0
    source_variance: float = 0.0
    calibration_preference_mode: str = "prefer_calibrated"
    warnings: List[str] = Field(default_factory=list)

class EnsembleOutputRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    ensemble_name: str
    final_probabilities: Dict[str, float]
    final_predicted_class: str
    component_sources: List[SourceContributionRecord]
    diagnostics: EnsembleDiagnosticsRecord
    status: str = "success"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EnsembleInputRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    predictions: List[StandardizedPredictionRecord]
