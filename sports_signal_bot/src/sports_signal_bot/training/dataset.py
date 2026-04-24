import pandas as pd
from typing import Dict, List, Optional, Tuple
from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.training.contracts import (
    TrainingDataset,
    DatasetBuildConfig,
    DatasetSummary,
    UnsupportedRowRecord,
    FeatureTargetAlignmentRecord
)
from sports_signal_bot.training.leakage import audit_feature_target_alignment, enforce_pre_match_only_feature_policy

logger = get_logger("TrainingDatasetBuilder")

class TrainingDatasetBuilder:
    def __init__(self, config: DatasetBuildConfig):
        self.config = config
        self.warnings: List[str] = []

    def build(self, features_df: pd.DataFrame, labels_df: pd.DataFrame) -> Tuple[pd.DataFrame, TrainingDataset]:
        """
        Builds the training dataset by joining features and labels,
        applying temporal filters, and conducting leakage checks.
        """
        logger.info(f"Building dataset for {self.config.sport} / {self.config.label_name}")

        # Ensure minimal columns
        if 'event_id' not in features_df.columns:
            raise ValueError("features_df must contain 'event_id'")
        if 'event_id' not in labels_df.columns:
            raise ValueError("labels_df must contain 'event_id'")

        # Filter labels for specific market/label
        if 'label_name' in labels_df.columns:
            filtered_labels = labels_df[labels_df['label_name'] == self.config.label_name].copy()
        else:
            filtered_labels = labels_df.copy()

        if filtered_labels.empty:
            raise ValueError(f"No labels found for label_name: {self.config.label_name}")

        # Drop invalid labels unless explicitly permitted
        if 'validity_status' in filtered_labels.columns and not self.config.allow_missing_labels:
            # Assumes LabelValidityStatus.VALID corresponds to some string, e.g., 'valid'
            # Check if using enum directly or string
            valid_mask = filtered_labels['validity_status'].astype(str).str.lower().str.endswith('valid') & ~filtered_labels['validity_status'].astype(str).str.lower().str.contains('invalid')
            filtered_labels = filtered_labels[valid_mask]

        if 'target_value' not in filtered_labels.columns and 'class_index' not in filtered_labels.columns:
             raise ValueError("Labels must contain 'target_value' or 'class_index'")

        # Choose the target column (class_index for classification, target_value for regression - but we default to class_index for this phase)
        target_col = 'class_index' if 'class_index' in filtered_labels.columns else 'target_value'

        # Leakage check: The target should never be in the features *before* join!
        from sports_signal_bot.core.exceptions import LeakageDetectedError
        if target_col in features_df.columns:
            raise LeakageDetectedError(f"Target column '{target_col}' already exists in feature matrix. This is data leakage.")

        # Join features and labels
        df = pd.merge(features_df, filtered_labels[['event_id', target_col]], on='event_id', how='inner')

        # Ensure event_datetime_utc exists for temporal sorting
        if 'event_datetime_utc' not in df.columns:
            logger.warning("No event_datetime_utc in dataset, adding a placeholder. Time-aware features might fail.")
            # Depending on how the feature matrix is built, event_datetime_utc might be buried in metadata
            # We'll expect it to be present for now.
            df['event_datetime_utc'] = pd.Timestamp.utcnow()

        # Convert to datetime
        df['event_datetime_utc'] = pd.to_datetime(df['event_datetime_utc'], utc=True)

        # Temporal filtering
        if self.config.min_event_date:
            min_date = pd.to_datetime(self.config.min_event_date, utc=True)
            df = df[df['event_datetime_utc'] >= min_date]
        if self.config.max_event_date:
            max_date = pd.to_datetime(self.config.max_event_date, utc=True)
            df = df[df['event_datetime_utc'] <= max_date]

        # Sort by time!
        df = df.sort_values('event_datetime_utc').reset_index(drop=True)

        # Drop nulls
        if self.config.drop_null_features:
            initial_len = len(df)
            df = df.dropna()
            if len(df) < initial_len:
                logger.info(f"Dropped {initial_len - len(df)} rows due to nulls.")

        # Exclude columns
        feature_cols = [c for c in features_df.columns if c not in ['event_id', 'event_datetime_utc', 'sport', 'league', 'feature_version', 'feature_build_run_id'] + self.config.exclude_columns]
        feature_cols = [c for c in feature_cols if c in df.columns]

        metadata_cols = ['event_id', 'event_datetime_utc']

        # Leakage Audit
        audit_feature_target_alignment(df, feature_cols, target_col)
        enforce_pre_match_only_feature_policy(df)

        summary = DatasetSummary(
            sport=self.config.sport,
            market_type=self.config.market_type,
            label_name=self.config.label_name,
            total_rows=len(df),
            valid_rows=len(df),
            unsupported_rows=0,
            feature_count=len(feature_cols),
            date_range={
                "min": str(df['event_datetime_utc'].min()),
                "max": str(df['event_datetime_utc'].max())
            } if not df.empty else {},
            warnings=self.warnings
        )

        if not df.empty and df[target_col].dtype.kind in 'biu':
            summary.class_distribution = {str(k): v for k, v in df[target_col].value_counts().to_dict().items()}

        dataset = TrainingDataset(
            summary=summary,
            feature_columns=feature_cols,
            metadata_columns=metadata_cols,
            target_column=target_col
        )

        return df, dataset
