from sports_signal_bot.bankroll.drawdown import DrawdownAnalyzer
from sports_signal_bot.bankroll.contracts import CapitalCurvePoint, StreakRecord
import datetime


def test_drawdown_analyzer():
    analyzer = DrawdownAnalyzer()
    streak = StreakRecord(
        event_id="e",
        timestamp=datetime.datetime.utcnow(),
        current_win_streak=0,
        current_loss_streak=0,
    )

    pt1 = CapitalCurvePoint(
        timestamp=datetime.datetime.utcnow(),
        bankroll=1000,
        pnl=0,
        peak_to_date=1000,
        drawdown_abs=0,
        drawdown_pct=0,
        streak_state=streak,
    )
    analyzer.update("e1", datetime.datetime.utcnow(), pt1)

    pt2 = CapitalCurvePoint(
        timestamp=datetime.datetime.utcnow(),
        bankroll=900,
        pnl=-100,
        peak_to_date=1000,
        drawdown_abs=100,
        drawdown_pct=0.1,
        streak_state=streak,
    )
    analyzer.update("e2", datetime.datetime.utcnow(), pt2)

    assert analyzer.max_drawdown_abs == 100.0
    assert analyzer.max_drawdown_pct == 0.1
    events = analyzer.get_events()
    assert len(events) == 1
    assert events[0].is_new_trough == True
