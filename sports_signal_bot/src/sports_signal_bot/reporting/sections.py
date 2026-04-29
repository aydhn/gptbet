from typing import Any, Dict, List

from sports_signal_bot.reporting.contracts import (MetricValueRecord,
                                                   ReportSectionRecord)
from sports_signal_bot.reporting.narratives import format_audience_summary


class SectionBuilderRegistry:
    def __init__(self):
        self._builders = {}

    def register(self, section_id: str, builder_func):
        self._builders[section_id] = builder_func

    def build(
        self, section_id: str, data: Dict[str, Any], audience: str
    ) -> ReportSectionRecord:
        if section_id in self._builders:
            return self._builders[section_id](data, audience)

        # Default builder fallback
        return ReportSectionRecord(
            section_name=section_id,
            audience=audience,
            narrative_summary="No data available.",
        )


# Sample builder implementations
def build_ops_health_section(
    data: Dict[str, Any], audience: str
) -> ReportSectionRecord:
    metrics = data.get("metrics", [])
    primary = [
        m
        for m in metrics
        if m.metric_name in ["Slot Health Score", "Dispatch Delivery Success Rate"]
    ]

    return ReportSectionRecord(
        section_name="ops_health_summary",
        audience=audience,
        primary_metrics=primary,
        narrative_summary=f"Ops Health: tracking {len(primary)} primary metrics.",
        warnings=data.get("warnings", []),
    )


def build_executive_overall_status(
    data: Dict[str, Any], audience: str
) -> ReportSectionRecord:
    metrics = data.get("metrics", [])
    narrative = data.get("narrative", "System is operating normally.")
    return ReportSectionRecord(
        section_name="executive_overall_status",
        audience=audience,
        primary_metrics=metrics[:3],
        narrative_summary=narrative,
    )


# Instantiate a global registry for convenience
registry = SectionBuilderRegistry()
registry.register("ops_health_summary", build_ops_health_section)
registry.register("executive_overall_status", build_executive_overall_status)
