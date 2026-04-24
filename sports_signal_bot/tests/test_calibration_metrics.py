import pytest
import numpy as np
from sports_signal_bot.calibration.metrics import calculate_log_loss, calculate_brier_score, calculate_ece_mce

def test_calculate_log_loss_binary():
    y_true = np.array([0, 1, 1, 0])
    y_prob = np.array([[0.9, 0.1], [0.2, 0.8], [0.3, 0.7], [0.6, 0.4]])

    loss = calculate_log_loss(y_true, y_prob)
    assert isinstance(loss, float)
    assert loss > 0

def test_calculate_brier_score_binary():
    y_true = np.array([0, 1, 1, 0])
    y_prob = np.array([[0.9, 0.1], [0.2, 0.8], [0.3, 0.7], [0.6, 0.4]])

    brier = calculate_brier_score(y_true, y_prob, positive_class_index=1)
    np.testing.assert_allclose(brier, 0.075)

def test_calculate_ece_binary():
    y_true = np.array([1, 1, 0, 0])
    # Very confident and correct
    y_prob = np.array([[0.1, 0.9], [0.1, 0.9], [0.9, 0.1], [0.9, 0.1]])

    ece, mce = calculate_ece_mce(y_true, y_prob, n_bins=5, positive_class_index=1)

    # In this exact case:
    # Bins [0, 0.2), ..., [0.8, 1.0]
    # confidences = [0.9, 0.9, 0.1, 0.1]
    # accuracies = [1, 1, 1, 1]
    # Bin [0.8, 1.0]: count 2, conf = 0.9, acc = 1.0 -> err = 0.1
    # Bin [0, 0.2): count 2, conf = 0.1, acc = 1.0 -> err = 0.9
    # This was a bad test design, because if y_true is 0, and prob is [0.9, 0.1], confidence in positive class is 0.1. The truth for positive class is 0.
    # Wait, if y_true=0, then acc for positive class is 0.
    # So conf=0.1, acc=0. Error = 0.1 - 0 = 0.1!
    # Let's re-verify:
    # Bin [0.8, 1.0]: conf=0.9, acc=(y=1)=1 -> gap = |0.9 - 1| = 0.1
    # Bin [0, 0.2): conf=0.1, acc=(y=0)=0 -> gap = |0.1 - 0| = 0.1
    # So ece and mce should both be exactly 0.1
    np.testing.assert_allclose(ece, 0.1)
    np.testing.assert_allclose(mce, 0.1)
