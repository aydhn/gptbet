import numpy as np
from typing import Dict, Any, Optional
import joblib
from sports_signal_bot.calibration.base import BaseCalibrator
from sports_signal_bot.calibration.registry import CalibrationRegistry

@CalibrationRegistry.register("binary_identity")
class BinaryIdentityCalibrator(BaseCalibrator):
    """
    A baseline calibrator that performs no transformation.
    Useful as a fallback or for comparison.
    """

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'BinaryIdentityCalibrator':
        self.is_fitted = True
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise RuntimeError("Calibrator not fitted.")
        return X.copy()

    def save_artifact(self, path: str) -> None:
        joblib.dump({"is_fitted": self.is_fitted, "config": self.config}, path)

    def load_artifact(self, path: str) -> None:
        state = joblib.load(path)
        self.is_fitted = state["is_fitted"]
        self.config = state["config"]
