import pytest
from sports_signal_bot.expansion_governance.pressure import compute_global_pressure
from sports_signal_bot.expansion_governance.contracts import PressureBand, GlobalPressureMetrics

def test_compute_global_pressure_critical():
    pressure = compute_global_pressure(
        metrics=GlobalPressureMetrics(
            active_cohort_count=10,
            simultaneously_growing_cohort_count=5,
            family_conflict_burden=1.0,
            verification_warning_density=0.8,
            review_backlog_pressure=0.9,
            dispute_burden=0.5,
            rollback_recentness_penalty=1.0,
            budget_saturation=0.95
        )
    )

    assert pressure.pressure_band == PressureBand.CRITICAL
    assert pressure.pressure_score > 0.85

def test_compute_global_pressure_low():
    pressure = compute_global_pressure(
        metrics=GlobalPressureMetrics(
            active_cohort_count=2,
            simultaneously_growing_cohort_count=0,
            family_conflict_burden=0.0,
            verification_warning_density=0.0,
            review_backlog_pressure=0.1,
            dispute_burden=0.0,
            rollback_recentness_penalty=0.0,
            budget_saturation=0.1
        )
    )

    assert pressure.pressure_band == PressureBand.LOW
    assert pressure.pressure_score < 0.30
