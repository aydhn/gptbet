from typing import Any, Dict, List, Optional

import pandas as pd

from .contracts import (EvaluationComparisonRecord, EvaluationSummaryRecord,
                        PairwiseComparisonRecord)
from .pairwise import compute_pairwise_comparison


def generate_comparison_matrix(
    df: pd.DataFrame,
    source_col: str = "source_name",
    event_id_col: str = "event_id",
    true_label_col: str = "true_label",
    pred_class_col: str = "predicted_class",
    proba_cols: Optional[List[str]] = None,
    labels: Optional[List[str]] = None,
    base_source: Optional[str] = None,
) -> List[EvaluationComparisonRecord]:
    """Generates pairwise comparisons between a base source and all others, or all pairs if base is None."""

    sources = df[source_col].unique().tolist()
    if len(sources) < 2:
        return []

    comparisons = []

    if base_source is not None and base_source in sources:
        # Compare base vs all others
        for other_source in sources:
            if other_source == base_source:
                continue

            pairwise = compute_pairwise_comparison(
                df=df,
                source_a=base_source,
                source_b=other_source,
                source_col=source_col,
                event_id_col=event_id_col,
                true_label_col=true_label_col,
                pred_class_col=pred_class_col,
                proba_cols=proba_cols,
                labels=labels,
            )

            if pairwise:
                comparisons.append(
                    EvaluationComparisonRecord(
                        base_source=base_source,
                        compared_source=other_source,
                        pairwise_stats=pairwise,
                    )
                )
    else:
        # All pairs (NxN upper triangle)
        for i, src_a in enumerate(sources):
            for j, src_b in enumerate(sources[i + 1 :], i + 1):
                pairwise = compute_pairwise_comparison(
                    df=df,
                    source_a=src_a,
                    source_b=src_b,
                    source_col=source_col,
                    event_id_col=event_id_col,
                    true_label_col=true_label_col,
                    pred_class_col=pred_class_col,
                    proba_cols=proba_cols,
                    labels=labels,
                )

                if pairwise:
                    comparisons.append(
                        EvaluationComparisonRecord(
                            base_source=src_a,
                            compared_source=src_b,
                            pairwise_stats=pairwise,
                        )
                    )

    return comparisons
