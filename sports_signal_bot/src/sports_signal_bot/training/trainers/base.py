import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple, List
import joblib
from pathlib import Path

from sports_signal_bot.training.contracts import TrainingDataset
from sports_signal_bot.training.preprocessing import build_preprocessing_pipeline

class BaseTrainer(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.is_fitted = False

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def fit(self, dataset: TrainingDataset, df: pd.DataFrame, train_indices: np.ndarray, valid_indices: Optional[np.ndarray] = None) -> Dict[str, float]:
        """Trains the model on the specified indices, returning validation metrics if valid_indices provided."""
        pass

    @abstractmethod
    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        """Returns class probabilities."""
        pass

    @abstractmethod
    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """Returns class predictions."""
        pass

    @abstractmethod
    def save_artifact(self, path: str) -> None:
        """Saves the trained model and preprocessing artifacts to disk."""
        pass

    @abstractmethod
    def load_artifact(self, path: str) -> None:
        """Loads the trained model and preprocessing artifacts from disk."""
        pass

    @abstractmethod
    def get_feature_importance(self) -> Dict[str, float]:
        """Returns feature importances if applicable."""
        pass


class SklearnClassifierTrainer(BaseTrainer):
    """Base class for Scikit-Learn compatible classifiers."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.model = None
        self.preprocessor = None
        self.feature_columns = []
        self.classes_ = []

    def _build_preprocessor(self, numeric_features: List[str], categorical_features: List[str] = None):
        scale_numeric = self.config.get('scale_numeric', False)
        return build_preprocessing_pipeline(numeric_features, categorical_features, scale_numeric)

    def fit(self, dataset: TrainingDataset, df: pd.DataFrame, train_indices: np.ndarray, valid_indices: Optional[np.ndarray] = None) -> Dict[str, float]:
        self.feature_columns = dataset.feature_columns
        target_col = dataset.target_column

        # In a real setup we might infer categorical/numeric, but here we assume mostly numeric for now
        # You could add logic here to split based on df dtypes
        numeric_features = self.feature_columns
        categorical_features = []

        self.preprocessor = self._build_preprocessor(numeric_features, categorical_features)

        train_df = df.iloc[train_indices]
        X_train = train_df[self.feature_columns]
        y_train = train_df[target_col]

        # Fit preprocessor and transform
        X_train_processed = self.preprocessor.fit_transform(X_train)

        # Fit model
        self.model.fit(X_train_processed, y_train)
        self.classes_ = self.model.classes_
        self.is_fitted = True

        metrics = {}
        if valid_indices is not None and len(valid_indices) > 0:
            valid_df = df.iloc[valid_indices]
            X_valid = valid_df[self.feature_columns]
            y_valid = valid_df[target_col]

            X_valid_processed = self.preprocessor.transform(X_valid)
            y_pred_proba = self.model.predict_proba(X_valid_processed)

            from sklearn.metrics import log_loss, accuracy_score
            metrics['log_loss'] = float(log_loss(y_valid, y_pred_proba, labels=self.classes_))
            y_pred = self.model.predict(X_valid_processed)
            metrics['accuracy'] = float(accuracy_score(y_valid, y_pred))

        return metrics

    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet.")
        X = df[self.feature_columns]
        X_processed = self.preprocessor.transform(X)
        return self.model.predict_proba(X_processed)

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet.")
        X = df[self.feature_columns]
        X_processed = self.preprocessor.transform(X)
        return self.model.predict(X_processed)

    def save_artifact(self, path: str) -> None:
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet.")
        artifact_path = Path(path)
        artifact_path.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, artifact_path / "model.joblib")
        joblib.dump(self.preprocessor, artifact_path / "preprocessor.joblib")
        joblib.dump({"feature_columns": self.feature_columns, "classes_": self.classes_.tolist()}, artifact_path / "metadata.joblib")

    def load_artifact(self, path: str) -> None:
        artifact_path = Path(path)
        self.model = joblib.load(artifact_path / "model.joblib")
        self.preprocessor = joblib.load(artifact_path / "preprocessor.joblib")
        meta = joblib.load(artifact_path / "metadata.joblib")
        self.feature_columns = meta["feature_columns"]
        self.classes_ = np.array(meta["classes_"])
        self.is_fitted = True

    def get_feature_importance(self) -> Dict[str, float]:
        if not self.is_fitted:
            return {}

        # Best effort attempt based on common sklearn attributes
        if hasattr(self.model, "feature_importances_"):
            importances = self.model.feature_importances_
        elif hasattr(self.model, "coef_"):
            importances = np.abs(self.model.coef_[0])
        else:
            return {}

        # Try to map back to feature names.
        # This is simple if only numeric features, complex if onehot encoded.
        # We'll just return raw array mapped to generic names if shapes mismatch.

        feature_names = getattr(self.preprocessor, "get_feature_names_out", lambda: None)()
        if feature_names is not None and len(feature_names) == len(importances):
             return dict(zip(feature_names, importances.tolist()))

        if len(self.feature_columns) == len(importances):
            return dict(zip(self.feature_columns, importances.tolist()))

        return {f"feature_{i}": imp for i, imp in enumerate(importances.tolist())}
