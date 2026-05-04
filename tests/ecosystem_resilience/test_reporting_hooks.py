from sports_signal_bot.ecosystem_resilience.reporting import get_kpi_metrics

def test_reporting_hooks():
    kpis = get_kpi_metrics(0.85, 0.95)
    assert kpis["trust_overlay_stability_score"] == 0.85
    assert kpis["mesh_route_bounded_success_rate"] == 0.95
