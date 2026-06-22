import pytest

from sports_signal_bot.geo_hardening.budgets import (
    build_geo_resilience_budgets, measure_geo_budget_consumption,
    summarize_geo_resilience_budgets)
from sports_signal_bot.geo_hardening.integration import (
    build_geo_operational_matrix, summarize_geo_operational_matrix,
    validate_geo_operational_row)


def test_operational_matrix():
    matrix = build_geo_operational_matrix()
    matrix = validate_geo_operational_row(
        matrix, {"owner": "test", "freshness_note": "ok"}
    )
    summary = summarize_geo_operational_matrix(matrix)
    assert summary["total_rows"] == 1
    assert summary["status"] == "ready"


def test_budgets():
    budget = build_geo_resilience_budgets()
    consumption = {"lag_seconds": 400}
    res = measure_geo_budget_consumption(budget, consumption)
    assert res["status"] == "breached"
    summary = summarize_geo_resilience_budgets(res)
    assert summary["breach_count"] == 1
