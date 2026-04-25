import datetime
from typing import Any, Dict, List

from sports_signal_bot.research.contracts import WindowDefinition


def validate_window_data_sufficiency(
    window: WindowDefinition,
    train_count: int,
    calibration_count: int,
    forward_count: int,
    minimum_rows: int,
) -> Dict[str, Any]:
    """
    Checks if a window has enough data across its stages.
    """
    issues = []
    sufficient = True

    if train_count < minimum_rows:
        issues.append(f"Train rows ({train_count}) < minimum ({minimum_rows})")
        sufficient = False

    if window.calibration_start and calibration_count < minimum_rows:
        issues.append(
            f"Calibration rows ({calibration_count}) < minimum ({minimum_rows})"
        )
        sufficient = False

    if forward_count == 0:
        issues.append("Forward test rows is 0")
        sufficient = False

    return {"is_sufficient": sufficient, "issues": issues}


def decide_skip_or_degrade(
    sufficiency_info: Dict[str, Any], skip_if_insufficient: bool
) -> str:
    """
    Decides whether to skip a period or proceed with warnings.
    """
    if sufficiency_info["is_sufficient"]:
        return "proceed"
    if skip_if_insufficient:
        return "skip"
    return "proceed_with_warnings"


def summarize_data_shortfall(sufficiency_info: Dict[str, Any]) -> str:
    """Summarizes why data was insufficient."""
    if sufficiency_info["is_sufficient"]:
        return "Data sufficient."
    return "Insufficient data: " + "; ".join(sufficiency_info["issues"])
