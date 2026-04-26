from sports_signal_bot.bankroll.contracts import BankrollConfig, BankrollDecisionRecord
from sports_signal_bot.bankroll.overlays.tiered_flat import SignalTieredFlatOverlay
import datetime

def test_tiered_flat():
    config = BankrollConfig(flat_stake_units=200.0)
    overlay = SignalTieredFlatOverlay(config)

    # Approved candidate
    dec_app = BankrollDecisionRecord(
        event_id="e1", market_type="m", sport="s",
        event_datetime_utc=datetime.datetime.utcnow(),
        action_class="approved_candidate", executed_flag=True,
        result_status="settled_win"
    )
    stake, warnings = overlay.compute_stake(dec_app, 10000.0)
    assert stake == 200.0

    # Candidate
    dec_cand = BankrollDecisionRecord(
        event_id="e2", market_type="m", sport="s",
        event_datetime_utc=datetime.datetime.utcnow(),
        action_class="candidate", executed_flag=True,
        result_status="settled_win"
    )
    stake, warnings = overlay.compute_stake(dec_cand, 10000.0)
    assert stake == 100.0

    # Watchlist
    dec_wl = BankrollDecisionRecord(
        event_id="e3", market_type="m", sport="s",
        event_datetime_utc=datetime.datetime.utcnow(),
        action_class="watchlist", executed_flag=True,
        result_status="settled_win"
    )
    stake, warnings = overlay.compute_stake(dec_wl, 10000.0)
    assert stake == 0.0
