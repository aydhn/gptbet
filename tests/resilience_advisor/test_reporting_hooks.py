from sports_signal_bot.resilience_advisor.reporting import generate_advisor_reporting_kpis

def test_kpis():
    kpis = generate_advisor_reporting_kpis()
    assert "advisory_recommendation_rate" in kpis
    assert kpis["no_safe_advice_rate"] == 0.05
