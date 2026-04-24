import pandas as pd
import numpy as np
from typing import Dict, Any
from .interfaces import BasePredictor

class DummyPredictor(BasePredictor):
    def __init__(self):
        self.is_fitted = False

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        self.is_fitted = True

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet.")
        # Return random probabilities for 2 classes
        probas = np.random.rand(len(X))
        return np.column_stack((1 - probas, probas))

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        probas = self.predict_proba(X)
        return (probas[:, 1] > 0.5).astype(int)

    def save(self, path: str) -> None:
        # Dummy save
        pass

    def load(self, path: str) -> None:
        # Dummy load
        self.is_fitted = True

    def get_metadata(self) -> Dict[str, Any]:
        return {"name": "DummyPredictor", "version": "1.0"}
