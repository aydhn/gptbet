import pytest
from pathlib import Path
from sports_signal_bot.reporting.registry import MetricRegistry

def test_registry_loading(tmp_path):
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
  executive:
    name: Executive
    description: High-level
    sections: ["executive_overall_status"]
    detail_level: low
    include_diagnostics: false
    focus_kpis: ["slot_health_score"]
    tone: concise
"""
    (tmp_path / "kpis.yaml").write_text(kpi_yaml)
    (tmp_path / "audiences.yaml").write_text(aud_yaml)

    registry = MetricRegistry(tmp_path)

    assert registry.get_kpi("slot_health_score") is not None
    assert registry.get_kpi("slot_health_score").name == "Slot Health Score"
    assert "operational_health_metrics" in registry.enabled_families

    assert registry.get_audience("executive") is not None
    assert registry.get_audience("executive").detail_level == "low"
