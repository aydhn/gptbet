import numpy as np
import pandas as pd
from typing import List, Dict

def ensure_class_order(probabilities: Dict[str, float], class_labels: List[str]) -> np.ndarray:
    """
    Converts a probability dictionary into a numpy array matching the specific class order.
    """
    return np.array([probabilities.get(label, 0.0) for label in class_labels], dtype=np.float64)

def validate_probability_vectors(X: np.ndarray, n_classes: int) -> bool:
    """
    Validates that a probability matrix X has valid values (0 to 1) and sums to 1.
    """
    if X.shape[1] != n_classes:
        return False

    if np.any(X < 0.0) or np.any(X > 1.0):
        return False

    sums = np.sum(X, axis=1)
    if not np.allclose(sums, 1.0, atol=1e-5):
        return False

    return True

def flatten_binary_probabilities(X: np.ndarray, positive_class_index: int = 1) -> np.ndarray:
    """
    Extracts the positive class probability from a binary probability matrix.
    """
    if X.shape[1] != 2:
        raise ValueError("flatten_binary_probabilities expects a matrix with 2 columns")
    return X[:, positive_class_index]

def expand_multiclass_probabilities(p: np.ndarray, positive_class_index: int = 1) -> np.ndarray:
    """
    Expands a 1D array of positive class probabilities into a 2D binary probability matrix.
    """
    n_samples = len(p)
    X = np.zeros((n_samples, 2), dtype=np.float64)
    X[:, positive_class_index] = p
    X[:, 1 - positive_class_index] = 1.0 - p
    return X

def clip_probabilities(X: np.ndarray, eps: float = 1e-15) -> np.ndarray:
    """
    Clips probabilities to be within [eps, 1 - eps] to prevent log(0) errors.
    If X is 2D, renormalizes after clipping.
    """
    clipped = np.clip(X, eps, 1 - eps)
    if len(clipped.shape) == 2:
        clipped = clipped / clipped.sum(axis=1, keepdims=True)
    return clipped
