from sports_signal_bot.geo_hardening.budgets import (
    build_geo_resilience_budgets,
    measure_geo_budget_consumption,
    summarize_geo_resilience_budgets,
)

def test_build_geo_resilience_budgets():
    budgets = build_geo_resilience_budgets()
    assert budgets["lag_budget_seconds"] == 300
    assert budgets["asymmetry_budget_percentage"] == 1

def test_measure_geo_budget_consumption_healthy():
    budget = build_geo_resilience_budgets()
    consumption = {"lag_seconds": 150}
    result = measure_geo_budget_consumption(budget, consumption)
    assert result["status"] == "healthy"
    assert "lag_budget_breached" not in result["breaches"]

def test_measure_geo_budget_consumption_breached():
    budget = build_geo_resilience_budgets()
    consumption = {"lag_seconds": 400}
    result = measure_geo_budget_consumption(budget, consumption)
    assert result["status"] == "breached"
    assert "lag_budget_breached" in result["breaches"]

def test_summarize_geo_resilience_budgets():
    result_healthy = summarize_geo_resilience_budgets({"status": "healthy", "breaches": []})
    assert result_healthy["budget_status"] == "healthy"
    assert result_healthy["breach_count"] == 0

    result_breached = summarize_geo_resilience_budgets({"status": "breached", "breaches": ["lag_budget_breached"]})
    assert result_breached["budget_status"] == "breached"
    assert result_breached["breach_count"] == 1
