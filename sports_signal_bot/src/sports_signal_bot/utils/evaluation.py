from typing import Any, Dict

import numpy as np
from sklearn.metrics import accuracy_score, brier_score_loss, log_loss


class EvaluationHelper:
    @staticmethod
    def evaluate_predictions(
        y_true: np.ndarray, y_pred_proba: np.ndarray
    ) -> Dict[str, float]:
        """
        Evaluates predictions using basic metrics.
        Assumes binary classification for Brier score currently.
        """
        y_pred = (y_pred_proba[:, 1] > 0.5).astype(int)

        metrics = {
            "accuracy": float(accuracy_score(y_true, y_pred)),
        }

        # In a smoke test we might only have one class present in y_true
        labels = [0, 1] if y_pred_proba.shape[1] == 2 else None
        try:
            metrics["log_loss"] = float(log_loss(y_true, y_pred_proba, labels=labels))
        except ValueError:
            # Handle edge case where there's an issue with the labels/data
            metrics["log_loss"] = 0.0

        # Brier score only applies well to binary out of the box in sklearn
        if y_pred_proba.shape[1] == 2:
            metrics["brier_score"] = float(brier_score_loss(y_true, y_pred_proba[:, 1]))

        return metrics
