import datetime
from typing import List, Optional
from sports_signal_bot.bankroll.contracts import StreakRecord

class StreakAnalyzer:
    def __init__(self):
        self.current_win_streak = 0
        self.current_loss_streak = 0
        self.longest_win_streak = 0
        self.longest_loss_streak = 0

    def update(self, event_id: str, timestamp: datetime.datetime, hit_flag: Optional[bool]) -> StreakRecord:
        is_new_win_record = False
        is_new_loss_record = False

        if hit_flag is True:
            self.current_win_streak += 1
            self.current_loss_streak = 0
            if self.current_win_streak > self.longest_win_streak:
                self.longest_win_streak = self.current_win_streak
                is_new_win_record = True
        elif hit_flag is False:
            self.current_loss_streak += 1
            self.current_win_streak = 0
            if self.current_loss_streak > self.longest_loss_streak:
                self.longest_loss_streak = self.current_loss_streak
                is_new_loss_record = True
        else:
            # Void/Push - breaks both streaks or leaves as is depending on policy.
            # Usually, a push breaks a streak, but let's just reset for safety, or we could preserve.
            # Preserving is safer for purely statistical streaks.
            pass

        return StreakRecord(
            event_id=event_id,
            timestamp=timestamp,
            current_win_streak=self.current_win_streak,
            current_loss_streak=self.current_loss_streak,
            is_new_win_record=is_new_win_record,
            is_new_loss_record=is_new_loss_record
        )
