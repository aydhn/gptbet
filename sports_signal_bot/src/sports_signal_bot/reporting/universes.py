from typing import Any, Dict, List, Tuple

from sports_signal_bot.reporting.contracts import (MetricValueRecord,
                                                   ReportingUniverseRecord)


def resolve_reporting_universe(
    filters: Dict[str, Any], events: List[Any] = None
) -> ReportingUniverseRecord:
    count = len(events) if events else 0
    return ReportingUniverseRecord(
        universe_id=f"univ_{hash(frozenset(filters.items()))}",
        description="Resolved reporting universe based on active filters.",
        filters=filters,
        event_count=count,
    )


def validate_reporting_universe(universe: ReportingUniverseRecord) -> bool:
    if universe.event_count == 0:
        return False
    return True


def detect_mixed_universe_metrics(
    metrics: List[MetricValueRecord],
) -> List[MetricValueRecord]:
    return [m for m in metrics if m.lineage and m.lineage.is_mixed_sample]


def mark_noncomparable_sections(sections: list, mixed_metrics: List[str]) -> list:
    for sec in sections:
        for m in sec.primary_metrics + sec.supporting_metrics:
            if m.metric_name in mixed_metrics:
                sec.warnings.append(
                    f"Metric {m.metric_name} is based on a mixed sample universe and should not be compared directly."
                )
    return sections


def summarize_coverage_caveats(universe: ReportingUniverseRecord) -> str:
    return f"Coverage warning: Universe {universe.universe_id} only covers {universe.event_count} events."
