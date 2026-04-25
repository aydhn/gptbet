import numpy as np
import pytest

from sports_signal_bot.calibration.factory import CalibrationFactory


def test_binary_sigmoid_calibrator():
    calibrator = CalibrationFactory.create("binary_sigmoid")

    # Simulate uncalibrated probabilities that are too extreme
    X_train = np.array(
        [
            [0.99, 0.01],  # true=0
            [0.99, 0.01],  # true=1  (overconfident wrong)
            [0.01, 0.99],  # true=1
            [0.01, 0.99],  # true=0  (overconfident wrong)
        ]
    )
    y_train = np.array([0, 1, 1, 0])

    calibrator.fit(X_train, y_train)
    X_cal = calibrator.transform(X_train)

    # Since accuracy is 50%, the calibrated probabilities should be pulled towards 0.5
    # rather than staying at 0.99
    assert X_cal.shape == X_train.shape
    assert np.allclose(X_cal.sum(axis=1), 1.0)

    # Check that they are less extreme
    assert np.all(X_cal[:, 1] > 0.1) and np.all(X_cal[:, 1] < 0.9)
