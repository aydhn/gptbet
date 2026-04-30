import pytest
from sports_signal_bot.expansion_governance.budgets import (
    build_global_risk_budget, compute_budget_burn, reserve_budget_for_wave,
    release_budget_after_pause_or_rollback, summarize_budget_pressure, commit_wave_budget
)
from sports_signal_bot.expansion_governance.contracts import ExpansionWaveRecord

def test_budget_reservation_and_commit():
    budget = build_global_risk_budget("adoption_risk", 100.0, ["test"])

    wave = ExpansionWaveRecord(
        wave_id="w1", concurrency_level=2, budget_cost=40.0,
        activation_window={}, coordination_notes=""
    )

    success = reserve_budget_for_wave(budget, wave)
    assert success is True
    assert budget.reserved_budget == 40.0
    assert budget.remaining_budget == 60.0

    commit_wave_budget(budget, wave)
    assert budget.reserved_budget == 0.0
    assert budget.used_budget == 40.0
    assert budget.budget_status == "healthy"

def test_budget_exhaustion():
    budget = build_global_risk_budget("adoption_risk", 100.0, ["test"])

    wave1 = ExpansionWaveRecord(
        wave_id="w1", concurrency_level=2, budget_cost=90.0,
        activation_window={}, coordination_notes=""
    )

    success1 = reserve_budget_for_wave(budget, wave1)
    assert success1 is True
    assert budget.budget_status == "critical"

    wave2 = ExpansionWaveRecord(
        wave_id="w2", concurrency_level=2, budget_cost=15.0,
        activation_window={}, coordination_notes=""
    )

    success2 = reserve_budget_for_wave(budget, wave2)
    assert success2 is False  # Cannot reserve, insufficient remaining budget
