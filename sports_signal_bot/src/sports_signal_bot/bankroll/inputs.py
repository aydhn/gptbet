from typing import List
from sports_signal_bot.bankroll.contracts import BankrollDecisionRecord

class BankrollInputBuilder:
    @staticmethod
    def build_from_ledger(ledger_df) -> List[BankrollDecisionRecord]:
        """
        Builds BankrollDecisionRecords from a settled backtest ledger dataframe.
        """
        records = []
        # Sort chronologically
        if 'decision_timestamp_utc' in ledger_df.columns:
             ledger_df = ledger_df.sort_values('decision_timestamp_utc')

        for _, row in ledger_df.iterrows():
            record = BankrollDecisionRecord(
                event_id=row['event_id'],
                market_type=row['market_type'],
                sport=row['sport'],
                event_datetime_utc=row['event_datetime_utc'],
                action_class=row['action_class'],
                executed_flag=row['executed_flag'],
                signal_score=row.get('signal_score', 0.0),
                implied_odds=row.get('implied_odds'),
                payout_multiple=row.get('payout_multiple'),
                result_status=row['result_status'],
                hit_flag=row.get('hit_flag')
            )
            records.append(record)
        return records
