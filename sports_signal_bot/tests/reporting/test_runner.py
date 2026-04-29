import pytest
from pathlib import Path
from sports_signal_bot.reporting.runner import ReportingRunner
from sports_signal_bot.reporting.contracts import ReportBundleRecord

def test_reporting_runner(tmp_path):
    kpi_yaml = """
enabled_metric_families:
  - operational_health_metrics
kpi_definitions:
  - id: slot_health_score
    name: "Slot Health Score"
    family: operational_health_metrics
    description: "test"
    unit: percentage
    directionality: higher_is_better
    aggregation_method: average
    source_components: []
"""
    aud_yaml = """
profiles:
  operator:
    name: Operator
    description: High-level
    sections: ["ops_health_summary"]
    detail_level: medium
    include_diagnostics: false
    focus_kpis: ["slot_health_score"]
    tone: operational
"""
    # Use the tmp_path as the config_dir
    (tmp_path / "kpis.yaml").write_text(kpi_yaml)
    (tmp_path / "audiences.yaml").write_text(aud_yaml)

    runner = ReportingRunner(tmp_path)
    bundle = runner.run("operator", "daily")

    assert isinstance(bundle, ReportBundleRecord)
    assert bundle.reporting_period == "daily"
    assert bundle.audience_profile == "operator"
    assert len(bundle.sections) == 1
    assert bundle.sections[0].section_name == "ops_health_summary"
    assert len(bundle.kpi_bundle.kpis) == 1
    assert bundle.kpi_bundle.kpis[0].kpi_id == "slot_health_score"
