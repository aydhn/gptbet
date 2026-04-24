from .contracts import (
    TrainingDataset,
    DatasetBuildConfig,
    DatasetSummary,
    FeatureTargetAlignmentRecord,
    UnsupportedRowRecord,
    TrainingRunManifest,
    ValidationPredictionRecord,
    SplitSummary,
    FoldManifest,
)
from .dataset import TrainingDatasetBuilder
from .leakage import detect_suspicious_feature_columns, audit_feature_target_alignment, enforce_pre_match_only_feature_policy
from .splits import HoldoutTimeSplit, ExpandingWindowSplit, RollingWindowSplit, WalkForwardSplit
from .preprocessing import build_preprocessing_pipeline
from .registry import TRAINER_REGISTRY
from .factory import TrainerFactory
from .runner import TrainingRunManager
from .metrics import evaluate_classification_metrics

__all__ = [
    "TrainingDataset",
    "DatasetBuildConfig",
    "DatasetSummary",
    "FeatureTargetAlignmentRecord",
    "UnsupportedRowRecord",
    "TrainingRunManifest",
    "ValidationPredictionRecord",
    "SplitSummary",
    "FoldManifest",
    "TrainingDatasetBuilder",
    "detect_suspicious_feature_columns",
    "audit_feature_target_alignment",
    "enforce_pre_match_only_feature_policy",
    "HoldoutTimeSplit",
    "ExpandingWindowSplit",
    "RollingWindowSplit",
    "WalkForwardSplit",
    "build_preprocessing_pipeline",
    "TRAINER_REGISTRY",
    "TrainerFactory",
    "TrainingRunManager",
    "evaluate_classification_metrics",
]
