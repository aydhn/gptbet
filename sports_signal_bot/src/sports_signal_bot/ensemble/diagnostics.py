from typing import Dict, List

import numpy as np


def probability_dispersion(
    probs_list: List[Dict[str, float]], class_labels: List[str]
) -> float:
    """Calculates the average variance of probabilities across sources for each class."""
    if not probs_list or not class_labels:
        return 0.0

    variances = []
    for cls in class_labels:
        cls_probs = [p.get(cls, 0.0) for p in probs_list]
        variances.append(np.var(cls_probs))

    return float(np.mean(variances))


def top_class_disagreement(
    probs_list: List[Dict[str, float]], class_labels: List[str]
) -> float:
    """Calculates the fraction of sources that disagree on the top class."""
    if not probs_list or len(probs_list) <= 1:
        return 0.0

    top_classes = []
    for probs in probs_list:
        if probs:
            top_cls = max(probs.items(), key=lambda x: x[1])[0]
            top_classes.append(top_cls)

    if not top_classes:
        return 0.0

    most_common = max(set(top_classes), key=top_classes.count)
    disagreements = sum(1 for c in top_classes if c != most_common)
    return float(disagreements / len(top_classes))


def calculate_entropy(probs: Dict[str, float]) -> float:
    """Calculates the entropy of a probability distribution."""
    if not probs:
        return 0.0

    entropy = 0.0
    for p in probs.values():
        if p > 0:
            entropy -= p * np.log2(p)
    return entropy


def source_count_summary(
    predictions: List["StandardizedPredictionRecord"],
) -> Dict[str, int]:
    from collections import Counter

    counts = Counter([p.source_family for p in predictions])
    return dict(counts)
