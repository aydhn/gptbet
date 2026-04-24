from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class CalibrationDataset(BaseModel):
    event_id: str
    fold_id: Optional[str] = None
    true_label: Optional[str] = None
    true_class_index: Optional[int] = None
    raw_predicted_probabilities: Dict[str, float]
    predicted_class: Optional[int] = None
    model_name: str
    market_type: str
    label_name: str
    sport: str
    split_metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp_utc: str

class ReliabilityBinRecord(BaseModel):
    bin_index: int
    lower_bound: float
    upper_bound: float
    count: int
    mean_predicted_probability: float
    empirical_frequency: float
    calibration_gap: float

class CalibrationSummary(BaseModel):
    method: str
    log_loss: float
    brier_score: float
    ece: float
    mce: float
    reliability_bins: List[ReliabilityBinRecord] = Field(default_factory=list)
    mean_confidence: float
    calibration_coverage: float
    class_name: Optional[str] = None

class CalibratedPredictionRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    label_name: str
    true_class_index: Optional[int] = None
    raw_predicted_probabilities: Dict[str, float]
    calibrated_predicted_probabilities: Dict[str, float]
    calibrated_predicted_class: int
    model_name: str
    calibration_method: str
    calibration_run_id: str
    fold_id: str
    timestamp_utc: str

class CalibrationComparisonRecord(BaseModel):
    run_id: str
    raw_log_loss: float
    calibrated_log_loss: float
    delta_log_loss: float
    raw_brier_score: float
    calibrated_brier_score: float
    delta_brier_score: float
    raw_ece: float
    calibrated_ece: float
    delta_ece: float
    calibration_improvement: bool
    possible_overfit_warning: bool

class CalibrationRunManifest(BaseModel):
    run_id: str
    source_model_run_id: Optional[str] = None
    sport: str
    market_type: str
    label_name: str
    calibration_method: str
    class_labels: List[str]
    calibration_dataset_size: int
    raw_metrics: Dict[str, float]
    calibrated_metrics: Dict[str, float]
    delta_metrics: Dict[str, float]
    calibrator_artifact_path: str
    reliability_summary_path: str
    warnings: List[str] = Field(default_factory=list)
    config_snapshot: Dict[str, Any] = Field(default_factory=dict)
    timestamp_utc: str
