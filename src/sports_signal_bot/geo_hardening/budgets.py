from typing import Any, Dict


def build_geo_resilience_budgets() -> Dict[str, Any]:
    return {"lag_budget_seconds": 300, "asymmetry_budget_percentage": 1}


def measure_geo_budget_consumption(
    budget: Dict[str, Any], consumption: Dict[str, Any]
) -> Dict[str, Any]:
    breaches = []
    if consumption.get("lag_seconds", 0) > budget.get("lag_budget_seconds", 300):
        breaches.append("lag_budget_breached")
    return {"status": "breached" if breaches else "healthy", "breaches": breaches}


def summarize_geo_resilience_budgets(
    consumption_result: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "budget_status": consumption_result.get("status", "unknown"),
        "breach_count": len(consumption_result.get("breaches", [])),
    }
