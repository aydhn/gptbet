import pytest
from src.sports_signal_bot.planetary_federation_hardening.budgets import (
    build_global_cadence_budgets, measure_global_cadence_budget_consumption,
    MeshFederationBudgetRecord, SuperchainBudgetRecord, SchedulerBusBudgetRecord, CadenceOrchestrationBudgetRecord
)

def test_measure_global_cadence_budget_consumption():
    budgets = build_global_cadence_budgets("b-01")
    budgets.mesh_federation_budgets.append(MeshFederationBudgetRecord("mfb-01", max_stale_members=2))
    budgets.superchain_budgets.append(SuperchainBudgetRecord("scb-01", max_stale_segments=1))
    budgets.scheduler_bus_budgets.append(SchedulerBusBudgetRecord("sbb-01", max_drift_ms=1000))
    budgets.cadence_budgets.append(CadenceOrchestrationBudgetRecord("cob-01", max_missing_acks=0))

    # Healthy state
    health_ok = measure_global_cadence_budget_consumption(budgets, {
        "stale_members": 1,
        "stale_segments": 1,
        "drift_ms": 500,
        "missing_acks": 0
    })
    assert health_ok.is_healthy
    assert len(health_ok.breaches) == 0

    # Breach state
    health_breach = measure_global_cadence_budget_consumption(budgets, {
        "stale_members": 3,
        "stale_segments": 0,
        "drift_ms": 1500,
        "missing_acks": 1
    })
    assert not health_breach.is_healthy
    assert len(health_breach.breaches) == 3
