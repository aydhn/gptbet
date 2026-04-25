import numpy as np
import pytest

from sports_signal_bot.calibration.factory import CalibrationFactory


def test_binary_identity_calibrator():
    calibrator = CalibrationFactory.create("binary_identity")
    X = np.array([[0.2, 0.8], [0.6, 0.4]])
    y = np.array([1, 0])

    calibrator.fit(X, y)
    X_cal = calibrator.transform(X)

    np.testing.assert_allclose(X, X_cal)
    assert calibrator.is_fitted


def test_multiclass_identity_calibrator():
    calibrator = CalibrationFactory.create("multiclass_identity")
    X = np.array([[0.2, 0.5, 0.3], [0.6, 0.2, 0.2]])
    y = np.array([1, 0])

    calibrator.fit(X, y)
    X_cal = calibrator.transform(X)

    np.testing.assert_allclose(X, X_cal)
    assert calibrator.is_fitted
