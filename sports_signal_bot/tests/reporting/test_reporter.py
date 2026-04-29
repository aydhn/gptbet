import pytest
from pathlib import Path
from sports_signal_bot.reporting.reporting import ReportingReporter
from sports_signal_bot.reporting.contracts import ReportBundleRecord, KPIBundleRecord, ReportingUniverseRecord, KPIValueRecord
from datetime import datetime

def test_reporting_reporter(tmp_path):
    bundle = ReportBundleRecord(
        reporting_period="daily",
        time_range_start=datetime.now(),
        time_range_end=datetime.now(),
        included_sports_markets=["ALL"],
        included_runs_artifacts=[],
        sample_universe_summary=ReportingUniverseRecord(
            universe_id="test", description="test", filters={}, event_count=0
        ),
        audience_profile="operator",
        sections=[],
        kpi_bundle=KPIBundleRecord(kpis=[
            KPIValueRecord(kpi_id="slot_health_score", value=95.0, unit="pct")
        ]),
        notable_events=[],
        warnings_caveats=[]
    )

    reporter = ReportingReporter(tmp_path)
    j_path = reporter.write_json_bundle(bundle)
    m_path = reporter.write_markdown_summary(bundle)
    c_path = reporter.write_csv_extracts(bundle)

    assert j_path.exists()
    assert m_path.exists()
    assert c_path.exists()

    content = c_path.read_text()
    assert "slot_health_score" in content
