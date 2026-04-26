from sports_signal_bot.bankroll.contracts import BankrollConfig, BankrollDecisionRecord
from sports_signal_bot.bankroll.overlays.flat_stake import FlatStakeOverlay
import datetime


def test_flat_stake():
    config = BankrollConfig(flat_stake_units=150.0)
    overlay = FlatStakeOverlay(config)

    decision = BankrollDecisionRecord(
        event_id="e1",
        market_type="m",
        sport="s",
        event_datetime_utc=datetime.datetime.utcnow(),
        action_class="candidate",
        executed_flag=True,
        result_status="settled_win",
    )

    stake, warnings = overlay.compute_stake(decision, 10000.0)
    assert stake == 150.0
    assert not warnings
