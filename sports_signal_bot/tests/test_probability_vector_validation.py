import pytest
import numpy as np
from sports_signal_bot.calibration.utils import validate_probability_vectors

def test_validate_probability_vectors():
    X_valid = np.array([[0.5, 0.5], [0.2, 0.8]])
    assert validate_probability_vectors(X_valid, 2) is True

    # Wrong classes
    assert validate_probability_vectors(X_valid, 3) is False

    # Doesn't sum to 1
    X_invalid_sum = np.array([[0.5, 0.6], [0.2, 0.8]])
    assert validate_probability_vectors(X_invalid_sum, 2) is False

    # Out of bounds
    X_invalid_bounds = np.array([[-0.1, 1.1], [0.2, 0.8]])
    assert validate_probability_vectors(X_invalid_bounds, 2) is False
