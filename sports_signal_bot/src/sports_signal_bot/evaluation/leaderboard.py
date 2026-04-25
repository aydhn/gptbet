from typing import Any, Dict, List, Optional

import pandas as pd

from .contracts import EvaluationSummaryRecord, LeaderboardRow


def build_leaderboard(
    summaries: List[EvaluationSummaryRecord],
    primary_metric: str = "log_loss",
    secondary_metric: str = "brier",
    tertiary_metric: str = "accuracy",
    min_rows: int = 1,
) -> List[LeaderboardRow]:
    """Constructs a sorted leaderboard from evaluation summaries."""

    # Filter by minimum rows
    valid_summaries = [s for s in summaries if s.row_count >= min_rows]

    # Define sorting directions (lower is better for loss metrics, higher is better for accuracy/f1)
    lower_is_better = {
        "log_loss": True,
        "brier": True,
        "accuracy": False,
        "macro_f1": False,
        "average_entropy": True,
    }

    def get_sort_key(summary: EvaluationSummaryRecord):
        # Extract metrics, handle None values by assigning worst possible value

        # Helper to get value and apply direction
        def get_val(metric_name):
            val = getattr(summary, metric_name, None)
            if val is None or pd.isna(val):
                return (
                    float("inf")
                    if lower_is_better.get(metric_name, False)
                    else float("-inf")
                )

            # Negate if higher is better so we can sort ascending globally
            if not lower_is_better.get(metric_name, False):
                return -val
            return val

        m1 = get_val(primary_metric)
        m2 = get_val(secondary_metric)
        m3 = get_val(tertiary_metric)

        return (m1, m2, m3)

    # Sort summaries
    sorted_summaries = sorted(valid_summaries, key=get_sort_key)

    # Build Leaderboard Rows
    leaderboard = []
    for rank, summary in enumerate(sorted_summaries, 1):
        warnings = []
        if summary.coverage_rate < 1.0:
            warnings.append(f"Incomplete coverage: {summary.coverage_rate:.1%}")

        leaderboard.append(
            LeaderboardRow(
                rank=rank,
                source_name=summary.source_name,
                source_family=summary.source_family,
                sport=summary.sport,
                market_type=summary.market_type,
                row_count=summary.row_count,
                coverage_rate=summary.coverage_rate,
                log_loss=summary.log_loss,
                brier=summary.brier,
                accuracy=summary.accuracy,
                macro_f1=summary.macro_f1,
                ece=None,  # Calibration specific, not in core evaluation yet
                warnings=warnings,
            )
        )

    return leaderboard
