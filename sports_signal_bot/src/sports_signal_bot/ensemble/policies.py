from typing import Dict, List, Optional

from .contracts import StandardizedPredictionRecord


def apply_calibrated_preference_policy(
    predictions: List[StandardizedPredictionRecord], mode: str = "prefer_calibrated"
) -> List[StandardizedPredictionRecord]:
    """
    Applies selection policy when multiple versions of the same source exist.
    Modes: 'prefer_calibrated', 'calibrated_only', 'raw_only', 'all'
    """
    if mode == "all":
        return predictions

    grouped: Dict[str, List[StandardizedPredictionRecord]] = {}
    for p in predictions:
        # Group by a unique identifier for the underlying source model
        # Using source_name and source_run_id if available to link raw and calibrated
        key = f"{p.source_name}_{p.source_run_id}" if p.source_run_id else p.source_name
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(p)

    selected = []
    for key, group in grouped.items():
        if mode == "calibrated_only":
            cals = [p for p in group if p.is_calibrated]
            selected.extend(cals)
        elif mode == "raw_only":
            raws = [p for p in group if not p.is_calibrated]
            selected.extend(raws)
        elif mode == "prefer_calibrated":
            cals = [p for p in group if p.is_calibrated]
            if cals:
                # If there are calibrated versions, use only the first one
                selected.append(cals[0])
            else:
                # Fallback to the first raw version
                selected.append(group[0])

    return selected
