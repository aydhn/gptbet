from typing import Dict, Any

from sports_signal_bot.geo_hardening.budgets import (
    build_geo_resilience_budgets,
    measure_geo_budget_consumption,
    summarize_geo_resilience_budgets
)

def test_build_geo_resilience_budgets():
    budgets = build_geo_resilience_budgets()
    assert budgets == {
        "lag_budget_seconds": 300,
        "asymmetry_budget_percentage": 1
    }

def test_measure_geo_budget_consumption_healthy():
    budget = build_geo_resilience_budgets()
    consumption = {"lag_seconds": 200}
    result = measure_geo_budget_consumption(budget, consumption)
    assert result == {
        "status": "healthy",
        "breaches": []
    }

def test_measure_geo_budget_consumption_breached():
    budget = build_geo_resilience_budgets()
    consumption = {"lag_seconds": 350}
    result = measure_geo_budget_consumption(budget, consumption)
    assert result == {
        "status": "breached",
        "breaches": ["lag_budget_breached"]
    }

def test_measure_geo_budget_consumption_missing_keys():
    budget = {} # defaults to 300
    consumption = {} # defaults to 0
    result = measure_geo_budget_consumption(budget, consumption)
    assert result == {
        "status": "healthy",
        "breaches": []
    }

    consumption_breach = {"lag_seconds": 301}
    result_breach = measure_geo_budget_consumption(budget, consumption_breach)
    assert result_breach == {
        "status": "breached",
        "breaches": ["lag_budget_breached"]
    }

def test_summarize_geo_resilience_budgets_healthy():
    consumption_result = {
        "status": "healthy",
        "breaches": []
    }
    summary = summarize_geo_resilience_budgets(consumption_result)
    assert summary == {
        "budget_status": "healthy",
        "breach_count": 0
    }

def test_summarize_geo_resilience_budgets_breached():
    consumption_result = {
        "status": "breached",
        "breaches": ["lag_budget_breached"]
    }
    summary = summarize_geo_resilience_budgets(consumption_result)
    assert summary == {
        "budget_status": "breached",
        "breach_count": 1
    }

def test_summarize_geo_resilience_budgets_missing_keys():
    consumption_result = {}
    summary = summarize_geo_resilience_budgets(consumption_result)
    assert summary == {
        "budget_status": "unknown",
        "breach_count": 0
    }
