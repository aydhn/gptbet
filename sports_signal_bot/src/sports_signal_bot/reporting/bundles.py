from datetime import datetime
from typing import Any, Dict, List

from sports_signal_bot.reporting.contracts import (ExecutiveSummaryRecord,
                                                   KPIBundleRecord,
                                                   ReportBundleRecord,
                                                   ReportingUniverseRecord,
                                                   TechnicalSummaryRecord)
from sports_signal_bot.reporting.sections import registry as section_registry


class ReportBundleBuilder:
    def __init__(self, period_id: str, audience: str, start: datetime, end: datetime):
        self.period_id = period_id
        self.audience = audience
        self.start = start
        self.end = end
        self.sections = []
        self.kpis = []
        self.notable_events = []
        self.warnings = []
        self.universe = ReportingUniverseRecord(
            universe_id="default",
            description="Default universe",
            filters={},
            event_count=0,
        )

    def set_universe(self, universe: ReportingUniverseRecord):
        self.universe = universe

    def add_kpis(self, kpi_bundle: KPIBundleRecord):
        self.kpis = kpi_bundle.kpis

    def add_event(self, event: str):
        self.notable_events.append(event)

    def add_warning(self, warning: str):
        self.warnings.append(warning)

    def build_sections(self, section_ids: List[str], data_store: Dict[str, Any]):
        for sid in section_ids:
            sec = section_registry.build(sid, data_store, self.audience)
            self.sections.append(sec)

    def build(self) -> ReportBundleRecord:
        return ReportBundleRecord(
            reporting_period=self.period_id,
            time_range_start=self.start,
            time_range_end=self.end,
            included_sports_markets=["ALL"],
            included_runs_artifacts=[],
            sample_universe_summary=self.universe,
            audience_profile=self.audience,
            sections=self.sections,
            kpi_bundle=KPIBundleRecord(kpis=self.kpis),
            notable_events=self.notable_events,
            warnings_caveats=self.warnings,
        )


class ExecutiveSummaryBuilder:
    @staticmethod
    def from_bundle(bundle: ReportBundleRecord) -> ExecutiveSummaryRecord:
        overall = next(
            (
                s.narrative_summary
                for s in bundle.sections
                if s.section_name == "executive_overall_status"
            ),
            "No status available",
        )

        return ExecutiveSummaryRecord(
            overall_status=overall,
            top_kpis=bundle.kpi_bundle,
            key_wins=[],
            key_risks=[],
            operational_health="Good",
            release_governance_highlights="Stable",
            immediate_attention_items=bundle.warnings_caveats,
        )


class TechnicalSummaryBuilder:
    @staticmethod
    def from_bundle(bundle: ReportBundleRecord) -> TechnicalSummaryRecord:
        return TechnicalSummaryRecord(sections=bundle.sections)
