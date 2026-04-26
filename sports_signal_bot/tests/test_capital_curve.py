from sports_signal_bot.bankroll.capital_curve import CapitalCurveBuilder
from sports_signal_bot.bankroll.contracts import StreakRecord
import datetime


def test_capital_curve():
    builder = CapitalCurveBuilder(1000.0)
    streak = StreakRecord(
        event_id="e",
        timestamp=datetime.datetime.utcnow(),
        current_win_streak=1,
        current_loss_streak=0,
    )

    pt1 = builder.add_point(datetime.datetime.utcnow(), 1100.0, 100.0, streak)
    assert pt1.peak_to_date == 1100.0
    assert pt1.drawdown_abs == 0.0

    pt2 = builder.add_point(datetime.datetime.utcnow(), 1050.0, -50.0, streak)
    assert pt2.peak_to_date == 1100.0
    assert pt2.drawdown_abs == 50.0
    assert pt2.drawdown_pct == 50.0 / 1100.0
