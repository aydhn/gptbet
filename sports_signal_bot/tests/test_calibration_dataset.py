import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timezone

from sports_signal_bot.training.contracts import ValidationPredictionRecord
from sports_signal_bot.calibration.dataset import build_calibration_dataset_from_validation_predictions, extract_calibration_features_and_targets

def test_build_calibration_dataset():
    records = [
        ValidationPredictionRecord(
            event_id="1",
            sport="football",
            market_type="1x2",
            label_name="football_1x2",
            true_class_index=1,
            predicted_class=1,
            predicted_probabilities={"home": 0.2, "draw": 0.5, "away": 0.3},
            model_name="test_model",
            fold_id="f1",
            timestamp_utc=datetime.now(timezone.utc).isoformat()
        ),
        ValidationPredictionRecord(
            event_id="2",
            sport="football",
            market_type="1x2",
            label_name="football_1x2",
            true_class_index=None, # Missing label
            predicted_class=0,
            predicted_probabilities={"home": 0.6, "draw": 0.2, "away": 0.2},
            model_name="test_model",
            fold_id="f1",
            timestamp_utc=datetime.now(timezone.utc).isoformat()
        )
    ]

    class_labels = ["home", "draw", "away"]
    df = build_calibration_dataset_from_validation_predictions(records, class_labels)

    assert len(df) == 2
    assert "prob_home" in df.columns
    assert "prob_draw" in df.columns
    assert "prob_away" in df.columns
    assert df.iloc[0]["true_label"] == "draw"
    assert pd.isna(df.iloc[1]["true_label"])

    # Drop missing for extraction
    df_clean = df.dropna(subset=["true_label"])
    assert len(df_clean) == 1

    X, y = extract_calibration_features_and_targets(df_clean, class_labels)
    assert X.shape == (1, 3)
    assert y.shape == (1,)
    np.testing.assert_allclose(X[0], [0.2, 0.5, 0.3])
    assert y[0] == 1
