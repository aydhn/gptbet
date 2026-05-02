from typing import Dict
from src.sports_signal_bot.resilience_fabric.contracts import TrustLoopCalibrationRecord

def enforce_calibration_safety(proposed: Dict[str, float], baseline: Dict[str, float], max_increase: float, max_decrease: float, hard_floor: float) -> Dict[str, float]:
    bounded = {}
    for key, base_val in baseline.items():
        prop_val = proposed.get(key, base_val)

        diff = prop_val - base_val
        if diff > max_increase:
            prop_val = base_val + max_increase
        elif diff < -max_decrease:
            prop_val = base_val - max_decrease

        if prop_val < hard_floor:
            prop_val = hard_floor

        bounded[key] = prop_val
    return bounded

def validate_calibration_bounds(record: TrustLoopCalibrationRecord) -> TrustLoopCalibrationRecord:
    # Simulated validation logic
    if record.bounded_adjustments == record.proposed_adjustments:
         record.validation_status = "validated_improvement"
    else:
         record.validation_status = "mixed_result"
         record.warnings.append("Adjustments were bounded by safety rules")
    return record
