from sports_signal_bot.bankroll.contracts import BankrollConfig, BankrollDecisionRecord
from sports_signal_bot.bankroll.overlays.fixed_fraction import FixedFractionOfBankrollOverlay
import datetime

def test_fixed_fraction():
    config = BankrollConfig(bankroll_fraction=0.03)
    overlay = FixedFractionOfBankrollOverlay(config)

    decision = BankrollDecisionRecord(
        event_id="e1", market_type="m", sport="s",
        event_datetime_utc=datetime.datetime.utcnow(),
        action_class="candidate", executed_flag=True,
        result_status="settled_win"
    )

    stake, warnings = overlay.compute_stake(decision, 10000.0)
    assert stake == 300.0
    assert not warnings
