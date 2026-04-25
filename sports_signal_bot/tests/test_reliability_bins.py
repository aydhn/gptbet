import numpy as np
import pytest

from sports_signal_bot.calibration.reliability import generate_reliability_bins


def test_generate_reliability_bins_binary():
    y_true = np.array([0, 0, 1, 1, 1])
    # Positive class probs
    y_prob = np.array([[0.9, 0.1], [0.85, 0.15], [0.2, 0.8], [0.15, 0.85], [0.1, 0.9]])

    bins = generate_reliability_bins(y_true, y_prob, n_bins=5, positive_class_index=1)
    assert len(bins) == 5

    # Bin 0: [0, 0.2) -> 0.1, 0.15
    assert bins[0].count == 2
    assert bins[0].empirical_frequency == 0.0
    np.testing.assert_allclose(bins[0].mean_predicted_probability, 0.125)

    # Bin 4: [0.8, 1.0] -> 0.8, 0.85, 0.9
    assert bins[4].count == 3
    assert bins[4].empirical_frequency == 1.0
    np.testing.assert_allclose(bins[4].mean_predicted_probability, 0.85)

    # Empty bins
    assert bins[1].count == 0
    assert bins[2].count == 0
