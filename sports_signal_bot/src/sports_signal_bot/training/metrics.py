from typing import Any, Dict

import numpy as np
from sklearn.metrics import (accuracy_score, brier_score_loss, f1_score,
                             log_loss)


def evaluate_classification_metrics(
    y_true: np.ndarray,
    y_pred_proba: np.ndarray,
    y_pred: np.ndarray,
    classes: np.ndarray,
) -> Dict[str, float]:
    """Evaluate common classification metrics."""
    metrics = {}

    # Accuracy
    metrics["accuracy"] = float(accuracy_score(y_true, y_pred))

    # Log loss
    try:
        metrics["log_loss"] = float(log_loss(y_true, y_pred_proba, labels=classes))
    except ValueError:
        # Might happen if classes are missing in y_true, fallback or NaN
        metrics["log_loss"] = float("nan")

    # Is it binary?
    if len(classes) == 2:
        # Assuming classes[1] is the positive class
        # Ensure we don't index out of bounds if y_pred_proba is 1D (should be 2D though)
        if y_pred_proba.ndim == 2 and y_pred_proba.shape[1] == 2:
            prob_pos = y_pred_proba[:, 1]
            try:
                metrics["brier_score"] = float(
                    brier_score_loss(y_true, prob_pos, pos_label=classes[1])
                )
            except ValueError:
                metrics["brier_score"] = float("nan")

            metrics["f1"] = float(
                f1_score(y_true, y_pred, pos_label=classes[1], zero_division=0)
            )
    else:
        # Multiclass F1
        metrics["macro_f1"] = float(
            f1_score(y_true, y_pred, average="macro", zero_division=0)
        )
        # Brier score for multiclass (sklearn doesn't have a direct brier multiclass, but we can compute it)
        # BS = 1/N * sum( sum( (y_ik - p_ik)^2 ) )
        # where y_ik is 1 if class k is true class, 0 otherwise

        # Simple multiclass brier:
        y_true_ohe = np.zeros_like(y_pred_proba)
        # Create mapping from class label to index
        class_to_idx = {c: i for i, c in enumerate(classes)}

        # Handle cases where true class might not be in the training classes (unlikely but safe)
        valid_mask = np.isin(y_true, classes)
        if valid_mask.any():
            indices = np.array([class_to_idx[y] for y in y_true[valid_mask]])
            y_true_ohe[np.arange(len(y_true))[valid_mask], indices] = 1.0

            brier_mc = np.mean(np.sum((y_pred_proba - y_true_ohe) ** 2, axis=1))
            metrics["brier_score_mc"] = float(brier_mc)
        else:
            metrics["brier_score_mc"] = float("nan")

    return metrics
