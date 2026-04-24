import pytest
import pandas as pd
import numpy as np
from sports_signal_bot.training.predictions import format_validation_predictions
from sports_signal_bot.labels.contracts import BenchmarkPredictionRecord

def test_benchmark_alignment():
    # We want to ensure that our ValidationPredictionRecord maps nicely or resembles BenchmarkPredictionRecord
    # This test asserts that the schema concepts align.

    df = pd.DataFrame({
        'event_id': ['e1'],
        'target': [1]
    })

    valid_indices = np.array([0])
    y_pred_proba = np.array([[0.2, 0.8]])
    classes = np.array([0, 1])

    valid_records = format_validation_predictions(
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
        split_metadata={}
    )

    vr = valid_records[0]

    # Can we construct a BenchmarkPredictionRecord from this?
    br = BenchmarkPredictionRecord(
        event_id=vr.event_id,
        market_type=vr.market_type,
        benchmark_name=vr.model_name,
        predicted_class=str(vr.predicted_class),
        predicted_probabilities=vr.predicted_probabilities,
        metadata={"fold_id": vr.fold_id, "split_metadata": vr.split_metadata}
    )

    assert br.event_id == "e1"
    assert br.benchmark_name == "test_model"
    assert br.predicted_class == "1"
    assert br.predicted_probabilities["1"] == 0.8
