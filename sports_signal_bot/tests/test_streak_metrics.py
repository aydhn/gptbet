from sports_signal_bot.bankroll.streaks import StreakAnalyzer
import datetime


def test_streaks():
    analyzer = StreakAnalyzer()

    r1 = analyzer.update("e1", datetime.datetime.utcnow(), hit_flag=True)
    assert r1.current_win_streak == 1
    assert r1.is_new_win_record == True

    r2 = analyzer.update("e2", datetime.datetime.utcnow(), hit_flag=True)
    assert r2.current_win_streak == 2
    assert r2.is_new_win_record == True

    r3 = analyzer.update("e3", datetime.datetime.utcnow(), hit_flag=False)
    assert r3.current_win_streak == 0
    assert r3.current_loss_streak == 1
    assert r3.is_new_loss_record == True

    assert analyzer.longest_win_streak == 2
    assert analyzer.longest_loss_streak == 1
