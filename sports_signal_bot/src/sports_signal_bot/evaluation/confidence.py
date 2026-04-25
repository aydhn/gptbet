import pandas as pd
import numpy as np
from typing import List, Optional
from .contracts import ConfidenceBucketRecord
from sklearn.metrics import accuracy_score, log_loss

def build_confidence_buckets(
    df: pd.DataFrame,
    true_label_col: str = "true_label",
    pred_class_col: str = "predicted_class",
    proba_cols: Optional[List[str]] = None,
    bins: int = 10,
    labels: Optional[List[str]] = None
) -> List[ConfidenceBucketRecord]:
    """Builds confidence buckets and computes metrics within each bucket."""

    if df.empty or proba_cols is None or len(proba_cols) == 0:
        return []

    y_true = df[true_label_col].values
    y_pred_class = df[pred_class_col].values
    y_pred_proba = df[proba_cols].values

    # Calculate max probability for each row as confidence
    if y_pred_proba.shape[1] > 1:
        confidences = np.max(y_pred_proba, axis=1)
    else:
        # Binary case with single probability
        p = y_pred_proba.flatten()
        confidences = np.maximum(p, 1.0 - p)

    df_eval = pd.DataFrame({
        "true_label": y_true,
        "pred_class": y_pred_class,
        "confidence": confidences
    })

    # Add full probability matrix columns for log_loss calculation
    for i, col in enumerate(proba_cols):
        df_eval[f"prob_{i}"] = y_pred_proba[:, i] if y_pred_proba.shape[1] > 1 else (y_pred_proba.flatten() if i == 0 else 1 - y_pred_proba.flatten())

    # Create bins
    bins_edges = np.linspace(1.0 / (len(proba_cols) if y_pred_proba.shape[1] > 1 else 2), 1.0, bins + 1)
    df_eval['bucket'] = pd.cut(df_eval['confidence'], bins=bins_edges, include_lowest=True)

    records = []

    for bucket_interval, group in df_eval.groupby('bucket', observed=False):
        if len(group) == 0:
            continue

        bucket_min = float(bucket_interval.left)
        bucket_max = float(bucket_interval.right)

        # Calculate Accuracy
        accuracy = float(accuracy_score(group['true_label'], group['pred_class']))

        # Calculate Log Loss
        try:
            prob_data = group[[f"prob_{i}" for i in range(len(proba_cols))]].values
            if labels is not None and len(labels) > 2:
                ll = float(log_loss(group['true_label'], prob_data, labels=labels))
            else:
                ll = float(log_loss(group['true_label'], prob_data))
        except Exception:
            ll = np.nan

        # Calculate empirical win rate (same as accuracy for top class)
        empirical_win_rate = accuracy

        # Calculate average predicted confidence
        avg_conf = float(group['confidence'].mean())

        records.append(ConfidenceBucketRecord(
            bucket_label=f"[{bucket_min:.2f}-{bucket_max:.2f})",
            bucket_min=bucket_min,
            bucket_max=bucket_max,
            count=len(group),
            accuracy=accuracy,
            avg_log_loss=ll,
            avg_predicted_confidence=avg_conf,
            empirical_win_rate=empirical_win_rate
        ))

    return records
