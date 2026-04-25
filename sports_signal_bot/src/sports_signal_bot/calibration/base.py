from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import numpy as np


class BaseCalibrator(ABC):
    """
    Abstract base class for all probability calibrators.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.is_fitted = False

    @abstractmethod
    def fit(self, X: np.ndarray, y: np.ndarray) -> "BaseCalibrator":
        """Fits the calibrator on raw probabilities X and true targets y."""
        pass

    @abstractmethod
    def transform(self, X: np.ndarray) -> np.ndarray:
        """Transforms raw probabilities X to calibrated probabilities."""
        pass

    def fit_transform(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Fits and transforms."""
        return self.fit(X, y).transform(X)

    @abstractmethod
    def save_artifact(self, path: str) -> None:
        """Saves the fitted calibrator state to disk."""
        pass

    @abstractmethod
    def load_artifact(self, path: str) -> None:
        """Loads the fitted calibrator state from disk."""
        pass

    def describe(self) -> Dict[str, Any]:
        """Returns metadata about the calibrator."""
        return {
            "name": self.__class__.__name__,
            "is_fitted": self.is_fitted,
            "config": self.config,
        }
