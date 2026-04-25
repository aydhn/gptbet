import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from sklearn.metrics import log_loss, brier_score_loss, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from pydantic import BaseModel

from .contracts import ClassLevelMetricRecord

def compute_probabilistic_metrics(
    y_true: np.ndarray,
    y_pred_proba: np.ndarray,
    labels: Optional[List[str]] = None
) -> Dict[str, float]:
    """Computes generic probabilistic metrics for binary or multiclass outputs."""
    metrics = {}

    # Log Loss (Negative Log Likelihood)
    try:
        if labels is not None and len(labels) > 2:
            metrics["log_loss"] = log_loss(y_true, y_pred_proba, labels=labels)
        else:
            # Binary log loss
            metrics["log_loss"] = log_loss(y_true, y_pred_proba)
    except Exception:
        metrics["log_loss"] = np.nan

    # Brier Score
    # Note: sklearn's brier_score_loss only supports binary classification directly.
    # For multiclass, we compute the multi-class Brier score (mean squared error of probabilities)
    try:
        if y_pred_proba.ndim == 1 or y_pred_proba.shape[1] == 1:
            metrics["brier"] = brier_score_loss(y_true, y_pred_proba)
        else:
            # Multiclass Brier score
            # Create one-hot encoding for true labels
            y_true_onehot = np.zeros_like(y_pred_proba)
            for i, label in enumerate(y_true):
                if labels is not None and label in labels:
                    idx = labels.index(label)
                    y_true_onehot[i, idx] = 1.0

            # Brier score is sum of squared differences across classes, averaged over instances
            # Brier score = 1/N * sum(sum((y_pred - y_true_onehot)^2))
            squared_diff = (y_pred_proba - y_true_onehot) ** 2
            metrics["brier"] = float(np.mean(np.sum(squared_diff, axis=1)))
    except Exception:
        metrics["brier"] = np.nan

    # Average Confidence (mean of max predicted probability)
    try:
        if y_pred_proba.ndim > 1 and y_pred_proba.shape[1] > 1:
            max_probs = np.max(y_pred_proba, axis=1)
            metrics["average_confidence"] = float(np.mean(max_probs))
        else:
            # binary probabilities
            max_probs = np.maximum(y_pred_proba, 1.0 - y_pred_proba)
            metrics["average_confidence"] = float(np.mean(max_probs))
    except Exception:
        metrics["average_confidence"] = np.nan

    # Average Entropy
    try:
        epsilon = 1e-15
        if y_pred_proba.ndim > 1 and y_pred_proba.shape[1] > 1:
            clipped_probs = np.clip(y_pred_proba, epsilon, 1 - epsilon)
            entropy = -np.sum(clipped_probs * np.log(clipped_probs), axis=1)
            metrics["average_entropy"] = float(np.mean(entropy))
        else:
            # binary
            p = np.clip(y_pred_proba, epsilon, 1 - epsilon)
            entropy = - (p * np.log(p) + (1 - p) * np.log(1 - p))
            metrics["average_entropy"] = float(np.mean(entropy))
    except Exception:
        metrics["average_entropy"] = np.nan

    return metrics

def compute_classification_metrics(
    y_true: np.ndarray,
    y_pred_class: np.ndarray,
    y_pred_proba: Optional[np.ndarray] = None,
    labels: Optional[List[str]] = None,
    is_multiclass: bool = False
) -> Tuple[Dict[str, float], List[ClassLevelMetricRecord]]:
    """Computes binary or multiclass classification metrics."""
    metrics = {}
    class_metrics = []

    try:
        metrics["accuracy"] = float(accuracy_score(y_true, y_pred_class))
    except Exception:
        metrics["accuracy"] = np.nan

    if is_multiclass:
        try:
            metrics["macro_f1"] = float(f1_score(y_true, y_pred_class, average="macro", labels=labels, zero_division=0))
            metrics["weighted_f1"] = float(f1_score(y_true, y_pred_class, average="weighted", labels=labels, zero_division=0))
        except Exception:
            metrics["macro_f1"] = np.nan
            metrics["weighted_f1"] = np.nan

        # Class level metrics
        if labels is not None:
            try:
                precisions = precision_score(y_true, y_pred_class, average=None, labels=labels, zero_division=0)
                recalls = recall_score(y_true, y_pred_class, average=None, labels=labels, zero_division=0)
                f1s = f1_score(y_true, y_pred_class, average=None, labels=labels, zero_division=0)

                # Calculate support manually or from classification_report
                for i, label in enumerate(labels):
                    support = int(np.sum(y_true == label))
                    class_metrics.append(ClassLevelMetricRecord(
                        class_name=str(label),
                        precision=float(precisions[i]),
                        recall=float(recalls[i]),
                        f1_score=float(f1s[i]),
                        support=support
                    ))
            except Exception:
                pass

    else: # Binary
        # Assume positive class is True or 1 or labels[1]
        pos_label = 1
        if labels is not None and len(labels) > 1:
            pos_label = labels[1]

        try:
            metrics["precision"] = float(precision_score(y_true, y_pred_class, pos_label=pos_label, zero_division=0))
            metrics["recall"] = float(recall_score(y_true, y_pred_class, pos_label=pos_label, zero_division=0))
            metrics["f1"] = float(f1_score(y_true, y_pred_class, pos_label=pos_label, zero_division=0))
            metrics["macro_f1"] = metrics["f1"] # for fallback
        except Exception:
            metrics["precision"] = np.nan
            metrics["recall"] = np.nan
            metrics["f1"] = np.nan
            metrics["macro_f1"] = np.nan

        if y_pred_proba is not None:
            try:
                # Assuming y_pred_proba is the probability of the positive class
                if y_pred_proba.ndim == 1:
                    metrics["roc_auc"] = float(roc_auc_score(y_true, y_pred_proba))
                elif y_pred_proba.ndim == 2 and y_pred_proba.shape[1] == 2:
                    metrics["roc_auc"] = float(roc_auc_score(y_true, y_pred_proba[:, 1]))
            except Exception:
                metrics["roc_auc"] = np.nan

    return metrics, class_metrics

def compute_all_metrics(
    df: pd.DataFrame,
    source_name: str,
    true_label_col: str = "true_label",
    pred_class_col: str = "predicted_class",
    proba_cols: Optional[List[str]] = None,
    labels: Optional[List[str]] = None
) -> Tuple[Dict[str, float], List[ClassLevelMetricRecord]]:
    """Helper to compute all metrics for a given source dataframe."""

    if df.empty:
        return {}, []

    y_true = df[true_label_col].values
    y_pred_class = df[pred_class_col].values

    is_multiclass = labels is not None and len(labels) > 2

    metrics = {}

    y_pred_proba = None
    if proba_cols is not None and len(proba_cols) > 0:
        y_pred_proba = df[proba_cols].values

        # If binary and we only passed one proba column, make it 1D
        if not is_multiclass and y_pred_proba.shape[1] == 1:
            y_pred_proba = y_pred_proba.flatten()

        prob_metrics = compute_probabilistic_metrics(y_true, y_pred_proba, labels)
        metrics.update(prob_metrics)

    clf_metrics, class_metrics = compute_classification_metrics(
        y_true, y_pred_class, y_pred_proba, labels, is_multiclass
    )
    metrics.update(clf_metrics)

    return metrics, class_metrics
