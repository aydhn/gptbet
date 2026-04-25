from typing import Dict, List, Optional



def validate_market_compatibility(
    source_classes: List[str], target_classes: List[str]
) -> bool:
    """Check if source classes can be aligned to target classes."""
    return set(source_classes).issubset(set(target_classes))


def align_probability_vector(
    probs: Dict[str, float], source_classes: List[str], target_classes: List[str]
) -> Optional[Dict[str, float]]:
    """Aligns a probability dictionary to match the target class order. Missing classes get 0.0."""
    if not validate_market_compatibility(source_classes, target_classes):
        return None

    aligned = {}
    for tc in target_classes:
        aligned[tc] = probs.get(tc, 0.0)

    return aligned


def align_predictions_to_reference_classes(
    predictions: List["StandardizedPredictionRecord"], reference_classes: List[str]
) -> List["StandardizedPredictionRecord"]:
    """Aligns multiple prediction records to a reference class list."""

    aligned_preds = []

    for p in predictions:
        aligned_probs = align_probability_vector(
            p.probabilities, p.class_labels, reference_classes
        )
        if aligned_probs is not None:
            # Create a copy with aligned probs and classes
            new_p = p.model_copy(deep=True)
            new_p.class_labels = reference_classes.copy()
            new_p.probabilities = aligned_probs
            aligned_preds.append(new_p)
        else:
            # Handle incompatible source appropriately, perhaps log a warning
            pass

    return aligned_preds


def drop_incompatible_sources(
    predictions: List["StandardizedPredictionRecord"], reference_classes: List[str]
) -> List["StandardizedPredictionRecord"]:
    """Returns only predictions that are compatible with the reference classes."""
    return [
        p
        for p in predictions
        if validate_market_compatibility(p.class_labels, reference_classes)
    ]
