import numpy as np
from typing import Dict, Any, Optional, List
import joblib

from sports_signal_bot.calibration.base import BaseCalibrator
from sports_signal_bot.calibration.registry import CalibrationRegistry
from sports_signal_bot.calibration.factory import CalibrationFactory
from sports_signal_bot.calibration.utils import clip_probabilities

@CalibrationRegistry.register("multiclass_wrapper")
class MulticlassWrapperCalibrator(BaseCalibrator):
    """
    A practical One-Vs-Rest wrapper for multiclass calibration.
    Fits a binary calibrator for each class independently, then normalizes
    the resulting probabilities to sum to 1.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.eps = self.config.get("clip_eps", 1e-15)
        self.base_calibrator_method = self.config.get("base_method", "binary_sigmoid")
        self.base_calibrator_config = self.config.get("base_config", {})
        self.calibrators: List[BaseCalibrator] = []
        self.n_classes = 0

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'MulticlassWrapperCalibrator':
        self.n_classes = X.shape[1]
        self.calibrators = []

        for i in range(self.n_classes):
            # Create a base calibrator for this class
            calibrator = CalibrationFactory.create(self.base_calibrator_method, self.base_calibrator_config)

            # Prepare binary data for One-Vs-Rest
            # X_bin: [P(not class i), P(class i)]
            p_i = X[:, i]
            X_bin = np.column_stack((1.0 - p_i, p_i))
            y_bin = (y == i).astype(int)

            try:
                if len(np.unique(y_bin)) > 1:
                    calibrator.fit(X_bin, y_bin)
                else:
                    # Fallback to Identity if a class is entirely missing from the validation set targets
                    calibrator = CalibrationFactory.create("binary_identity")
                    calibrator.fit(X_bin, y_bin)
            except Exception as e:
                calibrator = CalibrationFactory.create("binary_identity")
                calibrator.fit(X_bin, y_bin)

            self.calibrators.append(calibrator)

        self.is_fitted = True
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise RuntimeError("Calibrator not fitted.")

        if X.shape[1] != self.n_classes:
            raise ValueError(f"Expected {self.n_classes} classes, got {X.shape[1]}")

        N = X.shape[0]
        calibrated_probs = np.zeros_like(X)

        # Get calibrated probability for each class
        for i in range(self.n_classes):
            p_i = X[:, i]
            X_bin = np.column_stack((1.0 - p_i, p_i))
            # transform returns [P(not class i), P(class i)], we want index 1
            calibrated_bin = self.calibrators[i].transform(X_bin)
            calibrated_probs[:, i] = calibrated_bin[:, 1]

        # Normalize to sum to 1
        row_sums = calibrated_probs.sum(axis=1, keepdims=True)
        # Avoid division by zero just in case
        row_sums[row_sums == 0] = 1.0
        calibrated_probs = calibrated_probs / row_sums

        return clip_probabilities(calibrated_probs, eps=self.eps)

    def save_artifact(self, path: str) -> None:
        state = {
            "is_fitted": self.is_fitted,
            "config": self.config,
            "n_classes": self.n_classes,
        }
        joblib.dump({"state": state, "calibrators": self.calibrators}, path)

    def load_artifact(self, path: str) -> None:
        data = joblib.load(path)
        self.is_fitted = data["state"]["is_fitted"]
        self.config = data["state"]["config"]
        self.n_classes = data["state"]["n_classes"]
        self.calibrators = data["calibrators"]
