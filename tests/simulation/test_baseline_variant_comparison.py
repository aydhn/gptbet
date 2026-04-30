import pytest
from sports_signal_bot.simulation.baseline import build_baseline_snapshot
from sports_signal_bot.simulation.variant import build_variant_snapshot
from sports_signal_bot.simulation.comparisons import compute_before_after_metrics, validate_comparison_universe

def test_comparison():
    b_data = {"sample_size": 100, "metrics": {"hit_rate": 0.5}}
    v_data = {"sample_size": 100, "metrics": {"hit_rate": 0.6}}

    b_snap = build_baseline_snapshot("r1", b_data)
    v_snap = build_variant_snapshot("r1", v_data)

    universe = validate_comparison_universe(b_data, v_data)
    assert universe.is_identical is True

    metrics = compute_before_after_metrics(b_snap, v_snap)
    assert len(metrics) == 1
    assert metrics[0].delta == pytest.approx(0.1)
