import datetime
from typing import List, Optional
from sports_signal_bot.bankroll.contracts import CapitalCurvePoint, StreakRecord, ExposureRecord

class CapitalCurveBuilder:
    def __init__(self, initial_bankroll: float):
        self.initial_bankroll = initial_bankroll
        self.current_bankroll = initial_bankroll
        self.peak_bankroll = initial_bankroll
        self.curve_points: List[CapitalCurvePoint] = []

    def add_point(self,
                  timestamp: datetime.datetime,
                  bankroll: float,
                  pnl: float,
                  streak_state: StreakRecord,
                  exposure: Optional[ExposureRecord] = None):

        self.current_bankroll = bankroll
        if self.current_bankroll > self.peak_bankroll:
            self.peak_bankroll = self.current_bankroll

        drawdown_abs = self.peak_bankroll - self.current_bankroll
        drawdown_pct = drawdown_abs / self.peak_bankroll if self.peak_bankroll > 0 else 0.0

        point = CapitalCurvePoint(
            timestamp=timestamp,
            bankroll=self.current_bankroll,
            pnl=pnl,
            peak_to_date=self.peak_bankroll,
            drawdown_abs=drawdown_abs,
            drawdown_pct=drawdown_pct,
            streak_state=streak_state,
            exposure=exposure
        )
        self.curve_points.append(point)
        return point

    def get_points(self) -> List[CapitalCurvePoint]:
        return self.curve_points
