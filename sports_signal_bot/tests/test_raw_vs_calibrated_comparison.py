import pytest

from sports_signal_bot.calibration.comparison import create_comparison_record
from sports_signal_bot.calibration.contracts import CalibrationSummary


def test_create_comparison_record():
    raw = CalibrationSummary(
        method="raw",
        log_loss=0.6,
        brier_score=0.2,
        ece=0.1,
        mce=0.2,
        mean_confidence=0.8,
        calibration_coverage=1.0,
    )
    calib = CalibrationSummary(
        method="calib",
        log_loss=0.5,
        brier_score=0.15,
        ece=0.08,
        mce=0.05,
        mean_confidence=0.7,
        calibration_coverage=1.0,
    )

    comp = create_comparison_record("run_1", raw, calib)

    assert comp.delta_log_loss < 0
    assert comp.delta_ece < 0
    assert comp.calibration_improvement is True
    assert comp.possible_overfit_warning is False


def test_possible_overfit_warning():
    raw = CalibrationSummary(
        method="raw",
        log_loss=0.6,
        brier_score=0.2,
        ece=0.1,
        mce=0.2,
        mean_confidence=0.8,
        calibration_coverage=1.0,
    )
    calib = CalibrationSummary(
        method="calib",
        log_loss=0.59,
        brier_score=0.19,
        ece=0.001,
        mce=0.005,
        mean_confidence=0.75,
        calibration_coverage=1.0,
    )

    comp = create_comparison_record("run_1", raw, calib, overfit_ece_threshold=0.01)

    assert comp.possible_overfit_warning is True
