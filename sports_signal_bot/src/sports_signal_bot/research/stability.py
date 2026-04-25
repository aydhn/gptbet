from typing import Any, Dict, List

from sports_signal_bot.research.contracts import PeriodPerformanceRecord


def summarize_period_deltas(
    prev_metrics: Dict[str, float], curr_metrics: Dict[str, float]
) -> Dict[str, float]:
    """Calculates difference in metrics between two periods."""
    deltas = {}
    for k, curr_v in curr_metrics.items():
        if k in prev_metrics:
            deltas[k] = curr_v - prev_metrics[k]
    return deltas


def detect_performance_drop(
    deltas: Dict[str, float], metric: str = "log_loss", threshold: float = 0.05
) -> bool:
    """
    Detects if performance dropped significantly.
    For log_loss, a drop means it INCREASED by > threshold.
    For accuracy, a drop means it DECREASED by > threshold.
    """
    if metric not in deltas:
        return False

    delta = deltas[metric]
    if metric in ["log_loss", "brier_score"]:
        return delta > threshold  # Error went up
    else:
        return delta < -threshold  # Accuracy went down


def summarize_source_stability(
    performances: List[PeriodPerformanceRecord],
) -> Dict[str, Any]:
    """Summarizes stability of sources across periods."""
    if not performances:
        return {}

    sources = set()
    for p in performances:
        sources.update(p.metrics_by_source.keys())

    stability = {}
    for s in sources:
        log_losses = []
        for p in performances:
            if s in p.metrics_by_source and "log_loss" in p.metrics_by_source[s]:
                log_losses.append(p.metrics_by_source[s]["log_loss"])

        if len(log_losses) > 1:
            variance = sum(
                (x - (sum(log_losses) / len(log_losses))) ** 2 for x in log_losses
            ) / len(log_losses)
            stability[s] = {"variance": variance, "periods_present": len(log_losses)}

    return stability


def flag_time_slice_instability(
    performances: List[PeriodPerformanceRecord],
) -> List[str]:
    """Flags significant instabilities in the timeslice series."""
    warnings = []
    if len(performances) < 2:
        return warnings

    for i in range(1, len(performances)):
        prev = performances[i - 1]
        curr = performances[i]

        # Check ensemble stability
        if (
            "ensemble" in curr.metrics_by_source
            and "ensemble" in prev.metrics_by_source
        ):
            deltas = summarize_period_deltas(
                prev.metrics_by_source["ensemble"], curr.metrics_by_source["ensemble"]
            )
            if detect_performance_drop(deltas, "log_loss", 0.1):
                warnings.append(
                    f"Period {curr.period_id}: Ensemble log loss degraded by {deltas['log_loss']:.3f} from previous period."
                )

    return warnings
