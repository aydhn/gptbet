import pytest
import numpy as np
import pandas as pd
from sports_signal_bot.evaluation.metrics import compute_all_metrics

def test_metric_consistency_perfect_predictions():
    df = pd.DataFrame({
        "true_label": [1, 0, 1, 0],
        "predicted_class": [1, 0, 1, 0],
        "prob_0": [0.0, 1.0, 0.0, 1.0],
        "prob_1": [1.0, 0.0, 1.0, 0.0]
    })

    metrics, _ = compute_all_metrics(df, "A", proba_cols=["prob_0", "prob_1"], labels=[0, 1])

    assert metrics["accuracy"] == 1.0
    assert np.isclose(metrics["log_loss"], 0.0, atol=1e-5)
    assert np.isclose(metrics["brier"], 0.0, atol=1e-5)
