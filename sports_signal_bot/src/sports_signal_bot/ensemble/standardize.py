from typing import Dict, Any, List
from .contracts import StandardizedPredictionRecord

def standardize_prediction(
    event_id: str,
    sport: str,
    market_type: str,
    source_family: str,
    source_name: str,
    class_labels: List[str],
    probabilities: Dict[str, float],
    predicted_class: str,
    is_calibrated: bool = False,
    source_run_id: str = None,
    calibration_method: str = None,
    label_name: str = None,
    metadata: Dict[str, Any] = None
) -> StandardizedPredictionRecord:
    """Helper to create a standardized prediction record."""
    return StandardizedPredictionRecord(
        event_id=event_id,
        sport=sport,
        market_type=market_type,
        source_family=source_family,
        source_name=source_name,
        class_labels=class_labels,
        probabilities=probabilities,
        predicted_class=predicted_class,
        is_calibrated=is_calibrated,
        source_run_id=source_run_id,
        calibration_method=calibration_method,
        label_name=label_name,
        metadata=metadata or {}
    )
