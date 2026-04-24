from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class DatasetBuildConfig(BaseModel):
    sport: str
    market_type: str
    label_name: str
    min_event_date: Optional[str] = None
    max_event_date: Optional[str] = None
    allow_missing_labels: bool = False
    drop_null_features: bool = True
    exclude_columns: List[str] = Field(default_factory=list)

class UnsupportedRowRecord(BaseModel):
    event_id: str
    reason: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class FeatureTargetAlignmentRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    feature_version: str
    label_name: str
    target_value: Optional[float]
    target_text: Optional[str]
    class_index: Optional[int]
    line_value: Optional[float]
    event_datetime_utc: str
    is_valid: bool
    invalid_reason: Optional[str] = None

class DatasetSummary(BaseModel):
    sport: str
    market_type: str
    label_name: str
    total_rows: int
    valid_rows: int
    unsupported_rows: int
    feature_count: int
    class_distribution: Optional[Dict[str, int]] = None
    date_range: Dict[str, str]
    warnings: List[str] = Field(default_factory=list)

class TrainingDataset(BaseModel):
    # This class just holds references or summary data, the actual dataframe is handled by pandas
    # We use this as a strongly typed wrapper
    summary: DatasetSummary
    feature_columns: List[str]
    metadata_columns: List[str]
    target_column: str

    class Config:
        arbitrary_types_allowed = True

class ValidationPredictionRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    label_name: str
    true_class_index: Optional[int] = None
    predicted_class: Optional[int] = None
    predicted_probabilities: Dict[str, float]
    model_name: str
    fold_id: str
    split_metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp_utc: str

class SplitSummary(BaseModel):
    strategy_name: str
    fold_id: str
    train_rows: int
    valid_rows: int
    test_rows: Optional[int] = None
    train_date_range: Dict[str, str]
    valid_date_range: Dict[str, str]

class FoldManifest(BaseModel):
    fold_id: str
    train_start: str
    train_end: str
    valid_start: str
    valid_end: str
    train_rows: int
    valid_rows: int
    class_distribution: Optional[Dict[str, int]] = None
    metrics: Dict[str, float] = Field(default_factory=dict)

class TrainingRunManifest(BaseModel):
    run_id: str
    started_at_utc: str
    ended_at_utc: str
    sport: str
    market_type: str
    label_name: str
    model_name: str
    split_strategy: str
    total_train_rows: int
    total_valid_rows: int
    feature_count: int
    feature_list_path: str
    model_artifact_path: str
    metrics_summary: Dict[str, float] = Field(default_factory=dict)
    fold_manifests: List[FoldManifest] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    seed: int
    config_snapshot: Dict[str, Any] = Field(default_factory=dict)
