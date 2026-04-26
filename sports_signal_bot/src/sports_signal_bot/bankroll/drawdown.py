import datetime
from typing import List
from sports_signal_bot.bankroll.contracts import DrawdownRecord, CapitalCurvePoint

class DrawdownAnalyzer:
    def __init__(self):
        self.max_drawdown_abs = 0.0
        self.max_drawdown_pct = 0.0
        self.current_drawdown_abs = 0.0
        self.current_drawdown_pct = 0.0
        self.drawdown_events: List[DrawdownRecord] = []

    def update(self, event_id: str, timestamp: datetime.datetime, curve_point: CapitalCurvePoint):
        self.current_drawdown_abs = curve_point.drawdown_abs
        self.current_drawdown_pct = curve_point.drawdown_pct

        is_new_trough = False
        if self.current_drawdown_pct > self.max_drawdown_pct:
            self.max_drawdown_pct = self.current_drawdown_pct
            self.max_drawdown_abs = self.current_drawdown_abs
            is_new_trough = True

        if self.current_drawdown_abs > 0:
             record = DrawdownRecord(
                 event_id=event_id,
                 timestamp=timestamp,
                 drawdown_abs=self.current_drawdown_abs,
                 drawdown_pct=self.current_drawdown_pct,
                 is_new_trough=is_new_trough
             )
             self.drawdown_events.append(record)

    def get_events(self) -> List[DrawdownRecord]:
        return self.drawdown_events
