from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from sports_signal_bot.reporting.bundles import (ExecutiveSummaryBuilder,
                                                 ReportBundleBuilder)
from sports_signal_bot.reporting.contracts import (KPIBundleRecord,
                                                   KPIValueRecord)
from sports_signal_bot.reporting.periods import build_reporting_period
from sports_signal_bot.reporting.registry import MetricRegistry
from sports_signal_bot.reporting.universes import resolve_reporting_universe


class ReportingRunner:
    def __init__(self, config_dir: Path):
        self.registry = MetricRegistry(config_dir)

    def _fetch_mock_data(self) -> Dict[str, Any]:
        # In a real scenario, this would query evaluations, bankroll summaries, etc.
        return {"metrics": [], "warnings": [], "narrative": "System operational."}

    def _calculate_kpis(self, kpi_ids: List[str]) -> KPIBundleRecord:
        values = []
        for kid in kpi_ids:
            kdef = self.registry.get_kpi(kid)
            if kdef:
                # Mock calculation
                values.append(KPIValueRecord(kpi_id=kid, value=95.0, unit=kdef.unit))
        return KPIBundleRecord(kpis=values)

    def run(self, audience_id: str, period_id: str):
        audience_profile = self.registry.get_audience(audience_id)
        if not audience_profile:
            raise ValueError(f"Unknown audience: {audience_id}")

        start_time, end_time = build_reporting_period(period_id)

        builder = ReportBundleBuilder(period_id, audience_id, start_time, end_time)

        data_store = self._fetch_mock_data()

        # Build sections requested by audience
        builder.build_sections(audience_profile.sections, data_store)

        # Calculate focus KPIs
        kpi_bundle = self._calculate_kpis(audience_profile.focus_kpis)
        builder.add_kpis(kpi_bundle)

        # Setup mock universe
        builder.set_universe(resolve_reporting_universe({"period": period_id}))

        return builder.build()
