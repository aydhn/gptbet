import numpy as np
import pandas as pd
import pytest

from sports_signal_bot.training.predictions import \
    format_validation_predictions


def test_format_validation_predictions():
    df = pd.DataFrame({"event_id": ["e1", "e2", "e3"], "target": [0, 1, 1]})

    valid_indices = np.array([0, 1, 2])
    y_pred_proba = np.array([[0.8, 0.2], [0.3, 0.7], [0.6, 0.4]])
    classes = np.array([0, 1])

    records = format_validation_predictions(
        df=df,
        valid_indices=valid_indices,
        y_pred_proba=y_pred_proba,
        classes=classes,
        sport="test",
        market_type="test",
        label_name="test_lbl",
        target_column="target",
        model_name="test_model",
        fold_id="fold_1",
        split_metadata={},
    )

    assert len(records) == 3

    r1 = records[0]
    assert r1.event_id == "e1"
    assert r1.true_class_index == 0
    assert r1.predicted_class == 0
    assert r1.predicted_probabilities["0"] == 0.8
    assert r1.predicted_probabilities["1"] == 0.2

    r3 = records[2]
    assert r3.event_id == "e3"
    assert r3.true_class_index == 1
    assert r3.predicted_class == 0  # 0.6 > 0.4
