from .base import BaseCalibrator
# IMPORTANT: Import calibrator implementations so they register themselves!
from .binary.identity import BinaryIdentityCalibrator
from .binary.isotonic import BinaryIsotonicCalibrator
from .binary.sigmoid import BinarySigmoidCalibrator
from .comparison import create_comparison_record
from .contracts import (CalibratedPredictionRecord,
                        CalibrationComparisonRecord, CalibrationDataset,
                        CalibrationRunManifest, CalibrationSummary,
                        ReliabilityBinRecord)
from .dataset import (build_calibration_dataset_from_validation_predictions,
                      extract_calibration_features_and_targets)
from .factory import CalibrationFactory
from .metrics import (calculate_brier_score, calculate_ece_mce,
                      calculate_log_loss)
from .multiclass.identity import MulticlassIdentityCalibrator
from .multiclass.temperature_placeholder import TemperatureScalingPlaceholder
from .multiclass.wrapper import MulticlassWrapperCalibrator
from .registry import CalibrationRegistry
from .reliability import generate_reliability_bins
from .runner import CalibrationRunner
from .utils import (clip_probabilities, ensure_class_order,
                    expand_multiclass_probabilities,
                    flatten_binary_probabilities, validate_probability_vectors)

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
    "TemperatureScalingPlaceholder",
]
