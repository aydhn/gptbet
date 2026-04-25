import pandas as pd
from typing import Dict, List, Optional
from .metrics import compute_all_metrics
from .contracts import SegmentEvaluationRecord

def evaluate_by_segment(
    df: pd.DataFrame,
    segment_col: str,
    source_name: str,
    true_label_col: str = "true_label",
    pred_class_col: str = "predicted_class",
    proba_cols: Optional[List[str]] = None,
    labels: Optional[List[str]] = None,
    min_rows: int = 10
) -> List[SegmentEvaluationRecord]:
    """Evaluates a source grouped by a specific segment column."""

    if segment_col not in df.columns:
        return []

    records = []

    # Compute baseline metrics for lift calculation
    baseline_metrics, _ = compute_all_metrics(
        df=df,
        source_name=source_name,
        true_label_col=true_label_col,
        pred_class_col=pred_class_col,
        proba_cols=proba_cols,
        labels=labels
    )

    for segment_val, group in df.groupby(segment_col):
        if len(group) < min_rows:
            continue

        metrics, _ = compute_all_metrics(
            df=group,
            source_name=source_name,
            true_label_col=true_label_col,
            pred_class_col=pred_class_col,
            proba_cols=proba_cols,
            labels=labels
        )

        # Calculate lift vs baseline (diff)
        lift = {}
        for k, v in metrics.items():
            if pd.isna(v) or k not in baseline_metrics or pd.isna(baseline_metrics[k]):
                continue
            lift[k] = v - baseline_metrics[k]

        records.append(SegmentEvaluationRecord(
            segment_type=segment_col,
            segment_value=str(segment_val),
            row_count=len(group),
            metrics=metrics,
            lift_vs_baseline=lift if lift else None
        ))

    return records
