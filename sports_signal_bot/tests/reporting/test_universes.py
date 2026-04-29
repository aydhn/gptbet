import pytest
from sports_signal_bot.reporting.universes import resolve_reporting_universe, validate_reporting_universe, detect_mixed_universe_metrics, mark_noncomparable_sections, summarize_coverage_caveats
from sports_signal_bot.reporting.contracts import MetricValueRecord, MetricLineageRecord
from datetime import datetime

def test_resolve_reporting_universe():
    filters = {"sport": "football", "period": "daily"}
    events = [{"id": 1}, {"id": 2}]
    universe = resolve_reporting_universe(filters, events)
    assert universe.event_count == 2
    assert "football" in universe.filters.values()

def test_validate_reporting_universe():
    valid = resolve_reporting_universe({}, [{"id": 1}])
    invalid = resolve_reporting_universe({}, [])
    assert validate_reporting_universe(valid) is True
    assert validate_reporting_universe(invalid) is False

def test_detect_mixed_universe_metrics():
    m1 = MetricValueRecord(metric_name="m1", value=1.0, unit="pct")
    lineage = MetricLineageRecord(
        source_manifests=[],
        input_summaries=[],
        aggregation_method="avg",
        time_range_start=datetime.now(),
        time_range_end=datetime.now(),
        included_filters={},
        normalization_notes="",
        is_mixed_sample=True,
        freshness_timestamp=datetime.now()
    )
    m2 = MetricValueRecord(metric_name="m2", value=2.0, unit="pct", lineage=lineage)
    mixed = detect_mixed_universe_metrics([m1, m2])
    assert len(mixed) == 1
    assert mixed[0].metric_name == "m2"
