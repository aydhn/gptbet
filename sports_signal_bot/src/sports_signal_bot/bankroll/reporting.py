import pandas as pd
from typing import List
from sports_signal_bot.bankroll.contracts import BankrollLedgerRecord, CapitalCurvePoint, DrawdownRecord

def build_ledger_dataframe(records: List[BankrollLedgerRecord]) -> pd.DataFrame:
    if not records:
        return pd.DataFrame()
    return pd.DataFrame([r.model_dump() for r in records])

def build_curve_dataframe(points: List[CapitalCurvePoint]) -> pd.DataFrame:
    if not points:
        return pd.DataFrame()
    # Flattens nested fields like streak_state
    rows = []
    for p in points:
        d = p.model_dump()
        streak = d.pop('streak_state')
        d['current_win_streak'] = streak['current_win_streak']
        d['current_loss_streak'] = streak['current_loss_streak']
        d.pop('exposure', None)
        rows.append(d)
    return pd.DataFrame(rows)

def build_drawdown_dataframe(events: List[DrawdownRecord]) -> pd.DataFrame:
     if not events:
         return pd.DataFrame()
     return pd.DataFrame([e.model_dump() for e in events])
