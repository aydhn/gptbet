from typing import Any, Dict, Optional

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

from sports_signal_bot.calibration.base import BaseCalibrator
from sports_signal_bot.calibration.registry import CalibrationRegistry
from sports_signal_bot.calibration.utils import (
    clip_probabilities, expand_multiclass_probabilities,
    flatten_binary_probabilities)


@CalibrationRegistry.register("binary_sigmoid")
class BinarySigmoidCalibrator(BaseCalibrator):
    """
    Platt Scaling (Sigmoid) calibration for binary probabilities.
    Fits a logistic regression model on the log-odds of the raw probabilities.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.eps = self.config.get("clip_eps", 1e-15)
        self.model = LogisticRegression(
            solver="lbfgs", C=99999999.9
        )  # minimal regularization

    def _to_log_odds(self, p: np.ndarray) -> np.ndarray:
        p_clipped = clip_probabilities(p, eps=self.eps)
        return np.log(p_clipped / (1.0 - p_clipped))

    def fit(self, X: np.ndarray, y: np.ndarray) -> "BinarySigmoidCalibrator":
        # Assume X is (N, 2), we calibrate the positive class (index 1)
        if len(X.shape) != 2 or X.shape[1] != 2:
            raise ValueError("BinarySigmoidCalibrator requires X of shape (N, 2)")

        p1 = flatten_binary_probabilities(X, positive_class_index=1)
        log_odds = self._to_log_odds(p1).reshape(-1, 1)

        # Ensure y is binary 0/1
        y_binary = (y == 1).astype(int)

        self.model.fit(log_odds, y_binary)
        self.is_fitted = True
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise RuntimeError("Calibrator not fitted.")

        p1 = flatten_binary_probabilities(X, positive_class_index=1)
        log_odds = self._to_log_odds(p1).reshape(-1, 1)

        # predict_proba returns [P(y=0), P(y=1)]
        calibrated_probs = self.model.predict_proba(log_odds)
        return clip_probabilities(calibrated_probs, eps=self.eps)

    def save_artifact(self, path: str) -> None:
        state = {
            "is_fitted": self.is_fitted,
            "config": self.config,
            "model": self.model,
        }
        joblib.dump(state, path)

    def load_artifact(self, path: str) -> None:
        state = joblib.load(path)
        self.is_fitted = state["is_fitted"]
        self.config = state["config"]
        self.model = state["model"]
