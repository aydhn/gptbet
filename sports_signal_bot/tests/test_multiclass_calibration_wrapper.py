import pytest
import numpy as np
from sports_signal_bot.calibration.factory import CalibrationFactory

def test_multiclass_wrapper_calibrator():
    calibrator = CalibrationFactory.create("multiclass_wrapper", {"base_method": "binary_sigmoid"})

    X_train = np.array([
        [0.7, 0.2, 0.1],
        [0.2, 0.6, 0.2],
        [0.1, 0.1, 0.8],
        [0.4, 0.4, 0.2]
    ])
    y_train = np.array([0, 1, 2, 0])

    calibrator.fit(X_train, y_train)
    X_cal = calibrator.transform(X_train)

    assert X_cal.shape == X_train.shape

    # Ensure they sum to 1
    np.testing.assert_allclose(X_cal.sum(axis=1), 1.0, atol=1e-5)

    # Ensure probabilities are bounded
    assert np.all(X_cal >= 0) and np.all(X_cal <= 1)
