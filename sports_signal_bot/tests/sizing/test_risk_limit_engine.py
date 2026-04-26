import pytest
from sports_signal_bot.sizing.risk_limits import RiskLimitEngine
from sports_signal_bot.sizing.contracts import SizingConfig

def test_risk_limit_drawdown():
    config = SizingConfig(
        drawdown_throttle_bands={0.10: 0.8, 0.20: 0.5},
        max_fraction_per_decision=1.0, # disable cap for this test
        action_class_fraction_caps={}
    )
    engine = RiskLimitEngine(config)

    # No DD
    frac, _, _, _ = engine.resolve_size(0.1, 1000, 0.0, 0, "candidate")
    assert frac == pytest.approx(0.1)

    # 15% DD -> 0.8x
    frac, _, throttles, _ = engine.resolve_size(0.1, 1000, 0.15, 0, "candidate")
    assert frac == pytest.approx(0.08)
    assert len(throttles) == 1

    # 25% DD -> 0.5x
    frac, _, throttles, _ = engine.resolve_size(0.1, 1000, 0.25, 0, "candidate")
    assert frac == pytest.approx(0.05)

def test_action_class_caps():
    config = SizingConfig(
        action_class_fraction_caps={"candidate": 0.02, "approved_candidate": 0.05},
        max_fraction_per_decision=1.0
    )
    engine = RiskLimitEngine(config)

    frac, _, _, caps = engine.resolve_size(0.1, 1000, 0.0, 0, "candidate")
    assert frac == pytest.approx(0.02)
    assert len(caps) > 0

    frac, _, _, caps = engine.resolve_size(0.1, 1000, 0.0, 0, "approved_candidate")
    assert frac == pytest.approx(0.05)

def test_bankroll_floor():
    config = SizingConfig(
        bankroll_floor_buffer=100.0,
        min_stake_units=1.0,
        max_stake_units=500.0
    )
    engine = RiskLimitEngine(config)

    # Trying to bet 50 out of 120 -> leaves 70, which is below 100 floor
    # Max allowed is 120 - 100 = 20
    config.max_fraction_per_decision = 1.0
    frac, units, _, caps = engine.resolve_size(0.5, 120, 0.0, 0, "candidate")
    assert units == pytest.approx(20.0)
    assert len(caps) > 0
