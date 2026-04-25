from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone

class MetaFeatureRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    target_class_index: Optional[int] = None
    target_class_name: Optional[str] = None
    source_probabilities: Dict[str, float] = Field(default_factory=dict)
    confidence_features: Dict[str, float] = Field(default_factory=dict)
    agreement_features: Dict[str, float] = Field(default_factory=dict)
    metadata_features: Dict[str, Any] = Field(default_factory=dict)
    context_features: Dict[str, Any] = Field(default_factory=dict)
    missing_sources: List[str] = Field(default_factory=list)
    available_sources: List[str] = Field(default_factory=list)

class MetaTrainingDataset(BaseModel):
    records: List[MetaFeatureRecord]
    class_labels: List[str]
    sport: str
    market_type: str
    feature_names: List[str]
    created_at_utc: datetime = Field(default_factory=datetime.utcnow)

class SourceCoverageRecord(BaseModel):
    source_name: str
    total_events: int
    oof_events: int
    oof_coverage_ratio: float
    calibrated_ratio: float
    excluded_rows: int

class MetaFeatureManifest(BaseModel):
    sport: str
    market_type: str
    class_labels: List[str]
    source_coverage: List[SourceCoverageRecord]
    feature_columns: List[str]
    total_records: int
    missing_source_strategy: str

class OOFIntegrityReport(BaseModel):
    is_valid: bool
    violations_found: int
    violation_details: List[str] = Field(default_factory=list)

class MetaPredictionDiagnostics(BaseModel):
    sources_used: int
    missing_sources: int
    fallback_used: bool
    meta_confidence: float
    top_class_margin: float
    warnings: List[str] = Field(default_factory=list)

class MetaPredictionRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    stacker_name: str
    final_probabilities: Dict[str, float]
    predicted_class: str
    diagnostics: MetaPredictionDiagnostics
    status: str = "success"
    created_at_utc: datetime = Field(default_factory=datetime.utcnow)
