from typing import Dict, List

from sports_signal_bot.reporting.contracts import MetricComparisonRecord


def select_top_highlights(
    comparisons: List[MetricComparisonRecord], rules: Dict
) -> List[MetricComparisonRecord]:
    # prioritize degraded, then improved, etc.
    priority = rules.get(
        "priority", {"degraded": 1, "improved": 2, "volatile": 3, "stable": 4}
    )

    sorted_comps = sorted(
        comparisons,
        key=lambda c: (priority.get(c.classification, 99), -abs(c.delta_pct)),
    )
    max_h = rules.get("max_highlights", 5)
    return sorted_comps[:max_h]


def select_top_risks(
    comparisons: List[MetricComparisonRecord],
) -> List[MetricComparisonRecord]:
    risks = [c for c in comparisons if c.classification == "degraded"]
    return sorted(risks, key=lambda c: -abs(c.delta_pct))


def deduplicate_report_highlights(highlights: List[str]) -> List[str]:
    seen = set()
    result = []
    for h in highlights:
        if h not in seen:
            seen.add(h)
            result.append(h)
    return result
