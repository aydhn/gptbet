import pytest
import pandas as pd
from sports_signal_bot.training.splits import HoldoutTimeSplit, ExpandingWindowSplit, RollingWindowSplit

def test_holdout_time_split():
    df = pd.DataFrame({
        'event_id': list(range(10)),
        'event_datetime_utc': pd.date_range('2024-01-01', periods=10)
    })

    splitter = HoldoutTimeSplit(train_fraction=0.6, test_fraction=0.2)
    splits = list(splitter.split(df))

    assert len(splits) == 1
    fold_id, train_idx, valid_idx, test_idx = splits[0]

    assert len(train_idx) == 6
    assert len(valid_idx) == 2
    assert len(test_idx) == 2

    # Check chronological ordering
    assert train_idx.max() < valid_idx.min()
    assert valid_idx.max() < test_idx.min()

def test_expanding_window_split():
    df = pd.DataFrame({
        'event_id': list(range(10)),
        'event_datetime_utc': pd.date_range('2024-01-01', periods=10)
    })

    splitter = ExpandingWindowSplit(initial_train_size=4, valid_size=2, step_size=2)
    splits = list(splitter.split(df))

    assert len(splits) == 3

    # Fold 1: train=4, valid=2
    assert len(splits[0][1]) == 4
    assert len(splits[0][2]) == 2

    # Fold 2: train=6, valid=2
    assert len(splits[1][1]) == 6
    assert len(splits[1][2]) == 2

    # Fold 3: train=8, valid=2
    assert len(splits[2][1]) == 8
    assert len(splits[2][2]) == 2

def test_rolling_window_split():
    df = pd.DataFrame({
        'event_id': list(range(10)),
        'event_datetime_utc': pd.date_range('2024-01-01', periods=10)
    })

    splitter = RollingWindowSplit(train_size=4, valid_size=2, step_size=2)
    splits = list(splitter.split(df))

    assert len(splits) == 3

    # Fold 1: train=4, valid=2
    assert len(splits[0][1]) == 4
    assert len(splits[0][2]) == 2

    # Fold 2: train=4, valid=2
    assert len(splits[1][1]) == 4
    assert len(splits[1][2]) == 2

    # Fold 3: train=4, valid=2
    assert len(splits[2][1]) == 4
    assert len(splits[2][2]) == 2

    # Check rolling nature
    assert splits[0][1][0] == 0
    assert splits[1][1][0] == 2
    assert splits[2][1][0] == 4
