import numpy as np
from typing import Dict, Any, Optional
from sklearn.isotonic import IsotonicRegression
import joblib

from sports_signal_bot.calibration.base import BaseCalibrator
from sports_signal_bot.calibration.registry import CalibrationRegistry
from sports_signal_bot.calibration.utils import flatten_binary_probabilities, expand_multiclass_probabilities, clip_probabilities
from sports_signal_bot.core.logger import get_logger

logger = get_logger("IsotonicCalibrator")

@CalibrationRegistry.register("binary_isotonic")
class BinaryIsotonicCalibrator(BaseCalibrator):
    """
    Isotonic Regression calibration for binary probabilities.
    Non-parametric approach, requires more data than sigmoid to avoid overfitting.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.eps = self.config.get("clip_eps", 1e-15)
        self.min_samples = self.config.get("isotonic_min_samples", 1000)
        self.out_of_bounds = self.config.get("out_of_bounds", "clip")
        self.model = IsotonicRegression(out_of_bounds=self.out_of_bounds)

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'BinaryIsotonicCalibrator':
        if len(X.shape) != 2 or X.shape[1] != 2:
            raise ValueError("BinaryIsotonicCalibrator requires X of shape (N, 2)")

        if len(X) < self.min_samples:
            logger.warning(f"Isotonic calibration fitted with {len(X)} samples, less than recommended {self.min_samples}. Prone to overfitting.")

        p1 = flatten_binary_probabilities(X, positive_class_index=1)
        y_binary = (y == 1).astype(int)

        self.model.fit(p1, y_binary)
        self.is_fitted = True
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise RuntimeError("Calibrator not fitted.")

        p1 = flatten_binary_probabilities(X, positive_class_index=1)

        calibrated_p1 = self.model.predict(p1)
        # Expand back to 2D
        calibrated_probs = expand_multiclass_probabilities(calibrated_p1, positive_class_index=1)
        return clip_probabilities(calibrated_probs, eps=self.eps)

    def save_artifact(self, path: str) -> None:
        state = {
            "is_fitted": self.is_fitted,
            "config": self.config,
            "model": self.model
        }
        joblib.dump(state, path)

    def load_artifact(self, path: str) -> None:
        state = joblib.load(path)
        self.is_fitted = state["is_fitted"]
        self.config = state["config"]
        self.model = state["model"]
