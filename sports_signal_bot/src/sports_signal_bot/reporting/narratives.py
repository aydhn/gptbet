from typing import Any, Dict

from sports_signal_bot.reporting.contracts import MetricComparisonRecord


def build_metric_narrative(
    comparison: MetricComparisonRecord, templates: Dict[str, str]
) -> str:
    template = templates.get(comparison.classification, templates.get("stable", ""))
    if not template:
        return f"{comparison.metric_name}: {comparison.classification}"

    return template.format(
        metric_name=comparison.metric_name,
        delta_abs=round(abs(comparison.delta_abs), 2),
        delta_pct=round(abs(comparison.delta_pct), 2),
        curr_val=round(comparison.current_value, 2),
        prev_val=round(comparison.previous_value, 2),
        unit="",  # Could fetch from metric definition
    )


def format_audience_summary(narratives: list[str], audience_tone: str) -> str:
    if audience_tone == "concise":
        return " | ".join(narratives)
    elif audience_tone == "technical":
        return "\n".join([f"- {n}" for n in narratives])
    else:
        return " ".join(narratives)
