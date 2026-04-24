from .contracts import (
    CalibrationDataset,
    CalibrationSummary,
    CalibrationRunManifest,
    ReliabilityBinRecord,
    CalibratedPredictionRecord,
    CalibrationComparisonRecord
)
from .dataset import build_calibration_dataset_from_validation_predictions, extract_calibration_features_and_targets
from .utils import (
    ensure_class_order,
    validate_probability_vectors,
    flatten_binary_probabilities,
    expand_multiclass_probabilities,
    clip_probabilities
)
from .metrics import calculate_log_loss, calculate_brier_score, calculate_ece_mce
from .reliability import generate_reliability_bins
from .comparison import create_comparison_record
from .base import BaseCalibrator
from .registry import CalibrationRegistry
from .factory import CalibrationFactory
from .runner import CalibrationRunner

# IMPORTANT: Import calibrator implementations so they register themselves!
from .binary.identity import BinaryIdentityCalibrator
from .binary.sigmoid import BinarySigmoidCalibrator
from .binary.isotonic import BinaryIsotonicCalibrator
from .multiclass.identity import MulticlassIdentityCalibrator
from .multiclass.wrapper import MulticlassWrapperCalibrator
from .multiclass.temperature_placeholder import TemperatureScalingPlaceholder

__all__ = [
    "CalibrationDataset",
    "CalibrationSummary",
    "CalibrationRunManifest",
    "ReliabilityBinRecord",
    "CalibratedPredictionRecord",
    "CalibrationComparisonRecord",
    "build_calibration_dataset_from_validation_predictions",
    "extract_calibration_features_and_targets",
    "ensure_class_order",
    "validate_probability_vectors",
    "flatten_binary_probabilities",
    "expand_multiclass_probabilities",
    "clip_probabilities",
    "calculate_log_loss",
    "calculate_brier_score",
    "calculate_ece_mce",
    "generate_reliability_bins",
    "create_comparison_record",
    "BaseCalibrator",
    "CalibrationRegistry",
    "CalibrationFactory",
    "CalibrationRunner",
    "BinaryIdentityCalibrator",
    "BinarySigmoidCalibrator",
    "BinaryIsotonicCalibrator",
    "MulticlassIdentityCalibrator",
    "MulticlassWrapperCalibrator",
    "TemperatureScalingPlaceholder"
]
