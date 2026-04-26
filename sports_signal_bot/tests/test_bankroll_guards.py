from sports_signal_bot.bankroll.diagnostics import apply_stake_caps, enforce_bankroll_floor
from sports_signal_bot.bankroll.contracts import BankrollConfig

def test_stake_caps():
    config = BankrollConfig(min_stake_units=10.0, max_stake_units=100.0, max_fraction_per_decision=0.05)

    # Below min
    stake, w = apply_stake_caps(5.0, 10000.0, config)
    assert stake == 10.0

    # Above max
    stake, w = apply_stake_caps(150.0, 10000.0, config)
    assert stake == 100.0

    # Above fraction
    stake, w = apply_stake_caps(60.0, 1000.0, config) # 5% of 1000 is 50
    assert stake == 50.0

def test_bankroll_floor():
    config = BankrollConfig(bankroll_floor=10.0)
    b, w = enforce_bankroll_floor(5.0, config)
    assert b == 10.0

    b2, w2 = enforce_bankroll_floor(15.0, config)
    assert b2 == 15.0
