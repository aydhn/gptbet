import numpy as np
import pandas as pd
import pytest

from sports_signal_bot.training.contracts import (DatasetSummary,
                                                  TrainingDataset)
from sports_signal_bot.training.trainers.gradient_boosting import \
    GradientBoostingTrainer


def test_gradient_boosting_trainer():
    config = {"model_kwargs": {"max_iter": 10}, "scale_numeric": False}
    trainer = GradientBoostingTrainer(config)
    assert trainer.name == "gradient_boosting"

    # Mock data
    df = pd.DataFrame(
        {
            "feat1": np.random.rand(100),
            "feat2": np.random.rand(100) * 10,
            "target": np.random.randint(0, 2, 100),
        }
    )

    dataset = TrainingDataset(
        summary=DatasetSummary(
            sport="test",
            market_type="test",
            label_name="test",
            total_rows=100,
            valid_rows=100,
            unsupported_rows=0,
            feature_count=2,
            date_range={},
        ),
        feature_columns=["feat1", "feat2"],
        metadata_columns=[],
        target_column="target",
    )

    train_idx = np.arange(80)
    valid_idx = np.arange(80, 100)

    metrics = trainer.fit(dataset, df, train_idx, valid_idx)

    assert trainer.is_fitted
    assert "log_loss" in metrics
    assert "accuracy" in metrics

    # Predict
    preds = trainer.predict(df.iloc[valid_idx])
    assert len(preds) == 20

    probs = trainer.predict_proba(df.iloc[valid_idx])
    assert probs.shape == (20, 2)
