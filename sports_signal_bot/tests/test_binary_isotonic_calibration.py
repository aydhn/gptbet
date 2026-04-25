import numpy as np
import pytest

from sports_signal_bot.calibration.factory import CalibrationFactory


def test_binary_isotonic_calibrator():
    calibrator = CalibrationFactory.create(
        "binary_isotonic", {"isotonic_min_samples": 2}
    )

    X_train = np.array(
        [
            [0.9, 0.1],
            [0.8, 0.2],
            [0.4, 0.6],
            [0.1, 0.9],
        ]
    )
    y_train = np.array([0, 0, 1, 1])

    calibrator.fit(X_train, y_train)
    X_cal = calibrator.transform(X_train)

    assert X_cal.shape == X_train.shape
    assert np.allclose(X_cal.sum(axis=1), 1.0)

    # For monotonic data, isotonic might map directly to empirical frequencies or keep ordering
    # We mainly test it runs and normalizes correctly here
    assert X_cal[3, 1] >= X_cal[2, 1]
