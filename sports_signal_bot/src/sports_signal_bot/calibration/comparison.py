from typing import Dict, Optional
from sports_signal_bot.calibration.contracts import CalibrationSummary, CalibrationComparisonRecord

def create_comparison_record(
    run_id: str,
    raw_summary: CalibrationSummary,
    calibrated_summary: CalibrationSummary,
    overfit_ece_threshold: float = 0.05
) -> CalibrationComparisonRecord:
    """
    Compares raw and calibrated metrics and creates a summary record.
    """
    delta_log_loss = calibrated_summary.log_loss - raw_summary.log_loss
    delta_brier = calibrated_summary.brier_score - raw_summary.brier_score
    delta_ece = calibrated_summary.ece - raw_summary.ece

    # Simple heuristic: if log loss improves (goes down) or ECE improves (goes down) significantly
    improvement = (delta_log_loss < -1e-4) or (delta_ece < -1e-3)

    # Overfit warning: if calibrated ECE is super low, maybe overfitting the validation set
    possible_overfit = False
    if calibrated_summary.ece < overfit_ece_threshold and (raw_summary.ece - calibrated_summary.ece) > 0.05:
         possible_overfit = True

    return CalibrationComparisonRecord(
        run_id=run_id,
        raw_log_loss=raw_summary.log_loss,
        calibrated_log_loss=calibrated_summary.log_loss,
        delta_log_loss=delta_log_loss,
        raw_brier_score=raw_summary.brier_score,
        calibrated_brier_score=calibrated_summary.brier_score,
        delta_brier_score=delta_brier,
        raw_ece=raw_summary.ece,
        calibrated_ece=calibrated_summary.ece,
        delta_ece=delta_ece,
        calibration_improvement=improvement,
        possible_overfit_warning=possible_overfit
    )
