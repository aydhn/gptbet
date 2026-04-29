from sports_signal_bot.reporting.contracts import MetricComparisonRecord


def classify_improvement_or_regression(
    delta_pct: float, directionality: str, significance_threshold: float = 5.0
) -> str:
    if abs(delta_pct) < significance_threshold:
        return "stable"

    if directionality == "higher_is_better":
        return "improved" if delta_pct > 0 else "degraded"
    elif directionality == "lower_is_better":
        return "improved" if delta_pct < 0 else "degraded"
    else:
        return "volatile"


def compare_metric_periods(
    metric_name: str, current_value: float, previous_value: float, directionality: str
) -> MetricComparisonRecord:
    delta_abs = current_value - previous_value
    delta_pct = (delta_abs / abs(previous_value)) * 100 if previous_value != 0 else 0.0

    classification = classify_improvement_or_regression(delta_pct, directionality)

    return MetricComparisonRecord(
        metric_name=metric_name,
        current_value=current_value,
        previous_value=previous_value,
        delta_abs=delta_abs,
        delta_pct=delta_pct,
        classification=classification,
    )


def detect_significant_metric_shift(
    comparison: MetricComparisonRecord, threshold: float = 10.0
) -> bool:
    return abs(comparison.delta_pct) >= threshold


def build_trend_summary(comparisons: list[MetricComparisonRecord]) -> str:
    improved = sum(1 for c in comparisons if c.classification == "improved")
    degraded = sum(1 for c in comparisons if c.classification == "degraded")
    stable = sum(1 for c in comparisons if c.classification == "stable")

    return f"Trends: {improved} improved, {degraded} degraded, {stable} stable."
