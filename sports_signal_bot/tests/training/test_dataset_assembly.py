
import pytest
import pandas as pd
from sports_signal_bot.training.dataset import TrainingDatasetBuilder
from sports_signal_bot.training.contracts import DatasetBuildConfig
from sports_signal_bot.core.exceptions import LeakageDetectedError

def test_dataset_assembly_success():
    features_df = pd.DataFrame({
        'event_id': ['1', '2', '3'],
        'event_datetime_utc': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03'], utc=True),
        'feat_a': [1.0, 2.0, 3.0]
    })

    labels_df = pd.DataFrame({
        'event_id': ['2', '3', '1'], # Shuffled
        'label_name': ['test_lbl', 'test_lbl', 'test_lbl'],
        'class_index': [1, 0, 1],
        'validity_status': ['valid', 'valid', 'valid']
    })

    config = DatasetBuildConfig(sport="test", market_type="test", label_name="test_lbl")
    builder = TrainingDatasetBuilder(config)

    df, dataset = builder.build(features_df, labels_df)

    assert len(df) == 3
    assert dataset.summary.total_rows == 3
    assert 'feat_a' in dataset.feature_columns
    assert dataset.target_column == 'class_index'
    # Check temporal sorting
    assert df['event_id'].tolist() == ['1', '2', '3']

def test_dataset_assembly_filters_invalid_labels():
    features_df = pd.DataFrame({
        'event_id': ['1', '2'],
        'event_datetime_utc': pd.to_datetime(['2024-01-01', '2024-01-02'], utc=True),
        'feat_a': [1.0, 2.0]
    })

    labels_df = pd.DataFrame({
        'event_id': ['1', '2'],
        'label_name': ['test_lbl', 'test_lbl'],
        'class_index': [1, 0],
        # Only row 1 should be kept
        'validity_status': ['LabelValidityStatus.VALID', 'LabelValidityStatus.INVALID']
    })

    config = DatasetBuildConfig(sport="test", market_type="test", label_name="test_lbl", allow_missing_labels=False)
    builder = TrainingDatasetBuilder(config)

    df, dataset = builder.build(features_df, labels_df)

    assert len(df) == 1
    assert df.iloc[0]['event_id'] == '1'

def test_dataset_assembly_leakage_detection():
    features_df = pd.DataFrame({
        'event_id': ['1'],
        'event_datetime_utc': pd.to_datetime(['2024-01-01'], utc=True),
        'class_index': [1.0], # The target column is in features
        'target_score_leak': [2.0] # Will be caught by suspicious names
    })

    labels_df = pd.DataFrame({
        'event_id': ['1'],
        'label_name': ['test_lbl'],
        'class_index': [1],
        'validity_status': ['valid']
    })

    config = DatasetBuildConfig(sport="test", market_type="test", label_name="test_lbl")
    builder = TrainingDatasetBuilder(config)

    with pytest.raises(LeakageDetectedError):
        builder.build(features_df, labels_df)
