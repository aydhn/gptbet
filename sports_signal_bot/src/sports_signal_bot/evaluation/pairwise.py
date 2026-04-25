import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from .contracts import PairwiseComparisonRecord
from .alignment import get_common_universe
from .metrics import compute_all_metrics

def compute_pairwise_comparison(
    df: pd.DataFrame,
    source_a: str,
    source_b: str,
    source_col: str = "source_name",
    event_id_col: str = "event_id",
    true_label_col: str = "true_label",
    pred_class_col: str = "predicted_class",
    proba_cols: Optional[List[str]] = None,
    labels: Optional[List[str]] = None
) -> Optional[PairwiseComparisonRecord]:
    """Compares two sources on their exact common universe."""

    df_a = df[df[source_col] == source_a]
    df_b = df[df[source_col] == source_b]

    # Get common events directly between these two
    common_events = set(df_a[event_id_col].unique()).intersection(set(df_b[event_id_col].unique()))

    if len(common_events) == 0:
        return None

    df_a_common = df_a[df_a[event_id_col].isin(common_events)].sort_values(by=event_id_col)
    df_b_common = df_b[df_b[event_id_col].isin(common_events)].sort_values(by=event_id_col)

    metrics_a, _ = compute_all_metrics(
        df=df_a_common, source_name=source_a, true_label_col=true_label_col,
        pred_class_col=pred_class_col, proba_cols=proba_cols, labels=labels
    )

    metrics_b, _ = compute_all_metrics(
        df=df_b_common, source_name=source_b, true_label_col=true_label_col,
        pred_class_col=pred_class_col, proba_cols=proba_cols, labels=labels
    )

    # Calculate wins/losses at event level (using log loss if available, otherwise accuracy)
    # This is a simplified event-level comparison. For a true pairwise log-loss comparison,
    # we would compute loss per event.

    # Delta metrics (A - B)
    # Note: For log_loss and brier, lower is better. So negative delta means A is better.
    # For accuracy, higher is better. So positive delta means A is better.

    delta_log_loss = metrics_a.get("log_loss", np.nan) - metrics_b.get("log_loss", np.nan)
    delta_brier = metrics_a.get("brier", np.nan) - metrics_b.get("brier", np.nan)
    delta_accuracy = metrics_a.get("accuracy", np.nan) - metrics_b.get("accuracy", np.nan)

    # Determine who is better overall (using log_loss as primary if available, then accuracy)
    better_source = "tie"
    if not np.isnan(delta_log_loss):
        if delta_log_loss < 0:
            better_source = source_a
        elif delta_log_loss > 0:
            better_source = source_b
    elif not np.isnan(delta_accuracy):
        if delta_accuracy > 0:
            better_source = source_a
        elif delta_accuracy < 0:
            better_source = source_b

    return PairwiseComparisonRecord(
        source_a=source_a,
        source_b=source_b,
        common_event_count=len(common_events),
        delta_log_loss=delta_log_loss if not pd.isna(delta_log_loss) else 0.0,
        delta_brier=delta_brier if not pd.isna(delta_brier) else 0.0,
        delta_accuracy=delta_accuracy if not pd.isna(delta_accuracy) else 0.0,
        source_a_wins=0, # placeholder, requires row-by-row loss calculation
        source_b_wins=0, # placeholder
        ties=0,          # placeholder
        better_on_common_universe=better_source
    )
