from sports_signal_bot.context_assembly.reporting import get_context_assembly_kpis, generate_context_assembly_health_report

def test_kpis():
    kpis = get_context_assembly_kpis()
    assert kpis["trace_router_federation_currentness_rate"] > 0
    assert kpis["no_safe_visibility_across_contexts_rate"] == 1.0

def test_health_report():
    report = generate_context_assembly_health_report()
    assert report["health"] == "nominal"
    assert "context_bundle_counts" in report["summary"]
