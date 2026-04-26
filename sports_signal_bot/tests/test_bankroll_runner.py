from sports_signal_bot.bankroll.contracts import (
    BankrollConfig,
    BankrollDecisionRecord,
    OverlayStrategyName,
)
from sports_signal_bot.bankroll.runner import BankrollRunner
import datetime


def test_runner_basic():
    config = BankrollConfig(
        default_overlay_strategy=OverlayStrategyName.FLAT_STAKE, flat_stake_units=100.0
    )
    runner = BankrollRunner(config)

    now = datetime.datetime.utcnow()
    decisions = [
        BankrollDecisionRecord(
            event_id="e1",
            market_type="m",
            sport="s",
            event_datetime_utc=now,
            action_class="approved",
            executed_flag=True,
            result_status="settled_win",
            hit_flag=True,
            payout_multiple=1.0,
        ),
        BankrollDecisionRecord(
            event_id="e2",
            market_type="m",
            sport="s",
            event_datetime_utc=now + datetime.timedelta(hours=1),
            action_class="approved",
            executed_flag=True,
            result_status="settled_loss",
            hit_flag=False,
            payout_multiple=1.0,
        ),
    ]

    manifest, ledger, curve, drawdowns = runner.run(decisions, "s", "m")
    assert manifest.summary.executed_count == 2
    assert manifest.summary.net_pnl_units == 0.0  # +100 then -100
    assert len(ledger) == 2
    assert len(curve) == 2
